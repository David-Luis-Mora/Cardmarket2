// stores/authStore.ts
import { defineStore } from 'pinia';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { auth } from '../firebaseConfig';
export function isAuthenticated(): boolean {
  const token = localStorage.getItem("token");
  return !!token;
}
export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false, // Variable para indicar si el usuario está autenticado
  }),
  actions: {
    setUser(user: any) {
      this.user = user;
      this.isAuthenticated = !!user; // Si hay un usuario, se autentica
    },
    initAuth() {
      onAuthStateChanged(auth, (user) => {
        this.setUser(user); // Actualiza el estado de autenticación al cambiar el estado del auth
      });
    },
    logout() {
      this.user = null;
      this.isAuthenticated = false; // El usuario ya no está autenticado
    },
  },
});
