import { mount } from '@vue/test-utils';
import RegisterForm from '../RegisterForm.vue';
import { createTestingPinia } from '@pinia/testing';
import { createI18n } from 'vue-i18n';
import { RouterLink } from 'vue-router';
import { auth } from '../../firebaseConfig';
import { vi } from 'vitest';

describe('RegisterForm.vue', () => {
  const i18n = createI18n({
    legacy: false,
    locale: 'en',
    messages: {
      en: {
        login: 'Login',
      },
      es: {
        login: 'Iniciar sesión',
      },
    },
  });

  it('renders form correctly', () => {
    const wrapper = mount(RegisterForm, {
      global: {
        plugins: [createTestingPinia(), i18n],
        stubs: {
          RouterLink,
        },
      },
    });

    expect(wrapper.find('h1').text()).toBe('Registro');
    expect(wrapper.find('label[for="firstName"]').text()).toBe('Nombre');
    expect(wrapper.find('label[for="lastName"]').text()).toBe('Apellido');
    expect(wrapper.find('label[for="email"]').text()).toBe('Correo Electrónico');
    expect(wrapper.find('label[for="password"]').text()).toBe('Contraseña');
  });

  it('displays validation errors when inputs are empty', async () => {
    const wrapper = mount(RegisterForm, {
      global: {
        plugins: [createTestingPinia(), i18n],
        stubs: {
          RouterLink,
        },
      },
    });

    await wrapper.find('button[type="submit"]').trigger('click');

    expect(wrapper.text()).toContain('El nombre es obligatorio.');
    expect(wrapper.text()).toContain('El apellido es obligatorio.');
    expect(wrapper.text()).toContain('El formato del correo es inválido.');
    expect(wrapper.text()).toContain(
      'La contraseña debe tener al menos 8 caracteres, una letra mayúscula, un número y un carácter especial.'
    );
  });

  it('checks if email already exists', async () => {
    const wrapper = mount(RegisterForm, {
      global: {
        plugins: [createTestingPinia(), i18n],
        stubs: {
          RouterLink,
        },
      },
    });

    // Simulamos que el email ya está registrado usando vi.fn() de Vitest
    const mockGetDoc = vi.fn().mockResolvedValue({ exists: true });
    wrapper.vm.checkUsers = mockGetDoc;

    wrapper.vm.email = 'existingemail@example.com';
    await wrapper.find('button[type="submit"]').trigger('click');

    expect(mockGetDoc).toHaveBeenCalledWith('existingemail@example.com');
    expect(wrapper.text()).toContain('Ya el usuario está registrado');
  });

  it('registers user when all fields are valid', async () => {
    const wrapper = mount(RegisterForm, {
      global: {
        plugins: [createTestingPinia(), i18n],
        stubs: {
          RouterLink,
        },
      },
    });

    // Rellenamos los campos
    wrapper.vm.firstName = 'Juan';
    wrapper.vm.lastName = 'Pérez';
    wrapper.vm.email = 'newuser@example.com';
    wrapper.vm.password = 'Password123!';

    // Simulamos que el email no está registrado
    const mockCheckUsers = vi.fn().mockResolvedValue(false);
    wrapper.vm.checkUsers = mockCheckUsers;

    const mockAddUser = vi.fn();
    wrapper.vm.addUser = mockAddUser;

    await wrapper.find('button[type="submit"]').trigger('click');

    expect(mockCheckUsers).toHaveBeenCalledWith('newuser@example.com');
    expect(mockAddUser).toHaveBeenCalled();
  });

  it('shows error when registering fails', async () => {
    const wrapper = mount(RegisterForm, {
      global: {
        plugins: [createTestingPinia(), i18n],
        stubs: {
          RouterLink,
        },
      },
    });

    // Simulamos que el email ya está registrado
    const mockCheckUsers = vi.fn().mockResolvedValue(true);
    wrapper.vm.checkUsers = mockCheckUsers;

    await wrapper.find('button[type="submit"]').trigger('click');

    expect(wrapper.text()).toContain('Ya el usuario está registrado');
  });
});
