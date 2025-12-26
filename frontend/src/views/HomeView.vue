<template>
  <div class="home-container">
    
    <div class="top-section animate-fade-in">
      
      <section class="hero-box">
        <div class="hero-content">
          <span class="badge">FinMate 리포트 📢</span>
          <h1 class="main-title">
            똑똑한 금융 생활의 시작,<br>
            <strong>나에게 맞는 예적금</strong>
          </h1>
          <p class="sub-text">
            수많은 금융 상품 중 최고 금리 상품을<br>
            FinMate가 분석해서 추천해 드립니다.
          </p>
          <div class="hero-buttons">
            <button class="cta-btn" @click="router.push({ name: 'DepositView' })">예금 비교하기 &rarr;</button>
            <button class="cta-btn secondary" @click="router.push({ name: 'SavingView' })">적금 비교하기 &rarr;</button>
          </div>
        </div>
        <div class="hero-image">
          <div class="floating-icon">💰</div>
        </div>
      </section>

      <aside class="login-widget">
        <div v-if="!store.isLogin" class="card-content login-mode">
          <div class="avatar-circle">🔒</div>
          <p class="login-msg">
            로그인하고<br>
            <strong>나만의 맞춤 금리</strong>를 확인하세요.
          </p>
          <button class="primary-btn" @click="router.push({ name: 'LogInView' })">로그인하기</button>
          <div class="login-links">
            <span @click="router.push({ name: 'SignUpView' })">회원가입</span>
            <span class="divider">|</span>
            <span>ID/PW 찾기</span>
          </div>
        </div>

        <div v-else class="card-content user-mode">
          <div class="user-profile">
            <div class="avatar-circle active">
              <img 
                v-if="store.userImage" 
                :src="getProfileImageUrl(store.userImage)" 
                class="home-profile-img" 
                alt="프로필" 
              />
              <span v-else>👤</span>
            </div>
            <p class="welcome-text">
              <span class="username">{{ store.nickname }}</span>님,<br>
              부자 되세요! 💸
            </p>
          </div>
          <div class="my-menu">
            <button class="menu-btn" @click="router.push({ name: 'MyPageView' })">마이페이지</button>
            <button class="menu-btn" @click="router.push({ name: 'RecommendView' })">AI 추천</button>
          </div>
          <button class="primary-btn outline" @click="store.logOut()">로그아웃</button>
        </div>
      </aside>
    </div>

    <section class="quick-menu-section animate-slide-up">
      <h3 class="section-title">자주 찾는 서비스</h3>
      <div class="quick-icons">
        <div class="icon-item" @click="router.push({ name: 'MapView' })">
          <div class="icon-circle map-bg">🗺️</div>
          <span>은행 찾기</span>
        </div>
        <div class="icon-item" @click="router.push({ name: 'ChartView' })">
          <div class="icon-circle chart-bg">📈</div>
          <span>금/은 시세</span>
        </div>
        <div class="icon-item" @click="router.push({ name: 'DepositView' })">
          <div class="icon-circle deposit-bg">🏦</div>
          <span>예금 상품</span>
        </div>
        <div class="icon-item" @click="router.push('/')">
          <div class="icon-circle board-bg">💬</div>
          <span>커뮤니티</span>
        </div>
      </div>
    </section>

    <section class="feature-section animate-slide-up delay-1">
      <div class="feature-card chart-card" @click="router.push({ name: 'ChartView' })">
        <div class="text-area">
          <span class="tag">투자 정보</span>
          <h3>오늘의 금값은?</h3>
          <p>실시간 국제 시세를 차트로 확인하세요.</p>
        </div>
        <div class="visual-area">📊</div>
      </div>
      
      <div class="feature-card map-card" @click="router.push({ name: 'MapView' })">
        <div class="text-area">
          <span class="tag">위치 기반</span>
          <h3>내 주변 은행 찾기</h3>
          <p>특판 상품이 있는 은행을 지도에서 찾아보세요.</p>
        </div>
        <div class="visual-area">📍</div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { onMounted } from 'vue' // onMounted 추가

onMounted(async () => {
  // 로그인이 되어있고, 닉네임이나 이미지가 없다면 정보를 새로 불러옵니다.
  if (store.isLogin && (!store.nickname || !store.userImage)) {
    try {
      await store.getUserInfo() // 스토어에 유저 정보 요청 함수가 있다고 가정
    } catch (err) {
      console.error('메인화면 유저 정보 로드 실패:', err)
    }
  }
})

const store = useAccountStore()
const router = useRouter()
const searchQuery = ref('')

const goSearch = () => {
  if (searchQuery.value.trim()) {
    // 실제 검색 로직 구현 시 라우터 이동
    // router.push({ name: 'SearchView', query: { q: searchQuery.value } })
    alert(`'${searchQuery.value}' 검색 기능을 준비 중입니다!`)
  }
}

// [추가] 이미지 URL 처리 함수
const getProfileImageUrl = (path) => {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `${store.API_URL}${path}`
}
</script>

<style scoped>
/* 애니메이션 정의 */
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

.animate-fade-in { animation: fadeIn 0.8s ease-out; }
.animate-slide-up { animation: slideUp 0.8s ease-out forwards; opacity: 0; }
.delay-1 { animation-delay: 0.2s; }
.delay-2 { animation-delay: 0.4s; }

/* 전체 레이아웃 */
.home-container {
  max-width: 1200px;
  margin: 40px auto;
  padding: 0 20px 80px; /* 하단 여백 넉넉히 */
}

