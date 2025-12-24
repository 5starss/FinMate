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
  // payload에서 데이터를 추출
  const { username, password1, password2, nickname, gender, birth_date } = payload

  axios({
    method: 'post',
    url: `${API_URL}/accounts/signup/`,
    data: {
      username,
      nickname,
      gender,
      birth_date,
      // [중요 수정] 백엔드 에러 메시지 규격에 맞춰 키 이름을 수정합니다.
      password1: password1,
      password2: password2,
    }
  })
  .then((res) => {
    // 1. 성공 알림창 띄우기
    alert('회원가입이 성공했습니다! 로그인 페이지로 이동합니다.')
    // 2. 로그인 페이지 이동
    console.log('회원가입 성공!')
    router.push({ name: 'LogInView' })
  })
  .catch((err) => {
    // 에러 발생 시 서버가 보낸 구체적인 에러 문구를 콘솔에 출력 (디버깅용)
    console.error('회원가입 에러 상세:', err.response?.data)
    alert('회원가입에 실패했습니다. 입력 정보를 확인해주세요.')
  })
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