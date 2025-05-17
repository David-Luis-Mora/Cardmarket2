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
import SellCardList from "@/components/SellCards.vue";
import ProductDetail from '@/views/ProductDetail.vue';
import SellerProfile from '@/views/SellerProfile.vue'

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
  { path: "/:lang/sell-cards", name: "SellCards", component: SellCardList, meta: { requiresAuth: true },},
  {
    path: '/:lang/profile',
    name: 'MyProfile',
    component: ProfileForm,
    beforeEnter: validateLang,
    props: (route: any) => ({ lang: route.params.lang as string }),
  },
  {
    path: '/:lang/seller/:nickname',
    name: 'SellerProfile',
    component: SellerProfile,
    beforeEnter: validateLang,
    props: (route: any) => ({
      lang: route.params.lang as string,
      nickname: route.params.nickname as string,
    }),
  },
  {
    path: '/:lang/login',
    name: 'Login',
    component: LoginForm,
    beforeEnter: validateLang,
    props: (route: any) => ({ lang: route.params.lang as string }),
  },
  {
    path: '/:lang/product/:productId',
    name: 'ProductDetail',
    component: ProductDetail,
    beforeEnter: validateLang,
    props: (route: any) => ({
      lang: route.params.lang as string,
      productId: route.params.productId as string,
    }),
  },
  
  


  {
    path: '/products/:expansion',  
    component: ProductList,
    name: 'product-list',
    props: true  
  },
];

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
