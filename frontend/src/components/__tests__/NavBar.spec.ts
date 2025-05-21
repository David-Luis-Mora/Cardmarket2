import { mount, flushPromises } from '@vue/test-utils';
import NavBar from '../NavBar.vue';
import { createI18n } from 'vue-i18n';
import { createRouter, createWebHistory } from 'vue-router';
import { createTestingPinia } from '@pinia/testing';
import { getAuth, onAuthStateChanged, signOut } from 'firebase/auth';

// Simulación de Firebase Auth
jest.mock('firebase/auth', () => ({
  getAuth: () => ({}),
  onAuthStateChanged: jest.fn(),
  signOut: jest.fn(),
}));

const i18n = createI18n({
  locale: 'es',
  messages: {
    es: {
      cards: 'Cartas',
      cart: 'Carrito',
      language: 'Idioma',
      login: 'Iniciar sesión',
      logout: 'Cerrar sesión',
      options: 'Opciones',
      profile: 'Perfil',
      settings: 'Configuración',
    },
    en: {
      cards: 'Cards',
      cart: 'Cart',
      language: 'Language',
      login: 'Login',
      logout: 'Logout',
      options: 'Options',
      profile: 'Profile',
      settings: 'Settings',
    },
  },
});

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/:locale/', component: { template: '' } },
    { path: '/:locale/cards', component: { template: '' } },
    { path: '/:locale/cart', component: { template: '' } },
    { path: '/:locale/login', component: { template: '' } },
    { path: '/:locale/profile', component: { template: '' } },
  ],
});

describe('NavBar.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount(NavBar, {
      global: {
        plugins: [i18n, router, createTestingPinia()],
      },
    });
  });

  test('should render the navbar with the correct elements', () => {
    expect(wrapper.find('.logo').exists()).toBe(true);
    expect(wrapper.find('.nav-link').exists()).toBe(true);
  });

  test('should show login button when user is not logged in', async () => {
    onAuthStateChanged.mockImplementationOnce((auth, callback) => callback(null));

    // Simula el cambio en el estado de autenticación
    await flushPromises();

    const loginButton = wrapper.find('.nav-link');
    expect(loginButton.text()).toBe('Iniciar sesión');
  });

  test('should show logout button when user is logged in', async () => {
    onAuthStateChanged.mockImplementationOnce((auth, callback) =>
      callback({ uid: '123' })
    );

    // Simula el cambio en el estado de autenticación
    await flushPromises();

    const logoutButton = wrapper.find('.nav-link');
    expect(logoutButton.text()).toBe('Cerrar sesión');
  });

  test('should change language when language button is clicked', async () => {
    const languageButton = wrapper.find('.nav-item.dropdown');
    await languageButton.trigger('click');

    const spanishOption = wrapper.find('a.dropdown-item');
    await spanishOption.trigger('click');

    expect(i18n.global.locale.value).toBe('es');
  });

  test('should toggle sidebar visibility when menu button is clicked', async () => {
    const menuButton = wrapper.find('.menu-btn');
    await menuButton.trigger('click');
    expect(wrapper.find('.sidebar').classes()).toContain('open');
    await menuButton.trigger('click');
    expect(wrapper.find('.sidebar').classes()).not.toContain('open');
  });

  test('should logout the user when logout button is clicked', async () => {
    onAuthStateChanged.mockImplementationOnce((auth, callback) =>
      callback({ uid: '123' })
    );

    await flushPromises();

    const logoutButton = wrapper.find('.nav-link');
    await logoutButton.trigger('click');

    expect(signOut).toHaveBeenCalled();
  });

  test('should navigate to profile page when profile is clicked in sidebar', async () => {
    const profileLink = wrapper.find('.sidebar ul li a');
    await profileLink.trigger('click');
    expect(wrapper.vm.$router.currentRoute.value.path).toBe('/es/profile');
  });
});
