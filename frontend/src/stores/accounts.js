import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const API_URL = import.meta.env.VITE_API_URL
  const token = ref(null)
  const myname = ref(null) // 아이디
  const nickname = ref(null) // 닉네임
  const userImage = ref(null)

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
    data: { username, password }
  })
    .then(res => {
      // 1. 토큰 및 ID 저장
      token.value = res.data.key
      myname.value = username
      
      // 2. [추가] 닉네임을 가져오기 위해 프로필 요청
      axios({
        method: 'get',
        url: `${API_URL}/accounts/profile/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      .then(profileRes => {
        // 프로필 응답에서 닉네임 추출 (없으면 ID로 대체)
        nickname.value = profileRes.data.nickname || username
        console.log('로그인 완료: 닉네임 가져오기 성공', nickname.value)

        // [추가] 이미지 경로 저장 (백엔드 구조에 맞춰 profile.image 접근)
        // 만약 이미지가 없으면 null이 들어감
        userImage.value = profileRes.data.profile?.image || null

        router.push({ name: 'HomeView' })
      })
      .catch(err => {
        console.error('프로필 조회 실패:', err)
        // 프로필 조회 실패해도 로그인은 유지
        nickname.value = username 
        router.push({ name: 'HomeView' })
      })
    })
    .catch(err => {
      console.log(err)
      alert('아이디 혹은 비밀번호가 틀렸습니다.')
    })
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
    API_URL,
    signUp,
    logIn,
    token,
    isLogin,
    logOut,
    username: myname,
    nickname,
    userImage,
  }
}, { persist: true })