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
  id_letter_sale : string;
  cartItemId: string; 
}

interface CartItemDTO {
  id: string; 
  id_letter_sale: string;
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

export interface CartProduct {
  id_letter_sale: number;
  sellerNickname: string;
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
    quantityOf(id: number): number {
    const item = this.products.find(p => p.id === id)
    return item?.quantity ?? 0
  },
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
        rarity: ci.card.rarity,            
        sellerNickname: ci.card.seller,
        id_letter_sale : ci.id_letter_sale,
        cartItemId: ci.id 
      }));
    },

    /** 2) Añadir producto */
    async addProduct(product: CartProduct) {
      const token = localStorage.getItem("token");
      if (!token) throw new Error("No autenticado");

      console.log(
        "Identificación del objeto:",
        product.id_letter_sale,
        product.sellerNickname,
        product.quantity
      );

      const res = await fetch("http://localhost:8000/api/users/cart/add/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify({
          "card-id":       product.id_letter_sale,
          nickname:        product.sellerNickname,
          "number-cards":  product.quantity,
        }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.error || `HTTP ${res.status}`);
      }

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
      if (!token) throw new Error('No estás autenticado');

      console.log("🧾 Eliminando producto:", product);
      console.log("📦 ID del cart item:", product.cartItemId);
      console.log("👤 Nickname del vendedor:", product.sellerNickname);
    

      const res = await fetch(
  "http://localhost:8000/api/users/cart/delete/",
  {
    method: "POST",
    headers: {
      "Content-Type":  "application/json",
      "Authorization": `Token ${token}`,
    },
    body: JSON.stringify({
      'cart': product.cartItemId,
      // "nickname": product.sellerNickname,
    }),
  }
);

      if (!res.ok) {
  const err = await res.json().catch(() => ({}));
  throw new Error(err.error || `HTTP ${res.status}`);
}
await this.fetchCartFromAPI();
    },
    // Eliminar todas las cartas del carrito
  async clearCart() {
  const token = localStorage.getItem('token');
  if (!token) throw new Error('No autenticado');

  const res = await fetch('http://localhost:8000/api/users/cart/delete/all/', {
    method: 'POST',
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({}),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    console.error('Error vaciando carrito:', err);
    throw new Error(err.error || `HTTP ${res.status}`);
  }

  await this.fetchCartFromAPI();
},
  async payWithWallet() {
      const token = localStorage.getItem('token');
      if (!token) throw new Error('No estás autenticado.');

      const res = await fetch(
        'http://localhost:8000/api/users/cart/buy-wallet/',
        {
          method: 'POST',
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type':  'application/json'
          }
        }
      );

      const payload = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(payload.error || `HTTP ${res.status}`);
      }

      await this.fetchCartFromAPI();

      return payload;
    },
    
  }
});
