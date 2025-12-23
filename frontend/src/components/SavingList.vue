<template>
  <div class="product-list">
    <div v-if="sortedSavings.length === 0" class="no-data">
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
            v-for="saving in sortedSavings" 
            :key="saving.id" 
            @click="goDetail(saving.id)"
            class="clickable-row"
          >
            <td>{{ saving.dcls_month || '-' }}</td>
            <td class="bank-name">{{ saving.kor_co_nm }}</td>
            <td class="product-name">{{ saving.fin_prdt_nm }}</td>
            
            <td class="rate">{{ getInterestRate(saving.options, 6) }}</td>
            <td class="rate">{{ getInterestRate(saving.options, 12) }}</td>
            <td class="rate">{{ getInterestRate(saving.options, 24) }}</td>
            <td class="rate">{{ getInterestRate(saving.options, 36) }}</td>
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
  savings: {
    type: Array,
    required: true
  }
})

const router = useRouter()
const sortKey = ref(null)
const sortOrder = ref('desc')

const goDetail = (id) => {
  router.push(`/savings/${id}`)
}

const getInterestRate = (options, term) => {
  if (!options) return '-'
  const option = options.find(opt => opt.save_trm == term)
  return option ? `${option.intr_rate2}%` : '-'
}

const getRateValue = (options, term) => {
  if (!options) return -1
  const option = options.find(opt => opt.save_trm == term)
  return option ? Number(option.intr_rate2) : -1
}

// [핵심] 정렬된 리스트
const sortedSavings = computed(() => {
  if (!sortKey.value) return props.savings
  return [...props.savings].sort((a, b) => {
    const rateA = getRateValue(a.options, sortKey.value)
    const rateB = getRateValue(b.options, sortKey.value)
    if (rateA === rateB) return 0
    return sortOrder.value === 'desc' ? rateB - rateA : rateA - rateB
  })
})

const toggleSort = (key) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'desc' ? 'asc' : 'desc'
  } else {
    sortKey.value = key
    sortOrder.value = 'desc'
  }
}

const getSortIcon = (key) => {
  if (sortKey.value !== key) return '↕'
  return sortOrder.value === 'desc' ? '▼' : '▲'
}
</script>

<style scoped>
/* 기존 적금 스타일 유지 */
.table-container { overflow-x: auto; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); background: white; }
.compare-table { width: 100%; border-collapse: collapse; min-width: 800px; }

/* 헤더 */
.compare-table th { background-color: #e8f5e9; color: #333; font-weight: 700; padding: 15px 10px; font-size: 14px; white-space: nowrap; }
.compare-table th.sortable { cursor: pointer; user-select: none; }
.compare-table th.sortable:hover { background-color: #dceddf; } /* 적금 헤더 호버 */
.sort-icon { font-size: 12px; margin-left: 4px; color: #666; }

/* 본문 */
.compare-table td { padding: 15px 10px; border-bottom: 1px solid #eee; text-align: center; font-size: 14px; color: #555; transition: background-color 0.2s; }
.clickable-row { cursor: pointer; }
.clickable-row:hover td { background-color: #fafffc; } /* 적금 호버 */
.bank-name { font-weight: 600; color: #333; }
.product-name { text-align: center; font-weight: 700; color: #198754; }
.rate { font-family: 'Roboto', sans-serif; font-weight: 600; color: #333; }
.no-data { text-align: center; padding: 50px; color: #888; }
</style>