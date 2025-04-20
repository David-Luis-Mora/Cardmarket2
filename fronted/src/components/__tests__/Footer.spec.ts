import { mount } from '@vue/test-utils';
import Footer from '../Footer.vue';
import { createI18n } from 'vue-i18n';
import { createPinia } from 'pinia';
import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router'; // Corregir importación

// Mock de i18n
const i18n = createI18n({
  legacy: false,
  locale: 'es', // Idioma inicial
  messages: {
    es: {
      quickLinks: 'Enlaces rápidos',
      home: 'Inicio',
      products: 'Productos',
      aboutUs: 'Sobre nosotros',
      contact: 'Contacto',
      followUs: 'Síguenos',
      allRightsReserved: 'Todos los derechos reservados'
    },
    en: {
      quickLinks: 'Quick Links',
      home: 'Home',
      products: 'Products',
      aboutUs: 'About Us',
      contact: 'Contact',
      followUs: 'Follow Us',
      allRightsReserved: 'All Rights Reserved'
    }
  }
});

// Configurar el router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/:lang', name: 'home' },
    { path: '/:lang/cards', name: 'cards' },
    { path: '/:lang/about', name: 'about' },
    { path: '/:lang/contact', name: 'contact' },
  ]
});

// Crear la aplicación con los plugins necesarios
const app = createApp(Footer);
app.use(i18n);
app.use(createPinia());
app.use(router);

describe('Footer.vue', () => {
  it('debería mostrar enlaces de traducción en español por defecto', async () => {
    const wrapper = mount(Footer, {
      global: {
        plugins: [i18n, router]
      }
    });

    // Esperar a que Vue Router cargue las rutas
    await router.isReady();

    // Verificar que el texto de los enlaces esté en español
    expect(wrapper.text()).toContain('Enlaces rápidos');
    expect(wrapper.text()).toContain('Inicio');
    expect(wrapper.text()).toContain('Productos');
    expect(wrapper.text()).toContain('Sobre nosotros');
    expect(wrapper.text()).toContain('Contacto');
    expect(wrapper.text()).toContain('Síguenos');
  });

  it('debería cambiar las traducciones cuando se cambia el idioma a inglés', async () => {
    // Cambiar idioma a inglés
    i18n.global.locale.value = 'en';

    const wrapper = mount(Footer, {
      global: {
        plugins: [i18n, router]
      }
    });

    // Esperar a que Vue Router cargue las rutas
    await router.isReady();

    // Verificar que el texto de los enlaces esté en inglés
    expect(wrapper.text()).toContain('Quick Links');
    expect(wrapper.text()).toContain('Home');
    expect(wrapper.text()).toContain('Products');
    expect(wrapper.text()).toContain('About Us');
    expect(wrapper.text()).toContain('Contact');
    expect(wrapper.text()).toContain('Follow Us');
  });

  it('debería renderizar los enlaces de redes sociales', async () => {
    const wrapper = mount(Footer, {
      global: {
        plugins: [i18n, router]
      }
    });

    // Verificar que los íconos de redes sociales estén presentes
    expect(wrapper.find('.bi-facebook').exists()).toBe(true);
    expect(wrapper.find('.bi-twitter').exists()).toBe(true);
    expect(wrapper.find('.bi-instagram').exists()).toBe(true);
    expect(wrapper.find('.bi-discord').exists()).toBe(true);
  });

  it('debería renderizar el enlace de contacto con el correo y dirección', () => {
    const wrapper = mount(Footer, {
      global: {
        plugins: [i18n, router]
      }
    });

    // Verificar si el correo electrónico y la dirección están presentes
    expect(wrapper.text()).toContain('cardshop@gmail.com');
    expect(wrapper.text()).toContain('Calle Magic, 123, Planeswalker City');
  });
});
