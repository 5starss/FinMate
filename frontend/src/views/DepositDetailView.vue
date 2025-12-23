<template>
  <div v-if="product" class="container mt-4">
    <h1>{{ product.kor_co_nm }} - {{ product.fin_prdt_nm }}</h1>

    <div class="my-3">
      <div v-if="isLoggedIn">
        <button 
          @click="clickSubscribe" 
          :disabled="product.is_joined"
          :class="product.is_joined ? 'btn btn-secondary' : 'btn btn-primary'"
        >
          {{ product.is_joined ? '이미 가입된 상품입니다' : '가입하기' }}
        </button>
      </div>
      <div v-else class="alert alert-light">
        가입하시려면 <router-link :to="{ name: 'LogInView' }">로그인</router-link>이 필요합니다.
      </div>
    </div>

    <hr>
    <h3>금리 정보</h3>
    <ul>
      <li v-for="opt in uniqueOptions" :key="opt.id">
        {{ opt.save_trm }}개월 / {{ opt.intr_rate }}% ~ {{ opt.intr_rate2 }}%
      </li>
    </ul>

    <div class="mt-4">
      <p><strong>가입 방법:</strong> {{ product.join_way }}</p>
      <p><strong>우대 조건:</strong> {{ product.spcl_cnd }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useDepositStore } from '@/stores/deposits'
import { useAccountStore } from '@/stores/accounts' // 계정 스토어 추가

const route = useRoute()
const store = useDepositStore()
const accountStore = useAccountStore() // 추가

const product = ref(null)
const isLoggedIn = computed(() => accountStore.isLogin) // 추가

onMounted(async () => {
  const res = await store.getDepositDetail(route.params.id)
  product.value = res.data
})

// ✅ 기존의 훌륭한 로직 그대로 유지!
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

// ✅ 가입하기 함수 추가
const clickSubscribe = async () => {
  if (confirm('이 상품에 가입하시겠습니까?')) {
    try {
      // 스토어의 가입 함수 호출
      await store.subscribeDeposit(product.value.id, accountStore.token)
      alert('가입이 완료되었습니다!')
      product.value.is_joined = true 
    } catch (err) {
      alert(err.response?.data?.message || '가입 처리 중 오류가 발생했습니다.')
    }
  }
}
</script>

<style scoped>
.btn-primary { background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
.btn-secondary { background-color: #6c757d; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: not-allowed; }
</style>