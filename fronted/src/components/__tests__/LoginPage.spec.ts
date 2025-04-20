import { mount } from '@vue/test-utils';
import { vi } from 'vitest';
import LoginForm from '../LoginPage.vue';
import { createRouter, createMemoryHistory } from 'vue-router';
import { createI18n } from 'vue-i18n';

// Crear mock de i18n
const i18n = createI18n({
  locale: 'es',
  messages: {
    es: {
      welcome: 'Bienvenido',
    },
  },
});

describe('LoginForm.vue', () => {
  let wrapper: any;

  beforeEach(() => {
    // Configuración del router en memoria
    const router = createRouter({
      history: createMemoryHistory(),
      routes: [{ path: '/', component: {} }],
    });

    // Montar el componente
    wrapper = mount(LoginForm, {
      global: {
        plugins: [i18n, router],
      },
    });
  });

  it('debe renderizar el formulario correctamente', () => {
    expect(wrapper.find('h1').text()).toBe('Iniciar Sesión');
    expect(wrapper.find('input[type="email"]').exists()).toBe(true);
    expect(wrapper.find('input[type="password"]').exists()).toBe(true);
    expect(wrapper.find('button').text()).toBe('Iniciar Sesión');
  });

  it('debe mostrar error si el correo está vacío', async () => {
    await wrapper.find('input[type="password"]').setValue('password123');
    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.find('span').text()).toBe('El correo es obligatorio.');
  });

  it('debe mostrar error si la contraseña está vacía', async () => {
    await wrapper.find('input[type="email"]').setValue('user@example.com');
    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.findAll('span').at(1)?.text()).toBe('La contraseña es obligatoria.');
  });

  it('debe manejar error de correo no registrado', async () => {
    // Mock de la autenticación con Firebase
    vi.mock('@/firebaseConfig', () => ({
      auth: {
        signInWithEmailAndPassword: vi.fn().mockRejectedValue({
          code: 'auth/user-not-found',
        }),
      },
    }));

    await wrapper.find('input[type="email"]').setValue('nonexistent@example.com');
    await wrapper.find('input[type="password"]').setValue('wrongpassword');
    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.find('span').text()).toBe('El correo no está registrado.');
  });

  it('debe manejar error de contraseña incorrecta', async () => {
    vi.mock('@/firebaseConfig', () => ({
      auth: {
        signInWithEmailAndPassword: vi.fn().mockRejectedValue({
          code: 'auth/wrong-password',
        }),
      },
    }));

    await wrapper.find('input[type="email"]').setValue('user@example.com');
    await wrapper.find('input[type="password"]').setValue('wrongpassword');
    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.findAll('span').at(1)?.text()).toBe('La contraseña es incorrecta.');
  });

  it('debe redirigir al home si la autenticación es exitosa', async () => {
    vi.mock('@/firebaseConfig', () => ({
      auth: {
        signInWithEmailAndPassword: vi.fn().mockResolvedValue({ user: {} }),
      },
      db: {
        getDoc: vi.fn().mockResolvedValue({
          exists: () => true,
          data: () => ({ firstName: 'John', lastName: 'Doe' }),
        }),
      },
    }));

    await wrapper.find('input[type="email"]').setValue('user@example.com');
    await wrapper.find('input[type="password"]').setValue('correctpassword');
    await wrapper.find('form').trigger('submit.prevent');

    // Verificar que la redirección ocurra
    expect(wrapper.router.history.current.path).toBe('/');
  });
});
