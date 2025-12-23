import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const API_URL = import.meta.env.VITE_API_URL
  const token = ref(null)
  const myname = ref(null)

  const router = useRouter()

  const signUp = function (payload) {
    const username = payload.username
    const password1 = payload.password1
    const password2 = payload.password2

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2, 
      }
    })
      .then(res => {
        console.log('회원 가입이 완료되었습니다.')
        console.log(res)
        const password = password1
        logIn({ username, password })
      })
      .catch(err => console.log(err))
  }


  const logIn = function (payload) {
    const username = payload.username
    const password = payload.password

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then(res => {
        console.log('로그인이 완료되었습니다.')
        console.log(res.data)
        token.value = res.data.key
        myname.value = username
        router.push({ name: 'HomeView' })
      })
      .catch(err => console.log(err))
  }


  const isLogin = computed(() => {
    return token.value ? true : false
  })


  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`
    })
      .then(res => {
        token.value = null
        myname.value = null
        router.push({ name: 'HomeView' })
      })
      .catch(err => console.log(err))
  }

  return {
    signUp,
    logIn,
    token,
    isLogin,
    logOut,
    username: myname,
  }
}, { persist: true })