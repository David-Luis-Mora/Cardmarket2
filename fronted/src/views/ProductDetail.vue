<template>
  <div class="product-detail d-flex flex-column flex-md-row p-4">
    <!-- Left: Image and Basic Info -->
    <div class="info-box p-3 mb-4 mb-md-0 me-md-4 rounded">
      <div class="image-box mb-3">
        <img :src="product?.image" :alt="product?.name" class="detail-img rounded" />
      </div>
      <div class="basic-info text-center">
        <h2 class="detail-title mb-2">{{ product?.name }}</h2>
        <p class="mb-1">
          <strong>{{ $t("productDetail.typeLabel") }}:</strong>
          {{ product?.type }}
        </p>
        <p class="mb-1">
          <strong>{{ $t("productDetail.rarityLabel") }}:</strong>
          {{ product?.rarity }}
        </p>
        <p class="mb-0">
          <strong>{{ $t("productDetail.basePriceLabel") }}:</strong>
          ${{ cheapestPrice.toFixed(2) }}
        </p>
      </div>
    </div>

    <!-- Right: Sellers List -->
    <div class="sellers-box flex-grow-1 p-3 rounded">
      <h4 class="section-title mb-3">
        {{ $t("productDetail.sellersTitle", { total: totalSellers }) }}
      </h4>
      <div v-if="!sortedSellers.length" class="no-sellers">
        <i class="bi bi-emoji-frown-fill"></i>
        <p>{{ $t("productDetail.noSellers") }}</p>
      </div>
      <div
        v-else
        class="sellers-list"
        :style="{
          maxHeight: sortedSellers.length > 10 ? '400px' : 'none',
          overflowY: sortedSellers.length > 10 ? 'auto' : 'visible',
        }"
      >
        <div
          v-for="(seller, idx) in sortedSellers"
          :key="seller.username + '-' + idx"
          class="seller-row d-flex justify-content-between align-items-center p-2 mb-2 rounded"
        >
          <div>
            {{ $t("productDetail.sellerLabel") }}:
            <router-link
              :to="{
                name: 'SellerProfile',
                params: { lang: currentLang, nickname: seller.username },
              }"
              class="seller-link ms-1"
            >
              {{ seller.username }}
            </router-link>
            <span class="ms-3">
              {{ $t("productDetail.priceLabel") }}: ${{ seller.price.toFixed(2) }}
            </span>
            <span class="ms-3">
              {{ $t("productDetail.quantityLabel") }}:
              {{ seller.quantity }}
            </span>
          </div>
          <div class="action-controls d-flex align-items-center">
            <select v-model="selectedQuantities[idx]" class="form-select form-select-sm me-2">
              <option v-for="n in seller.quantity" :key="n" :value="n">{{ n }}</option>
            </select>
            <button class="btn btn-success btn-sm" @click="addToCart(seller, idx)">
              {{ $t("productDetail.add") }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, watch, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useCartStore } from "@/stores/cart";

interface Seller {
  username: string;
  price: number;
  quantity: number;
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
const productId = route.params.productId as string;
const cartStore = useCartStore();

const product = ref<Product | null>(null);
const selectedQuantities = ref<number[]>([]);

async function fetchProduct(): Promise<void> {
  const res = await fetch(`http://localhost:8000/api/cards/${productId}/`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const data = (await res.json()) as Product;
  product.value = data;
}

// 1) Filtrar solo sellers con quantity > 0 y luego ordenar
const sortedSellers = computed<Seller[]>((): Seller[] => {
  if (!product.value) return [];
  return product.value.sellers
    .filter((seller) => seller.quantity > 0)
    .sort((a, b) => a.price - b.price || a.username.localeCompare(b.username));
});

// 2) Ajustar selectedQuantities al número de sellers filtrados
watch(
  sortedSellers,
  (sellers) => {
    selectedQuantities.value = sellers.map(() => 1);
  },
  { immediate: true }
);

// 3) totalSellers cuenta solo los filtrados
const totalSellers = computed((): number => sortedSellers.value.length);

// cheapestPrice toma el mínimo de los filtrados
const cheapestPrice = computed((): number => {
  const sellers = sortedSellers.value;
  return sellers.length ? sellers[0].price : product.value?.basePrice ?? 0;
});

function addToCart(seller: Seller, idx: number) {
  const qty = selectedQuantities.value[idx] || 1;
  cartStore
    .addProduct({
      id: product.value!.id,
      name: product.value!.name,
      img: product.value!.image,
      price: seller.price,
      quantity: qty,
      rarity: product.value!.rarity,
      sellerNickname: seller.username,
    })
    .catch((e) => alert("Error al añadir: " + e.message));
}

onMounted(fetchProduct);
</script>

<style scoped>
.product-detail {
  background-color: #0f172a;
  color: #e9d8fd;
}
.info-box {
  background-color: #1e293b;
}
.image-box {
  text-align: center;
}
.detail-img {
  width: 100%;
  height: auto;
  max-width: 200px;
  object-fit: cover;
  border: 2px solid #334155;
}
.basic-info h2 {
  font-size: 1.75rem;
  color: #facc15;
}
.basic-info p {
  margin: 0.25rem 0;
}
.sellers-box {
  background-color: #1e293b;
}
.section-title {
  color: #facc15;
  font-size: 1.5rem;
}
.sellers-list {
  display: flex;
  flex-direction: column;
}
.seller-row {
  background-color: #273549;
  transition: background-color 0.3s;
}
.seller-row:hover {
  background-color: #334155;
}
.seller-link {
  color: #a78bfa;
  text-decoration: none;
}
.seller-link:hover {
  text-decoration: underline;
}
.form-select-sm {
  background-color: #ffffff;
  color: #000000;
  border: 1px solid #334155;
}
.btn-success {
  background-color: #28a745;
  border-color: #28a745;
}
.no-sellers {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #facc15;
  padding: 1rem;
}
.no-sellers i {
  font-size: 3rem;
}
</style>
