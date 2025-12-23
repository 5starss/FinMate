<template>
  <div class="auth-container">
    <div class="auth-card animate-up">
      <div class="card-header">
        <h1 class="brand-logo">FinMate</h1>
        <p class="sub-text">로그인하고 금융 생활을 시작하세요</p>
      </div>

      <form @submit.prevent="logIn" class="auth-form">
        <div class="form-group">
          <label for="username">아이디</label>
          <input 
            type="text" 
            id="username" 
            v-model.trim="username" 
            placeholder="아이디를 입력하세요"
            required
          >
        </div>

        <div class="form-group">
          <label for="password">비밀번호</label>
          <input 
            type="password" 
            id="password" 
            v-model.trim="password"
            placeholder="비밀번호를 입력하세요"
            required
          >
        </div>

        <button type="submit" class="submit-btn">로그인</button>
      </form>

      <div class="card-footer">
        <p>아직 계정이 없으신가요?</p>
        <RouterLink :to="{ name: 'SignUpView' }" class="link-text">회원가입 하러가기</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { RouterLink } from 'vue-router'

const accountStore = useAccountStore()

const username = ref(null)
const password = ref(null)

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value,
  }
  accountStore.logIn(payload)
}
</script>

<style scoped>
/* 전체 화면 중앙 정렬 */
.auth-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  /* min-height: calc(100vh - 70px); 헤더 제외 높이 */
  background-color: #f5f7fa;
  padding: 20px;
}

/* 카드 스타일 */
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

/* 등장 애니메이션 */
.animate-up {
  animation: slideUp 0.6s ease-out;
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 헤더 스타일 */
.brand-logo {
  font-size: 28px;
  font-weight: 800;
  color: #2F65F6;
  margin-bottom: 10px;
}

.sub-text {
  color: #666;
  font-size: 15px;
  margin-bottom: 30px;
}

/* 폼 스타일 */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
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

/* 입력창 포커스 효과 */
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

/* 하단 링크 */
.card-footer {
  font-size: 14px;
  color: #888;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
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