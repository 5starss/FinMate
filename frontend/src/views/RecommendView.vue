<template>
  <div class="view-container">
    <div class="header-section">
      <h1 class="page-title">AI 맞춤 자산 관리</h1>
      <p class="subtitle">FinMate 수석 AI가 고객님의 가계부와 자산을 분석합니다.</p>
    </div>

    <div class="content-area">
      
      <div v-if="!loading && !result" class="intro-box">
        <div class="icon-area">🤖</div>
        <h2>나에게 딱 맞는 금융 상품은?</h2>
        <p>나이, 자산, 그리고 <strong>이번 달 소비 패턴</strong>을 분석하여<br>최적의 상품과 투자 전략을 제안해 드립니다.</p>
        <button @click="getRecommendation" class="action-btn">
          무료로 분석 시작하기
        </button>
      </div>

      <div v-else-if="loading" class="loading-box">
        <div class="spinner"></div>
        <h3>고객님의 가계부를 분석하고 있습니다...</h3>
        <p>잠시만 기다려주세요 (약 3~5초 소요)</p>
      </div>

      <div v-else class="result-container">
        <div class="ai-message">
          <span class="ai-badge">FinMate Analysis</span>
          <h2>"{{ userStore.userInfo?.username }}님을 위한 솔루션입니다."</h2>
        </div>

        <div class="recommendation-section">
          <h3 class="section-title">🏆 최적의 추천 상품</h3>
          
          <div v-if="recommendedProduct" class="product-card" @click="goDetail">
            <div class="card-header">
              <span class="bank-name">{{ recommendedProduct.kor_co_nm }}</span>
              <span class="product-type-badge">{{ result.product_type }}</span>
            </div>
            <h2 class="product-name">{{ recommendedProduct.fin_prdt_nm }}</h2>
            
            <div class="rate-info">
              <span class="label">최고 우대 금리</span>
              <span class="value">{{ maxRate }}%</span>
            </div>
            
            <div class="arrow-icon">➜ 상품 상세 보기</div>
          </div>
          <div v-else class="error-msg">추천 상품 정보를 불러올 수 없습니다.</div>

          <div class="reason-box">
            <h4>💡 왜 이 상품인가요?</h4>
            <p>{{ result.recommendation_reason }}</p>
          </div>
        </div>

        <div class="advice-section">
          <div class="advice-card">
            <h3 class="card-title">📊 가계부 기반 재무 조언</h3>
            <p class="advice-text">{{ result.financial_advice }}</p>
          </div>

          <div class="advice-card highlight">
            <h3 class="card-title">🚀 추가 투자 제안 (Portfolio)</h3>
            <p class="advice-text">{{ result.additional_category }}</p>
          </div>
        </div>

        <button @click="getRecommendation" class="retry-btn">
          다시 분석하기
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts' // 스토어 경로 확인 필요
import axios from 'axios'

const store = useAccountStore()
const userStore = useAccountStore() // 유저 정보용
const router = useRouter()

const loading = ref(false)
const result = ref(null)            // LLM 응답 데이터 (JSON)
const recommendedProduct = ref(null) // DB에서 가져온 실제 상품 데이터

// 최고 금리 계산 (옵션 중 가장 높은 것)
const maxRate = computed(() => {
  if (!recommendedProduct.value?.options) return '-'
  const rates = recommendedProduct.value.options.map(o => o.intr_rate2)
  return Math.max(...rates)
})

// 분석 요청 함수
const getRecommendation = async () => {
  loading.value = true
  result.value = null
  recommendedProduct.value = null

  try {
    // 1. Django 백엔드에 LLM 분석 요청
    const res = await axios.post(`${store.API_URL}/products/recommend/`, {}, {
      headers: { Authorization: `Token ${store.token}` }
    })
    
    // 2. 결과 저장
    result.value = res.data

    // 3. 추천된 상품의 상세 정보 가져오기 (DB 조회)
    // result.value.recommended_product_id 와 product_type을 사용
    const productId = result.value.recommended_product_id
    
    // 예금인지 적금인지에 따라 URL 분기
    // (store나 API 구조에 따라 URL은 수정이 필요할 수 있습니다)
    let productUrl = ''
    if (result.value.product_type.includes('예금')) {
      productUrl = `${store.API_URL}/products/deposit-products/${productId}/`
    } else {
      productUrl = `${store.API_URL}/products/saving-products/${productId}/`
    }

    const productRes = await axios.get(productUrl)
    recommendedProduct.value = productRes.data

  } catch (err) {
    console.error(err)
    alert('분석 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.')
  } finally {
    loading.value = false
  }
}

