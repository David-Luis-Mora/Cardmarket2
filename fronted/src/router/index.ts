import { createRouter, createWebHistory } from 'vue-router';
import ProductList from '../views/ProductList.vue';
import Cart from '../components/Cart.vue';
import HomePage from '../components/HomePage.vue';
import RegisterForm from '../components/RegisterForm.vue';
import LoginForm from '../components/LoginPage.vue';
import ProfileForm from '../components/ProfilePage.vue'
import AboutUs from '../components/AboutUs.vue';
import PaymentForm from '@/components/PaymentPage.vue';
import ProfilePage from '../components/ProfilePage.vue';

const routes = [
  { path: "/", redirect: "/en/" },
  { path: '/:lang/', name: "Home", component: HomePage, beforeEnter: validateLang },
  { path: '/:lang/cards', name: "Cards", component: ProductList, beforeEnter: validateLang },
  { path: '/:lang/cart', name: "Cart", component: Cart, beforeEnter: validateLang },
  { path: '/:lang/login', name: "Login", component: LoginForm, beforeEnter: validateLang },
  { path: '/:lang/register', name: "Register", component: RegisterForm, beforeEnter: validateLang },
  { path: '/:lang/user', name: "User", component: ProfileForm, beforeEnter: validateLang },
  { path: '/:lang/aboutus', name: "AboutUs", component: AboutUs, beforeEnter: validateLang },
  { path: '/:lang/payment', name: "Payment", component: PaymentForm, beforeEnter: validateLang },
  { path: '/:lang/profile', name: "Profile", component: ProfilePage, beforeEnter: validateLang},


  {
    path: '/products/:expansion',  // Ruta con parámetro 'expansion'
    component: ProductList,
    name: 'product-list',
    props: true  // Esto permite pasar el parámetro 'expansion' como prop al componente
  },
];

// Función para validar el idioma
function validateLang(to: any, from: any, next: any) {
  const lang = to.params.lang;
  const supportedLanguages = ["en", "es"];

  if (!supportedLanguages.includes(lang)) {
    return next("/en/");
  }

  next();
}

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
