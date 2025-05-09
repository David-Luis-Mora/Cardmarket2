<template>
  <nav>
    <div class="logo-menu-container">
      <router-link class="nav-link js-scroll-trigger" :to="`/${locale}/`">
        <img src="/logo.png" alt="CardShop Logo" class="logo" />
      </router-link>
      <button class="menu-btn" @click="toggleSidebar" aria-label="Abrir menú lateral">
        <i class="bi bi-list" aria-hidden="true"></i>
      </button>
    </div>

    <div class="nav-links">
      <div class="box">
        <router-link class="nav-link js-scroll-trigger" :to="`/${locale}/cards`">
          <i class="bi bi-suit-spade"></i> {{ t("cards") }}
        </router-link>
      </div>
      <div class="box">
        <router-link class="nav-link js-scroll-trigger" :to="`/${locale}/cart`">
          <i class="bi bi-cart2"></i> {{ t("cart") }}
        </router-link>
      </div>
      <div class="nav-item dropdown box">
        <a
          class="nav-link dropdown-toggle"
          href="#"
          id="navbarDropdown"
          role="button"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          <i class="bi bi-translate"></i> {{ t("language") }}
        </a>
        <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
          <li><a class="dropdown-item" @click.prevent="changeLanguage('es')">Español</a></li>
          <li><a class="dropdown-item" @click.prevent="changeLanguage('en')">English</a></li>
        </ul>
      </div>
      <div v-if="isLoggedIn" class="box">
        <router-link class="nav-link" :to="{ name: 'MyProfile', params: { lang: locale } }">
          <i class="bi bi-person-fill"></i> {{ t("profile") }}
        </router-link>
      </div>
      <div v-if="!isLoggedIn" class="box">
        <router-link class="nav-link" :to="`/${locale}/login`">
          <i class="bi bi-person"></i> {{ t("login") }}
        </router-link>
      </div>
      <div v-else class="box">
        <button class="nav-link btn-logout" @click="logout">
          <i class="bi bi-box-arrow-right"></i> {{ t("logout") }}
        </button>
      </div>
    </div>
  </nav>

  <div class="overlay" v-if="isSidebarOpen" @click="toggleSidebar"></div>
  <div class="sidebar" :class="{ open: isSidebarOpen }">
    <button class="close-btn" @click="toggleSidebar">&times;</button>
    <h3>{{ t("options") }}</h3>
    <ul>
      <li>
        <a @click.prevent="goToProfile">{{ t("profile") }}</a>
      </li>
      <li>
        <a href="#">{{ t("settings") }}</a>
      </li>
      <li>
        <a @click.prevent="logout">{{ t("logout") }}</a>
      </li>
    </ul>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";

const { t, locale } = useI18n();
const router = useRouter();

const isSidebarOpen = ref(false);
const isLoggedIn = ref(false);

function toggleSidebar() {
  isSidebarOpen.value = !isSidebarOpen.value;
}

function changeLanguage(lang: string) {
  locale.value = lang;
  const path = window.location.pathname.split("/").slice(2).join("/");
  router.push(`/${lang}/${path}`);
}

function logout() {
  localStorage.removeItem("token");
  isLoggedIn.value = false;
  router.push(`/${locale.value}/login`);
}

function goToProfile() {
  router.push(`/${locale.value}/profile`);
}