/* 1. 상단 섹션 */
.top-section {
  display: flex;
  gap: 30px;
  margin-bottom: 50px;
  align-items: stretch;
}

/* 히어로 배너 */
.hero-box {
  flex: 2.2;
  background-color: #F0F4FF;
  border-radius: 24px;
  padding: 50px 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(47, 101, 246, 0.05);
}

.badge {
  color: #2F65F6;
  font-weight: 800;
  font-size: 13px;
  background: #fff;
  padding: 6px 14px;
  border-radius: 20px;
  display: inline-block;
  margin-bottom: 15px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.main-title {
  font-size: 36px;
  line-height: 1.35;
  color: #111;
  margin-bottom: 16px;
  letter-spacing: -0.5px;
}

.main-title strong { color: #2F65F6; }

.sub-text {
  color: #666;
  font-size: 17px;
  margin-bottom: 32px;
  line-height: 1.6;
}

.hero-buttons { display: flex; gap: 12px; }

.cta-btn {
  border: none;
  background-color: #2F65F6;
  color: white;
  padding: 14px 28px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 10px rgba(47, 101, 246, 0.2);
}

.cta-btn.secondary {
  background-color: white;
  color: #2F65F6;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

.cta-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(47, 101, 246, 0.3); }

.floating-icon {
  font-size: 120px;
  animation: float 3s ease-in-out infinite;
}
@keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-15px); } 100% { transform: translateY(0px); } }


/* 로그인 위젯 */
.login-widget {
  flex: 1;
  background-color: #fff;
  border: 1px solid #f1f3f5;
  border-radius: 24px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.03);
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
}

.avatar-circle {
  width: 100px;
  height: 100px;
  background-color: #f8f9fa;
  border-radius: 50%; /* 부모도 원형 */
  margin: 0 auto 15px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 24px;
  overflow: hidden; /* 넘치는 부분 자르기 */
  border: 1px solid #eee;
}

.home-profile-img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 비율 유지하며 꽉 채움 */
  border-radius: 50%; /* 이미지 자체를 둥글게 깎음 */
  display: block; /* 이미지 하단 공백 제거용 */
}

.avatar-circle.active { background-color: #e7f1ff; }

.login-msg { font-size: 16px; color: #333; margin-bottom: 20px; line-height: 1.5; }
.primary-btn { width: 100%; padding: 14px; background-color: #2F65F6; color: white; border: none; border-radius: 12px; font-size: 16px; font-weight: bold; cursor: pointer; transition: background-color 0.2s; }
.primary-btn:hover { background-color: #1c50d8; }
.primary-btn.outline { background-color: white; color: #555; border: 1px solid #ddd; margin-top: auto; }
.primary-btn.outline:hover { background-color: #f8f9fa; border-color: #ccc; }

.login-links { margin-top: 15px; font-size: 13px; color: #888; }
.login-links span { cursor: pointer; }
.login-links span:hover { text-decoration: underline; }
.divider { margin: 0 8px; color: #eee; }

.welcome-text { font-size: 18px; line-height: 1.5; margin-bottom: 20px; color: #333; }
.my-menu { display: flex; gap: 10px; margin-bottom: 20px; }
.menu-btn { flex: 1; padding: 10px; border: 1px solid #eee; border-radius: 8px; background: white; color: #555; cursor: pointer; font-size: 13px; transition: all 0.2s; }
.menu-btn:hover { background: #f8f9fa; border-color: #ddd; }


/* 2. 퀵 메뉴 섹션 */
.section-title { font-size: 20px; font-weight: 800; margin-bottom: 20px; color: #333; }
.quick-menu-section { margin-bottom: 50px; }
.quick-icons { display: flex; justify-content: space-around; background: white; padding: 30px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.03); border: 1px solid #f5f5f5; }
.icon-item { display: flex; flex-direction: column; align-items: center; cursor: pointer; transition: transform 0.2s; }
.icon-item:hover { transform: translateY(-5px); }
.icon-circle { width: 60px; height: 60px; border-radius: 20px; display: flex; justify-content: center; align-items: center; font-size: 28px; margin-bottom: 10px; }
.icon-item span { font-size: 14px; font-weight: 600; color: #444; }

/* 퀵 메뉴 아이콘 배경색 */
.map-bg { background-color: #e3f2fd; }
.chart-bg { background-color: #fff3cd; }
.deposit-bg { background-color: #e8f5e9; }
.board-bg { background-color: #f3e5f5; }


/* 3. 기능 소개 카드 섹션 */
.feature-section { display: flex; gap: 20px; margin-bottom: 50px; }
.feature-card { flex: 1; background: white; padding: 30px; border-radius: 20px; border: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; cursor: pointer; transition: all 0.3s; box-shadow: 0 4px 15px rgba(0,0,0,0.02); }
.feature-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.08); border-color: #2F65F6; }
.text-area .tag { font-size: 12px; font-weight: 800; color: #2F65F6; background: #eef4ff; padding: 4px 8px; border-radius: 4px; display: inline-block; margin-bottom: 10px; }
.text-area h3 { font-size: 20px; font-weight: 800; margin-bottom: 8px; color: #333; }
.text-area p { font-size: 14px; color: #777; margin: 0; }
.visual-area { font-size: 48px; opacity: 0.8; }

/* 모바일 반응형 */
@media (max-width: 900px) {
  .top-section { flex-direction: column; }
  .feature-section { flex-direction: column; }
  .quick-icons { flex-wrap: wrap; gap: 20px; }
}
</style>