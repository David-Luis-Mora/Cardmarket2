import { mount } from '@vue/test-utils';
import ProductItem from '../ProductItem.vue';
import { createTestingPinia } from '@pinia/testing';
import { useCartStore } from '@/stores/cart';
import { createI18n } from 'vue-i18n';
import { RouterLink } from 'vue-router';
import { vi } from 'vitest';

describe('ProductItem.vue', () => {
  const i18n = createI18n({
    legacy: false,
    locale: 'en',
    messages: {
      en: {
        login: 'Login',
        // Otros textos aquí
      },
      es: {
        login: 'Iniciar sesión',
        // Otros textos aquí
      }
    },
  });

  it('renders product info correctly', () => {
    const product = {
      img: 'path/to/img',
      name: 'Test Product',
      price: 10.99,
      quantity: 5,
    };

    const wrapper = mount(ProductItem, {
      global: {
        plugins: [createTestingPinia(), i18n],
        stubs: {
          RouterLink,
        },
      },
      props: {
        product,
      },
    });

    expect(wrapper.find('img').attributes('src')).toBe('path/to/img');
    expect(wrapper.find('p').text()).toBe('10.99 $');
    expect(wrapper.find('select').findAll('option').length).toBe(5);
  });

  it('redirects to login if user is not logged in', async () => {
    const product = {
      img: 'path/to/img',
      name: 'Test Product',
      price: 10.99,
      quantity: 5,
    };

    const wrapper = mount(ProductItem, {
      global: {
        plugins: [createTestingPinia(), i18n],
        stubs: {
          RouterLink,
        },
      },
      props: {
        product,
      },
    });

    const routerPushMock = vi.fn();
    wrapper.vm.$router.push = routerPushMock;

    // Simulamos que el usuario no está logueado
    wrapper.vm.logueado = false;

    await wrapper.find('button').trigger('click');

    expect(routerPushMock).toHaveBeenCalledWith('/en/login');
  });

  it('adds product to cart when logged in', async () => {
    const product = {
      img: 'path/to/img',
      name: 'Test Product',
      price: 10.99,
      quantity: 5,
    };

    const wrapper = mount(ProductItem, {
      global: {
        plugins: [createTestingPinia(), i18n],
        stubs: {
          RouterLink,
        },
      },
      props: {
        product,
      },
    });

    const cartStore = useCartStore();
    const addProductMock = vi.spyOn(cartStore, 'addProduct');

    // Simulamos que el usuario está logueado
    wrapper.vm.logueado = true;
    wrapper.vm.selectedQuantity = 2;

    await wrapper.find('button').trigger('click');

    expect(addProductMock).toHaveBeenCalledWith({
      ...product,
      quantity: 2,
    });
  });
});
