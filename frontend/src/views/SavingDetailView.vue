<template>
  <div v-if="product" class="detail-container">
    <div class="header-section">
      <div class="product-badge saving">적금 상품</div>
      <h1 class="product-title">{{ product.fin_prdt_nm }}</h1>
      <p class="bank-name">{{ product.kor_co_nm }}</p>
    </div>

    <div class="main-card">
      <h4 class="card-title">📅 저축 기간을 선택하세요</h4>
      
      <div v-if="!product.is_joined">
        <div class="option-grid">
          <div 
            v-for="opt in uniqueOptions" 
            :key="opt.id" 
            class="option-card saving-card"
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
          <label class="input-label">월 납입 금액</label>
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
      
      <div v-else class="joined-alert saving">
        ✅ 이미 가입한 상품입니다.
      </div>

      <div class="btn-area">
        <button 
          v-if="isLoggedIn"
          @click="clickSubscribe" 
          :disabled="product.is_joined || !selectedOptionId || !amount"
          class="submit-btn saving-btn"
        >
          {{ product.is_joined ? '가입 완료' : '적금 가입하기' }}
        </button>
        <div v-else class="login-msg">
          <router-link :to="{ name: 'LogInView' }" class="saving-link">로그인</router-link>이 필요합니다.
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
import { useSavingStore } from '@/stores/savings'
import { useAccountStore } from '@/stores/accounts'

const route = useRoute()
const store = useSavingStore()
const accountStore = useAccountStore()

const product = ref(null)
const selectedOptionId = ref(null)
const amount = ref(null)
const isLoggedIn = computed(() => accountStore.isLogin)

onMounted(async () => {
  try {
    const res = await store.getSavingDetail(route.params.id)
    product.value = res.data
  } catch (err) {
    console.error(err)
  }
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
      await store.subscribeSaving(payload, accountStore.token)
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

.header-section { text-align: center; margin-bottom: 40px; }
.product-badge {
  display: inline-block;
  background-color: rgba(47, 101, 246, 0.1); color: #2F65F6;
  font-weight: 800; padding: 6px 15px; border-radius: 30px; margin-bottom: 15px; font-size: 14px;
}
.product-badge.saving { background-color: #e8f5e9; color: #198754; }
.product-title { font-size: 2.2rem; font-weight: 800; color: #333; margin-bottom: 10px; word-break: keep-all; }
.bank-name { font-size: 1.2rem; color: #777; }

.main-card {
  background: white; padding: 50px; border-radius: 30px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.08); margin-bottom: 40px;
}
.card-title { text-align: center; font-weight: 800; margin-bottom: 30px; color: #333; }

/* [수정 1] 옵션 그리드: Flex & 고정 크기 */
.option-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

/* [수정 2] 옵션 카드: 정사각형 고정 */
.option-card {
  width: 170px;
  height: 170px;
  flex-shrink: 0;
  
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

.option-card.saving-card:hover {
  border-color: #198754; transform: translateY(-5px); box-shadow: 0 8px 20px rgba(25, 135, 84, 0.15);
}
.option-card.saving-card.active {
  border-color: #198754; background-color: #e8f5e9; box-shadow: 0 0 0 2px #198754 inset;
}

.term-badge {
  display: inline-block; font-size: 1.4rem; font-weight: 800; color: #333;
  margin-bottom: 12px;
}
.option-card.saving-card.active .term-badge { color: #198754; }

/* [수정 3] 세로선 진하게 */
.rate-container { 
  display: flex; 
  justify-content: center; 
  align-items: center; 
  gap: 12px; 
  width: 100%;
}
.vertical-divider { 
  width: 1.5px;
  height: 30px; 
  background: #d1d5db; /* 진한 회색 */
  flex-shrink: 0;
}
.rate-item { display: flex; flex-direction: column; align-items: center; }
.rate-label { font-size: 13px; color: #888; margin-bottom: 4px; font-weight: 500; }
.rate-value { font-size: 16px; font-weight: 600; color: #666; }
.rate-item.highlight .rate-label { color: #198754; }
.rate-item.highlight .rate-value.big { font-size: 20px; font-weight: 800; color: #198754; line-height: 1; }

.amount-box { margin-top: 40px; background: #f8f9fa; padding: 25px; border-radius: 20px; }
.input-label { display: block; font-weight: 700; color: #555; margin-bottom: 10px; }
.custom-input-group { display: flex; align-items: center; background: white; border: 1px solid #ddd; border-radius: 12px; padding: 0 20px; overflow: hidden; }
.custom-input-group:focus-within { border-color: #198754; box-shadow: 0 0 0 3px rgba(25, 135, 84, 0.1); }
.custom-input-group input { border: none; outline: none; flex-grow: 1; padding: 15px 0; font-size: 18px; font-weight: 700; color: #333; }
.unit { font-weight: 700; color: #888; margin-left: 10px; }

.btn-area { margin-top: 30px; }
.submit-btn { width: 100%; padding: 18px; border-radius: 16px; border: none; background: #198754; color: white; font-size: 18px; font-weight: 800; cursor: pointer; transition: background 0.2s; }
.submit-btn.saving-btn:hover { background: #146c43; }
.submit-btn:disabled { background: #ccc; cursor: not-allowed; }
.joined-alert.saving { text-align: center; background: #e8f5e9; color: #198754; padding: 20px; border-radius: 16px; font-weight: 700; margin: 20px 0; }
.login-msg { text-align: center; color: #666; font-weight: 600; }
.saving-link { color: #198754; text-decoration: none; }

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