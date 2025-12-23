<template>
  <div v-if="product" class="detail-container">
    <div class="header-section">
      <div class="product-badge">예금 상품</div>
      <h1 class="product-title">{{ product.fin_prdt_nm }}</h1>
      <p class="bank-name">{{ product.kor_co_nm }}</p>
    </div>

    <div class="main-card">
      <h4 class="card-title">💰 가입 기간을 선택하세요</h4>
      
      <div v-if="!product.is_joined">
        <div class="option-grid">
          <div 
            v-for="opt in uniqueOptions" 
            :key="opt.id" 
            class="option-card"
            :class="{ active: selectedOptionId === opt.id }"
            @click="selectedOptionId = opt.id"
          >
            <div class="term-badge">{{ opt.save_trm }}개월</div>
            
            <div class="rate-container">
              <div class="rate-item">
                <span class="rate-label">기본</span>
                <span class="rate-value">{{ opt.intr_rate }}%</span>
              </div>
              <div class="vertical-divider"></div>
              <div class="rate-item highlight">
                <span class="rate-label">최고</span>
                <span class="rate-value big">{{ opt.intr_rate2 }}%</span>
              </div>
            </div>
          </div>
        </div>

        <div class="amount-box">
          <label class="input-label">예치 금액</label>
          <div class="custom-input-group">
            <input 
              type="number" 
              v-model="amount" 
              placeholder="금액 입력"
            >
            <span class="unit">원</span>
          </div>
        </div>
      </div>
      
      <div v-else class="joined-alert">
        ✅ 이미 가입한 상품입니다.
      </div>

      <div class="btn-area">
        <button 
          v-if="isLoggedIn"
          @click="clickSubscribe" 
          :disabled="product.is_joined || !selectedOptionId || !amount"
          class="submit-btn"
        >
          {{ product.is_joined ? '가입 완료' : '가입하기' }}
        </button>
        <div v-else class="login-msg">
          <router-link :to="{ name: 'LogInView' }">로그인</router-link>이 필요합니다.
        </div>
      </div>
    </div>

    <div class="info-card">
      <h5 class="info-title">📌 상품 상세 안내</h5>
      <div class="info-list">
        <div class="info-item">
          <span class="label">가입 방법</span>
          <span class="value">{{ product.join_way }}</span>
        </div>
        <div class="info-item">
          <span class="label">우대 조건</span>
          <span class="value">{{ product.spcl_cnd }}</span>
        </div>
        <div class="info-item">
          <span class="label">만기 이율</span>
          <span class="value">{{ product.mtrt_int || '은행 문의' }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useDepositStore } from '@/stores/deposits'
import { useAccountStore } from '@/stores/accounts'

const route = useRoute()
const store = useDepositStore()
const accountStore = useAccountStore()

const product = ref(null)
const selectedOptionId = ref(null)
const amount = ref(null)
const isLoggedIn = computed(() => accountStore.isLogin)

onMounted(async () => {
  const res = await store.getDepositDetail(route.params.id)
  product.value = res.data
})

const uniqueOptions = computed(() => {
  if (!product.value?.options) return []
  const bestByTerm = new Map()
  for (const opt of product.value.options) {
    const term = Number(opt.save_trm)
    const prev = bestByTerm.get(term)
    if (!prev || Number(opt.intr_rate2) > Number(prev.intr_rate2)) {
      bestByTerm.set(term, opt)
    }
  }
  return [...bestByTerm.values()].sort((a, b) => Number(a.save_trm) - Number(b.save_trm))
})

const clickSubscribe = async () => {
  if (confirm('가입하시겠습니까?')) {
    try {
      const payload = {
        product_id: product.value.id,
        option_id: selectedOptionId.value,
        amount: amount.value 
      }
      await store.subscribeDeposit(payload, accountStore.token)
      alert('가입이 완료되었습니다!')
      product.value.is_joined = true
    } catch (err) {
      alert(err.response?.data?.message || '오류가 발생했습니다.')
    }
  }
}
</script>

<style scoped>
.detail-container {
  max-width: 840px; 
  margin: 60px auto; 
  padding: 0 20px;
}

