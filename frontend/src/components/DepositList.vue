<template>
  <div class="product-list">
    <div v-if="sortedDeposits.length === 0" class="no-data">
      조건에 맞는 상품이 없습니다.
    </div>

    <div v-else class="table-container">
      <table class="compare-table">
        <thead>
          <tr>
            <th class="fixed-col">공시 일자</th>
            <th class="fixed-col">금융회사</th>
            <th class="wide-col">상품명</th>
            
            <th @click="toggleSort(6)" class="sortable">
              6개월 <span class="sort-icon">{{ getSortIcon(6) }}</span>
            </th>
            <th @click="toggleSort(12)" class="sortable">
              12개월 <span class="sort-icon">{{ getSortIcon(12) }}</span>
            </th>
            <th @click="toggleSort(24)" class="sortable">
              24개월 <span class="sort-icon">{{ getSortIcon(24) }}</span>
            </th>
            <th @click="toggleSort(36)" class="sortable">
              36개월 <span class="sort-icon">{{ getSortIcon(36) }}</span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="deposit in sortedDeposits" 
            :key="deposit.id" 
            @click="goDetail(deposit.id)"
            class="clickable-row"
          >
            <td>{{ deposit.dcls_month || '-' }}</td>
            <td class="bank-name">{{ deposit.kor_co_nm }}</td>
            <td class="product-name">{{ deposit.fin_prdt_nm }}</td>
            
            <td class="rate">{{ getInterestRate(deposit.options, 6) }}</td>
            <td class="rate">{{ getInterestRate(deposit.options, 12) }}</td>
            <td class="rate">{{ getInterestRate(deposit.options, 24) }}</td>
            <td class="rate">{{ getInterestRate(deposit.options, 36) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  deposits: {
    type: Array,
    required: true
  }
})

const router = useRouter()
const sortKey = ref(null)     // 현재 정렬 기준 (6, 12, 24, 36)
const sortOrder = ref('desc') // 정렬 순서 (desc: 내림차순, asc: 오름차순)

const goDetail = (id) => {
  router.push(`/deposits/${id}`)
}

// 화면 표시용 (문자열 반환)
const getInterestRate = (options, term) => {
  if (!options) return '-'
  const option = options.find(opt => opt.save_trm == term)
  return option ? `${option.intr_rate2}%` : '-'
}

// 정렬용 (숫자 반환, 없으면 -1)
const getRateValue = (options, term) => {
  if (!options) return -1
  const option = options.find(opt => opt.save_trm == term)
  return option ? Number(option.intr_rate2) : -1
}

// [핵심] 정렬된 리스트 계산
const sortedDeposits = computed(() => {
  if (!sortKey.value) return props.deposits

  // 원본 배열 복사 후 정렬
  return [...props.deposits].sort((a, b) => {
    const rateA = getRateValue(a.options, sortKey.value)
    const rateB = getRateValue(b.options, sortKey.value)
    
    // 금리가 같으면 유지
    if (rateA === rateB) return 0

    // 내림차순(높은 금리 순) / 오름차순(낮은 금리 순)
    return sortOrder.value === 'desc' ? rateB - rateA : rateA - rateB
  })
})

// 헤더 클릭 시 정렬 토글
const toggleSort = (key) => {
  if (sortKey.value === key) {
    // 같은 거 또 누르면 순서 반전
    sortOrder.value = sortOrder.value === 'desc' ? 'asc' : 'desc'
  } else {
    // 다른 거 누르면 해당 키로 내림차순(높은게 좋으니까) 시작
    sortKey.value = key
    sortOrder.value = 'desc'
  }
}

// 화살표 아이콘 표시
const getSortIcon = (key) => {
  if (sortKey.value !== key) return '↕' // 선택 안됨
  return sortOrder.value === 'desc' ? '▼' : '▲'
}
</script>

<style scoped>
/* 기존 스타일 유지 + 정렬 관련 스타일 추가 */
.table-container { overflow-x: auto; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); background: white; }
.compare-table { width: 100%; border-collapse: collapse; min-width: 800px; }

/* [수정] 정렬 가능한 헤더 스타일 */
.compare-table th { background-color: #eef4ff; color: #333; font-weight: 700; padding: 15px 10px; font-size: 14px; white-space: nowrap; }
.compare-table th.sortable { cursor: pointer; user-select: none; } /* 클릭 커서 추가 */
.compare-table th.sortable:hover { background-color: #dbeaff; }    /* 헤더 호버 효과 */
.sort-icon { font-size: 12px; margin-left: 4px; color: #666; }

.compare-table td { padding: 15px 10px; border-bottom: 1px solid #eee; text-align: center; font-size: 14px; color: #555; transition: background-color 0.2s; }
.clickable-row { cursor: pointer; }
.clickable-row:hover td { background-color: #f8fbff; }
.bank-name { font-weight: 600; color: #333; }
.product-name { text-align: center; font-weight: 700; color: #2F65F6; }
.rate { font-family: 'Roboto', sans-serif; font-weight: 600; color: #333; }
.no-data { text-align: center; padding: 50px; color: #888; }
</style>