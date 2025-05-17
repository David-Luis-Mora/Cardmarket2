import { defineStore } from 'pinia'

export interface UserProfile {
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  nickname: string;
  avatar?: string;
  country?: string;
  address?: string;
  phone?: string;
  bio?: string;
}

export const useUserStore = defineStore("user", {
  state: () => ({
    user: null as UserProfile | null,
  }),
  actions: {
    setUser(userData: UserProfile) {
      this.user = userData;
    },
  },
});



