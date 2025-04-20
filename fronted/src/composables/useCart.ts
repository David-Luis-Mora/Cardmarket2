import { useCartStore } from '@/stores/cart';

export function useCart() {
  const cartStore = useCartStore();

  const calculateTax = (rate: number = 0.07) => {
    return cartStore.total * rate;
  };

  const getTotalWithTax = (rate: number = 0.07) => {
    return cartStore.total + calculateTax(rate);
  };

  return {
    cartStore,
    calculateTax,
    getTotalWithTax,
  };
}