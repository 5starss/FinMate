<template>
  <header class="header">
    <div class="header-content">
      <RouterLink to="/" class="logo">
        FinMate
      </RouterLink>

      <nav class="nav-links">
        <RouterLink :to="{ name: 'DepositView' }">예금비교</RouterLink>
        <RouterLink :to="{ name: 'SavingView' }">적금비교</RouterLink>
        <!-- <RouterLink to="/articles">커뮤니티</RouterLink> -->
        <RouterLink :to="{ name: 'SearchView' }">비디오 검색</RouterLink>
        <RouterLink :to="{ name: 'MapView' }">지도</RouterLink>
        <RouterLink :to="{ name: 'ChartView' }">현물검색</RouterLink>
      </nav>

      <div class="user-actions">
        <RouterLink to="/login" class="login-btn">로그인</RouterLink>
        <RouterLink to="/signup" class="signup-btn">회원가입</RouterLink>
      </div>
    </div>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
/* 헤더 스타일 */
.header {
  background-color: #fff;
  border-bottom: 1px solid #eee; /* 하단 구분선 추가 */
  position: sticky; /* 스크롤 내려도 상단 고정 (선택사항) */
  top: 0;
  z-index: 1000;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 24px;
  font-weight: 800;
  color: #2F65F6; /* 포인트 컬러 */
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 30px;
}

.nav-links a {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  font-size: 16px;
  transition: color 0.2s;
}

.nav-links a:hover, .nav-links a.router-link-active {
  color: #2F65F6; /* 마우스 올리거나 현재 페이지일 때 색상 변경 */
}

.user-actions {
  display: flex;
  gap: 15px;
}

.login-btn {
  text-decoration: none;
  color: #666;
  font-weight: 500;
}

.signup-btn {
  text-decoration: none;
  background-color: #2F65F6;
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: bold;
  font-size: 14px;
}
</style>