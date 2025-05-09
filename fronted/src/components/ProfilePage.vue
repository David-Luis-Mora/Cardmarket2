<template>
  <div class="container my-4">
    <div class="row">
      <!-- Left column: user info / form -->
      <div class="col-md-4">
        <div class="card mb-4">
          <div class="card-body text-center">
            <img
              :src="avatarPreview"
              class="rounded-circle mb-3"
              alt="Avatar"
              style="width: 120px; height: 120px; object-fit: cover"
            />
            <h5 class="card-title">{{ user?.username }}</h5>

            <form @submit.prevent="save" v-if="editing">
              <div class="mb-3">
                <label class="form-label">Nickname</label>
                <input v-model="form.nickname" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">First Name</label>
                <input v-model="form.first_name" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Last Name</label>
                <input v-model="form.last_name" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input v-model="form.email" type="email" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Avatar URL</label>
                <input
                  v-model="form.avatar_url"
                  type="url"
                  class="form-control"
                  placeholder="Avatar por URL"
                />
                <input type="file" class="form-control mt-2" @change="onFileChange" />
              </div>
              <div class="mb-3">
                <label class="form-label">País</label>
                <select v-model="form.country" class="form-select">
                  <option v-for="c in countries" :key="c.code" :value="c.name">
                    {{ c.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Dirección</label>
                <input
                  v-model="form.address"
                  type="text"
                  class="form-control"
                  placeholder="Tu dirección"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Teléfono</label>
                <input v-model="form.phone" type="text" class="form-control" placeholder="+54..." />
              </div>
              <div class="mb-3">
                <label class="form-label">Biografía</label>
                <textarea
                  v-model="form.bio"
                  rows="3"
                  class="form-control"
                  placeholder="Algo sobre ti..."
                ></textarea>
              </div>
              <div class="d-flex justify-content-between">
                <button type="submit" class="btn btn-primary">Guardar</button>
                <button type="button" class="btn btn-secondary" @click="cancel">Cancelar</button>
              </div>
            </form>

            <div v-else>
              <p>
                <strong>{{ user?.nickname }}</strong>
              </p>
              <p><strong>Nombre:</strong> {{ user?.first_name }}</p>
              <p><strong>Apellidos:</strong> {{ user?.last_name }}</p>
              <p><strong>Email:</strong> {{ user?.email }}</p>
              <p><strong>País:</strong> {{ user?.country }}</p>
              <p><strong>Dirección:</strong> {{ user?.address }}</p>
              <p><strong>Teléfono:</strong> {{ user?.phone }}</p>
              <p><strong>Bio:</strong> {{ user?.bio }}</p>
              <button class="btn btn-outline-primary mt-2" @click="edit">Editar Perfil</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Right column: sales, sold, and purchases -->
      <div class="col-md-8">
        <div class="row">
          <!-- Sales box -->
          <div class="col-12 mb-4">
            <div class="card">
              <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Mis cartas en venta</h5>
                <router-link :to="`/${$i18n.locale}/sell-cards`" class="btn btn-danger btn-sm">
                  Vender cartas
                </router-link>
              </div>
              <ul class="list-group list-group-flush">
                <li v-if="cardsForSale.length === 0" class="list-group-item text-center text-muted">
                  No hay cartas en venta.
                </li>
                <li
                  v-for="card in cardsForSale"
                  :key="card.id"
                  class="list-group-item d-flex align-items-center justify-content-between"
                >
                  <!-- Left: image, name, price, quantity -->
                  <div class="d-flex align-items-center">
                    <!-- <img
                      :src="card.image"
                      :alt="card.name"
                      class="rounded"
                      style="width: 60px; height: 60px; object-fit: cover"
                    /> -->
                    <span class="ms-3">Nombre: {{ card.name }}</span>
                    <template v-if="editingCardId !== card.id">
                      <span class="ms-3">Precio: ${{ card.price }}</span>
                      <span class="ms-3">Cantidad: {{ card.quantity }}</span>
                    </template>
                    <template v-else>
                      <span class="ms-3 d-flex align-items-center">
                        Precio:
                        <input
                          v-model.number="tempEdits[card.id].price"
                          type="number"
                          step="0.01"
                          min="0"
                          class="form-control form-control-sm ms-1"
                          style="width: 100px; display: inline-block"
                        />
                      </span>
                      <span class="ms-3 d-flex align-items-center">
                        Cantidad:
                        <input
                          v-model.number="tempEdits[card.id].quantity"
                          type="number"
                          min="1"
                          class="form-control form-control-sm ms-1"
                          style="width: 80px; display: inline-block"
                        />
                      </span>
                    </template>
                  </div>
                  <!-- Right: action buttons -->
                  <div>
                    <button
                      v-if="editingCardId !== card.id"
                      @click="startEdit(card)"
                      class="btn btn-primary btn-sm me-2"
                    >
                      Editar
                    </button>
                    <button v-else @click="saveEdit(card)" class="btn btn-success btn-sm me-2">
                      Guardar
                    </button>
                    <button
                      v-if="editingCardId === card.id"
                      @click="cancelEdit()"
                      class="btn btn-secondary btn-sm me-2"
                    >
                      Cancelar
                    </button>
                    <button
                      v-if="editingCardId !== card.id"
                      @click="confirmDelete(card)"
                      class="btn btn-secondary btn-sm"
                    >
                      Eliminar
                    </button>
                  </div>
                </li>
              </ul>
            </div>
          </div>
          <!-- Sold box -->
          <div class="col-12 mb-4">
            <div class="card">
              <div class="card-header">
                <h5 class="mb-0">Mis cartas vendidas</h5>
              </div>
              <ul class="list-group list-group-flush">
                <li
                  v-for="card in soldCards"
                  :key="card.id"
                  class="list-group-item d-flex align-items-center"
                >
                  <img
                    :src="card.image"
                    :alt="card.name"
                    class="me-3 rounded"
                    style="width: 60px; height: 60px; object-fit: cover"
                  />
                  <div>
                    <h6 class="mb-1">{{ card.name }}</h6>
                    <small>Precio: ${{ card.price }} &middot; Cantidad: {{ card.quantity }}</small>
                  </div>
                </li>
                <li v-if="soldCards.length === 0" class="list-group-item text-center text-muted">
                  No has vendido cartas todavía.
                </li>
              </ul>
            </div>
          </div>

          <!-- Purchases box -->
          <div class="col-12">
            <div class="card">
              <div class="card-header">
                <h5 class="mb-0">Mis cartas compradas</h5>
              </div>
              <ul class="list-group list-group-flush">
                <li
                  v-for="card in purchasedCards"
                  :key="card.id"
                  class="list-group-item d-flex align-items-center"
                >
                  <img
                    :src="card.image"
                    :alt="card.name"
                    class="me-3 rounded"
                    style="width: 60px; height: 60px; object-fit: cover"
                  />
                  <div>
                    <h6 class="mb-1">{{ card.name }}</h6>
                    <small>Precio: ${{ card.price }} &middot; Cantidad: {{ card.quantity }}</small>
                  </div>
                </li>
                <li
                  v-if="purchasedCards.length === 0"
                  class="list-group-item text-center text-muted"
                >
                  No has comprado cartas todavía.
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
import { onMounted } from "vue";
import { ref, computed, reactive } from "vue";
import { useUserStore } from "@/stores/userStore";
const countries = ref([
  { code: "AR", name: "Argentina" },
  { code: "BR", name: "Brasil" },
  { code: "CL", name: "Chile" },
  { code: "US", name: "Estados Unidos" },
  { code: "MX", name: "México" },
  { code: "ES", name: "España" },
  { code: "FR", name: "Francia" },
  { code: "DE", name: "Alemania" },
  { code: "IT", name: "Italia" },
  { code: "JP", name: "Japón" },
]);
// Definir el tipo para una carta
interface Card {
  id: number;
  name: string;
  price: number;
  quantity: number;
  image: string;
}
const fetchUserProfile = async () => {
  const token = localStorage.getItem("token"); // Asegúrate de que este es el nombre correcto
  try {
    const res = await fetch("http://localhost:8000/api/users/edit/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    const raw = await res.text();
    console.log("🔍 Respuesta cruda:", raw);

    let data;
    try {
      data = JSON.parse(raw);
      userStore.setUser(data); // ✅ data.avatar debe estar ahí
    } catch {
      throw new Error("Respuesta no válida: " + raw);
    }

    if (!res.ok) throw new Error(data.error || "Error al cargar perfil");

    userStore.setUser(data); // Asumiendo que esto guarda en Pinia
  } catch (error) {
    console.error("❌ Error al cargar perfil:", error);
    alert("No se pudo cargar el perfil del usuario.");
  }
};

const userStore = useUserStore();
const user = computed(() => userStore.user);

const editing = ref(false);
const defaultAvatar = "https://www.gravatar.com/avatar/?d=mp&f=y";

const form = ref({
  username: "",
  first_name: "",
  last_name: "",
  email: "",
  nickname: "",
  avatar_url: "",
  avatar_file: null as File | null,
  country: "",
  address: "",
  phone: "",
  bio: "",
});

const onFileChange = (e: Event) => {
  const file = (e.target as HTMLInputElement).files?.[0];
  if (file) {
    form.value.avatar_file = file;
    form.value.avatar_url = ""; // Limpiar URL si sube imagen
  }
};

const avatarPreview = computed(() => {
  if (form.value.avatar_file) {
    return URL.createObjectURL(form.value.avatar_file);
  }
  return form.value.avatar_url || user.value?.avatar || defaultAvatar;
});

const save = async () => {
  const token = localStorage.getItem("token");

  let updatedData;
  let response;

  try {
    if (form.value.avatar_file) {
      const formData = new FormData();
      formData.append("username", form.value.username);
      formData.append("avatar_file", form.value.avatar_file);
      formData.append("first_name", form.value.first_name);
      formData.append("last_name", form.value.last_name);
      formData.append("email", form.value.email);
      formData.append("nickname", form.value.nickname || "");
      formData.append("country", form.value.country);
      formData.append("address", form.value.address);
      formData.append("phone", form.value.phone);
      formData.append("bio", form.value.bio);

      response = await fetch("http://localhost:8000/api/users/edit/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });
    } else {
      response = await fetch("http://localhost:8000/api/users/edit/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          username: form.value.username,
          first_name: form.value.first_name,
          last_name: form.value.last_name,
          email: form.value.email,
          nickname: form.value.nickname,
          country: form.value.country,
          address: form.value.address,
          phone: form.value.phone,
          bio: form.value.bio,
          avatar: form.value.avatar_url,
        }),
      });
    }

    const raw = await response.text();
    updatedData = JSON.parse(raw);

    if (!response.ok) throw new Error(updatedData.error || "Error al guardar los datos.");

    userStore.setUser(updatedData);
    editing.value = false;
    alert("Perfil actualizado correctamente");
  } catch (err) {
    console.error("❌ Error al guardar perfil:", err);
    alert("Hubo un problema al guardar los datos del perfil.");
  }
};

function edit() {
  if (user.value) {
    form.value.username = user.value.username;
    form.value.first_name = user.value.first_name;
    form.value.last_name = user.value.last_name;
    form.value.email = user.value.email;
    form.value.nickname = user.value.nickname;
    form.value.avatar_url = user.value.avatar || "";
    form.value.country = user.value.country || "";
    form.value.address = user.value.address || "";
    form.value.phone = user.value.phone || "";
    form.value.bio = user.value.bio || "";
    form.value.avatar_file = null;
    editing.value = true;
  }
}

function cancel() {
  editing.value = false;
  form.value.avatar_file = null;
}

// Sales listings
const cardsForSale = ref<Card[]>([]);
const editingCardId = ref<number | null>(null);
const tempEdits = reactive<Record<number, { quantity: number; price: number }>>({});

async function fetchMyCardsForSale() {
  const token = localStorage.getItem("token");
  const res = await fetch("http://localhost:8000/api/users/my-cards-for-sale/", {
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await res.json();
  cardsForSale.value = data.cards_for_sale;
  // Inicializar tempEdits
  data.cards_for_sale.forEach((c: Card) => {
    tempEdits[c.id] = { quantity: c.quantity, price: c.price };
  });
}

function startEdit(card: Card) {
  editingCardId.value = card.id;
}

function cancelEdit() {
  if (editingCardId.value !== null) {
    // Restaurar valores
    const orig = cardsForSale.value.find((c) => c.id === editingCardId.value);
    if (orig) {
      tempEdits[orig.id].quantity = orig.quantity;
      tempEdits[orig.id].price = orig.price;
    }
    editingCardId.value = null;
  }
}

async function saveEdit(card: Card) {
  const token = localStorage.getItem("token");
  await fetch(`http://localhost:8000/api/users/my-cards-for-sale/${card.id}/`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      quantity: tempEdits[card.id].quantity,
      price: tempEdits[card.id].price,
    }),
  });
  // Aplicar cambios localmente
  card.quantity = tempEdits[card.id].quantity;
  card.price = tempEdits[card.id].price;
  editingCardId.value = null;
}

