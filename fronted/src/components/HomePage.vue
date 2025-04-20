<template>
  <div class="container mt-5">
    <h1 class="text-center display-4 mb-4">{{ $t("welcome") }}</h1>

    <div
      id="carouselid"
      class="carousel slide border border-4 border-facc15 rounded"
      data-bs-ride="carousel"
      data-bs-interval="3000"
    >
      <div class="carousel-inner">
        <div class="carousel-item active">
          <img
            src="/img/lightning.png"
            class="d-block w-100"
            alt="Imagen de cartas 1"
            style="height: 400px; object-fit: cover"
          />
        </div>
        <div class="carousel-item">
          <img
            src="/img/phyrexia.png"
            class="d-block w-100"
            alt="Imagen de cartas 2"
            style="height: 400px; object-fit: cover"
          />
        </div>
        <div class="carousel-item">
          <img
            src="/img/bosque.png"
            class="d-block w-100"
            alt="Imagen de cartas 3"
            style="height: 400px; object-fit: cover"
          />
        </div>
      </div>
      <button
        class="carousel-control-prev"
        type="button"
        data-bs-target="#carouselid"
        data-bs-slide="prev"
      >
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button
        class="carousel-control-next"
        type="button"
        data-bs-target="#carouselid"
        data-bs-slide="next"
      >
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>

    <div class="row mt-5">
      <h2 class="section-title">{{ $t("tendencies") }}</h2>
      <hr />
      <!-- Iteramos sobre las 6 cartas aleatorias -->
      <div class="col-md-3 mb-2" v-for="(card, index) in randomCards" :key="card.id">
        <div class="card">
          <img
            :src="card.img"
            class="card-img-top"
            :alt="`Carta ${card.name}`"
            style="height: 370px; object-fit: cover"
          />
          <div class="card-body">
            <h5 class="card-title">{{ card.name }}</h5>
            <p class="card-text">{{ card.price }}$</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Productos -->
    <div class="row mt-5">
      <h2>{{ $t("products") }}</h2>
      <hr />
      <div class="col-md-4 mb-3" v-for="producto in productos" :key="producto.id">
        <button class="card-button" @click="seleccionarProducto(producto.expansions)">
          <div class="card">
            <img :src="producto.imagen" class="card-img-top" :alt="producto.nombre" />
            <div class="card-body">
              <h5 class="card-title">{{ producto.nombre }}</h5>
              <p class="card-text">{{ producto.descripcion }}</p>
            </div>
          </div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useCartStore } from "@/stores/cart";
import { useRouter } from "vue-router";

const randomCards = ref([]);
const productStore = useCartStore();
const selectedCard = ref(null);
const selectedQuantity = ref(1);
const availableQuantities = ref([]);

const router = useRouter(); // Inicializar router

const productos = [
  {
    nombre: "Cimiento",
    imagen: "/img/cimientos.jpg",
    expansions: "Cimiento",
    descripcion:
      "Foundations is a new type of set designed to carry through multiple Standard rotations. It contains mechanically unique card designs as well as 'less-complex, clean and elegant' reprints, functioning similarly to an 'evergreen Core set'Unlike other Standard-legal sets, cards in Foundations will remain legal in Standard until 2029, at least. Foundations is intended to be reprinted and released annually over that period.",
  },
  {
    nombre: "Dominaria United",
    imagen: "/img/dominaria_united.jpg",
    expansions: "Dominaria United",
    descripcion:
      "Public domain name registries connected to this name were filed by a subsidiary registrar in January 2021. A further registration with the gg domain was filed by Wizards of the Coast itself in May 2021. Dominaria United contains 281 cards (101 commons, 80 uncommons, 60 rares, 20 mythic rares, 20 basic lands), and includes randomly inserted premium versions of all cards. Set, Draft and Collector Boosters contain a legendary card in each booster, showing off a cast of beloved legends and characters that longtime fans will recognize.",
  },
  {
    nombre: "The Brothers' War",
    imagen: "/img/the_brothers_war.jpeg",
    expansions: "The Brothers' War",
    descripcion:
      "The Brothers' War was designed as an 'event set', meaning that its mechanical structure was built around an event rather than a world. In this case, the set revolves around the story of the Brothers' War, a major event in Magic's timeline that was previously portrayed in the set Antiquities and various works of fiction such as the novel The Brothers' War by Jeff Grubb. The Vision Design team, working in conjunction with the Creative team, divided the story into three acts: Childhood.",
  },
];

