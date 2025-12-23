<template>
  <header class="header-wrapper">
    <div class="top-bar">
      <div class="inner-container top-content">
        <div class="user-menu">
          <ul>
            <template v-if="store.isLogin">
              <li class="greeting">
                <span class="username">{{ store.username }}</span>님 환영합니다
              </li>
              <li>
                <a @click.prevent="handleLogout" class="util-link logout-btn">로그아웃</a>
              </li>
            </template>
            <template v-else>
              <li> 
                <RouterLink :to="{ name: 'LogInView' }" class="util-link">로그인</RouterLink>
              </li>
              <li>
                <RouterLink :to="{ name: 'SignUpView' }" class="util-link">회원가입</RouterLink>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </div>

    <div class="main-header">
      <div class="inner-container nav-content">
        <RouterLink to="/" class="logo">
          FinMate
        </RouterLink>

        <nav class="nav-links">
          <RouterLink :to="{ name: 'DepositView' }">예금비교</RouterLink>
          <RouterLink :to="{ name: 'SavingView' }">적금비교</RouterLink>
          <RouterLink :to="{ name: 'MyPageView' }">마이페이지</RouterLink>
          <RouterLink :to="{ name: 'SearchView' }">정보검색</RouterLink>
          <RouterLink :to="{ name: 'MapView' }">지도</RouterLink>
          <RouterLink :to="{ name: 'ChartView' }">현물검색</RouterLink>
          <RouterLink to="/">커뮤니티</RouterLink>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const store = useAccountStore()
const router = useRouter()

// 로그아웃 핸들러
const handleLogout = () => {
  const confirmLogout = confirm('로그아웃 하시겠습니까?')
  if (confirmLogout) {
    store.logOut()
    alert('로그아웃 되었습니다.')
    router.push('/') // 메인 페이지로 이동
  }
}
</script>

<style scoped>
.header-wrapper {
  position: sticky; /* 스크롤 시 화면에 붙도록 설정 */
  top: 0; /* 화면 최상단에 고정 */
  z-index: 1000; /* 다른 콘텐츠보다 위에 오도록 순서 지정 */
  background-color: #fff; /* 스크롤 시 뒤에 내용이 비치지 않게 배경색 지정 */
  width: 100%;
}

/* 공통 레이아웃 (가운데 정렬용) */
.inner-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 1. 상단 유틸리티 바 스타일 */
.top-bar {
  border-bottom: 1px solid #eee;
  font-size: 5px; /* 작은 글씨 */
  padding: 10px 0;
}

.top-content {
  display: flex;
  justify-content: flex-end; /* 오른쪽 정렬 */
}

.user-menu ul {
  display: flex;
  align-items: center;
  /* margin-left: 2.4rem; */
  gap: 10px;
}

.user-menu li {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
  /* margin-left: 2.4rem; */
}

.util-link {
  text-decoration: none;
  color: #666;
  cursor: pointer;
  padding: 0 10px;
  transition: color 0.2s;
}

.util-link:hover {
  text-decoration: underline;
}

/* 2. 메인 헤더 스타일 */
.main-header {
  background-color: #fff;
  padding: 20px 0;
  border-bottom: 1px solid #eee; /* 헤더 하단 구분선 */
}

.nav-content {
  display: flex;
  align-items: center;
  /* 로고와 메뉴 사이 간격 조절 */
  gap: 60px; 
}

.logo {
  margin-left: 15px;
  font-size: 26px;
  font-weight: 800;
  color: #2F65F6;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 50px; /* 메뉴 간격 넓게 */
  align-items: center;
  margin-left: 50px;
}

.nav-links a {
  text-decoration: none;
  color: #333;
  font-weight: 600;
  font-size: 17px;
  position: relative; /* 밑줄 효과를 위해 필요 */
}

/* 메뉴 호버 효과 (파란색 + 밑줄) */
.nav-links a:hover,
.nav-links a.router-link-active {
  color: #2F65F6;
}

.greeting {
  color: #666;
  cursor: default; /* 드래그/클릭 느낌 제거 */
}
.username {
  font-weight: 700;
  color: #333;
}
.logout-btn {
  color: #999; /* 로그아웃은 약간 흐리게 */
}
.logout-btn:hover {
  color: #ff4d4f; /* 로그아웃 호버 시 빨간색 경고 느낌 */
}
</style>