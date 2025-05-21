<template>
  <nav>
    <div class="logo-menu-container">
      <!-- Menu Button for Mobile -->
      <button class="menu-btn" @click="isSidebarOpen = true">
        <i class="bi bi-list"></i>
      </button>
      <router-link class="nav-link js-scroll-trigger" :to="`/${locale}/`">
        <img src="/logo.png" alt="CardShop Logo" class="logo" />
      </router-link>
    </div>

    <!-- Desktop Links -->
    <div class="nav-links">
      <div class="box">
        <router-link class="nav-link js-scroll-trigger" :to="`/${locale}/cards`">
          <i class="bi bi-droplet"></i> {{ t("cards") }}
        </router-link>
      </div>
      <div class="box">
        <router-link class="nav-link js-scroll-trigger" :to="`/${locale}/cart`">
          <i class="bi bi-cart2"></i> {{ t("cart") }}
        </router-link>
      </div>
      <div class="box dropdown">
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
      <!-- Authentication -->
      <div v-if="isLoggedIn" class="box">
        <router-link class="nav-link" :to="{ name: 'MyProfile', params: { lang: locale } }">
          <i class="bi bi-person-fill"></i> {{ t("navprofile") }}
        </router-link>
      </div>
      <div v-if="!isLoggedIn" class="box">
        <router-link class="nav-link" :to="`/${locale}/login`">
          <i class="bi bi-person"></i> {{ t("navlogin") }}
        </router-link>
      </div>
      <div v-if="isLoggedIn" class="box">
        <button class="nav-link btn-logout" @click="logout">
          <i class="bi bi-box-arrow-right"></i> {{ t("navlogout") }}
        </button>
      </div>
    </div>

    <!-- Sidebar for Mobile -->
    <div class="sidebar" :class="{ open: isSidebarOpen }">
      <button class="close-btn" @click="isSidebarOpen = false">
        <i class="bi bi-x-lg"></i>
      </button>
      <ul>
        <li>
          <router-link @click="isSidebarOpen = false" :to="`/${locale}/cards`">{{
            t("cards")
          }}</router-link>
        </li>
        <li>
          <router-link @click="isSidebarOpen = false" :to="`/${locale}/cart`">{{
            t("cart")
          }}</router-link>
        </li>
        <li class="dropdown">
          <a href="#" class="dropdown-toggle" data-bs-toggle="dropdown">{{ t("language") }}</a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" @click.prevent="changeLanguage('es')">Español</a></li>
            <li><a class="dropdown-item" @click.prevent="changeLanguage('en')">English</a></li>
          </ul>
        </li>
        <li v-if="isLoggedIn">
          <router-link
            @click="isSidebarOpen = false"
            :to="{ name: 'MyProfile', params: { lang: locale } }"
            >{{ t("navprofile") }}</router-link
          >
        </li>
        <li v-if="!isLoggedIn">
          <router-link @click="isSidebarOpen = false" :to="`/${locale}/login`">{{
            t("navlogin")
          }}</router-link>
        </li>
        <li v-if="isLoggedIn">
          <button class="btn-logout" @click="logout">{{ t("navlogout") }}</button>
        </li>
      </ul>
    </div>
    <div class="overlay" v-if="isSidebarOpen" @click="isSidebarOpen = false"></div>
  </nav>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";

const { t, locale } = useI18n();
const router = useRouter();

const isSidebarOpen = ref(false);
const isLoggedIn = ref(false);

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

async function checkLogin() {
  const token = localStorage.getItem("token");
  if (!token) {
    isLoggedIn.value = false;
    return;
  }
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/api/users/check-token/`, {
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
  position: fixed;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 20px;
  width: 50%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #1e1b4b;
  color: #e9d8fd;
  border-radius: 15px;
  border: 3px solid #facc15;
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
  display: none;
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
  color: #e9d8fd;
  font-weight: 500;
  transition: color 0.3s ease-in-out;
}

nav a.router-link-active {
  font-weight: bold;
  color: #facc15;
}
.dropdown-item {
  color: #000000;
}

.box {
  padding: 8px 15px;
  border-radius: 10px;
  transition: transform 0.2s ease-in-out, background-color 0.3s ease-in-out;
}

.box:hover {
  background-color: rgba(250, 204, 21, 0.1);
  transform: scale(1.1);
}

/* Sidebar & overlay hidden by default */
.sidebar,
.overlay {
  display: none;
}

/* ESCRITORIO */
@media (max-width: 1300px) {
  nav {
    width: 100%;
    padding: 10px 15px;
  }
}
@media (max-width: 1000px) {
  .sidebar,
  .overlay {
    display: none;
  }
  .menu-btn {
    display: none;
  }

  .nav-links {
    display: flex;
    gap: 20px;
  }
}
/* Mobile specific */
@media (max-width: 800px) {
  nav {
    width: 100%;
    padding: 10px 15px;
  }
  .menu-btn {
    display: block;
  }
  /* Hide desktop links in mobile */
  .nav-links {
    display: none;
  }
  .sidebar {
    position: fixed;
    top: 0;
    left: -250px;
    width: 250px;
    height: 100vh;
    background: #1e1b4b;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
    padding: 20px;
    transition: left 0.3s ease-in-out;
    z-index: 1000;
    display: block;
  }
  .sidebar.open {
    left: 0;
  }
  .close-btn {
    background: none;
    border: none;
    font-size: 28px;
    cursor: pointer;
    color: #e9d8fd;
    position: absolute;
    right: 10px;
    top: 10px;
  }
  .close-btn:hover {
    color: #facc15;
  }

  .sidebar ul {
    list-style: none;
    padding: 0;
    margin-top: 40px;
  }
  .sidebar ul li {
    margin: 10px 0;
  }
  .sidebar ul li a {
    text-align: center;
  }
  .sidebar ul li a,
  .sidebar ul li button {
    text-decoration: none;
    color: #facc15;
    font-weight: 500;
    background: none;
    border: none;
    padding: 0;
    cursor: pointer;
    transition: color 0.3s ease-in-out;
  }
  .sidebar ul li a:hover,
  .sidebar ul li button:hover {
    color: #e9d8fd;
  }
  .overlay {
    display: block;
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    z-index: 999;
  }
}

/* Mobile text sizes */
@media (max-width: 768px) {
  nav .nav-link,
  nav .box {
    font-size: 0.85rem;
  }
  nav .box {
    padding: 6px 10px;
  }
}

@media (max-width: 570px) {
  nav .nav-link,
  nav .box {
    font-size: 0.3rem;
  }
  nav .box {
    padding: 6px 10px;
  }
}
</style>
