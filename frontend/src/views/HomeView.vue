<template>
  <div class="home-wrapper">
    <main class="main-content">
      <section class="hero-section">
        <div class="hero-text">
          <span class="badge">FinMate 리포트</span>
          <h1>똑똑한 금융 생활의 시작<br><strong>내게 딱 맞는 예적금 찾기</strong></h1>
          <p>수많은 금융 상품 중 나에게 최고의 혜택을 주는 상품을 분석해 드립니다.</p>
        </div>
      </section>

      <aside class="side-widget">
        <div class="login-card">
          <div class="avatar-placeholder"></div>
          <p>로그인 후<br>나만의 맞춤 정보를 이용하세요.</p>
          <button class="primary-btn">로그인</button>
        </div>
        
        <div class="info-card">
          <span class="tag">HOT</span>
          <p>이번 달 인기 적금 상품 TOP 5</p>
        </div>
      </aside>
    </main>

    <section class="search-bar-section">
      <div class="search-container">
        <input type="text" placeholder="상품명, 은행명을 검색해보세요" />
        <button class="search-btn">🔍</button>
      </div>
      <div class="hashtags">
        <span>#신한은행</span> <span>#청년도약계좌</span> <span>#최고금리</span>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* 색상 변수 */
:root {
  --primary-blue: #2F65F6;
  --bg-gray: #F8F9FA;
}

.home-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px; /* 양옆 여백 */
}

/* 1. 헤더 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
}
.logo { font-size: 24px; font-weight: bold; color: var(--primary-blue, #2F65F6); }
.nav-links a { margin: 0 15px; text-decoration: none; color: #333; font-weight: 500; }
.login-btn { border: none; background: none; font-weight: bold; cursor: pointer; }

/* 2. 메인 콘텐츠 레이아웃 */
.main-content {
  display: flex;
  gap: 30px;
  margin-top: 40px;
  align-items: flex-start; /* 높이 맞춤 방지 */
}

/* 왼쪽 히어로 섹션 */
.hero-section {
  flex: 2; /* 2:1 비율 */
  background-color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.hero-text h1 { font-size: 32px; line-height: 1.4; margin: 20px 0; }
.badge { color: var(--primary-blue, #2F65F6); font-weight: bold; }
.cta-link { color: #666; text-decoration: none; font-size: 14px; }
.illustration { width: 200px; height: auto; } /* 이미지 없을 시 크기 조절 필요 */

/* 오른쪽 사이드 위젯 */
.side-widget {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.login-card {
  background: #fff;
  border: 1px solid #eee;
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.primary-btn {
  width: 100%;
  padding: 12px;
  background-color: #2F65F6; /* 레퍼런스 블루 */
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 15px;
}
.info-card {
  background: #EFF6FF; /* 아주 연한 블루 */
  padding: 20px;
  border-radius: 20px;
}

/* 3. 하단 검색바 (파란 배경) */
.search-bar-section {
  margin-top: 60px;
  background-color: #2F65F6;
  border-radius: 20px;
  padding: 40px;
  text-align: center;
  color: white;
}
.search-container {
  display: flex;
  justify-content: center;
  gap: 10px;
  max-width: 600px;
  margin: 0 auto;
  position: relative;
}
.search-container input {
  width: 100%;
  padding: 15px 20px;
  border-radius: 30px;
  border: none;
  font-size: 16px;
  outline: none;
}
.search-btn {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}
.hashtags {
  margin-top: 15px;
  font-size: 14px;
  opacity: 0.9;
}
.hashtags span { margin: 0 5px; }
</style>