async function confirmDelete(card: Card) {
  if (confirm(`¿Eliminar "${card.name}" de tus ventas?`)) {
    const token = localStorage.getItem("token");
    await fetch(`http://localhost:8000/api/users/my-cards-for-sale/${card.id}/`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    cardsForSale.value = cardsForSale.value.filter((c) => c.id !== card.id);
  }
}

// Sold
const soldCards = ref<Card[]>([]);
async function fetchMySoldCards() {
  const token = localStorage.getItem("token");
  const res = await fetch("http://localhost:8000/api/users/my-sold-cards/", {
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await res.json();
  soldCards.value = data.cards_sold;
}

// Purchases
const purchasedCards = ref<Card[]>([]);
async function fetchMyPurchasedCards() {
  const token = localStorage.getItem("token");
  const res = await fetch("http://localhost:8000/api/users/my-purchased-cards/", {
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await res.json();
  purchasedCards.value = data.cards_purchased;
}

// Inicialización
onMounted(() => {
  fetchUserProfile();
  fetchMyCardsForSale();
  fetchMyPurchasedCards();
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

.btn-blue {
  background-color: #2563eb;
  color: white;
}

.btn-blue:hover {
  background-color: #1d4ed8;
}

.profile-info {
  text-align: left;
  padding: 1rem;
  border: 1px solid #334155;
  border-radius: 0.75rem;
  background-color: #1e293b;
  margin-top: 1.5rem;
  line-height: 1.6;
  color: #e2e8f0;
}
</style>
