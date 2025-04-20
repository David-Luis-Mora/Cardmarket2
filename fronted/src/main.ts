import { createApp, watchEffect } from "vue";
import i18n from "./i18n";
import App from './App.vue';
import router from "./router";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import "bootstrap";
import "../style.css"
import { createPinia } from 'pinia';
const pinia = createPinia();
const app = createApp(App);
// Sincroniza el idioma en la URL con i18n
watchEffect(() => {
    const currentRoute = router.currentRoute.value;
    const langParam = currentRoute.params.lang;
    const lang = (typeof langParam === 'string' && (langParam === 'es' || langParam === 'en'))
      ? langParam
      : 'es'; // por defecto 'es'
  
    if (i18n.global.locale.value !== lang) {
      i18n.global.locale.value = lang;
      localStorage.setItem("language", lang);
    }
  });
  
app.use(pinia);
app.use(i18n);
app.use(router);
app.mount("#app");