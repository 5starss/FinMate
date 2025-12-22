// src/stores/counter.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const router = useRouter()
  
  // 1. State: 토큰과 사용자 이름 저장
  const token = ref(localStorage.getItem('token') || null)
  const username = ref(localStorage.getItem('username') || null)

  // 2. Getters: 로그인 여부 확인 (토큰이 있으면 true)
  const isLogin = computed(() => !!token.value)

  // 3. Actions: 로그인/로그아웃 기능
  const logIn = (paramToken, paramUsername) => {
    token.value = paramToken
    username.value = paramUsername
    // 새로고침 해도 유지되도록 로컬스토리지 저장
    localStorage.setItem('token', paramToken)
    localStorage.setItem('username', paramUsername)
  }

  const logOut = () => {
    token.value = null
    username.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    
    // 로그아웃 후 메인 페이지로 이동
    // (router가 store 내부에서 안 먹힐 경우, 컴포넌트에서 처리해도 됨)
    // window.location.reload() // 필요 시 깔끔하게 새로고침
  }

  return { token, username, isLogin, logIn, logOut }
}, { persist: true }) // pinia-plugin-persistedstate가 설치되어 있다면 유용