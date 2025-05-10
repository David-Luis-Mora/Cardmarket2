// stores/cart.ts
import { defineStore } from 'pinia';

export interface Product {
  id: number;
  name: string;
  img: string;
  price: number;
  quantity: number;
  rarity: string;
  sellerNickname: string;
}
interface CartItemDTO {
  card_id: number;
  number_cards: number;
  card: {
    id: number;
    name: string;
    img: string;
    price: number;
    seller: string;
    rarity : string;
  };
  quantity: number;
}

export const useCartStore = defineStore('cart', {
  state: () => ({
    products: [] as Product[],
  }),

  getters: {
    total:   (state) => state.products.reduce((sum,p) => sum + p.price*p.quantity, 0),
    totalQuantity: (state) => state.products.reduce((sum,p) => sum + p.quantity, 0),
  },

  actions: {
    /** 1) Traer carrito */
    async fetchCartFromAPI() {
      const token = localStorage.getItem('token');
      if (!token) return;
      const res = await fetch('http://localhost:8000/api/users/cart/', {
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
      }
      });
      if (!res.ok) throw new Error('No autorizado');
      const { cart } = await res.json() as { cart: CartItemDTO[] };

      this.products = cart.map(ci => ({
        id: ci.card.id,
        name: ci.card.name,
        img: ci.card.img,
        price: ci.card.price,
        quantity: ci.quantity,
        rarity: ci.card.rarity,             // rellénalo si lo necesitas
        sellerNickname: ci.card.seller
      }));
    },

    /** 2) Añadir producto */
    async addProduct(product: Product) {
      const token = localStorage.getItem('token');
      if (!token) throw new Error('No autenticado');

      const res = await fetch('http://localhost:8000/api/users/cart/add/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // ¡OJO! tu vista espera "Token", no "Bearer"
          'Authorization': `Token ${token}`,
        },
        body: JSON.stringify({
          'card-id': product.id,
          nickname: product.sellerNickname,
          'number-cards': product.quantity
        })
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.error || `HTTP ${res.status}`);
      }

      // recargamos el carrito tras añadir
      await this.fetchCartFromAPI();
    },

    /** 3) Actualizar cantidad */
    async updateQuantity(itemId: number, quantity: number) {
      const token = localStorage.getItem('token');
      if (!token) throw new Error('No autenticado');
      const res = await fetch(`http://localhost:8000/api/cart/${itemId}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type':  'application/json',
          'Authorization': `Token ${token}`,
        },
        body: JSON.stringify({ quantity }),
      });
      if (!res.ok) console.error('Error actualizando:', await res.text());
      await this.fetchCartFromAPI();
    },

    /** 4) Eliminar item */
    async removeProduct(product: Product) {
      const token = localStorage.getItem('token');

      console.log("🛒 Eliminando producto:", {
        id: product.id,
        nickname: product.sellerNickname
      });
      const res = await fetch(`http://localhost:8000/api/users/cart/delete/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${token}`,
          
        },
        body: JSON.stringify({
          'card-id': product.id,
          'nickname': product.sellerNickname,
          // 'number-cards': product.quantity
        })
      });
      if (!res.ok) console.error('Error eliminando del carrito');
      await this.fetchCartFromAPI();
    },
    // Eliminar todas las cartas del carrito
    async clearCart() {
      const token = localStorage.getItem('token');
      const res = await fetch('http://localhost:8000/api/users/cart/delete/all/', {
        method: 'POST',
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        }
      });
    
      if (!res.ok) {
        console.error('❌ Error vaciando el carrito');
      } else {
        console.log('🧹 Carrito vaciado correctamente');
        await this.fetchCartFromAPI(); // recarga el carrito vacío
      }
    }
  },
  

});
