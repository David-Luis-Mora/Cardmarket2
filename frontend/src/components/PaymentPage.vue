<template>
  <div class="payment-container">
    <h2>{{ $t("payment.title") }}</h2>
    <div class="payment-method-selector">
      <label>
        <input type="radio" v-model="method" value="wallet" />
        {{ $t("payment.useWallet") }}
      </label>
      <label>
        <input type="radio" v-model="method" value="card" />
        {{ $t("payment.useCard") }}
      </label>
    </div>

    <div class="payment-grid">
      <div class="left-column">
        <div class="card info-card">
          <h3>
            {{ $t("payment.customerInfo") }}
          </h3>
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

        <div v-if="method === 'card'" class="card card-data">
          <h3>{{ $t("payment.cardInfo") }}</h3>
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
        </div>
      </div>

      <div class="right-column">
        <div class="card summary-card">
          <div v-if="method === 'wallet'" class="card wallet-card">
            <h3>{{ $t("payment.walletBalance") }}</h3>
            <p v-if="walletLoading">{{ $t("payment.loading") }}...</p>
            <p v-else-if="walletError" class="error">{{ walletError }}</p>
            <p v-else class="balance">
              {{ $t("payment.availableBalance") }}: ${{ walletBalance.toFixed(2) }}
            </p>
          </div>
          <h3>{{ $t("payment.orderSummary") }}</h3>
          <ul
            class="summary-list"
            :style="cartItems.length >= 10 ? { maxHeight: '200px', overflowY: 'auto' } : {}"
          >
            <li v-for="(item, i) in cartItems" :key="i">
              <strong>{{ item.name }}</strong> – {{ item.quantity }} × ${{
                item.price.toFixed(2)
              }}
              = <span class="item-total">${{ (item.quantity * item.price).toFixed(2) }}</span>
            </li>
          </ul>

          <p class="total">{{ $t("payment.total") }}: ${{ totalAmount.toFixed(2) }}</p>

          <button
            @click="submitPayment"
            class="submit-btn"
            :disabled="loading || (method === 'wallet' && walletBalance < totalAmount)"
          >
            {{
              method === "wallet"
                ? $t("payment.payWithWallet", { total: totalAmount.toFixed(2) })
                : $t("payment.payWithCard", { total: totalAmount.toFixed(2) })
            }}
          </button>

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
import { defineComponent, ref, computed, watch, onMounted } from "vue";
import { useCartStore } from "@/stores/cart";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";

