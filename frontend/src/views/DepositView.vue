<template>
  <div class="view-container">
    <div class="header-section">
      <h1 class="page-title">예금 상품 비교</h1>
      
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
      <DepositList :deposits="filteredDeposits" />
    </div>
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

<style scoped>
/* [수정] 전체 컨테이너 너비 확장 */
.view-container {
  max-width: 1200px; /* 기존 1000px -> 1200px로 확장 */
  width: 100%;
  margin: 50px auto; /* 상단 여백 조금 더 줌 */
  padding: 0 20px;
  min-height: 600px;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 40px; /* 간격 넓힘 */
  border-bottom: 2px solid #2F65F6;
  padding-bottom: 20px;
}

.page-title {
  font-size: 30px; /* 제목 크기 확대 */
  font-weight: 800;
  color: #333;
  margin: 0;
}

.filter-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
}

.filter-wrapper label {
  font-size: 14px;
  color: #555;
  font-weight: 700;
}

.custom-select {
  padding: 12px 35px 12px 15px; /* 패딩 넉넉하게 */
  font-size: 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  outline: none;
  background-color: white;
  cursor: pointer;
  appearance: none;
  min-width: 200px; /* 선택박스 너비도 살짝 키움 */
  
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23999' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px;
  transition: all 0.2s;
  box-shadow: 0 2px 5px rgba(0,0,0,0.03);
}

.custom-select:hover, .custom-select:focus {
  border-color: #2F65F6;
  box-shadow: 0 0 0 3px rgba(47, 101, 246, 0.1);
}
</style>