<template>
  <div v-if="product">
    <h1>{{ product.kor_co_nm }} - {{ product.fin_prdt_nm }}</h1>

    <h3>예금 옵션</h3>
    <ul>
      <!-- ✅ 기간별로 1개(최고금리 intr_rate2 최대)만 출력 -->
      <li v-for="opt in uniqueOptions" :key="opt.id">
        {{ opt.save_trm }}개월 /
        {{ opt.intr_rate }}% ~ {{ opt.intr_rate2 }}%
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useDepositStore } from '@/stores/deposits'

const route = useRoute()
const store = useDepositStore()
const product = ref(null)

onMounted(async () => {
  const res = await store.getDepositDetail(route.params.id)
  product.value = res.data
})

/**
 * ✅ 같은 save_trm(개월) 옵션이 여러 개면
 * intr_rate2(최고금리)가 가장 큰 것만 남기고,
 * save_trm 오름차순 정렬
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
