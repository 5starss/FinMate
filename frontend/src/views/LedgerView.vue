<template>
  <div class="container mt-4 pb-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="fw-bold mb-0"><i class="bi bi-wallet2 text-primary"></i> 나의 가계부</h2>
      <div class="d-flex align-items-center bg-white shadow-sm rounded-pill px-3 py-1">
        <button @click="changeMonth(-1)" class="btn btn-link text-dark p-1"><i class="bi bi-chevron-left"></i></button>
        <span class="fw-bold mx-3 fs-5">{{ currentYear }}년 {{ currentMonth }}월</span>
        <button @click="changeMonth(1)" class="btn btn-link text-dark p-1"><i class="bi bi-chevron-right"></i></button>
        <button @click="resetToToday" class="btn btn-sm btn-outline-primary ms-2 rounded-pill">오늘</button>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div class="col-md-4">
        <div class="card border-0 shadow-sm bg-success text-white">
          <div class="card-body p-4">
            <h6 class="small opacity-75 fw-bold">이달의 수입</h6>
            <h2 class="fw-bold mb-0">+ {{ formatPrice(totalIncome) }}원</h2>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm bg-danger text-white">
          <div class="card-body p-4">
            <h6 class="small opacity-75 fw-bold">이달의 지출</h6>
            <h2 class="fw-bold mb-0">- {{ formatPrice(totalExpense) }}원</h2>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm bg-primary text-white">
          <div class="card-body p-4">
            <h6 class="small opacity-75 fw-bold">현재 잔액</h6>
            <h2 class="fw-bold mb-0">{{ formatPrice(totalBalance) }}원</h2>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <div class="col-lg-8">
        <div class="card shadow-sm mb-4 border-0">
          <div class="card-body p-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="card-title fw-bold mb-0">내역 기록하기</h5>
              <div class="btn-group btn-group-sm">
                <input type="radio" class="btn-check" name="type" id="type_expense" value="EXPENSE" v-model="transactionType" @change="onTypeChange">
                <label class="btn btn-outline-danger" for="type_expense">지출</label>
                <input type="radio" class="btn-check" name="type" id="type_income" value="INCOME" v-model="transactionType" @change="onTypeChange">
                <label class="btn btn-outline-success" for="type_income">수입</label>
              </div>
            </div>

            <form @submit.prevent="handleCreateTransaction" class="row g-2">
              <div class="col-md-2">
                <input type="date" v-model="newTransaction.date" class="form-control" required>
              </div>
              
              <div class="col-md-3">
                <select v-model="selectedCategoryId" class="form-select" required>
                  <option value="" disabled>카테고리 선택</option>
                  <option v-for="cat in store.categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
                  <option value="new">+ 직접 입력</option>
                </select>
              </div>

              <div v-if="selectedCategoryId === 'new'" class="col-md-3">
                <input type="text" v-model="customCategoryName" class="form-control border-primary" placeholder="카테고리명 입력" required>
              </div>

              <div :class="selectedCategoryId === 'new' ? 'col-md-2' : 'col-md-3'">
                <input type="text" v-model="newTransaction.title" class="form-control" placeholder="내역(예: 점심)" required>
              </div>
              <div :class="selectedCategoryId === 'new' ? 'col-md-2' : 'col-md-4'">
                <div class="input-group">
                  <input type="number" v-model="newTransaction.amount" class="form-control" placeholder="금액" required>
                  <button type="submit" class="btn btn-primary fw-bold px-3">추가</button>
                </div>
              </div>
              <div class="col-12 mt-2">
                <input type="text" v-model="newTransaction.memo" class="form-control form-control-sm" placeholder="메모를 입력하세요 (선택)">
              </div>
            </form>
          </div>
        </div>

        <div class="card shadow-sm border-0">
          <div class="card-header bg-white border-0 pt-4 px-4">
            <h5 class="fw-bold mb-0">상세 내역 <span class="badge bg-secondary ms-2 small">{{ filteredTransactions.length }}건</span></h5>
          </div>
          <div class="card-body px-0">
            <div v-if="filteredTransactions.length > 0" class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead class="table-light">
                  <tr>
                    <th class="ps-4">날짜</th>
                    <th>카테고리</th>
                    <th>내역</th>
                    <th class="text-end">금액</th>
                    <th class="text-center">삭제</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in filteredTransactions" :key="item.id">
                    <td class="ps-4 text-muted small">{{ item.date }}</td>
                    <td>
                      <span :class="item.category_type === 'INCOME' ? 'badge bg-success-subtle text-success' : 'badge bg-danger-subtle text-danger'">
                        {{ item.category_name }}
                      </span>
                    </td>
                    <td class="fw-semibold">
                      {{ item.title }}
                      <div v-if="item.memo" class="small text-muted fw-normal">{{ item.memo }}</div>
                    </td>
                    <td :class="item.category_type === 'INCOME' ? 'text-success text-end fw-bold' : 'text-danger text-end fw-bold'">
                      {{ item.category_type === 'INCOME' ? '+' : '-' }} {{ formatPrice(item.amount) }}
                    </td>
                    <td class="text-center">
                      <button @click="confirmDelete(item.id)" class="btn btn-sm btn-link text-muted p-0"><i class="bi bi-trash"></i></button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-else class="text-center py-5">
              <i class="bi bi-inbox fs-1 text-light"></i>
              <p class="text-muted mt-2">이달에 기록된 내역이 없습니다.</p>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-4">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <h5 class="fw-bold mb-0">{{ chartMode === 'EXPENSE' ? '지출' : '수입' }} 분석</h5>
              <button @click="toggleChartMode" class="btn btn-sm btn-outline-secondary">
                {{ chartMode === 'EXPENSE' ? '수입' : '지출' }} 보기
              </button>
            </div>
            
            <div v-if="hasChartData" class="chart-container">
              <Pie :data="chartData" :options="chartOptions" />
            </div>
            <div v-else class="h-100 d-flex flex-column align-items-center justify-content-center text-muted py-5">
              <i class="bi bi-bar-chart fs-1 mb-2"></i>
              데이터가 없습니다.
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useLedgerStore } from '@/stores/ledgers'
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

