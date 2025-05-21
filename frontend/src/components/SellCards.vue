<template>
  <div class="container my-4">
    <h2 class="mb-4">{{ $t("sellCards.title") }}</h2>

    <div class="row mb-3">
      <div class="col-md-6 mb-2">
        <input
          v-model="searchTerm"
          @input="resetPage"
          class="form-control"
          :placeholder="$t('sellCards.searchPlaceholder')"
        />
      </div>
      <div class="col-md-6">
        <select v-model="selectedExpansion" @change="resetPage" class="form-select">
          <option value="">{{ $t("sellCards.allExpansions") }}</option>
          <option v-for="exp in expansions" :key="exp.set_code" :value="exp.set_name">
            {{ exp.set_name }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">{{ $t("sellCards.loadingCards") }}</span>
      </div>
    </div>
    <div class="row" v-else>
      <div v-for="card in currentCards" :key="card.id" class="col-12 mb-3">
        <div class="card p-3 d-flex flex-column flex-md-row align-items-start">
          <img
            :src="card.image"
            :alt="$t('sellCards.cardImageAlt', { name: card.name })"
            class="img-fluid me-3"
            style="max-height: 150px"
          />
          <div class="flex-grow-1">
            <h5>{{ card.name }}</h5>
            <p>
              <strong>{{ $t("sellCards.rarityLabel") }}:</strong> {{ card.rarity }}
            </p>
            <div class="d-flex align-items-center">
              <input
                v-model.number="sellPrice[card.id]"
                type="number"
                :placeholder="$t('sellCards.pricePlaceholder')"
                class="form-control me-2"
              />
              <input
                v-model.number="sellQuantity[card.id]"
                type="number"
                :placeholder="$t('sellCards.quantityPlaceholder')"
                class="form-control me-2"
              />
              <button class="btn btn-success" @click="publish(card)">
                {{ $t("sellCards.publish") }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="!loading && totalPages > 1"
      class="d-flex justify-content-center align-items-center gap-2 mt-4 flex-wrap"
    >
      <button
        class="btn btn-sm btn-outline-secondary"
        @click="goToPage(1)"
        :disabled="currentPage === 1"
      >
        «<span class="visually-hidden">{{ $t("sellCards.firstPage") }}</span>
      </button>

      <button
        class="btn btn-sm btn-outline-secondary"
        @click="prevPage"
        :disabled="currentPage === 1"
      >
        ‹<span class="visually-hidden">{{ $t("sellCards.prevPage") }}</span>
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
        @click="nextPage"
        :disabled="currentPage === totalPages"
      >
        ›<span class="visually-hidden">{{ $t("sellCards.nextPage") }}</span>
      </button>

      <button
        class="btn btn-sm btn-outline-secondary"
        @click="goToPage(totalPages)"
        :disabled="currentPage === totalPages"
      >
        »<span class="visually-hidden">{{ $t("sellCards.lastPage") }}</span>
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, watch } from "vue";
import { useI18n } from "vue-i18n";
export default defineComponent({
  name: "SellCardList",
  setup() {
    const { t } = useI18n();
    const cards = ref<any[]>([]);
    const searchTerm = ref("");
    const selectedExpansion = ref("");
    const expansions = ref<{ set_name: string; set_code: string }[]>([]);
    const currentPage = ref(1);
    const totalCards = ref(0);
    const cardsPerPage = 20;
    const pageWindowSize = 6;

    const sellPrice = ref<Record<number, number>>({});
    const sellQuantity = ref<Record<number, number>>({});

    const loading = ref(false);

    const fetchExpansions = async () => {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/cards/expansions/`);
      const data = await res.json();
      expansions.value = data.expansions || [];
    };

    const fetchCards = async () => {
      loading.value = true;
      try {
        const selected = expansions.value.find((e) => e.set_name === selectedExpansion.value);
        const expansionCode = selected?.set_code || "";

        const params = new URLSearchParams({
          "number-start": currentPage.value.toString(),
          search: searchTerm.value,
          sort: "name",
        });

        const url = selected
          ? `${
              import.meta.env.VITE_API_URL
            }/api/cards/expansion/${expansionCode}/?${params.toString()}`
          : `${import.meta.env.VITE_API_URL}/api/cards/all/?${params.toString()}`;

        const res = await fetch(url);
        if (!res.ok) {
          const text = await res.text();
          throw new Error(`Error: ${res.status} ${text}`);
        }

        const data = await res.json();
        cards.value = data.cards || [];
        totalCards.value = data.total || 0;
      } catch (error) {
        console.error("Error al obtener cartas:", error);
        alert(t("sellcards.fetchError"));
      } finally {
        loading.value = false;
      }
    };

    const publish = async (card: any) => {
      const price = sellPrice.value[card.id];
      const quantity = sellQuantity.value[card.id];

      if (!price || !quantity) {
        alert(t("sellcards.invalidInput"));
        return;
      }

      try {
        const token = localStorage.getItem("token");
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/users/sell/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            "card-id": card.id,
            price,
            quantity,
          }),
        });

        const raw = await res.text();
        let data;
        try {
          data = JSON.parse(raw);
        } catch {
          throw new Error(`Respuesta inválida del servidor: ${raw}`);
        }

        if (!res.ok) {
          throw new Error(data.error || `Error ${res.status}`);
        }

        alert(t("sellcards.publishSuccess"));
        sellPrice.value[card.id] = 0;
        sellQuantity.value[card.id] = 0;
      } catch (err: any) {
        alert(t("sellcards.publishError", { message: err.message }));
      }
    };

    const totalPages = computed(() => Math.max(1, Math.ceil(totalCards.value / cardsPerPage)));
    const currentCards = computed(() => cards.value);

    const paginationStart = computed(() =>
      Math.max(1, currentPage.value - Math.floor(pageWindowSize / 2))
    );
    const paginationEnd = computed(() =>
      Math.min(totalPages.value, paginationStart.value + pageWindowSize - 1)
    );
    const visiblePages = computed(() => {
      const pages: number[] = [];
      for (let i = paginationStart.value; i <= paginationEnd.value; i++) {
        pages.push(i);
      }
      return pages;
    });

    const resetPage = () => (currentPage.value = 1);
    const prevPage = () => {
      if (currentPage.value > 1) currentPage.value--;
    };
    const nextPage = () => {
      if (currentPage.value < totalPages.value) currentPage.value++;
    };
    const goToPage = (page: number) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page;
      }
    };

    onMounted(async () => {
      await fetchExpansions();
      await fetchCards();
    });

    watch([searchTerm, selectedExpansion], () => {
      resetPage();
      fetchCards();
    });
    watch(currentPage, fetchCards);

    return {
      searchTerm,
      selectedExpansion,
      expansions,
      currentPage,
      currentCards,
      totalPages,
      paginationStart,
      paginationEnd,
      visiblePages,
      goToPage,
      prevPage,
      nextPage,
      sellPrice,
      sellQuantity,
      publish,
      resetPage,
      loading,
    };
  },
});
</script>