export default defineComponent({
  name: "CreditCardPayment",
  setup() {
    const cartStore = useCartStore();
    const router = useRouter();
    const { t, locale } = useI18n();

    const method = ref<"wallet" | "card">("wallet");
    const cardHolderName = ref("");
    const address = ref("");
    const cardNumber = ref("");
    const expiryDate = ref("");
    const cvv = ref("");
    const loading = ref(false);
    const paymentStatus = ref<{ success: boolean; message: string } | null>(null);

    const walletBalance = ref(0);
    const walletLoading = ref(false);
    const walletError = ref("");

    const cartItems = computed(() => cartStore.products);
    const totalAmount = computed(() => cartStore.total);

    function getAuthHeaders() {
      const token = localStorage.getItem("token") || "";
      return {
        Authorization: `Token ${token}`,
        "Content-Type": "application/json",
      };
    }

    async function fetchWalletBalance() {
      walletLoading.value = true;
      walletError.value = "";
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/users/wallet/`, {
          method: "GET",
          headers: getAuthHeaders(),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Error al obtener saldo");
        walletBalance.value = data.balance;
      } catch (err: any) {
        walletError.value = err.message;
      } finally {
        walletLoading.value = false;
      }
    }

    onMounted(() => {
      if (method.value === "wallet") fetchWalletBalance();
    });
    watch(method, (m) => {
      if (m === "wallet") fetchWalletBalance();
    });

    async function submitPayment() {
      if (!cardHolderName.value || !address.value) {
        paymentStatus.value = {
          success: false,
          message: t("payment.errorFillCustomer"),
        };
        return;
      }
      if (method.value === "card") {
        if (!cardNumber.value || !expiryDate.value || !cvv.value) {
          paymentStatus.value = {
            success: false,
            message: t("payment.errorFillCard"),
          };
          return;
        }
      }

      if (method.value === "wallet" && walletBalance.value < totalAmount.value) {
        paymentStatus.value = {
          success: false,
          message: t("payment.errorInsufficientFunds"),
        };
        return;
      }

      loading.value = true;
      paymentStatus.value = null;

      try {
        let res, data;
        if (method.value === "wallet") {
          res = await fetch(`${import.meta.env.VITE_API_URL}/api/users/cart/buy-for-wallet/`, {
            method: "POST",
            headers: getAuthHeaders(),
            body: null,
          });
        } else {
          res = await fetch(`${import.meta.env.VITE_API_URL}/api/users/cart/buy-for-card/`, {
            method: "POST",
            headers: getAuthHeaders(),
            body: JSON.stringify({
              "card-number": cardNumber.value,
              "exp-date": expiryDate.value,
              cvc: cvv.value,
            }),
          });
        }
        data = await res.json();
        if (!res.ok) {
          throw new Error(data.error || t("payment.errorGeneric"));
        }
        paymentStatus.value = {
          success: true,
          message: data.message || t("payment.successMessage"),
        };
        cartStore.clearCart();
        alert(t("payment.successMessage"));
        router.push({
          name: "MyProfile",
          params: { lang: locale.value },
        });
      } catch (err: any) {
        paymentStatus.value = {
          success: false,
          message: err.message,
        };
      } finally {
        loading.value = false;
      }
    }

    return {
      method,
      cardHolderName,
      address,
      cardNumber,
      expiryDate,
      cvv,
      cartItems,
      totalAmount,
      loading,
      paymentStatus,
      walletBalance,
      walletLoading,
      walletError,
      submitPayment,
    };
  },
});
</script>

<style scoped>
.payment-container {
  padding: 1rem;
}
.payment-method-selector {
  margin-bottom: 1rem;
  display: flex;
  gap: 1rem;
}
.payment-grid {
  display: flex;
  gap: 1rem;
}
.left-column,
.right-column {
  flex: 1;
}
.card {
  background: #fff;
  padding: 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
}
.wallet-card p.balance {
  font-size: 1.25rem;
  font-weight: bold;
}
.form-group {
  margin-bottom: 0.75rem;
}
.summary-list {
  list-style: none;
  padding: 0;
}
.total {
  font-weight: bold;
  margin-top: 1rem;
}
.submit-btn {
  width: 100%;
  padding: 0.75rem;
  margin-top: 1rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
}
.submit-btn[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}
.success {
  color: green;
  margin-top: 1rem;
}
.error {
  color: red;
  margin-top: 1rem;
}

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

.payment-container {
  padding: 1rem;
  max-width: 1100px;
  margin: 40px auto;
  background: linear-gradient(135deg, #6964ae, #652597, #363636);
  border-radius: 12px;
  color: #e9d8fd;
}

/* Rejilla principal */
.payment-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

/* Columnas */
.left-column,
.right-column {
  width: 100%;
}

/* Tarjetas */
.card {
  background: rgba(59, 7, 100, 0.7);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
  color: #e9d8fd;
}

/* Formularios */
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

/* ==========================
   RESPONSIVE
   ========================== */

/* Tablets y pantallas medias */
@media (max-width: 1024px) {
  .payment-grid {
    grid-template-columns: 1fr; /* Una sola columna */
  }
  .payment-method-selector {
    flex-direction: column;
    gap: 0.5rem;
  }
}

/* Móviles */
@media (max-width: 600px) {
  .payment-container {
    padding: 0.5rem;
    margin: 20px auto;
  }
  .payment-method-selector label {
    font-size: 0.9rem;
  }
  .card {
    padding: 15px;
  }
  input {
    font-size: 14px;
    padding: 8px;
  }
  .submit-btn {
    padding: 10px;
    font-size: 14px;
  }
  .summary-list {
    max-height: 150px;
    overflow-y: auto;
  }
}
</style>
