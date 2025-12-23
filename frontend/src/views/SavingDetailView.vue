<template>
  <div v-if="product" class="container mt-4">
    <h1 class="text-success">{{ product.kor_co_nm }} - {{ product.fin_prdt_nm }} (적금)</h1>
    <hr>

    <div class="selection-box p-3 bg-light rounded shadow-sm mb-4">
      <h4 class="mb-3 text-dark">저축 기간을 선택하세요</h4>
      <div v-if="!product.is_joined">
        <div v-for="opt in uniqueOptions" :key="opt.id" class="form-check mb-3 p-2 border rounded-3 bg-white hover-shadow">
          <input 
            class="form-check-input ms-1" 
            type="radio" 
            :id="'saving-opt-' + opt.id" 
            :value="opt.id" 
            v-model="selectedOptionId"
          >
          <label class="form-check-label ms-2" :for="'saving-opt-' + opt.id">
            <span class="badge bg-success me-2">{{ opt.save_trm }}개월</span>
            <strong>기본 {{ opt.intr_rate }}%</strong> 
            <span class="text-muted mx-1">|</span> 
            <span class="text-danger">최고 {{ opt.intr_rate2 }}%</span>
          </label>
        </div>
      </div>
      <div v-else class="alert alert-success d-flex align-items-center mb-0">
        <i class="bi bi-check-circle-fill me-2"></i>
        <div>이미 가입 완료된 적금입니다. 마이페이지에서 상세 내역을 확인하세요.</div>
      </div>
    </div>

    <div class="my-3">
      <div v-if="isLoggedIn">
        <button 
          @click="clickSubscribe" 
          :disabled="product.is_joined || !selectedOptionId"
          :class="product.is_joined ? 'btn btn-secondary' : 'btn btn-success btn-lg w-100 w-md-auto'"
        >
          {{ product.is_joined ? '이미 가입된 상품' : '선택한 기간으로 적금 가입하기' }}
        </button>
        <p v-if="!selectedOptionId && !product.is_joined" class="text-muted mt-2 small">
          * 원하시는 저축 기간을 선택해 주세요.
        </p>
      </div>
      <div v-else class="alert alert-light border">
        적금에 가입하시려면 <router-link :to="{ name: 'LogInView' }">로그인</router-link>이 필요합니다.
      </div>
    </div>

    <hr>
    
    <div class="mt-4">
      <h5 class="fw-bold mb-3">상품 상세 및 우대 조건</h5>
      <div class="card p-4 shadow-sm border-0 bg-white">
        <div class="row">
          <div class="col-md-6 mb-3">
            <p class="mb-1 text-muted">가입 방법</p>
            <p class="fw-bold">{{ product.join_way }}</p>
          </div>
          <div class="col-md-6 mb-3">
            <p class="mb-1 text-muted">중도해지 이율</p>
            <p class="fw-bold">{{ product.mtrt_int || '홈페이지 참조' }}</p>
          </div>
        </div>
        <div class="mt-2">
          <p class="mb-1 text-muted">우대 조건 (상세)</p>
          <div class="p-3 bg-light rounded text-break" style="white-space: pre-line;">
            {{ product.spcl_cnd }}
          </div>
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
const isLoggedIn = computed(() => accountStore.isLogin)

onMounted(async () => {
  try {
    const res = await store.getSavingDetail(route.params.id)
    product.value = res.data
  } catch (err) {
    console.error('적금 상세 정보 로드 실패:', err)
  }
})

// 기간별 최고금리 옵션 필터링 로직 (기존 유지)
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

// 가입 처리
const clickSubscribe = async () => {
  if (confirm(`[${product.value.fin_prdt_nm}] 적금에 가입하시겠습니까?`)) {
    try {
      const payload = {
        product_id: product.value.id,
        option_id: selectedOptionId.value // 선택된 옵션 ID 전송
      }
      await store.subscribeSaving(payload, accountStore.token)
      alert('적금 가입이 완료되었습니다! 마이페이지에서 확인해보세요.')
      product.value.is_joined = true
    } catch (err) {
      alert(err.response?.data?.message || '가입 중 오류가 발생했습니다.')
    }
  }
}
</script>

<style scoped>
.selection-box { border-left: 5px solid #198754; }
.hover-shadow:hover { box-shadow: 0 4px 8px rgba(0,0,0,0.1); transition: 0.3s; }
.btn-lg { padding: 12px 30px; font-weight: bold; }
</style>