/* 헤더 */
.header-section { text-align: center; margin-bottom: 40px; }
.product-badge {
  display: inline-block;
  background-color: rgba(47, 101, 246, 0.1); color: #2F65F6;
  font-weight: 800; padding: 6px 15px; border-radius: 30px; margin-bottom: 15px; font-size: 14px;
}
.product-title { font-size: 2.2rem; font-weight: 800; color: #333; margin-bottom: 10px; word-break: keep-all; }
.bank-name { font-size: 1.2rem; color: #777; }

/* 메인 카드 */
.main-card {
  background: white; padding: 50px; border-radius: 30px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.08); margin-bottom: 40px;
}
.card-title { text-align: center; font-weight: 800; margin-bottom: 30px; color: #333; }

/* [수정 1] 옵션 그리드: 크기 강제 고정 */
.option-grid {
  display: flex;           /* Grid 대신 Flex 사용 (고정 크기 배치에 유리) */
  flex-wrap: wrap;         /* 줄바꿈 허용 */
  gap: 20px;               /* 카드 사이 간격 */
  justify-content: center; /* 전체 중앙 정렬 */
}

/* [수정 2] 옵션 카드: 정사각형 고정 */
.option-card {
  width: 170px;      /* 너비 고정 */
  height: 170px;     /* 높이 고정 (정사각형) */
  flex-shrink: 0;    /* 화면 줄어도 찌그러지지 않게 설정 */
  
  border: 2px solid #f0f2f5; 
  border-radius: 20px; 
  padding: 20px;
  text-align: center; 
  cursor: pointer; 
  transition: all 0.2s ease; 
  background: #fff;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.option-card:hover { border-color: #2F65F6; transform: translateY(-5px); box-shadow: 0 8px 20px rgba(47, 101, 246, 0.15); }
.option-card.active { border-color: #2F65F6; background-color: #f5f9ff; box-shadow: 0 0 0 2px #2F65F6 inset; }

.term-badge {
  display: inline-block; font-size: 1.4rem; font-weight: 800; color: #333;
  margin-bottom: 12px;
}
.option-card.active .term-badge { color: #2F65F6; }

/* [수정 3] 세로선 및 금리 배치 */
.rate-container { 
  display: flex; 
  justify-content: center; 
  align-items: center; 
  gap: 12px; 
  width: 100%;
}

.vertical-divider { 
  width: 1.5px;         /* 선 두께 약간 증가 */
  height: 30px;         /* 선 높이 */
  background: #d1d5db;  /* [핵심] 진한 회색으로 변경 (안 보임 방지) */
  flex-shrink: 0;       /* 찌그러짐 방지 */
}

.rate-item { display: flex; flex-direction: column; align-items: center; }
.rate-label { font-size: 13px; color: #888; margin-bottom: 4px; font-weight: 500; }
.rate-value { font-size: 16px; font-weight: 600; color: #555; }
.rate-item.highlight .rate-label { color: #2F65F6; }
.rate-item.highlight .rate-value.big { font-size: 20px; font-weight: 800; color: #2F65F6; line-height: 1; }

/* 나머지 스타일 유지 */
.amount-box { margin-top: 40px; background: #f8f9fa; padding: 25px; border-radius: 20px; }
.input-label { display: block; font-weight: 700; color: #555; margin-bottom: 10px; }
.custom-input-group { display: flex; align-items: center; background: white; border: 1px solid #ddd; border-radius: 12px; padding: 0 20px; overflow: hidden; }
.custom-input-group:focus-within { border-color: #2F65F6; box-shadow: 0 0 0 3px rgba(47, 101, 246, 0.1); }
.custom-input-group input { border: none; outline: none; flex-grow: 1; padding: 15px 0; font-size: 18px; font-weight: 700; color: #333; }
.unit { font-weight: 700; color: #888; margin-left: 10px; }

.btn-area { margin-top: 30px; }
.submit-btn { width: 100%; padding: 18px; border-radius: 16px; border: none; background: #2F65F6; color: white; font-size: 18px; font-weight: 800; cursor: pointer; transition: background 0.2s; }
.submit-btn:hover { background: #1c50d8; }
.submit-btn:disabled { background: #ccc; cursor: not-allowed; }
.joined-alert { text-align: center; background: #eef4ff; color: #2F65F6; padding: 20px; border-radius: 16px; font-weight: 700; margin: 20px 0; }
.login-msg { text-align: center; color: #666; font-weight: 600; }
.login-msg a { color: #2F65F6; text-decoration: none; }

.info-card { background: #f9fafb; padding: 40px; border-radius: 30px; }
.info-title { font-size: 18px; font-weight: 800; margin-bottom: 20px; color: #333; }
.info-list { display: flex; flex-direction: column; gap: 15px; }
.info-item { display: flex; gap: 30px; }
.info-item .label { width: 80px; font-weight: 700; color: #666; flex-shrink: 0; }
.info-item .value { color: #333; line-height: 1.6; }

@media (max-width: 600px) {
  .detail-container { margin: 30px auto; }
  .main-card { padding: 25px; }
  .product-title { font-size: 1.8rem; }
  .info-item { flex-direction: column; gap: 5px; }
}
</style>