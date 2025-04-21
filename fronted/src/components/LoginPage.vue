<template>
  <div class="login-form">
    <h1>Iniciar Sesión</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Nombre de usuario</label>
        <input
          id="username"
          v-model="username"
          type="text"
          maxlength="50"
          placeholder="Ingresa tu nombre de usuario"
          required
        />
        <span v-if="errors.username">{{ errors.username }}</span>
      </div>

      <div>
        <label for="password">Contraseña</label>
        <input
          id="password"
          v-model="password"
          type="password"
          placeholder="Ingresa tu contraseña"
          required
        />
        <span v-if="errors.password">{{ errors.password }}</span>
      </div>

      <button type="submit">Iniciar Sesión</button>
      <p>
        ¿No tienes cuenta?
        <router-link :to="`/${$i18n.locale}/register`">Regístrate aquí</router-link>
      </p>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, inject, type Ref } from "vue";
import { useRouter } from "vue-router";
import { getAuth, signInWithEmailAndPassword, onAuthStateChanged } from "firebase/auth";
import { doc, getDoc } from "firebase/firestore";
import { auth, db } from "../firebaseConfig";
import ChildComponent from "./ProductItem.vue";

const login = inject("login") as (userData: any) => void;

const username = ref("");
const password = ref("");
const errors = ref({
  username: "",
  password: "",
});
const logueado = inject("logueado") as Ref<boolean>;
const router = useRouter();
const handleLogin = async () => {
  errors.value = {
    username: "",
    password: "",
  };

  if (!username.value.trim()) {
    errors.value.username = "El correo es obligatorio.";
    return;
  }

  if (!password.value.trim()) {
    errors.value.password = "La contraseña es obligatoria.";
    return;
  }

  try {
    const response = await fetch("http://localhost:8000/api/users/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      // Guardar el token en localStorage o en Pinia/composable
      localStorage.setItem("token", data.token);
      logueado.value = true;
      alert("Inicio de sesión exitoso");
      router.push("/");
    } else {
      if (data.error === "Invalid credentials") {
        errors.value.password = "Correo o contraseña incorrectos.";
      } else {
        alert("Error inesperado");
      }
    }
  } catch (error) {
    console.error("Error al hacer login:", error);
    alert("Error de red o servidor.");
  }
};
</script>

<style scoped>
.login-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.login-form h1 {
  text-align: center;
  margin-bottom: 20px;
}

.login-form label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.login-form input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.login-form span {
  color: red;
  font-size: 0.875rem;
  display: block;
  margin-top: -8px;
  margin-bottom: 10px;
}

.login-form button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.login-form button:hover {
  background-color: #0056b3;
}
</style>
