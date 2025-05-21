// stores/authStore.ts
import { defineStore } from 'pinia';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { auth } from '../firebaseConfig';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false, 
  }),
  actions: {
    setUser(user: any) {
      this.user = user;
      this.isAuthenticated = !!user; 
    },
    initAuth() {
      onAuthStateChanged(auth, (user) => {
        this.setUser(user); 
      });
    },
    logout() {
      this.user = null;
      this.isAuthenticated = false;
    },
  },
});
