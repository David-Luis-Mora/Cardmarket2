<template>
  <div class="container my-4">
    <div class="row mb-3">
      <div class="col-md-6 mb-2">
        <input
          v-model="searchTerm"
          @input="resetPage"
          class="form-control"
          :placeholder="$t('productList.searchPlaceholder')"
        />
      </div>
      <div class="col-md-6">
        <select v-model="selectedExpansion" @change="resetPage" class="form-select">
          <option value="">{{ $t("productList.allExpansions") }}</option>
          <option v-for="exp in expansions" :key="exp.set_code" :value="exp.set_name">
            {{ exp.set_name }}
          </option>
        </select>
      </div>
    </div>

    <div
      v-if="!loading && currentProducts.length === 0"
      class="no-results my-4 text-center text-warning"
    >
      <i class="bi bi-emoji-frown-fill"></i>
      <p>{{ $t("productList.noResults") }}</p>
    </div>

    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">{{ $t("productList.loadingCards") }}</span>
      </div>
    </div>

    <div class="product-list-grid">
      <ProductItem
        v-for="product in currentProducts"
        :key="product.id"
        :product="product"
        @add-to-cart="addToCart"
      />
    </div>

    <div
      v-if="!loading && !error && totalPages > 1"
      class="d-flex justify-content-center align-items-center gap-2 mt-4 flex-wrap"
    >
      <button
        class="btn btn-sm btn-outline-secondary"
        @click="goToPage(1)"
        :disabled="currentPage === 1"
      >
        «<span class="visually-hidden">{{ $t("productList.firstPage") }}</span>
      </button>

      <button
        class="btn btn-sm btn-outline-secondary"
        @click="goToPage(currentPage - 1)"
        :disabled="currentPage === 1"
      >
        ‹<span class="visually-hidden">{{ $t("productList.prevPage") }}</span>
      </button>

      <button
        v-for="page in visiblePages"
        :key="page"
        class="btn btn-sm"
        :class="page === currentPage ? 'btn-primary' : 'btn-outline-primary'"
        @click="goToPage(page)"
      >
        {{ page }}
      </button>

      <button
        class="btn btn-sm btn-outline-secondary"
        @click="goToPage(currentPage + 1)"
        :disabled="currentPage === totalPages"
      >
        ›<span class="visually-hidden">{{ $t("productList.nextPage") }}</span>
      </button>

      <button
        class="btn btn-sm btn-outline-secondary"
        @click="goToPage(totalPages)"
        :disabled="currentPage === totalPages"
      >
        »<span class="visually-hidden">{{ $t("productList.lastPage") }}</span>
      </button>
    </div>

    <div v-if="selectedProduct" class="modal-overlay" @click.self="closeModal">
      <div class="modal modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ selectedProduct.name }}</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <img :src="selectedProduct.image" :alt="selectedProduct.name" class="img-fluid mb-3" />
            <p>
              <strong>{{ $t("type") }}:</strong> {{ selectedProduct.type }}
            </p>
            <p>
              <strong>{{ $t("rarity") }}:</strong> {{ selectedProduct.rarity }}
            </p>
            <p>
              <strong>{{ $t("price") }}:</strong> ${{ selectedProduct.price }}
            </p>
            <button class="btn btn-success" @click="addToCart(selectedProduct)">
              {{ $t("addToCart") }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, watch } from "vue";
