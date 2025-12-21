<template>
  <div>
    <div v-if="loading">로딩중...</div>
    <div v-else-if="error">에러: {{ error }}</div>

    <div v-else-if="product">
      <h1>{{ product.kor_co_nm }} - {{ product.fin_prdt_nm }}</h1>

      <h3>금리 옵션</h3>
      <ul>
        <!-- ✅ 중복 제거된 옵션 출력 -->
        <li v-for="opt in uniqueOptions" :key="opt.id">
          {{ opt.save_trm }}개월 /
          {{ opt.intr_rate }}% ~ {{ opt.intr_rate2 }}%
        </li>
      </ul>
    </div>

    <div v-else>데이터가 없습니다.</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useSavingStore } from '@/stores/savings'

const route = useRoute()
const store = useSavingStore()

const product = ref(null)
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await store.getSavingDetail(route.params.id)
    product.value = res.data
  } catch (e) {
    console.error(e)
    error.value = e?.message || 'API 호출 실패'
  } finally {
    loading.value = false
  }
})

/**
 * ✅ 같은 save_trm(개월) 옵션이 여러 개면,
 * intr_rate2(최고금리)가 가장 큰 것만 남김
 * 그리고 save_trm 오름차순으로 정렬
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
</script>