// Función para obtener una carta aleatoria
const selectAndCopyCards = () => {
  // Limpiar cartas previas
  randomCards.value = [];

  const cartProductIds = productStore.products.map((product) => product.id);
  const usedIds = new Set();

  // Filtrar productos válidos
  const validProducts = productStore.storeProducts.filter(
    (product) => !cartProductIds.includes(product.id)
  );

  // Barajar aleatoriamente
  const shuffled = validProducts.sort(() => Math.random() - 0.5);

  const selected = shuffled.slice(0, 4);

  randomCards.value = selected.map((card, index) => ({
    ...card,
    id: `${card.id}-${Date.now()}-${index}`,
  }));
};

// Función para mostrar el modal con la carta seleccionada
const showModal = (card) => {
  selectedCard.value = card;
  availableQuantities.value = Array.from({ length: card.stock }, (_, i) => i + 1);
  const modal = new bootstrap.Modal(document.getElementById("addToCartModal"));
  modal.show();
};

// Función para añadir la carta al carrito
const addToCart = () => {
  if (selectedCard.value) {
    const productToAdd = {
      ...selectedCard.value,
      quantity: selectedQuantity.value,
    };
    productStore.addProduct(productToAdd);
  }
  // Cerrar el modal
  const modal = bootstrap.Modal.getInstance(document.getElementById("addToCartModal"));
  modal.hide();
};

onMounted(async () => {
  await productStore.fetchProducts();
  selectAndCopyCards();
});

const seleccionarProducto = (expansion) => {
  // Redirige a la ruta de ProductList, pasando el parámetro de expansión
  router.push({ name: "product-list", params: { expansion } });
  return {
    seleccionarProducto,
    // otros métodos y propiedades
  };
};
</script>

<style scoped>
.carousel-item img {
  height: 400px;
  object-fit: cover;
}

.container {
  max-width: 1200px;
}

.card-img-top {
  height: 200px;
  object-fit: cover;
}

.custom-card {
  border: 1px solid #7c3aed; /* Morado oscuro */
  border-radius: 10px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-body {
  background-color: #1e1b4b; /* Fondo oscuro */
  color: #e9d8fd; /* Color suave de texto */
  border-bottom-right-radius: 10px;
  border-bottom-left-radius: 10px;
}

.title {
  color: #facc15; /* Amarillo brillante */
}

.card-title {
  color: #facc15; /* Amarillo brillante */
  font-size: 1.1rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.card-text {
  color: #e9d8fd; /* Color suave de texto */
  font-size: 0.9rem;
}

.card-button {
  background: none;
  border: none;
  width: 100%;
  padding: 0;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-button:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.card-button:focus {
  outline: none;
}

.section-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #facc15; /* Amarillo brillante */
  text-transform: uppercase;
  letter-spacing: 1px;
  text-align: center;
}

.section-divider {
  border-color: rgba(255, 255, 255, 0.2);
  margin: 20px 0;
}

@media (max-width: 768px) {
  .section-title {
    font-size: 1.3rem;
  }

  .card-title {
    font-size: 1rem;
  }

  .card-text {
    font-size: 0.85rem;
  }
}
</style>

<!-- <style scoped>
.carousel-item img {
    height: 400px;
    object-fit: cover;
}

.container {
    max-width: 1200px;
}

.card-img-top {
    height: 200px;
    object-fit: cover;
}

.custom-card {
    border: 1px solid #f39c12;
    border-radius: 10px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-body {
    background-color: #3e2723;
    color: #f1e0c6;
    border-bottom-right-radius: 10px;
    border-bottom-left-radius: 10px;

}

.title {
    color: #f39c12;
}

.card-title {
    color: #f39c12;
    font-size: 1.1rem;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.card-text {
    color: #f1e0c6;
    font-size: 0.9rem;
}

.card-button {
    background: none;
    border: none;
    width: 100%;
    padding: 0;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-button:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.card-button:focus {
    outline: none;
}

.section-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: #f39c12;
    text-transform: uppercase;
    letter-spacing: 1px;
    text-align: center;
}

.section-divider {
    border-color: rgba(255, 255, 255, 0.2);
    margin: 20px 0;
}

@media (max-width: 768px) {
    .section-title {
        font-size: 1.3rem;
    }

    .card-title {
        font-size: 1rem;
    }

    .card-text {
        font-size: 0.85rem;
    }
}
</style> -->