// 상품 상세 페이지로 이동
const goDetail = () => {
  if (!recommendedProduct.value) return
  const id = recommendedProduct.value.id
  // 타입에 따라 라우팅 분기
  if (result.value.product_type.includes('예금')) {
    router.push({ name: 'DepositDetail', params: { id } })
  } else {
    router.push({ name: 'SavingDetail', params: { id } })
  }
}
</script>

<style scoped>
.view-container {
  max-width: 800px; /* 리포트 형식이므로 폭을 조금 좁혀서 집중도 높임 */
  margin: 50px auto;
  padding: 0 20px;
  min-height: 800px;
}

.header-section { text-align: center; margin-bottom: 40px; }
.page-title { font-size: 2rem; font-weight: 800; color: #333; margin-bottom: 10px; }
.subtitle { color: #666; font-size: 1.1rem; }

/* 1. 인트로 박스 */
.intro-box {
  background: white; padding: 60px 20px; border-radius: 30px;
  text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  border: 1px solid #f0f0f0;
}
.icon-area { font-size: 4rem; margin-bottom: 20px; }
.intro-box h2 { font-size: 1.8rem; font-weight: 800; color: #333; margin-bottom: 15px; }
.intro-box p { color: #666; line-height: 1.6; margin-bottom: 30px; }

.action-btn {
  background: #2F65F6; color: white; padding: 15px 40px;
  font-size: 1.2rem; font-weight: 700; border-radius: 50px;
  border: none; cursor: pointer; transition: all 0.2s;
}
.action-btn:hover { background: #1c50d8; transform: translateY(-3px); box-shadow: 0 5px 15px rgba(47, 101, 246, 0.3); }

/* 2. 로딩 박스 */
.loading-box { text-align: center; padding: 60px 0; }
.spinner {
  width: 50px; height: 50px; border: 5px solid #f3f3f3;
  border-top: 5px solid #2F65F6; border-radius: 50%;
  animation: spin 1s linear infinite; margin: 0 auto 30px;
}
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
.loading-box h3 { font-size: 1.5rem; color: #333; margin-bottom: 10px; }
.loading-box p { color: #888; }

/* 3. 결과 컨테이너 */
.result-container { animation: fadeIn 0.5s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

.ai-message { text-align: center; margin-bottom: 40px; }
.ai-badge { background: #eef4ff; color: #2F65F6; font-weight: 700; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem; margin-bottom: 10px; display: inline-block; }
.ai-message h2 { font-size: 1.6rem; font-weight: 800; color: #333; }

/* 추천 섹션 */
.recommendation-section { margin-bottom: 40px; }
.section-title { font-size: 1.3rem; font-weight: 800; color: #333; margin-bottom: 20px; }

/* 상품 카드 */
.product-card {
  background: white; border: 2px solid #2F65F6; border-radius: 20px;
  padding: 30px; cursor: pointer; transition: transform 0.2s;
  box-shadow: 0 10px 25px rgba(47, 101, 246, 0.1);
  position: relative; overflow: hidden;
}
.product-card:hover { transform: translateY(-5px); }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.bank-name { font-weight: 700; color: #666; }
.product-type-badge { background: #2F65F6; color: white; padding: 4px 10px; border-radius: 10px; font-size: 0.8rem; font-weight: 700; }
.product-name { font-size: 1.8rem; font-weight: 800; color: #333; margin-bottom: 20px; }
.rate-info { display: flex; align-items: baseline; gap: 10px; }
.rate-info .label { color: #666; font-weight: 600; }
.rate-info .value { color: #2F65F6; font-size: 2rem; font-weight: 900; }
.arrow-icon { margin-top: 20px; text-align: right; color: #2F65F6; font-weight: 700; }

.reason-box {
  background: #f8fbff; padding: 20px; border-radius: 15px; margin-top: 20px;
  border-left: 5px solid #2F65F6;
}
.reason-box h4 { margin: 0 0 10px; color: #2F65F6; font-size: 1.1rem; }
.reason-box p { margin: 0; color: #555; line-height: 1.6; }

/* 조언 섹션 */
.advice-section { display: grid; gap: 20px; margin-bottom: 40px; }
.advice-card { background: white; padding: 25px; border-radius: 20px; border: 1px solid #eee; box-shadow: 0 5px 15px rgba(0,0,0,0.03); }
.advice-card h3 { font-size: 1.2rem; font-weight: 800; margin-bottom: 15px; color: #333; }
.advice-text { color: #555; line-height: 1.7; white-space: pre-line; } /* 줄바꿈 반영 */

.advice-card.highlight { background: #fff8e1; border-color: #ffe082; } /* 노란색 포인트 */
.advice-card.highlight h3 { color: #f57f17; }

.retry-btn {
  display: block; width: 100%; padding: 15px; background: #f1f3f5; color: #666;
  border: none; border-radius: 15px; font-weight: 700; cursor: pointer; transition: 0.2s;
}
.retry-btn:hover { background: #e9ecef; color: #333; }
</style>