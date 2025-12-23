<template>
  <div class="view-container">
    <div class="header-section">
      <h1 class="page-title">적금 상품 비교</h1>

      <div class="filter-wrapper">
        <label>은행 선택</label>
        <select v-model="selectedBank" class="custom-select">
          <option value="">전체 은행 보기</option>
          <option
            v-for="bank in bankList"
            :key="bank"
            :value="bank"
          >
            {{ bank }}
          </option>
        </select>
      </div>
    </div>

    <div class="list-section">
      <SavingList :savings="filteredSavings" />
    </div>
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

<style scoped>
/* DepositView와 동일한 스타일 사용 (통일감) */
.view-container {
  max-width: 1000px;
  margin: 40px auto;
  padding: 0 20px;
  min-height: 600px;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 30px;
  border-bottom: 2px solid #2F65F6;
  padding-bottom: 20px;
}

.page-title {
  font-size: 28px;
  font-weight: 800;
  color: #333;
  margin: 0;
}

.filter-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.filter-wrapper label {
  font-size: 13px;
  color: #666;
  font-weight: 600;
}

.custom-select {
  padding: 10px 30px 10px 15px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  outline: none;
  background-color: white;
  cursor: pointer;
  appearance: none;
  min-width: 180px;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23999' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 16px;
  transition: all 0.2s;
}

.custom-select:hover, .custom-select:focus {
  border-color: #2F65F6;
  box-shadow: 0 0 0 3px rgba(47, 101, 246, 0.1);
}
</style>