ChartJS.register(ArcElement, Tooltip, Legend)

const store = useLedgerStore()

// --- 상태 관리 ---
const viewDate = ref(new Date())
const currentYear = computed(() => viewDate.value.getFullYear())
const currentMonth = computed(() => viewDate.value.getMonth() + 1)

// 입력 관련 상태
const transactionType = ref('EXPENSE') // 작성 모드 (수입/지출)
const selectedCategoryId = ref('') // 선택된 카테고리 ID
const customCategoryName = ref('') // 직접 입력 카테고리명
const chartMode = ref('EXPENSE') // 차트 표시 모드

const newTransaction = ref({
  date: new Date().toISOString().substr(0, 10),
  title: '',
  amount: null,
  memo: ''
})

// --- 초기화 및 데이터 로드 ---
onMounted(async () => {
  await store.getTransactions()
  await store.getCategories(transactionType.value) // 초기값(지출) 카테고리 로드
})

// 수입/지출 버튼 클릭 시 카테고리 새로고침
const onTypeChange = () => {
  selectedCategoryId.value = ''
  store.getCategories(transactionType.value)
}

const toggleChartMode = () => {
  chartMode.value = chartMode.value === 'EXPENSE' ? 'INCOME' : 'EXPENSE'
}

// --- 거래 생성 로직 (중요!) ---
const handleCreateTransaction = async () => {
  try {
    let finalCategoryId = selectedCategoryId.value

    // [A방식] 카테고리 직접 입력인 경우 먼저 생성
    if (selectedCategoryId.value === 'new') {
      const newCat = await store.createCategory({
        name: customCategoryName.value,
        type: transactionType.value
      })
      finalCategoryId = newCat.id
    }

    await store.createTransaction({
      ...newTransaction.value,
      category: finalCategoryId
    })

    // 초기화
    newTransaction.value = { date: new Date().toISOString().substr(0, 10), title: '', amount: null, memo: '' }
    selectedCategoryId.value = ''
    customCategoryName.value = ''
    
  } catch (err) {
    alert('저장에 실패했습니다. 내용을 확인해주세요.')
  }
}

const confirmDelete = async (id) => {
  if (confirm('정말 삭제하시겠습니까?')) {
    await store.deleteTransaction(id)
  }
}

// --- 필터링 및 계산 로직 (기존 유지) ---
const filteredTransactions = computed(() => {
  return store.transactions.filter(item => {
    const itemDate = new Date(item.date)
    return itemDate.getFullYear() === currentYear.value && 
           itemDate.getMonth() + 1 === currentMonth.value
  })
})

const totalIncome = computed(() => filteredTransactions.value
  .filter(t => t.category_type === 'INCOME').reduce((acc, cur) => acc + cur.amount, 0))

const totalExpense = computed(() => filteredTransactions.value
  .filter(t => t.category_type === 'EXPENSE').reduce((acc, cur) => acc + cur.amount, 0))

const totalBalance = computed(() => totalIncome.value - totalExpense.value)

// --- 차트 로직 (수입/지출 전환 기능 포함) ---
const hasChartData = computed(() => {
  return filteredTransactions.value.some(t => t.category_type === chartMode.value)
})

const chartData = computed(() => {
  const items = filteredTransactions.value.filter(t => t.category_type === chartMode.value)
  const categorySums = {}
  
  items.forEach(item => {
    categorySums[item.category_name] = (categorySums[item.category_name] || 0) + item.amount
  })

  return {
    labels: Object.keys(categorySums),
    datasets: [{
      backgroundColor: chartMode.value === 'EXPENSE' 
        ? ['#FF6384', '#FF9F40', '#FFCE56', '#4BC0C0', '#9966FF'] // 지출 색상 (웜톤)
        : ['#28a745', '#20c997', '#17a2b8', '#343a40', '#6c757d'], // 수입 색상 (쿨톤)
      data: Object.values(categorySums)
    }]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { position: 'bottom' } }
}

const changeMonth = (delta) => {
  const newDate = new Date(viewDate.value)
  newDate.setMonth(newDate.getMonth() + delta)
  viewDate.value = newDate
}
const resetToToday = () => { viewDate.value = new Date() }
const formatPrice = (value) => value?.toLocaleString() || 0
</script>

<style scoped>
.chart-container { height: 300px; position: relative; }
.btn-check:checked + .btn-outline-danger { background-color: #dc3545; color: white; }
.btn-check:checked + .btn-outline-success { background-color: #28a745; color: white; }
.bg-success-subtle { background-color: #e8f5e9; color: #2e7d32; }
.bg-danger-subtle { background-color: #ffebee; color: #c62828; }
</style>