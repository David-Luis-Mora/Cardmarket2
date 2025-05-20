<template>
  <div class="product-card card shadow-sm">
    <div class="d-flex justify-content-between align-items-center mb-3 title-row p-3">
      <h5 class="card-title text-primary mb-0">{{ product.name }}</h5>
      <router-link
        v-if="totalSellers > 5"
        class="btn btn-link p-0 view-button"
        :to="{ name: 'ProductDetail', params: { locale: $i18n.locale, productId: product.id } }"
      >
        {{ totalSellers }} {{ $t("productCard.items") }} →
      </router-link>
    </div>

    <div class="row g-0 align-items-stretch">
      <div class="col-md-2 p-0">
        <router-link
          class="btn btn-link p-0 view-button"
          :to="{ name: 'ProductDetail', params: { locale: $i18n.locale, productId: product.id } }"
        >
          <img
            :src="product.image"
            :alt="product.name"
            class="img-fluid rounded-start product-img"
          />
        </router-link>
      </div>
      <div class="col-md-10">
        <div class="card-body d-flex flex-column">
          <div v-if="totalSellers === 0" class="no-sellers mt-3 text-center text-muted">
            <i class="bi bi-emoji-frown-fill"></i>
            <p>{{ $t("productCard.noAvailable") }}</p>
          </div>

          <div v-else>
            <div
              v-for="(seller, index) in displayedSellers"
              :key="seller.sellerNickname + '-' + index"
              class="seller-row d-flex justify-content-between align-items-center py-2 px-4 border-top"
            >
              <div class="seller-info d-flex align-items-center">
                <span class="me-4">
                  <strong>{{ $t("productCard.seller") }}:</strong>
                  <router-link
                    :to="{
                      name: 'SellerProfile',
                      params: { locale: $i18n.locale, nickname: seller.sellerNickname },
                    }"
                    class="seller-link ms-1"
                  >
                    {{ seller.sellerNickname }}
                  </router-link>
                </span>
                <span class="me-4">
                  <strong>{{ $t("productCard.price") }}:</strong>
                  <span class="text-warning">${{ seller.price.toFixed(2) }}</span>
                </span>
                <span>
                  <strong>{{ $t("productCard.available") }}:</strong>
                  {{ seller.quantity }}
                </span>
              </div>
              <div class="action-controls d-flex align-items-center">
                <select v-model="selectedQuantities[index]" class="form-select form-select-sm me-2">
                  <option v-for="n in seller.quantity" :key="n" :value="n">{{ n }}</option>
                </select>
                <button class="btn btn-success btn-sm" @click="onAddToCart(seller, index)">
                  {{ $t("productCard.add") }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, watch } from "vue";
import { useCartStore } from "@/stores/cart";
import { useRoute, useRouter } from "vue-router";

interface Seller {
  sellerNickname: string;
  price: number;
  quantity: number;
  id_letter_sale: string;
}

interface CartProduct {
  id: number;
  name: string;
  type: string;
  rarity: string;
  basePrice: number;
  price: number;
  quantity: number;
  sellerNickname: string;
  img: string;
}

interface Product {
  id: number;
  name: string;
  image: string;
  type: string;
  rarity: string;
  basePrice: number;
  sellers: Seller[];
}

const route = useRoute();
const currentLang = (route.params.lang as string) || "es";
const props = defineProps<{ product: Product }>();
const cartStore = useCartStore();
const router = useRouter();

const selectedQuantities = ref<number[]>([]);

const totalSellers = computed(() => props.product.sellers.length);
const displayedSellers = computed(() =>
  props.product.sellers
    .slice()
    .sort((a, b) => a.price - b.price || a.sellerNickname.localeCompare(b.sellerNickname))
    .slice(0, 5)
);

watch(
  () => props.product.sellers,
  (sellers) => {
    selectedQuantities.value = sellers.map(() => 1);
  },
  { immediate: true }
);

async function onAddToCart(seller: Seller, idx: number) {
  const qty = selectedQuantities.value[idx] || 1;
  const cartItem: CartProduct = {
    id: props.product.id,
    name: props.product.name,
    type: props.product.type,
    rarity: props.product.rarity,
    basePrice: props.product.basePrice,
    price: seller.price,
    quantity: qty,
    sellerNickname: seller.sellerNickname,
    img: props.product.image,
    id_letter_sale: seller.id,
  };
  console.log(cartItem);
  try {
    console.log(cartItem);
    await cartStore.addProduct(cartItem);
    alert("¡Carta añadida al carrito!");
  } catch (err: any) {
    console.error("Error al añadir al carrito:", err);
    alert("Error al añadir: " + err.message);
  }
}

function viewAllSellers() {
  router.push({
    name: "ProductSellers",
    params: { locale: currentLang, productId: props.product.id },
  });
}
</script>

<style scoped>
.product-card {
  border: none;
  border-radius: 1rem;
  background-color: #0f172a;
  color: #e9d8fd;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.product-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
}

.title-row {
  background-color: #1e293b;
  border-bottom: 1px solid #334155;
}
.title-row .text-primary {
  color: #facc15 !important;
}
.view-button {
  color: #facc15;
  font-weight: 600;
}
.view-button:hover {
  color: #bb9a15;
}

.col-md-2 {
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-img {
  width: 100%;
  height: auto;
  object-fit: contain;
  background-color: #1e293b;
}

.seller-row {
  background-color: #1e293b;
}
.seller-info span {
  font-size: 0.9rem;
}

.form-select-sm {
  background-color: #ffffff;
  color: #000000;
  border: 1px solid #334155;
}
.btn-success {
  background-color: #28a745;
  border-color: #28a745;
  color: white;
  transition: background 0.2s ease-in-out;
}
.btn-success:hover {
  background-color: #218838;
  border-color: #218838;
}
.text-warning {
  color: #facc15 !important;
}

.btn-link {
  text-decoration: none;
  padding: 0;
}
.btn-link:hover {
  text-decoration: underline;
}

.no-sellers {
  color: #facc15;
  padding: 1rem;
  font-size: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.no-sellers i {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.seller-link {
  color: #a78bfa;
  text-decoration: none;
}
.seller-link:hover {
  text-decoration: underline;
}
</style>
