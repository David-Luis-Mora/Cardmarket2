<template>
  <div class="cart">
    <h2>{{ $t('cartt.title') }}</h2>
    <ul>
      <li v-for="product in cartStore.products" :key="product.id + product.rarity" class="cart-item">
        <img :src="product.img" :alt="product.name" class="product-image" />
        <div class="product-info">
          <span class="product-name">{{ product.name }} ({{ $t('cartt.rarity') }}: {{ product.rarity }})</span>
          <div class="quantity">
            <!-- Select para elegir la cantidad, basado en la cantidad máxima del producto -->
            <select v-model="product.quantity" @change="updateQuantity(product.id, product.quantity)" class="quantity-input">
              <!-- Generar opciones desde 1 hasta la cantidad máxima del producto -->
              <option v-for="n in Math.min(product.quantity, 30)" :key="n" :value="n">{{ n }}</option>
            </select>
            <span class="product-price">{{ (product.price * product.quantity).toFixed(2) }} $</span>
          </div>
        </div>
        <button @click="removeProduct(product.id)" class="remove-btn">{{ $t('cartt.remove') }}</button>
      </li>
    </ul>
    <div class="cart-summary">
      <p>{{ $t('cartt.total') }}: <strong>{{ cartStore.total.toFixed(2) }} $</strong></p>
      <button @click="cartStore.clearCart()" class="clear-cart-btn">{{ $t('cartt.clear') }}</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { useCartStore } from '@/stores/cart';

export default defineComponent({
  name: 'Cart',
  setup() {
    const cartStore = useCartStore();

    onMounted(() => {
      cartStore.loadCartFromLocalStorage();
    });

    const updateQuantity = (id: number, quantity: number) => {
      cartStore.updateQuantity(id, quantity);
    };

    const removeProduct = (id: number) => {
      cartStore.removeProduct(id);
    };

    return {
      cartStore,
      updateQuantity,
      removeProduct,
    };
  },
});
</script>

<style scoped>
.cart {
  background-color: #f4f4f4;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: auto;
}

h2 {
  text-align: center;
  font-size: 24px;
  color: #333;
}

.cart-item {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #ddd;
  padding: 10px 0;
}

.product-image {
  width: 100px;
  height: 140px;
  object-fit: contain;
  margin-right: 20px;
}

.product-info {
  flex: 1;
}

.product-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.quantity {
  display: flex;
  align-items: center;
}

.quantity-input {
  width: 60px;
  padding: 5px;
  margin-right: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.product-price {
  font-size: 16px;
  font-weight: bold;
  color: #555;
}

.remove-btn {
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.remove-btn:hover {
  background-color: #e43f3f;
}

.cart-summary {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.clear-cart-btn {
  background-color: #00aaff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.clear-cart-btn:hover {
  background-color: #0088cc;
}
</style>
