<template>
  <div class="login-form">
    <h1>Iniciar Sesión</h1>
    <form @submit.prevent="handleLogin">
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
          placeholder="Ingresa tu contraseña"
          required
        />
        <span v-if="errors.password">{{ errors.password }}</span>
      </div>

      <button type="submit">Iniciar Sesión</button>
      <p>¿No tienes cuenta? <router-link :to="`/${$i18n.locale}/register`">Regístrate aquí</router-link></p>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, inject, type Ref } from 'vue';
import { useRouter } from 'vue-router';
import { getAuth, signInWithEmailAndPassword, onAuthStateChanged } from 'firebase/auth';
import { doc, getDoc } from 'firebase/firestore';
import { auth, db } from '../firebaseConfig';
import ChildComponent from './ProductItem.vue';


const login = inject('login') as (userData: any) => void;

const email = ref('');
const password = ref('');
const errors = ref({
  email: '',
  password: '',
});
const logueado = inject('logueado') as Ref<boolean>;
const router = useRouter();

const handleLogin = async () => {
  errors.value = {
    email: '',
    password: '',
  };

  // Validaciones de los campos
  if (!email.value.trim()) {
    errors.value.email = 'El correo es obligatorio.';
    return;
  }

  if (!password.value.trim()) {
    errors.value.password = 'La contraseña es obligatoria.';
    return;
  }

  try {
    // Autenticación con Firebase
    // const userCredential = await signInWithEmailAndPassword(auth, email.value, password.value);
    // const user = userCredential.user;
    
    // Ahora obtenemos datos adicionales desde Firestore si es necesario
    const userDocRef = doc(db, 'Users',  email.value); // Usamos UID para obtener el doc
    const userDoc = await getDoc(userDocRef);

    if (userDoc.exists()) {
      const userData = userDoc.data();
      alert(`Bienvenido ${userData.firstName} ${userData.lastName}!`);
      logueado.value = true; // Definir la variable 'logueado' como un ref      
    } else {
      console.log('No se encontraron datos adicionales del usuario.');
    }
    router.push('/');
  } catch (error: any) {
    console.error('Error al iniciar sesión:', error);
    if (error.code === 'auth/user-not-found') {
      errors.value.email = 'El correo no está registrado.';
    } else if (error.code === 'auth/wrong-password') {
      errors.value.password = 'La contraseña es incorrecta.';
    } else {
      alert('Ocurrió un error inesperado. Inténtalo nuevamente.');
    }
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
