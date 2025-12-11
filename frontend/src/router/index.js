import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import DepositView from '@/views/DepositView.vue'
import SavingView from '@/views/SavingView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomeView',
      component: HomeView,
    },
    {
      path: '/deposit',
      name: 'DepositView',
      component: DepositView,
    },
    {
      path: '/saving',
      name: 'SavingView',
      component: SavingView,
    },
  ],
})

export default router
