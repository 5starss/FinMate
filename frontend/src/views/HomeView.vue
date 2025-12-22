<template>
  <div class="home-container">
    
    <div class="top-section">
      
      <section class="hero-box">
        <div class="hero-content">
          <span class="badge">FinMate 리포트 📢</span>
          <h1 class="main-title">
            똑똑한 금융 생활의 시작,<br>
            <strong>나에게 딱 맞는 예적금</strong>
          </h1>
          <p class="sub-text">
            수많은 금융 상품 중 최고 금리 상품을<br>
            FinMate가 분석해서 추천해 드립니다.
          </p>
          <div class="hero-buttons">
            <button class="cta-btn" @click="router.push('/deposit')">예금 비교하기 ></button>
            <button class="cta-btn secondary" @click="router.push('/saving')">적금 비교하기 ></button>
          </div>
        </div>
        <div class="hero-image">
          💰🏦
        </div>
      </section>

      <aside class="login-widget">
        <div v-if="!isLogin" class="card-content login-mode">
          <div class="avatar-circle">👤</div>
          <p class="login-msg">
            로그인 후<br>
            <strong>나만의 맞춤 정보</strong>를 이용하세요.
          </p>
          <button class="primary-btn" @click="router.push('/login')">로그인</button>
          <div class="sub-links">
            <span>아이디 찾기</span> | <span>비밀번호 찾기</span>
          </div>
        </div>

        <div v-else class="card-content user-mode">
          <p><strong>홍길동</strong>님 환영합니다! 👋</p>
          <button class="primary-btn outline">마이페이지</button>
        </div>
      </aside>
    </div>

    <section class="search-section">
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchQuery" 
          @keyup.enter="goSearch"
          placeholder="은행명, 상품명을 검색해보세요 (예: 신한은행)" 
        />
        <button class="search-icon-btn" @click="goSearch">🔍</button>
      </div>
      <div class="hashtags">
        <span>#최고금리</span>
        <span>#청년도약계좌</span>
        <span>#특판상품</span>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
// 나중에 Pinia 등에서 로그인 상태를 가져올 변수 (일단 false로 가정)
const isLogin = ref(false) 

// 검색어 상태
const searchQuery = ref('')

const goSearch = () => {
  if (searchQuery.value.trim()) {
    alert(`'${searchQuery.value}' 검색 기능은 아직 구현 중입니다!`)
    // router.push({ name: 'search', query: { q: searchQuery.value } })
  }
}
</script>

<style scoped>
/* 전체 레이아웃 */
.home-container {
  max-width: 1200px;
  margin: 40px auto; /* 상하 여백 40px, 가운데 정렬 */
  padding: 0 20px;
}

/* 1. 상단 섹션 (Grid or Flex) */
.top-section {
  display: flex;
  gap: 30px;
  margin-bottom: 60px;
  align-items: stretch; /* 높이 맞춤 */
}

/* 왼쪽 히어로 배너 */
.hero-box {
  flex: 2; /* 2:1 비율 */
  background-color: #F0F4FF; /* 아주 연한 블루 배경 */
  border-radius: 24px;
  padding: 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.badge {
  color: #2F65F6;
  font-weight: 700;
  font-size: 14px;
  background: #fff;
  padding: 6px 12px;
  border-radius: 20px;
  display: inline-block;
  margin-bottom: 15px;
}

.main-title {
  font-size: 32px;
  line-height: 1.4;
  color: #111;
  margin-bottom: 15px;
}

.main-title strong {
  color: #2F65F6; /* 강조색 */
}

.sub-text {
  color: #666;
  font-size: 16px;
  margin-bottom: 30px;
  line-height: 1.6;
}

.hero-buttons {
  display: flex;
  gap: 10px;
}

.cta-btn {
  border: none;
  background-color: #2F65F6;
  color: white;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: bold;
  cursor: pointer;
  transition: opacity 0.2s;
}

.cta-btn.secondary {
  background-color: #fff;
  color: #2F65F6;
  border: 1px solid #2F65F6;
}

.cta-btn:hover {
  opacity: 0.9;
}

.hero-image {
  font-size: 100px; /* 아이콘 크기 */
  /* 실제 이미지가 있다면 img 태그로 교체하고 width 설정 */
}

/* 오른쪽 로그인 위젯 */
.login-widget {
  flex: 1;
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 24px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.03); /* 은은한 그림자 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
}

.avatar-circle {
  width: 60px;
  height: 60px;
  background-color: #f1f3f5;
  border-radius: 50%;
  margin: 0 auto 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 30px;
}

.login-msg {
  font-size: 16px;
  color: #333;
  margin-bottom: 20px;
  line-height: 1.5;
}

.primary-btn {
  width: 100%;
  padding: 14px;
  background-color: #2F65F6;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
}

.primary-btn.outline {
  background-color: white;
  color: #2F65F6;
  border: 1px solid #2F65F6;
}

.sub-links {
  margin-top: 15px;
  font-size: 13px;
  color: #999;
}

.sub-links span {
  cursor: pointer;
}

/* 2. 하단 검색 섹션 */
.search-section {
  background: linear-gradient(135deg, #2F65F6, #1E40AF); /* 파란색 그라데이션 */
  border-radius: 24px;
  padding: 50px;
  text-align: center;
  color: white;
}

.search-box {
  position: relative;
  max-width: 600px;
  margin: 0 auto 20px;
}

.search-box input {
  width: 100%;
  padding: 18px 25px;
  border-radius: 50px;
  border: none;
  font-size: 16px;
  outline: none;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.search-icon-btn {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: 22px;
  cursor: pointer;
}

.hashtags span {
  margin: 0 8px;
  font-size: 14px;
  opacity: 0.8;
  cursor: pointer;
}
.hashtags span:hover {
  text-decoration: underline;
  opacity: 1;
}

</style>