<template>
  <div class="payment-container">
    <h2>{{ $t("payment.title") }}</h2>
    <div class="payment-grid">
      <!-- Columna izquierda -->
      <div class="left-column">
        <!-- Información del cliente -->
        <div class="card info-card">
          <h3>{{ $t("payment.customerInfo") }}</h3>
          <div class="form-group">
            <label for="cardHolderName">{{ $t("payment.cardHolderName") }}</label>
            <input
              v-model="cardHolderName"
              type="text"
              id="cardHolderName"
              placeholder="John Doe"
              required
            />
          </div>
          <div class="form-group">
            <label for="address">{{ $t("payment.address") }}</label>
            <input
              v-model="address"
              type="text"
              id="address"
              placeholder="123 Main St, City"
              required
            />
          </div>
        </div>

        <!-- Datos de la tarjeta -->
        <div class="card card-data">
          <h3>{{ $t("payment.cardInfo") }}</h3>
          <form @submit.prevent="submitPayment" class="payment-form">
            <div class="form-group">
              <label for="cardNumber">{{ $t("payment.cardNumber") }}</label>
              <input
                v-model="cardNumber"
                type="text"
                id="cardNumber"
                placeholder="1234 5678 9876 5432"
                maxlength="19"
                required
              />
            </div>

            <div class="form-group">
              <label for="expiryDate">{{ $t("payment.expiryDate") }}</label>
              <input
                v-model="expiryDate"
                type="text"
                id="expiryDate"
                placeholder="MM/YY"
                maxlength="5"
                required
              />
            </div>

            <div class="form-group">
              <label for="cvv">{{ $t("payment.cvv") }}</label>
              <input v-model="cvv" type="text" id="cvv" placeholder="123" maxlength="3" required />
            </div>
          </form>
        </div>
      </div>

      <!-- Columna derecha -->
      <div class="right-column">
        <div class="card summary-card">
          <h3>{{ $t("payment.orderSummary") }}</h3>
          <ul
            class="summary-list"
            :style="cartItems.length >= 10 ? { maxHeight: '200px', overflowY: 'auto' } : {}"
          >
            <li v-for="(item, index) in cartItems" :key="index">
              {{ item.name }} - {{ item.quantity }} × ${{ item.price.toFixed(2) }}
            </li>
          </ul>

          <p class="total">Total: ${{ totalAmount.toFixed(2) }}</p>
          <button @click="submitPayment" class="submit-btn">{{ $t("payment.pay") }}</button>

          <div
            v-if="paymentStatus"
            :class="paymentStatus.success ? 'success' : 'error'"
            class="payment-status"
          >
            <p>{{ paymentStatus.message }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from "vue";

export default defineComponent({
  name: "CreditCardPayment",
  setup() {
    const cardNumber = ref("");
    const expiryDate = ref("");
    const cvv = ref("");
    const cardHolderName = ref("");
    const address = ref("");
    const paymentStatus = ref<{ success: boolean; message: string } | null>(null);

    const cartItems = ref([
      { name: "Item 1", quantity: 2, price: 12.99 },
      { name: "Item 2", quantity: 1, price: 24.5 },
      { name: "Item 1", quantity: 2, price: 12.99 },
      { name: "Item 2", quantity: 1, price: 24.5 },
      { name: "Item 1", quantity: 2, price: 12.99 },
      { name: "Item 2", quantity: 1, price: 24.5 },
      { name: "Item 1", quantity: 2, price: 12.99 },
      { name: "Item 2", quantity: 1, price: 24.5 },
      { name: "Item 1", quantity: 2, price: 12.99 },
      { name: "Item 2", quantity: 1, price: 24.5 },
      { name: "Item 1", quantity: 2, price: 12.99 },
      { name: "Item 2", quantity: 1, price: 24.5 },
      { name: "Item 1", quantity: 2, price: 12.99 },
      { name: "Item 2", quantity: 1, price: 24.5 },
    ]);

    const totalAmount = computed(() =>
      cartItems.value.reduce((sum, item) => sum + item.quantity * item.price, 0)
    );

    const submitPayment = () => {
      if (
        !cardNumber.value ||
        !expiryDate.value ||
        !cvv.value ||
        !cardHolderName.value ||
        !address.value
      ) {
        paymentStatus.value = {
          success: false,
          message: "Please fill all fields correctly.",
        };
        return;
      }

      paymentStatus.value = { success: true, message: "Payment successful! Thank you." };
    };

    return {
      cardNumber,
      expiryDate,
      cvv,
      cardHolderName,
      address,
      cartItems,
      totalAmount,
      paymentStatus,
      submitPayment,
    };
  },
});
</script>

<style scoped>
.payment-container {
  max-width: 1100px;
  margin: 40px auto;
  padding: 20px;
  background: linear-gradient(135deg, #6964ae, #652597, #363636);
  border-radius: 12px;
  color: #e9d8fd;
}

.payment-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.left-column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.right-column {
  display: flex;
  justify-content: center;
  align-items: center;
}

.card {
  background: rgba(59, 7, 100, 0.7);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
  width: 100%;
  color: #e9d8fd;
}

.payment-form,
.form-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

input {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #7c3aed;
  border-radius: 6px;
  background-color: #1e1b4b;
  color: #e9d8fd;
}

input::placeholder {
  color: #c4b5fd;
}

input:focus {
  outline: none;
  border-color: #c084fc;
  box-shadow: 0 0 0 2px #c084fc55;
}

.submit-btn {
  padding: 12px;
  background-color: #7c3aed;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  width: 100%;
  margin-top: 10px;
}

.submit-btn:hover {
  background-color: #a855f7;
}

.summary-list {
  list-style: none;
  padding: 0;
  margin: 0 0 10px 0;
}

.summary-list li {
  padding: 4px 0;
}

.total {
  font-weight: bold;
  margin-bottom: 10px;
}

.payment-status {
  margin-top: 10px;
  padding: 10px;
  border-radius: 6px;
  font-weight: bold;
}

.success {
  background-color: #4ade80;
  color: #1e3a1e;
}

.error {
  background-color: #f87171;
  color: #7f1d1d;
}
</style>
