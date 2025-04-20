// stores/cart.ts
import { defineStore } from 'pinia';

interface Product {
  id: number;
  name: string;
  type: string;
  rarity: string;
  basePrice: number;
  price: number;
  quantity: number;
  img: string;
}

interface CartState {
  products: Product[]; // Productos en el carrito
  storeProducts: Product[]; // Productos disponibles en la tienda
}

export const useCartStore = defineStore('cart', {
  state: (): CartState => ({
    products: [],
    storeProducts: [],
  }),

  getters: {
    total: (state) => state.products.reduce((sum, product) => sum + product.price * product.quantity, 0),
  },

  actions: {
    // Cargar carrito desde localStorage
    loadCartFromLocalStorage() {
      const cartData = localStorage.getItem('cart');
      if (cartData) {
        const parsedData = JSON.parse(cartData);
        this.products = parsedData.products;
      }
    },

    // Guardar carrito en localStorage
    saveCartToLocalStorage() {
      const cartData = {
        products: this.products,
      };
      localStorage.setItem('cart', JSON.stringify(cartData));
    },

    // Fetch productos de una fuente externa (como un archivo JSON)
    async fetchProducts() {
      try {
        const response = await fetch("/cards.json"); // 📌 Ajusta la ruta de tu JSON
        const data: Product[] = await response.json();
        this.storeProducts = this.getRandomItems(data, 5); // Guardar en storeProducts, NO en el carrito
      } catch (error) {
        console.error("Error al cargar los productos:", error);
      }
    },

    // Agregar producto al carrito con la cantidad del JSON
    addProduct(product: Product) {
      const existingProduct = this.products.find(
        (p) => p.id === product.id && p.rarity === product.rarity
      );
      if (existingProduct) {
        existingProduct.quantity += product.quantity;
      } else {
        this.products.push({...product, quantity: product.quantity});
      }
      this.saveCartToLocalStorage(); // Guardar cada vez que se agregue un producto
    },

    removeProduct(id: number) {
      this.products = this.products.filter((product) => product.id !== id);
      this.saveCartToLocalStorage(); // Guardar después de eliminar un producto
    },

    updateQuantity(id: number, quantity: number) {
      const product = this.products.find((p) => p.id === id);
      if (product) {
        product.quantity = quantity;
      }
      this.saveCartToLocalStorage(); // Guardar después de actualizar cantidad
    },

    clearCart() {
      this.products = [];
      localStorage.removeItem('cart'); // Eliminar carrito de localStorage
    },

    getRandomItems(items: Product[], n: number): Product[] {
      const shuffled = [...items].sort(() => 0.5 - Math.random());
      return shuffled.slice(0, n);
    },
  },
});
