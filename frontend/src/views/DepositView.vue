<template>
  <div>
    <h1>예금 상품 목록</h1>

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

    <DepositList :deposits="filteredDeposits" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useDepositStore } from '@/stores/deposits'
import DepositList from '@/components/DepositList.vue'

const store = useDepositStore()
const selectedBank = ref('')

onMounted(() => {
  store.getDeposits()
})

const bankList = computed(() => {
  return [...new Set(store.deposits.map(d => d.kor_co_nm))]
})

const filteredDeposits = computed(() => {
  if (!selectedBank.value) return store.deposits
  return store.deposits.filter(
    d => d.kor_co_nm === selectedBank.value
  )
})
</script>
