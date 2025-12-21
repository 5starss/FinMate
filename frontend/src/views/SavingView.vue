<template>
  <div>
    <h1>적금 상품 목록</h1>

    <!-- 은행 필터 -->
    <select v-model="selectedBank">
      <option value="">전체 은행</option>
      <option
        v-for="bank in bankList"
        :key="bank"
        :value="bank"
      >
        {{ bank }}
      </option>
    </select>

    <!-- 필터된 목록 전달 -->
    <SavingList :savings="filteredSavings" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useSavingStore } from '@/stores/savings'
import SavingList from '@/components/SavingList.vue'

const store = useSavingStore()
const selectedBank = ref('')

onMounted(() => {
  store.getSavings()
})

const bankList = computed(() => {
  return [...new Set(store.savings.map(s => s.kor_co_nm))]
})

const filteredSavings = computed(() => {
  if (!selectedBank.value) return store.savings
  return store.savings.filter(
    s => s.kor_co_nm === selectedBank.value
  )
})
</script>
