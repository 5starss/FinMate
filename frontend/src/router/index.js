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
import DepositDetailView from '@/views/DepositDetailView.vue'
import SavingDetailView from '@/views/SavingDetailView.vue'
import MyPageView from '@/views/MyPageView.vue' 
import LedgerView from '@/views/LedgerView.vue' 
import ArticleView from '@/views/ArticleView.vue'
import ArticleCreateView from '@/views/ArticleCreateView.vue'
import ArticleDetailView from '@/views/ArticleDetailView.vue'

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
      path: '/deposits/:id',
      name: 'DepositDetailView',
      component: DepositDetailView
    },
    {
      path: '/savings/:id', // ✅ URL 설계와 일치하도록
      name: 'SavingDetailView',
      component: SavingDetailView
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
    },
    {
      path: '/profile',
      name: 'MyPageView',
      component: MyPageView,
    },
    {
      path: '/ledger',
      name: 'LedgerView',
      component: LedgerView
    },
    {
      path: '/articles',
      name: 'ArticleView',
      component: ArticleView
    },
    {
      path: '/articles/create',
      name: 'ArticleCreateView',
      component: ArticleCreateView
    },
    {
      path: '/articles/:id',
      name: 'ArticleDetailView',
      component: ArticleDetailView
    },
  ]
})

router.beforeEach((to, from) => {
  const accountStore = useAccountStore()

  // 1. 로그인이 반드시 필요한 페이지들 관리
  // MyPageView를 추가했습니다.
  const authRequiredPages = ['MyPageView', 'DepositDetailView', 'SavingDetailView']
  
  if (authRequiredPages.includes(to.name) && !accountStore.isLogin) {
    window.alert('로그인이 필요한 서비스입니다.')
    return { name: 'LogInView' }
  }

  // 2. 이미 로그인한 사용자가 로그인/회원가입 페이지에 접근할 때
  // 기존 코드에서 ArticleView 대신 HomeView나 MyPageView로 보내는 것이 자연스럽습니다.
  if ((to.name === 'SignUpView' || to.name === 'LogInView') && accountStore.isLogin) {
    window.alert('이미 로그인 되어 있습니다.')
    return { name: 'HomeView' } // 혹은 MyPageView
  }
  
})

export default router
