<template>
  <div class="container my-4">
    <div class="mb-4">
      <label for="expansionFilter" class="form-label">{{ $t('filterByExpansion') }}</label>
      <select id="expansionFilter" v-model="selectedExpansion" class="form-select" @change="resetPage">
        <option value="">{{ $t('allExpansions') }} ({{ totalCardCount }})</option>
        <option value="Cimientos">{{ $t('Cimientos') }} ({{ getCardCount('Cimientos') }})</option>
        <option value="The Brothers' War">{{ $t("The Brothers' War") }} ({{ getCardCount("The Brothers' War") }})</option>
        <option value="Dominaria United">{{ $t('Dominaria United') }} ({{ getCardCount('Dominaria United') }})</option>
      </select>
    </div>

    <div class="row row-cols-1 row-cols-md-3 row-cols-lg-4 g-4 justify-content-center">
      <ProductItem v-for="product in currentProducts" :key="product.id" :product="product" @add-to-cart="addToCart"
        class="col" />
    </div>

    <!-- Botones de Paginación -->
    <div v-if="!loading && !error" class="d-flex justify-content-center mt-4">
      <button class="btn btn-primary" @click="prevPage" :disabled="currentPage === 1">{{ $t('prev') }}</button>
      <span class="mx-3">{{ $t('page') }} {{ currentPage }} {{ $t('of') }} {{ totalPages }}</span>
      <button class="btn btn-primary" @click="nextPage" :disabled="currentPage === totalPages">{{ $t('next') }}</button>
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
            <p><strong>{{ $t('type') }}:</strong> {{ selectedProduct.type }}</p>
            <p><strong>{{ $t('rarity') }}:</strong> {{ selectedProduct.rarity }}</p>
            <p><strong>{{ $t('price') }}:</strong> ${{ selectedProduct.price }}</p>
            <button class="btn btn-success" @click="addToCart(selectedProduct)">{{ $t('addToCart') }}</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from 'vue';
import ProductItem from '../components/ProductItem.vue';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { auth } from '../firebaseConfig'; // Asegúrate de tener la configuración de Firebase correctamente importada
import { useAuthStore } from '../stores/authStore';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'ProductList',
  components: { ProductItem },
  setup() {
    const products = ref<any[]>([]); // Definir la variable como un arreglo vacío
    const selectedProduct = ref<any | null>(null); // Aquí defines la variable selectedProduct
    const selectedExpansion = ref('');
    const currentPage = ref(1);
    const productsPerPage = 20;
    const loading = ref(true); // Estado de carga
    const error = ref<string | null>(null); // Estado de error
    const cart = ref<any[]>([]); // El carrito de compras

    // Cargar los productos desde el archivo JSON
    const fetchProducts = async () => {
      try {
        const response = await fetch("/cards.json");
        if (!response.ok) {
          throw new Error("No se pudo cargar el archivo JSON");
        }
        const data = await response.json();
        products.value = data; // Asignar los productos cargados
        loading.value = false; // Cambiar el estado de carga a falso
      } catch (err) {
        error.value = err instanceof Error ? err.message : 'Error desconocido';
        loading.value = false;
      }
    };

    // Llamar a la función fetchProducts cuando el componente se monta
    onMounted(() => {
      fetchProducts();
    });

    const filteredProducts = computed(() => {
      return selectedExpansion.value
        ? products.value.filter((product: any) =>
          product.expansions === selectedExpansion.value // Compara directamente como cadenas

          )
        : products.value;
    });

    const totalPages = computed(() => {
      return Math.ceil(filteredProducts.value.length / productsPerPage);
    });

    const currentProducts = computed(() => {
      const startIndex = (currentPage.value - 1) * productsPerPage;
      return filteredProducts.value.slice(startIndex, startIndex + productsPerPage);
    });

    const totalCardCount = computed(() => {
      return products.value.length;
    });

    const getCardCount = (expansion: string) => {
      return products.value.filter((product: any) =>
      product.expansions === expansion

      ).length;
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

    onMounted(() => {
      authStore.initAuth();
    });

    // **Aquí está la corrección del método addToCart**
    const addToCart = (product: any) => {
    if (isAuthenticated.value) {
      cart.value.push(product);
      console.log('Added to cart:', product);
    } else {
      alert('Por favor, inicie sesión para añadir productos al carrito.');
    }
  };

    // Devolver todas las variables y métodos a la plantilla
    return {
      selectedExpansion,
      filteredProducts,
      totalPages,
      currentPage,
      currentProducts,
      totalCardCount,
      getCardCount,
      selectedProduct,
      selectProduct,
      closeModal,
      addToCart,
      prevPage,
      nextPage,
      resetPage,
      loading,
      error,
      cart
    };
  }
});
</script>


<style scoped>
.container {
  max-width: 1200px;
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
  /* Asegúrate de que la pantalla esté más oscura */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
  /* Asegura que esté por encima del contenido */
}

/* Modal Dialog */
.modal-dialog {
  max-width: 800px;
  width: 100%;
  /* Asegura que ocupe un buen porcentaje del ancho */
  background: white;
  border-radius: 8px;
  /* Mejora el diseño del modal */
  padding: 20px;
}

/* Modal Content */
.modal-content {
  display: flex;
  flex-direction: column;
}
</style>
