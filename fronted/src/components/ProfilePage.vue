<template>
  <div class="profile-container">
    <h2 class="profile-title">Perfil del Usuario</h2>

    <div class="avatar-container">
      <img :src="form.avatar || defaultAvatar" class="avatar-img" alt="Avatar" />
    </div>

    <form @submit.prevent="save" v-if="editing" class="profile-form">
      <div class="form-group">
        <label>Nombre</label>
        <input v-model="form.name" type="text" required />
      </div>
      <div class="form-group">
        <label>Email</label>
        <input v-model="form.email" type="email" required />
      </div>
      <div class="form-group">
        <label>Rol</label>
        <input v-model="form.role" type="text" required />
      </div>
      <div class="form-group">
        <label>Avatar (URL)</label>
        <input v-model="form.avatar" type="url" />
      </div>

      <div class="button-group">
        <button type="submit" class="btn btn-green">Guardar</button>
        <button @click="cancel" type="button" class="btn btn-gray">Cancelar</button>
      </div>
    </form>

    <div v-else class="profile-info">
      <p><strong>Nombre:</strong> {{ user?.name }}</p>
      <p><strong>Email:</strong> {{ user?.email }}</p>
      <p><strong>Rol:</strong> {{ user?.role }}</p>
      <button @click="edit" class="btn btn-blue">Editar Perfil</button>
    </div>
  </div>
  <!-- Cartas Compradas -->
  <div class="cards-section">
    <h3 class="cards-title">Cartas Compradas</h3>
    <table class="cards-table">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Precio</th>
          <th>Fecha</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="card in purchasedCards" :key="card.id">
          <td>{{ card.name }}</td>
          <td>{{ card.price }} €</td>
          <td>{{ card.date }}</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Cartas Vendidas -->
  <div class="cards-section">
    <h3 class="cards-title">Cartas Vendidas</h3>
    <table class="cards-table">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Precio</th>
          <th>Fecha</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="card in soldCards" :key="card.id">
          <td>{{ card.name }}</td>
          <td>{{ card.price }} €</td>
          <td>{{ card.date }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
const purchasedCards = ref([
  { id: 1, name: "Dragón de Fuego", price: 12.5, date: "April 12, 2025" },
  { id: 2, name: "Caballero de Hielo", price: 7.0, date: "April 15, 2025" },
]);

const soldCards = ref([
  { id: 1, name: "Gólem de Piedra", price: 9.99, date: "April 10, 2025" },
  { id: 2, name: "Hechicera Arcana", price: 15.0, date: "April 14, 2025" },
]);

import { ref, computed } from "vue";
import { useUserStore } from "@/stores/userStore";

const userStore = useUserStore();
const user = computed(() => userStore.user);

const editing = ref(false);
const defaultAvatar = "https://www.gravatar.com/avatar/?d=mp&f=y";

const form = ref({
  name: "",
  email: "",
  role: "",
  avatar: "",
});

function edit() {
  if (user.value) {
    Object.assign(form.value, user.value);
    editing.value = true;
  }
}

function cancel() {
  editing.value = false;
}

function save() {
  userStore.setUser({ ...form.value });
  editing.value = false;
}
// async function save() {
//   if (!user.value) return

//   try {
//     const response = await fetch(`/api/users/${user.value.id}`, {
//       method: 'PUT',
//       headers: {
//         'Content-Type': 'application/json',
//         // Si necesitas token:
//         // 'Authorization': `Bearer ${token}`
//       },
//       body: JSON.stringify(form.value)
//     })

//     if (!response.ok) {
//       throw new Error('Error al guardar el perfil')
//     }

//     const updatedUser = await response.json()
//     userStore.setUser(updatedUser)
//     editing.value = false
//   } catch (err) {
//     console.error(err)
//     alert('Hubo un error al guardar los cambios.')
//   }
// }
</script>

<style scoped>
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
  max-width: 500px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  font-family: Arial, sans-serif;
  color: #e9d8fd; /* Texto suave */
}

.profile-title {
  text-align: center;
  font-size: 1.75rem;
  font-weight: bold;
  color: #facc15; /* Amarillo brillante */
  margin-bottom: 1.5rem;
}

.avatar-container {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.avatar-img {
  width: 100px;
  height: 100px;
  border-radius: 9999px;
  object-fit: cover;
  border: 3px solid #facc15; /* Amarillo brillante */
  transition: transform 0.3s ease;
}

.avatar-img:hover {
  transform: scale(1.05);
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #facc15; /* Amarillo brillante */
}

.form-group input {
  padding: 0.5rem 0.75rem;
  border: 1px solid #facc15; /* Amarillo brillante */
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus {
  border-color: #e9d8fd; /* Azul suave al enfocarse */
  outline: none;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  font-weight: 600;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-green {
  background-color: #28a745;
  color: white;
}

.btn-green:hover {
  background-color: #218838;
}

.btn-gray {
  background-color: #e0e0e0;
  color: #333;
}

.btn-gray:hover {
  background-color: #c6c6c6;
}

.btn-blue {
  background-color: #007bff;
  color: white;
}

.btn-blue:hover {
  background-color: #0056b3;
}

.profile-info {
  text-align: center;
  color: #e9d8fd; /* Texto suave */
  line-height: 1.6;
}
</style>

<!-- <style scoped>
.profile-container {
  max-width: 500px;
  margin: 2rem auto;
  padding: 2rem;
  background: #ffffff;
  border-radius: 1rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  font-family: Arial, sans-serif;
}

.profile-title {
  text-align: center;
  font-size: 1.75rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 1.5rem;
}

.avatar-container {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.avatar-img {
  width: 100px;
  height: 100px;
  border-radius: 9999px;
  object-fit: cover;
  border: 3px solid #ddd;
  transition: transform 0.3s ease;
}

.avatar-img:hover {
  transform: scale(1.05);
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #444;
}

.form-group input {
  padding: 0.5rem 0.75rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus {
  border-color: #007bff;
  outline: none;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  font-weight: 600;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-green {
  background-color: #28a745;
  color: white;
}

.btn-green:hover {
  background-color: #218838;
}

.btn-gray {
  background-color: #e0e0e0;
  color: #333;
}

.btn-gray:hover {
  background-color: #c6c6c6;
}

.btn-blue {
  background-color: #007bff;
  color: white;
}

.btn-blue:hover {
  background-color: #0056b3;
}

.profile-info {
  text-align: center;
  color: #555;
  line-height: 1.6;
}


</style> -->
