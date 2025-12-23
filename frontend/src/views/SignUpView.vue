<template>
  <div class="auth-container">
    <div class="auth-card animate-up">
      
      <div class="card-header">
        <h1 class="title">회원가입</h1>
        <p class="sub-text">FinMate와 함께 스마트한 자산 관리를 시작하세요</p>
      </div>

      <form @submit.prevent="signUp" class="auth-form">
        <div class="form-group">
          <label for="username">아이디</label>
          <input 
            type="text" 
            id="username" 
            v-model.trim="username" 
            placeholder="사용할 아이디를 입력하세요"
            required
          >
        </div>

        <div class="form-group">
          <label for="password1">비밀번호</label>
          <input 
            type="password" 
            id="password1" 
            v-model.trim="password1"
            placeholder="비밀번호를 입력하세요"
            required
          >
        </div>

        <div class="form-group">
          <label for="password2">비밀번호 확인</label>
          <input 
            type="password" 
            id="password2" 
            v-model.trim="password2"
            placeholder="비밀번호를 한 번 더 입력하세요"
            required
          >
        </div>

        <button type="submit" class="submit-btn">가입하기</button>
      </form>

      <div class="card-footer">
        <p>이미 계정이 있으신가요?</p>
        <RouterLink :to="{ name: 'LogInView' }" class="link-text">로그인 하러가기</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/accounts'
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const accountStore = useAccountStore()

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
  }
  accountStore.signUp(payload)
}
</script>

<style scoped>
/* LogInView와 동일한 스타일 적용 (통일감 유지) */
.auth-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 70px);
  background-color: #f5f7fa;
  padding: 20px;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  background: white;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  text-align: center;
  border: 1px solid #eee;
}

.animate-up {
  animation: slideUp 0.6s ease-out;
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.title {
  font-size: 26px;
  font-weight: 800;
  color: #333;
  margin-bottom: 10px;
}

.sub-text {
  color: #666;
  font-size: 14px;
  margin-bottom: 30px;
  word-break: keep-all; /* 단어 단위 줄바꿈 */
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 18px; /* 간격 미세 조정 */
  margin-bottom: 25px;
}

.form-group {
  text-align: left;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.form-group input {
  box-sizing: border-box;
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 15px;
  outline: none;
  transition: all 0.2s;
}

.form-group input:focus {
  border-color: #2F65F6;
  box-shadow: 0 0 0 3px rgba(47, 101, 246, 0.1);
}

.submit-btn {
  width: 100%;
  padding: 14px;
  background-color: #2F65F6;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 10px;
}

.submit-btn:hover {
  background-color: #1c50d8;
}

.card-footer {
  font-size: 14px;
  color: #888;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  /* padding-top: 5px; */
}

.card-footer p {
  margin: 0;
}

.link-text {
  color: #2F65F6;
  font-weight: 600;
  text-decoration: none;
}

.link-text:hover {
  text-decoration: underline;
}
</style>