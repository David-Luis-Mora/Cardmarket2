<template>
  <div v-if="profile" class="container my-4">
    <div class="row">
      <!-- Columna izquierda: info de usuario -->
      <div class="col-md-4">
        <div class="card mb-4">
          <div class="card-body text-center">
            <img
              :src="avatarSrc"
              class="rounded-circle mb-3"
              :alt="$t('profile.avatarAlt')"
              style="width: 120px; height: 120px; object-fit: cover"
            />
            <h5 class="card-title">{{ profile.user.username }}</h5>

            <div class="profile-info">
              <p>
                <strong>{{ $t("profile.nickname") }}:</strong> {{ profile.nickname }}
              </p>
              <p>
                <strong>{{ $t("profile.email") }}:</strong> {{ profile.email }}
              </p>
              <p>
                <strong>{{ $t("profile.country") }}:</strong> {{ profile.country }}
              </p>
              <p>
                <strong>{{ $t("profile.address") }}:</strong> {{ profile.address }}
              </p>
              <p>
                <strong>{{ $t("profile.phone") }}:</strong> {{ profile.phone }}
              </p>
              <p>
                <strong>{{ $t("profile.bio") }}:</strong> {{ profile.bio }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Columna derecha: ventas -->
      <div class="col-md-8">
        <div class="row">
          <!-- Cartas en venta -->
          <div class="col-12 mb-12">
            <div class="card">
              <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">{{ $t("profile.forSaleTitle") }}</h5>
              </div>
              <ul class="list-group list-group-flush">
                <li v-if="cardsForSale.length === 0" class="list-group-item text-center text-muted">
                  {{ $t("profile.noForSale") }}
                </li>
                <li
                  v-for="card in cardsForSale"
                  :key="card.id"
                  class="list-group-item d-flex align-items-center justify-content-between"
                >
                  <div class="d-flex align-items-center">
                    <span class="ms-3">{{ $t("profile.name") }}: {{ card.name }}</span>
                    <span class="ms-3">{{ $t("profile.price") }}: ${{ card.price }}</span>
                    <span class="ms-3">{{ $t("profile.quantity") }}: {{ card.quantity }}</span>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, defineProps } from "vue";
import { useRoute } from "vue-router";

interface Profile {
  user: { username: string; first_name: string; last_name: string };
  nickname: string;
  first_name: string;
  last_name: string;
  email: string;
  country: string;
  address: string;
  phone: string;
  bio: string;
  avatar_url?: string;
}
interface CardForSale {
  id: number;
  name: string;
  price: number;
  quantity: number;
}

const route = useRoute();
const profile = ref<Profile | null>(null);
const cardsForSale = ref<CardForSale[]>([]);
const defaultAvatar = "https://www.gravatar.com/avatar/?d=mp&f=y";
const props = defineProps<{
  lang: string;
  nickname: string;
}>();
const sellerUsername = props.nickname;
const avatarSrc = computed(() => {
  return profile.value?.avatar_url || defaultAvatar;
});

async function fetchProfile() {
  try {
    const res = await fetch(`http://localhost:8000/api/seller/${props.nickname}/profile/`);
    if (!res.ok) throw new Error("Error al cargar perfil");
    const data = await res.json();
    profile.value = data.profile;
    cardsForSale.value = data.cards_for_sale || [];
  } catch (err) {
    console.error(err);
  }
}

onMounted(() => {
  fetchProfile();
});
</script>

<style scoped>
.avatar-img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
}

.cards-section {
  margin-top: 2rem;
  background-color: rgba(255, 255, 255, 0.05);
  padding: 1rem;
  border-radius: 1rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.cards-title {
  color: #facc15;
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 1rem;
  text-align: center;
}

.cards-table {
  width: 100%;
  border-collapse: collapse;
  color: #e9d8fd;
}

.cards-table th,
.cards-table td {
  padding: 0.75rem;
  border: 1px solid #facc15;
  text-align: center;
}

.cards-table th {
  background-color: #1e293b;
  color: #facc15;
}
.profile-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #0f172a; /* fondo oscuro */
  border-radius: 1rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  font-family: "Segoe UI", sans-serif;
  color: #e9d8fd;
}
.card {
  background-color: #e9d8fd;
}
.card-body {
  background-color: #e9d8fd;
}

.rounded-circle {
  border: 2px solid #facc15;
}

.profile-title {
  text-align: center;
  font-size: 2rem;
  font-weight: bold;
  color: #facc15;
  margin-bottom: 1.5rem;
}

.avatar-container {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.avatar-img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #facc15;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.avatar-img:hover {
  transform: scale(1.05);
  box-shadow: 0 0 12px #facc15;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 0.4rem;
  color: #facc15;
}

.form-group input,
.form-group textarea,
.form-group select {
  padding: 0.6rem 0.75rem;
  background-color: #1e293b;
  color: #e9d8fd;
  border: 1px solid #facc15;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.2s, background-color 0.2s;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
  border-color: #e9d8fd;
  outline: none;
  background-color: #0f172a;
}

.button-group {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn {
  padding: 0.5rem 1.25rem;
  font-weight: 600;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s ease-in-out;
}

.btn-green {
  background-color: #28a745;
  color: white;
}

.btn-green:hover {
  background-color: #218838;
}

.btn-gray {
  background-color: #94a3b8;
  color: #0f172a;
}

.btn-gray:hover {
  background-color: #cbd5e1;
}

.profile-info {
  padding: 1rem;
  border-radius: 0.75rem;
  margin-top: 1.5rem;
  line-height: 1.6;
  color: #000000;
}
</style>
