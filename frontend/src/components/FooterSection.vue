<template>
  <footer class="footer-wrapper">
    <div class="inner-container">
      
      <div class="footer-left">
        <h2 class="footer-logo">FinMate</h2>
        <p class="desc">
          금융 상품 비교부터 자산 관리까지,<br>
          FinMate가 당신의 부자 되는 길을 함께합니다.
        </p>
      </div>

      <div class="footer-right">
        <div class="company-info">
          <p>
            (주)핀메이트 | 대표: 싸피 | 사업자등록번호: 123-45-67890<br>
            서울특별시 강남구 테헤란로 212<br>
            <span class="copyright">© 2025 FinMate Corp. All rights reserved.</span>
          </p>
        </div>
      </div>

    </div>
  </footer>
</template>

<style scoped>
.footer-wrapper {
  background-color: #f8f9fa;
  border-top: 1px solid #eee;
  padding-bottom: 30px;
  margin-top: auto;
  color: #666;
}

.inner-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 10px 0;
  padding-left: 20px;
  
  display: flex;
  justify-content: flex-start; 
  /* 아래쪽(flex-end) 기준으로 정렬 */
  align-items: flex-end; 
  
  gap: 100px; 
}

/* 왼쪽 영역 */
.footer-left {
  flex-shrink: 0;
}

.footer-logo {
  font-size: 24px;
  font-weight: 800;
  color: #ccc;
  margin-bottom: 10px;
}

.desc {
  font-size: 14px;
  line-height: 1.6;
  color: #888;
  margin: 0;
}

/* 오른쪽 영역 */
.footer-right {
  text-align: left;
}

.company-info p {
  font-size: 12px;
  color: #999;
  line-height: 1.8;
  margin: 0;
}

.copyright {
  display: block;
  margin-top: 5px;
  font-weight: 600;
  color: #bbb;
}

/* 반응형: 화면이 좁아지면 다시 왼쪽 정렬로 복귀 */
@media (max-width: 768px) {
  .inner-container {
    flex-direction: column;
    align-items: flex-start; /* 모바일에서는 다시 왼쪽(위쪽) 정렬 */
    gap: 30px;
  }
}
</style>