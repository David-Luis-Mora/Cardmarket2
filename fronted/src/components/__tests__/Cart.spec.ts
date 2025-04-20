import { describe, it, expect, vi } from "vitest";
import { mount } from "@vue/test-utils";
import Cart from "../Cart.vue"; // Ajusta la ruta según la ubicación de tu componente
import { createPinia, setActivePinia } from "pinia";
import { useCartStore } from "../../stores/cart";
import { createI18n } from "vue-i18n"; // Importa Vue I18n

describe('Cart.vue', () => {
  let cartStore;
  let i18n;
  let pinia;  // Definir pinia aquí


  // Configuración previa para cada test
  beforeEach(() => {
    const pinia = createPinia();
    setActivePinia(pinia); // Establece la tienda de Pinia
    cartStore = useCartStore(); // Usa la tienda del carrito
    cartStore.clearCart(); // Limpia el carrito antes de cada test

    // Configuración de Vue I18n
    i18n = createI18n({
      legacy: false,
      locale: "es", // Establece el idioma por defecto
      messages: {
        es: {
          cartt: {
            title: "Carrito de Compras"
          }
        }
      }
    });
  });

  it('should display cart items correctly', async () => {
    // Agregar un producto al carrito
    cartStore.addProduct({
      id: 1,
      name: "Producto 1",
      img: "/img/cimientos.jpg",
      price: 10,
      quantity: 1,
      rarity: "Rare",
      expansions: "Cimientos"
    });

    const wrapper = mount(Cart, {
      global: {
        plugins: [pinia, i18n] // Añadir Vue I18n y Pinia como plugins globales
      }
    });

    // Verifica que el producto aparece en el carrito
    await wrapper.vm.$nextTick(); // Asegura que la actualización del DOM haya ocurrido
    expect(wrapper.html()).toContain("Producto 1");
    expect(wrapper.html()).toContain("10.00 $");
  });

  // Aquí puedes seguir con los otros tests...
});
