import { mount } from '@vue/test-utils';
import HomePage from '../HomePage.vue'; // Asegúrate de usar la ruta correcta
import { createPinia, defineStore } from 'pinia';
import { vi } from 'vitest';

describe('HomePage.vue', () => {
  let wrapper;

  // Mock del store de productos
  const useProductStore = defineStore('product', {
    state: () => ({
      products: [],
    }),
    actions: {
      addProduct(product) {
        this.products.push(product);
      },
    },
  });

  beforeEach(() => {
    // Crear una nueva instancia de Pinia para cada test
    const pinia = createPinia();

    wrapper = mount(HomePage, {
      global: {
        plugins: [pinia], // Agregar el store de Pinia
        mocks: {
          $t: (key: string) => key, // Mock de traducción, devuelve la clave como texto
        },
      },
    });
  });

  it('debe mostrar las cartas aleatorias', async () => {
    // Simulamos que se hayan cargado cartas aleatorias
    await wrapper.vm.selectAndCopyCards();
    const cards = wrapper.findAll('.card');
    expect(cards.length).toBe(6); // Comprobamos que haya 6 cartas
  });

  it('debe redirigir al hacer clic en un producto', async () => {
    const routerPushSpy = vi.fn();
    const router = { push: routerPushSpy };

    wrapper = mount(HomePage, {
      global: {
        mocks: {
          $router: router, // Mock de router
        },
        plugins: [createPinia()],
      },
    });

    const producto = wrapper.find('.card-button');
    await producto.trigger('click');
    expect(routerPushSpy).toHaveBeenCalledWith({
      name: 'product-list',
      params: { expansion: 'Dominaria United' },
    });
  });

});
