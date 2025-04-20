// store/globalState.ts
import { reactive } from 'vue';

export const globalState = reactive({
  logueado: false,
  user: null,
});

export const setUser = (userData: any) => {
  globalState.logueado = true;
  globalState.user = userData;
};

export const logOut = () => {
  globalState.logueado = false;
  globalState.user = null;
};
