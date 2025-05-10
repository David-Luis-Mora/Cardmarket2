<template>
  <div class="cart-container">
    <div class="cart-wrapper">
      <div class="cart">
        <h2 class="cart-title">{{ $t("cartt.title") }}</h2>
        <template v-if="cartStore.products.length > 0">
          <transition-group name="fade" tag="ul" class="cart-list">
            <li
              v-for="product in cartStore.products"
              :key="product.id + product.rarity"
              class="cart-item"
            >
              <img :src="product.img" :alt="product.name" class="product-image" />

              <div class="product-info">
                <span class="product-name">
                  {{ product.name }}
                  <span class="rarity-badge">{{ $t("cartt.rarity") }}: {{ product.rarity }}</span>
                </span>

                <div class="product-actions">
                  <label class="quantity-label">
                    {{ $t("cartt.quantity") }}:
                    <select
                      v-model="product.quantity"
                      @change="updateQuantity(product.id, product.quantity)"
                      class="quantity-input"
                    >
                      <option v-for="n in Math.min(product.quantity + 10, 30)" :key="n" :value="n">
                        {{ n }}
                      </option>
                    </select>
                  </label>
                  <span class="product-price"
                    >{{ (product.price * product.quantity).toFixed(2) }} $</span
                  >
                </div>
              </div>

              <button @click="removeProduct(product)" class="remove-btn">✕</button>
            </li>
          </transition-group>
        </template>
        <template v-else>
          <div class="empty-cart">
            <p>{{ $t("cartt.emptyMessage") }}</p>
            <router-link :to="`/${$i18n.locale}/cards`">
              <button class="go-shop-btn">{{ $t("cartt.goShop") }}</button>
            </router-link>
          </div>
        </template>
      </div>

      <!-- Tabla lateral -->
      <div class="cart-side-summary">
        <h3>{{ $t("cartt.summary") }}</h3>
        <table class="summary-table">
          <tr>
            <td>{{ $t("cartt.totalQuantity") }}:</td>
            <td>
              <strong>{{ cartStore.totalQuantity }}</strong>
            </td>
          </tr>
          <tr>
            <td>{{ $t("cartt.totalPrice") }}:</td>
            <td>
              <strong>{{ cartStore.total.toFixed(2) }} $</strong>
            </td>
          </tr>
        </table>
        <router-link :to="`/${$i18n.locale}/payment`" v-if="cartStore.products.length > 0">
          <button class="buy-btn">{{ $t("cartt.buy") }}</button>
        </router-link>

        <button class="buy-btn" disabled v-else>
          {{ $t("cartt.buy") }}
        </button>

        <button @click="cartStore.clearCart()" class="clear-cart-btn">
          {{ $t("cartt.clear") }}
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from "vue";
import { useCartStore, type Product } from "@/stores/cart";

export default defineComponent({
  name: "Cart",
  setup() {
    const cartStore = useCartStore();
    onMounted(() => {
      cartStore.fetchCartFromAPI();
    });

    const updateQuantity = (id: number, quantity: number) => {
      cartStore.updateQuantity(id, quantity);
    };

    function removeProduct(product: Product) {
      cartStore.removeProduct(product);
    }

    function clearCart() {
      cartStore.clearCart();
    }

    return {
      cartStore,
      updateQuantity,
      removeProduct,
      clearCart,
    };
  },
});
</script>

<style scoped>
.empty-cart {
  text-align: center;
  padding: 40px 20px;
  background: rgba(59, 7, 100, 0.7);
  border-radius: 12px;
  color: #e9d8fd;
  font-size: 18px;
}

.buy-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.go-shop-btn {
  margin-top: 20px;
  background-color: #facc15;
  color: #2d2d2d;
  font-weight: bold;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.go-shop-btn:hover {
  background-color: #eab308;
}

.cart-container {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  justify-content: center;
}

.cart-side-summary {
  min-width: 280px;
  max-width: 300px;
  background: #f0f4f8;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.cart-side-summary h3 {
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 20px;
  color: #e9d8fd;
  text-align: center;
}

.summary-table {
  width: 100%;
  margin-bottom: 20px;
  font-size: 16px;
  color: #e9d8fd;
}

.summary-table td {
  padding: 8px 0;
}

.buy-btn {
  background-color: #28a745;
  color: white;
  padding: 12px;
  width: 100%;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  margin-bottom: 10px;
  transition: background-color 0.3s;
}

.buy-btn:hover {
  background-color: #218838;
}

.cart-side-summary .clear-cart-btn {
  width: 100%;
}

.cart {
  max-width: 960px;
  margin: 40px auto;
  background: linear-gradient(135deg, #6964ae, #652597, #363636);
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.cart-title {
  font-size: 28px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 30px;
  color: #e9d8fd;
}

.cart-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.cart-item {
  display: flex;
  align-items: flex-start;
  padding: 20px;
  border: 3px solid #facc15;
  position: relative;
  background: rgba(59, 7, 100, 0.7);
  border-radius: 8px;
  margin-bottom: 20px;
  transition: all 0.3s ease;
}

.product-image {
  width: 120px;
  height: 170px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-right: 20px;
}

.product-info {
  flex: 1;
}

.product-name {
  font-size: 20px;
  font-weight: 600;
  color: #e9d8fd;
  display: block;
  margin-bottom: 8px;
}

.rarity-badge {
  font-size: 14px;
  color: #777;
  display: inline-block;
  margin-left: 10px;
  background: #e5e5e5;
  padding: 2px 8px;
  border-radius: 4px;
}

.product-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 15px;
  margin-top: 10px;
}

.quantity-label {
  font-size: 14px;
  color: #e9d8fd;
}

.quantity-input {
  margin-left: 8px;
  padding: 4px 8px;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.product-price {
  font-size: 16px;
  font-weight: 600;
  color: #e9d8fd;
}

.remove-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: #ff6b6b;
  color: white;
  border: none;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  cursor: pointer;
  font-size: 16px;
  line-height: 28px;
  text-align: center;
  transition: background 0.3s;
}

.remove-btn:hover {
  background: #e64545;
}

.cart-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 2px solid #ddd;
  flex-wrap: wrap;
  gap: 10px;
}

.cart-summary p {
  font-size: 18px;
  font-weight: bold;
  color: #e9d8fd;
}

.clear-cart-btn {
  background-color: #ff0000;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

.clear-cart-btn:hover {
  background-color: #b30000;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.4s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.cart-container {
  display: flex;
  justify-content: center;
  padding: 20px;
}

.cart-wrapper {
  display: flex;
  align-items: flex-start;
  gap: 40px;
  width: 100%;
  max-width: 1300px;
}

.cart {
  flex: 1;
  margin: 0;
}

.cart-side-summary {
  border: 3px solid #facc15;
  position: sticky;
  top: 20px;
  align-self: flex-start;
  min-width: 280px;
  max-width: 300px;
  background: rgba(59, 7, 100, 0.7);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  height: fit-content;
  margin-top: 0;
}

@media (max-width: 768px) {
  .cart-item {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .product-image {
    margin-right: 0;
    margin-bottom: 10px;
  }

  .product-actions {
    justify-content: center;
  }

  .remove-btn {
    top: 10px;
    right: 10px;
  }
}
</style>
