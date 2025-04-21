<template>
  <div class="register-form">
    <h1>Registro</h1>
    <form @submit.prevent="handleRegister">
      <div>
        <label for="firstName">Nombre</label>
        <input
          id="firstName"
          v-model="firstName"
          type="text"
          maxlength="50"
          placeholder="Ingresa tu nombre"
          required
        />
        <span v-if="errors.firstName">{{ errors.firstName }}</span>
      </div>

      <div>
        <label for="lastName">Apellido</label>
        <input
          id="lastName"
          v-model="lastName"
          type="text"
          maxlength="50"
          placeholder="Ingresa tu apellido"
          required
        />
        <span v-if="errors.lastName">{{ errors.lastName }}</span>
      </div>

      <div>
        <label for="email">Correo Electrónico</label>
        <input id="email" v-model="email" type="email" placeholder="Ingresa tu correo" required />
        <span v-if="errors.email">{{ errors.email }}</span>
      </div>

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
          placeholder="Crea tu contraseña"
          required
        />
        <span v-if="errors.password">{{ errors.password }}</span>
      </div>

      <button type="submit">Registrar</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, inject } from "vue";
import { createUserWithEmailAndPassword } from "firebase/auth";
import { doc, setDoc, getDoc } from "firebase/firestore";
import { auth, db } from "../firebaseConfig";
import { useRouter } from "vue-router";

const register = inject("register") as (userData: any) => void;

const firstName = ref("");
const lastName = ref("");
const email = ref("");
const password = ref("");
const username = ref("");
const errors = ref({
  firstName: "",
  lastName: "",
  email: "",
  username: "",
  password: "",
});

const router = useRouter();

const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

const validatePassword = (password: string): boolean => {
  const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$/;
  return passwordRegex.test(password);
};

const checkUsers = async (email: string) => {
  const docRef = doc(db, "Users", email);
  const docSnap = await getDoc(docRef);

  return docSnap.exists();
};

const addUser = async () => {
  try {
    const data = {
      firstName: firstName.value,
      lastName: lastName.value,
      username: username.value,
      email: email.value,
      password: password.value,
    };

    await setDoc(doc(db, "Users", email.value), data);
    alert("Registro exitoso!");
    firstName.value = "";
    lastName.value = "";
    username.value = "";
    email.value = "";
    password.value = "";
  } catch (error: any) {
    console.error("Error al registrar:", error.message);
    if (error.code === "auth/email-already-in-use") {
      errors.value.email = "El correo ya está en uso.";
    } else {
      alert("Ocurrió un error inesperado.");
    }
  }
};

const handleRegister = async () => {
  errors.value = {
    firstName: "",
    lastName: "",
    email: "",
    username: "",
    password: "",
  };

  let isValid = true;

  if (firstName.value.trim() === "") {
    errors.value.firstName = "El nombre es obligatorio.";
    isValid = false;
  }

  if (lastName.value.trim() === "") {
    errors.value.lastName = "El apellido es obligatorio.";
    isValid = false;
  }

  if (!validateEmail(email.value)) {
    errors.value.email = "El formato del correo es inválido.";
    isValid = false;
  }

  if (!validatePassword(password.value)) {
    errors.value.password =
      "La contraseña debe tener al menos 8 caracteres, una letra mayúscula, un número y un carácter especial.";
    isValid = false;
  }

  if (!isValid) return;

  try {
    const response = await fetch("http://localhost:8000/api/users/signup/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username.value,
        firstname: firstName.value,
        lastname: lastName.value,
        email: email.value,
        password: password.value,
      }),
    });

    const result = await response.json();

    if (!response.ok) {
      if (result.error.includes("email")) {
        errors.value.email = result.error;
      } else if (result.error.includes("username")) {
        errors.value.username = result.error; // O crea un campo `username` separado
      } else {
        alert(result.error || "Error desconocido");
      }
    } else {
      alert("Registro exitoso");
      // Guarda el token si lo deseas
      localStorage.setItem("token", result.token);
      router.push("/"); // redirige a la página principal
    }
  } catch (error) {
    console.error("Error al registrar:", error);
    alert("Hubo un error al conectar con el servidor.");
  }
};
</script>

<style scoped>
.register-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.register-form h1 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 1.8rem;
  color: #333;
}

.register-form label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #555;
}

.register-form input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  color: #333;
  background-color: #fff;
}

.register-form input:focus {
  border-color: #007bff;
  outline: none;
}

.register-form span {
  color: red;
  font-size: 0.875rem;
  display: block;
  margin-top: -8px;
  margin-bottom: 10px;
}

.register-form button {
  width: 100%;
  padding: 12px;
  background-color: #007bff;
  color: white;
  font-size: 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.register-form button:hover {
  background-color: #0056b3;
}

.register-form button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.register-form .form-group {
  margin-bottom: 20px;
}

@media (max-width: 600px) {
  .register-form {
    padding: 15px;
  }

  .register-form h1 {
    font-size: 1.5rem;
  }
}
</style>
