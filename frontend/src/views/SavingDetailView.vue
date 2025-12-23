<template>
  <div v-if="product" class="container mt-4">
    <h1>{{ product.kor_co_nm }} - {{ product.fin_prdt_nm }} (적금)</h1>

    <div class="my-3">
      <div v-if="isLoggedIn">
        <button 
          @click="clickSubscribe" 
          :disabled="product.is_joined"
          :class="product.is_joined ? 'btn btn-secondary' : 'btn btn-success'"
        >
          {{ product.is_joined ? '이미 가입된 상품입니다' : '적금 가입하기' }}
        </button>
      </div>
      <div v-else class="alert alert-light border">
        가입하시려면 <router-link :to="{ name: 'LogInView' }">로그인</router-link>이 필요합니다.
      </div>
    </div>

    <hr>
    
    <h3>금리 정보</h3>
    <div class="card p-3 mb-4 bg-light">
      <ul class="mb-0">
        <li v-for="opt in uniqueOptions" :key="opt.id">
          <strong>{{ opt.save_trm }}개월</strong> 저축 시: 
          <span class="text-primary">{{ opt.intr_rate }}%</span> ~ 
          <span class="text-danger">{{ opt.intr_rate2 }}% (최고)</span>
        </li>
      </ul>
    </div>

    <div class="mt-4">
      <h5>상세 정보</h5>
      <p><strong>가입 방법:</strong> {{ product.join_way }}</p>
      <p><strong>우대 조건:</strong> {{ product.spcl_cnd }}</p>
      <p><strong>기타 메모:</strong> {{ product.etc_note }}</p>
    </div>
  </div>
  <div v-else class="text-center mt-5">
    <p>적금 정보를 불러오고 있습니다...</p>
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
const isLoggedIn = computed(() => accountStore.isLogin)

onMounted(async () => {
  try {
    const res = await store.getSavingDetail(route.params.id)
    product.data = res.data // 여기서 product.value가 아니라 res.data 자체를 할당
    product.value = res.data
  } catch (err) {
    console.error('적금 상세 조회 실패:', err)
  }
})

/**
 * ✅ 기존 로직: 같은 개월수 중 최고금리가 가장 높은 옵션만 추출
 */
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

/**
 * ✅ 가입하기 함수
 */
const clickSubscribe = async () => {
  if (confirm(`[${product.value.fin_prdt_nm}] 적금에 가입하시겠습니까?`)) {
    try {
      // 스토어에 구현된 subscribeSaving 호출
      await store.subscribeSaving(product.value.id, accountStore.token)
      alert('적금 가입이 성공적으로 완료되었습니다!')
      product.value.is_joined = true // 버튼 상태 즉시 업데이트
    } catch (err) {
      alert(err.response?.data?.message || '가입 중 오류가 발생했습니다.')
    }
  }
}
</script>

<style scoped>
.container { max-width: 900px; }
.btn-success { background-color: #28a745; color: white; padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }
.btn-secondary { background-color: #6c757d; color: white; padding: 12px 24px; border: none; border-radius: 6px; cursor: not-allowed; }
.text-danger { font-weight: bold; }
</style>