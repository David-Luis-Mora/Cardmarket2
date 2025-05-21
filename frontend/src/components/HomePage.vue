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
            src="/img/ff.png"
            class="d-block w-100"
            alt="Imagen de cartas 2"
            style="height: 400px; object-fit: cover"
          />
        </div>
        <div class="carousel-item">
          <img
            src="/img/fo.png"
            class="d-block w-100"
            alt="Imagen de cartas 3"
            style="height: 400px; object-fit: cover"
          />
        </div>
        <div class="carousel-item">
          <img
            src="/img/ld.png"
            class="d-block w-100"
            alt="Imagen de cartas 4"
            style="height: 400px; object-fit: cover"
          />
        </div>
        <div class="carousel-item">
          <img
            src="/img/w4.png"
            class="d-block w-100"
            alt="Imagen de cartas 5"
            style="height: 400px; object-fit: cover"
          />
        </div>
        <div class="carousel-item">
          <img
            src="/img/phyrexia.png"
            class="d-block w-100"
            alt="Imagen de cartas 5"
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
      <div class="col-md-3 mb-2" v-for="card in randomCards" :key="card.id">
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

    <div class="row mt-5">
      <h2 class="section-title">{{ $t("mainproducts") }}</h2>
      <hr />
      <div class="col-md-4 mb-3" v-for="producto in productos" :key="producto.key">
        <button type="button" class="card-button" @click="goToCards">
          <div class="card">
            <img
              :src="producto.imagen"
              class="card-img-top"
              :alt="$t(`products.${producto.key}.nombre`)"
            />
            <div class="card-body">
              <h5 class="card-title">
                {{ $t(`products.${producto.key}.nombre`) }}
              </h5>
              <p class="card-text">
                {{ $t(`products.${producto.key}.descripcion`) }}
              </p>
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
import { useRouter, useRoute } from "vue-router";
import { useI18n } from "vue-i18n";

const randomCards = ref([]);
const productStore = useCartStore();
const router = useRouter();
const route = useRoute();
const { locale } = useI18n();
const productos = [
  {
    key: "foundations",
    imagen: "/img/cimientos.jpg",
    expansions: "Foundations",
  },
  {
    key: "dominaria_united",
    imagen: "/img/dominaria_united.jpg",
    expansions: "Dominaria United",
  },
  {
    key: "brothers_war",
    imagen: "/img/the_brothers_war.jpeg",
    expansions: "The Brothers' War",
  },
];

function goToCards() {
  console.log("🔵 goToCards fired!", { locale: locale.value, routeLang: route.params.lang });
  router.push({
    name: "Cards",
    params: { lang: route.params.lang || locale.value },
  });
}
const fetchRandomCards = async (count = 6) => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/cards/random/?count=${count}`, {
      headers: { Accept: "application/json" },
    });
    if (!response.ok) {
      console.error("Error al cargar cartas:", response.statusText);
      return;
    }

    const data = await response.json();
    console.log("Respuesta completa de random-cards:", data);
    data.cards.forEach((c) => console.log("card.img ->", c.img));

    randomCards.value = data.cards;
  } catch (error) {
    console.error("Falló la petición de cartas aleatorias:", error);
  }
};

const seleccionarProducto = (expansion) => {
  router.push({ name: "product-list", params: { expansion } });
};

onMounted(async () => {
  await fetchRandomCards(6);
});
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
  border: 1px solid #7c3aed;
  border-radius: 10px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-body {
  background-color: #1e1b4b;
  color: #e9d8fd;
  border-bottom-right-radius: 10px;
  border-bottom-left-radius: 10px;
}

.title {
  color: #facc15;
}

.card-title {
  color: #facc15;
  font-size: 1.1rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.card-text {
  color: #e9d8fd;
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
  color: #facc15;
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

  .row.mt-5 .col-md-3 {
    flex: 0 0 50% !important;
    max-width: 50% !important;
  }

  .card-img-top {
    height: 250px !important;
  }

  .card-body h5,
  .card-body .card-title {
    font-size: 0.85rem;
  }
  .card-body p,
  .card-text {
    font-size: 0.75rem;
  }
}
</style>
