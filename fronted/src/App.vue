<template>
  <div id="app">
    <NavBar></NavBar>
    <router-view />
    <Footer></Footer>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, provide, onMounted } from 'vue';
import { useAuthStore } from './stores/authStore';
import NavBar from './components/NavBar.vue';
import Footer from './components/Footer.vue';

export default defineComponent({
  name: 'App',
  components: {
    NavBar,
    Footer,
  },
  setup() {
    const authStore = useAuthStore();
    const logueado = ref(false);

    // Proveemos la variable logueado a los componentes hijos
    provide('logueado', logueado);

    onMounted(() => {
      // Inicializamos la autenticación cuando la app se monta
      authStore.initAuth();
    });

    return {
      authStore,
    };
  },
});
</script>

<style>
html, body, #app {
  height: 100%;
  margin: 0;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content {
  flex: 1;
}
</style>