import { useI18n } from "vue-i18n";
import ProductItem from "../components/ProductItem.vue";
import { useAuthStore } from "../stores/authStore";
export default defineComponent({
  name: "ProductList",
  components: { ProductItem },
  setup() {
    const { t } = useI18n();
    const searchTerm = ref("");
    const sort = ref("name");
    const selectedProduct = ref<any | null>(null);
    const selectedExpansion = ref("");
    const currentPage = ref(1);
    const productsPerPage = 20;
    const loading = ref(true);
    const error = ref<string | null>(null);
    const cart = ref<any[]>([]);
    const products = ref<any[]>([]);

    const totalCardCount = ref(0);
    const expansions = ref<{ set_name: string; set_code: string }[]>([]);
    const pageWindowSize = 6;

    const paginationStart = computed(() => {
      return Math.max(1, currentPage.value - Math.floor(pageWindowSize / 2));
    });

    const paginationEnd = computed(() => {
      return Math.min(totalPages.value, paginationStart.value + pageWindowSize - 1);
    });

    const visiblePages = computed(() => {
      const pages = [];
      for (let i = paginationStart.value; i <= paginationEnd.value; i++) {
        pages.push(i);
      }
      return pages;
    });

    const goToPage = (page: number) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page;
      }
    };

    const fetchExpansions = async () => {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/cards/expansions/`);
        const text = await res.text();

        let data;
        try {
          data = JSON.parse(text);
        } catch {
          throw new Error("Respuesta no válida: no es JSON");
        }

        expansions.value = data.expansions || [];

        if (expansions.value.length > 0 && !selectedExpansion.value) {
          selectedExpansion.value = expansions.value[0].set_name;
        }
      } catch (err) {
        console.error("❌ Error al cargar expansiones:", err);
      }
    };

    const fetchProducts = async () => {
      loading.value = true;

      const selected = expansions.value.find((e) => e.set_name === selectedExpansion.value);
      const expansionCode = selected?.set_code;

      const params = new URLSearchParams({
        "number-start": currentPage.value.toString(),
        search: searchTerm.value,
        sort: sort.value,
      });

      const url = expansionCode
        ? `${
            import.meta.env.VITE_API_URL
          }/api/cards/expansion/${expansionCode}/?${params.toString()}`
        : `${import.meta.env.VITE_API_URL}/api/cards/all/?${params.toString()}`;

      try {
        console.log(url);
        const response = await fetch(url);
        const responseText = await response.text();
        const data = JSON.parse(responseText);

        if (!response.ok) {
          throw new Error(data.error || `Error ${response.status}`);
        }

        products.value = data.cards || [];
        totalCardCount.value = data.total || 0;
        error.value = null;
      } catch (err: any) {
        error.value = err.message || "Error desconocido";
        products.value = [];
        totalCardCount.value = 0;
        console.error("❌ Error al obtener productos:", err);
      } finally {
        loading.value = false;
      }
    };

    watch([searchTerm, selectedExpansion, sort], () => {
      resetPage();
      fetchProducts();
    });

    watch(currentPage, fetchProducts);

    const totalPages = computed(() => {
      return Math.ceil(totalCardCount.value / productsPerPage);
    });

    const currentProducts = computed(() => {
      console.log("📦 currentProducts:", products.value);
      return products.value;
    });

    const getCardCount = (expansion: string) => {
      return products.value.filter((product: any) => product.expansion === expansion).length;
    };

    const resetPage = () => {
      currentPage.value = 1;
    };

    const selectProduct = (product: any) => {
      selectedProduct.value = product;
    };

    const closeModal = () => {
      selectedProduct.value = null;
    };

    const prevPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--;
      }
    };

    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++;
      }
    };

    const authStore = useAuthStore();
    const isAuthenticated = computed(() => authStore.isAuthenticated);

    const init = async () => {
      authStore.initAuth();
      await fetchExpansions();
      await fetchProducts();
    };

    onMounted(init);

    const addToCart = (product: any) => {
      if (isAuthenticated.value) {
        cart.value.push(product);
        console.log("Added to cart:", product);
      } else {
        alert(t("productList.loginRequired"));
      }
    };

    return {
      searchTerm,
      sort,
      selectedExpansion,
      selectedProduct,
      currentPage,
      currentProducts,
      totalPages,
      totalCardCount,
      getCardCount,
      loading,
      error,
      addToCart,
      selectProduct,
      closeModal,
      prevPage,
      nextPage,
      resetPage,
      cart,
      expansions,
      goToPage,
      paginationStart,
      visiblePages,
      paginationEnd,
    };
  },
});
</script>

<style scoped>
.container {
  max-width: 1200px;
}

.text-center {
  color: white;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-dialog {
  max-width: 800px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-dialog {
  max-width: 800px;
  width: 100%;
  background: white;
  border-radius: 8px;
  padding: 20px;
}

.modal-content {
  display: flex;
  flex-direction: column;
}

.no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #facc15;
}
.no-results i {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}
.product-list-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.product-list-grid .card-img-top {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

@media (max-width: 768px) {
  .product-list-grid {
    grid-template-columns: repeat(1, 1fr);
    gap: 0.5rem;
  }
  .product-list-grid .card-img-top {
    height: 100px;
  }
}
</style>
