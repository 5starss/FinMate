<template>
  <div v-if="product" class="container mt-4">
    <h1>{{ product.kor_co_nm }} - {{ product.fin_prdt_nm }}</h1>
    <hr>

    <div class="selection-box p-3 bg-light rounded shadow-sm mb-4">
      <h4 class="mb-3">가입 기간을 선택하세요</h4>
      <div v-if="!product.is_joined">
        <div v-for="opt in uniqueOptions" :key="opt.id" class="form-check mb-2">
          <input 
            class="form-check-input" 
            type="radio" 
            :id="'opt-' + opt.id" 
            :value="opt.id" 
            v-model="selectedOptionId"
          >
          <label class="form-check-label" :for="'opt-' + opt.id">
            <strong>{{ opt.save_trm }}개월</strong> 
            (기본 금리: {{ opt.intr_rate }}% | 최고 우대: {{ opt.intr_rate2 }}%)
          </label>
        </div>
      </div>
      <div v-else class="text-primary fw-bold">
        이미 가입 완료된 상품입니다. 마이페이지에서 상세 정보를 확인하세요!
      </div>
    </div>

    <div class="my-3">
      <div v-if="isLoggedIn">
        <button 
          @click="clickSubscribe" 
          :disabled="product.is_joined || !selectedOptionId"
          :class="product.is_joined ? 'btn btn-secondary' : 'btn btn-primary btn-lg'"
        >
          {{ product.is_joined ? '가입 완료' : '선택한 조건으로 가입하기' }}
        </button>
        <p v-if="!selectedOptionId && !product.is_joined" class="text-muted mt-2 small">
          * 기간을 선택해야 가입 버튼이 활성화됩니다.
        </p>
      </div>
      <div v-else class="alert alert-warning">
        가입하시려면 <router-link :to="{ name: 'LogInView' }">로그인</router-link>이 필요합니다.
      </div>
    </div>

    <hr>
    <div class="mt-4">
      <h5>상세 안내 및 우대 조건</h5>
      <div class="card p-3 shadow-sm border-0 bg-white">
        <p><strong>가입 방법:</strong> {{ product.join_way }}</p>
        <p><strong>우대 조건:</strong> {{ product.spcl_cnd }}</p>
        <p class="mb-0 text-muted"><small>* 상세 우대 조건은 해당 은행 지점 또는 홈페이지를 참고하세요.</small></p>
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
const selectedOptionId = ref(null) // 사용자가 선택한 라디오 버튼 ID
const isLoggedIn = computed(() => accountStore.isLogin)

onMounted(async () => {
  const res = await store.getDepositDetail(route.params.id)
  product.value = res.data
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
  if (confirm('가입 후에는 기간 변경이 어려울 수 있습니다. 가입하시겠습니까?')) {
    try {
      const payload = {
        product_id: product.value.id,
        option_id: selectedOptionId.value // 선택된 옵션 ID 전송
      }
      await store.subscribeDeposit(payload, accountStore.token)
      alert('가입이 성공적으로 완료되었습니다!')
      product.value.is_joined = true
    } catch (err) {
      alert(err.response?.data?.message || '이미 가입했거나 오류가 발생했습니다.')
    }
  }
}
</script>

<style scoped>
.selection-box { border-left: 5px solid #0d6efd; }
.btn-lg { padding: 12px 30px; font-weight: bold; }
</style>