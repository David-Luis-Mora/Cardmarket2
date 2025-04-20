<template>
  <div class="product-item">
    <img :src="product.img" :alt="product.name" />
    <p>{{ product.price }} $</p>
    <!-- Selección de cantidad basada en la cantidad disponible en el JSON -->
    <select v-model="selectedQuantity" class="quantity-select">
      <option v-for="n in product.quantity" :key="n" :value="n">{{ n }}</option>
    </select>

    <button @click="addToCart">Add to Cart</button>
  </div>
</template>

<script lang="ts">
import { defineComponent, inject, ref, type Ref } from 'vue';
import { useCartStore } from '@/stores/cart';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';

interface Product {
  id: number;
  name: string;
  type: string;
  rarity: string;
  price: number;
  quantity: number;
  img: string;
  basePrice: number;
}

export default defineComponent({
  name: 'ProductItem',
  props: {
    product: {
      type: Object as () => Product,
      required: true,
    },
  },
  setup(props) {
    const logueado = inject('logueado') as Ref<boolean>;
    const cartStore = useCartStore();
    const router = useRouter();
    const { locale } = useI18n();

    const selectedQuantity = ref(1);

    const addToCart = () => {
      if (!logueado.value) {
        router.push(`/${locale.value}/login`);
        return;
      }

      const productToAdd: Product = {
      ...(props.product as Product),
      quantity: selectedQuantity.value,
    };


      cartStore.addProduct(productToAdd);
    };

    return {
      selectedQuantity,
      addToCart,
    };
  },
});

</script>

<style scoped>
.product-item {
  border: none;
  background: none;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 220px;
  box-sizing: border-box;
}

.product-item:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.image-card {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

.image-card img {
  width: 200px;
  object-fit: cover;
  border-radius: 8px;
}

.name-card {
  text-align: center;
  font-weight: bold;
}

.product-item img {
  width: 100px;
  height: 100px;
  object-fit: cover;
}

.product-item img {
  width: 100%;   /* Ajusta el ancho de la imagen al contenedor */
  height: auto;  /* Mantiene la proporción de la imagen */
  object-fit: contain;  /* Asegura que la imagen se vea completa sin recorte */
}

.quantity-select {
  margin: 5px 0;
  padding: 5px;
  font-size: 14px;
  border-radius: 5px;
  border: 1px solid #ccc;
}
</style>
