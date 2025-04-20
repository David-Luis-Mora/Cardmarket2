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
        <input
          id="email"
          v-model="email"
          type="email"
          placeholder="Ingresa tu correo"
          required
        />
        <span v-if="errors.email">{{ errors.email }}</span>
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
import { ref, inject } from 'vue';
import { createUserWithEmailAndPassword } from 'firebase/auth';
import { doc, setDoc, getDoc } from 'firebase/firestore';
import { auth, db } from '../firebaseConfig';
import { useRouter } from 'vue-router';

const register = inject('register') as (userData: any) => void;

const firstName = ref('');
const lastName = ref('');
const email = ref('');
const password = ref('');
const errors = ref({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
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
  const docRef = doc(db, 'Users', email);
  const docSnap = await getDoc(docRef);

  return docSnap.exists();
};

const addUser = async () => {
  try {
    const data = {
      firstName: firstName.value,
      lastName: lastName.value,
      email: email.value,
      password: password.value,
    };

    await setDoc(doc(db, 'Users', email.value), data);
    alert('Registro exitoso!');
    firstName.value = '';
    lastName.value = '';
    email.value = '';
    password.value = '';
  } catch (error: any) {
    console.error('Error al registrar:', error.message);
    if (error.code === 'auth/email-already-in-use') {
      errors.value.email = 'El correo ya está en uso.';
    } else {
      alert('Ocurrió un error inesperado.');
    }
  }
};

const handleRegister = async () => {
  errors.value = {
    firstName: '',
    lastName: '',
    email: '',
    password: '',
  };

  let isValid = true;

  if (firstName.value.trim() === '') {
    errors.value.firstName = 'El nombre es obligatorio.';
    isValid = false;
  }

  if (lastName.value.trim() === '') {
    errors.value.lastName = 'El apellido es obligatorio.';
    isValid = false;
  }

  if (!validateEmail(email.value)) {
    errors.value.email = 'El formato del correo es inválido.';
    isValid = false;
  }

  if (!validatePassword(password.value)) {
    errors.value.password =
      'La contraseña debe tener al menos 8 caracteres, una letra mayúscula, un número y un carácter especial.';
    isValid = false;
  }

  if (isValid) {
    const userExists = await checkUsers(email.value);
    if (!userExists) {
      try {
        await addUser();
        alert('Registro exitoso');

        // const userData = { email: email.value, name: firstName.value };

        // register(userData);
      } catch (error: any) {
        console.error('Error al registrar:', error.message);
        alert('Hubo un problema con el registro');
      }
    } else {
      alert('Ya el usuario está registrado');
    }
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