async function checkLogin() {
  const token = localStorage.getItem("token");
  if (!token) {
    isLoggedIn.value = false;
    return;
  }
  try {
    const res = await fetch(`http://localhost:8000/api/users/check-token/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    isLoggedIn.value = res.ok;
  } catch {
    isLoggedIn.value = false;
  }
}

onMounted(() => {
  checkLogin();
});
</script>

<style scoped>
nav {
  position: sticky;
  top: 0;
  padding: 12px 20px;
  width: 50%;
  margin: 15px auto 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #1e1b4b; /* Fondo oscuro */
  color: #e9d8fd; /* Texto suave */
  border-radius: 15px;
  border: 3px solid #facc15; /* Amarillo brillante */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease-in-out;
  z-index: 1000;
}

.logo-menu-container {
  display: flex;
  align-items: center;
  gap: 15px;
}

.logo {
  width: 50px;
  border-radius: 5px;
  transition: transform 0.2s ease-in-out;
}

.logo:hover {
  transform: rotate(5deg) scale(1.1);
}

.menu-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 8px;
  transition: transform 0.2s ease-in-out;
}

.menu-btn:hover {
  transform: scale(1.1);
}

.nav-links {
  display: flex;
  gap: 20px;
}

nav a {
  text-decoration: none;
  color: #e9d8fd; /* Texto suave */
  font-weight: 500;
  transition: color 0.3s ease-in-out;
}

nav a.router-link-active {
  font-weight: bold;
  color: #facc15; /* Amarillo brillante para enlace activo */
}

.box {
  padding: 8px 15px;
  border-radius: 10px;
  transition: transform 0.2s ease-in-out, background-color 0.3s ease-in-out;
}

.box:hover {
  background-color: rgba(250, 204, 21, 0.1); /* Fondo dorado sutil */
  transform: scale(1.1);
}

.sidebar {
  position: fixed;
  top: 0;
  left: -250px;
  width: 250px;
  height: 100vh;
  background: #1e1b4b; /* Fondo oscuro */
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
  padding: 20px;
  transition: left 0.3s ease-in-out;
  z-index: 1000;
}

.sidebar.open {
  left: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: #e9d8fd; /* Texto suave */
  position: absolute;
  right: 10px;
  top: 10px;
}

.close-btn:hover {
  color: #facc15; /* Amarillo brillante al pasar el ratón */
}

.sidebar h3 {
  margin-bottom: 10px;
  color: #facc15; /* Amarillo brillante para el título */
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar ul li {
  margin: 10px 0;
}

.sidebar ul li a {
  text-decoration: none;
  color: #facc15; /* Amarillo brillante para enlaces */
  font-weight: 500;
  transition: color 0.3s ease-in-out;
}

.sidebar ul li a:hover {
  color: #e9d8fd; /* Texto suave al pasar el ratón */
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}
</style>

<!-- 
<style scoped>
nav {
  position: sticky;
  top: 0;
  padding: 12px 20px;
  width: 50%;
  margin: 15px auto 0 auto;
  position: sticky;
  width: 50%;
  top: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  background-color: #fff2d0;
  color: #cda465;
  border-radius: 15px;
  border: 3px solid #f39c12;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease-in-out;
  z-index: 1000;
}

.logo-menu-container {
  display: flex;
  align-items: center;
  gap: 15px;
}

.logo {
  width: 50px;
  border-radius: 5px;
  transition: transform 0.2s ease-in-out;
}

.logo:hover {
  transform: rotate(5deg) scale(1.1);
}

.menu-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 8px;
  transition: transform 0.2s ease-in-out;
}

.menu-btn:hover {
  transform: scale(1.1);
}

.nav-links {
  display: flex;
  gap: 20px;
}

nav a {
  text-decoration: none;
  color: #ffc979;
  /* Mismo color de texto que en el footer */
  font-weight: 500;
  transition: color 0.3s ease-in-out;
}

nav a.router-link-active {
  font-weight: bold;
  color: #f39c12;
  /* Color dorado en el enlace activo */
}

.box {
  padding: 8px 15px;
  border-radius: 10px;
  transition: transform 0.2s ease-in-out, background-color 0.3s ease-in-out;
}

.box:hover {
  background-color: rgba(243, 156, 18, 0.1);
  /* Fondo dorado sutil */
  transform: scale(1.1);
}

.sidebar {
  position: fixed;
  top: 0;
  left: -250px;
  width: 250px;
  height: 100vh;
  background: #fffbf0;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
  padding: 20px;
  transition: left 0.3s ease-in-out;
  z-index: 1000;
}

.sidebar.open {
  left: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: #333;
  position: absolute;
  right: 10px;
  top: 10px;
}

.close-btn:hover {
  color: #f39c12;
  /* Color dorado */
}

.sidebar h3 {
  margin-bottom: 10px;
  color: #3e2723;
  /* Color oscuro para el título */
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar ul li {
  margin: 10px 0;
}

.sidebar ul li a {
  text-decoration: none;
  color: #f39c12;
  /* Color dorado para los enlaces */
  font-weight: 500;
  transition: color 0.3s ease-in-out;
}

.sidebar ul li a:hover {
  color: #3e2723;
  /* Color oscuro al pasar el ratón */
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}
</style> -->
