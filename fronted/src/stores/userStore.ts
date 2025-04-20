import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: {
      name: 'Juan Pérez',
      email: 'juan@example.com',
      role: 'Administrador',
      avatar: ''
    } as null | { name: string; email: string; role: string; avatar?: string }
  }),

  actions: {
    setUser(newUser) {
      this.user = newUser
    }
  }
})
