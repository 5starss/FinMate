import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import HomeView from '@/views/HomeView.vue'
import DepositView from '@/views/DepositView.vue'
import SavingView from '@/views/SavingView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import SearchView from '@/views/SearchView.vue'
import VideoDetail from '@/views/VideoDetail.vue'
import MapView from '@/views/MapView.vue'
import ChartView from '@/views/ChartView.vue'

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
    {
      path: '/deposit/:id',
      name: 'DepositDetailView',
      component: () => import('@/views/DepositDetailView.vue'),
    },
    {
      path: '/saving/:id',
      name: 'SavingDetailView',
      component: () => import('@/views/SavingDetailView.vue'),
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView
    },
    {
      path: '/search',
      name: 'SearchView',
      component: SearchView
    },
    {
      path: '/video/:id',
      name: 'detail',
      component: VideoDetail
    },
    {
      path: '/map', 
      name: 'MapView',
      component: MapView
    },
    {
      path: '/chart', 
      name: 'ChartView',
      component: ChartView
    }
  ]
})

router.beforeEach((to, from) => {
  const accountStore = useAccountStore()

  if (to.name === 'ArticleView' && !accountStore.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'LogInView' }
  }

  if ((to.name === 'SignUpView' || to.name === 'LogInView') && (accountStore.isLogin) ) {
    window.alert('이미 로그인 되어 있습니다.')
    return { name: 'ArticleView' }
  }
})

export default router
