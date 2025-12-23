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
            <h5 class="card-title mb-3 fw-bold">내역 기록하기</h5>
            <form @submit.prevent="handleCreateTransaction" class="row g-2">
              <div class="col-md-3">
                <input type="date" v-model="newTransaction.date" class="form-control" required>
              </div>
              <div class="col-md-3">
                <select v-model="newTransaction.category" class="form-select" required>
                  <option disabled value="">카테고리</option>
                  <option v-for="cat in store.categories" :key="cat.id" :value="cat.id">
                    {{ cat.name }} ({{ cat.type === 'INCOME' ? '수입' : '지출' }})
                  </option>
                </select>
              </div>
              <div class="col-md-3">
                <input type="text" v-model="newTransaction.title" class="form-control" placeholder="내역(예: 점심)" required>
              </div>
              <div class="col-md-3">
                <div class="input-group">
                  <input type="number" v-model="newTransaction.amount" class="form-control" placeholder="금액" required>
                  <button type="submit" class="btn btn-primary fw-bold px-3">추가</button>
                </div>
              </div>
            </form>
          </div>
        </div>

        <div class="card shadow-sm border-0">
          <div class="card-header bg-white border-0 pt-4 px-4 d-flex justify-content-between align-items-center">
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
                    <td class="fw-semibold">{{ item.title }}</td>
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
            <h5 class="card-title fw-bold mb-4">지출 카테고리 분석</h5>
            <div v-if="totalExpense > 0" class="chart-container">
              <Pie :data="chartData" :options="chartOptions" />
            </div>
            <div v-else class="h-100 d-flex align-items-center justify-content-center text-muted">
              지출 데이터가 없습니다.
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

const newTransaction = ref({
  date: new Date().toISOString().substr(0, 10),
  category: '',
  title: '',
  amount: null
})

// --- 데이터 로드 및 삭제 ---
onMounted(async () => {
  await store.getCategories()
  await store.getTransactions()
})

const confirmDelete = async (id) => {
  if (confirm('정말 삭제하시겠습니까?')) {
    // ledgerStore에 deleteTransaction 함수가 구현되어 있어야 합니다 (아래에서 추가)
    try {
      await store.deleteTransaction(id)
    } catch (err) {
      alert('삭제에 실패했습니다.')
    }
  }
}

// --- 필터링 및 계산 로직 ---
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

// --- 월 제어 ---
const changeMonth = (delta) => {
  const newDate = new Date(viewDate.value)
  newDate.setMonth(newDate.getMonth() + delta)
  viewDate.value = newDate
}
const resetToToday = () => { viewDate.value = new Date() }

const formatPrice = (value) => value?.toLocaleString() || 0

const handleCreateTransaction = async () => {
  try {
    await store.createTransaction(newTransaction.value)
    newTransaction.value = { date: new Date().toISOString().substr(0, 10), category: '', title: '', amount: null }
  } catch (err) { alert('저장 실패') }
}

// --- 차트 설정 ---
const chartData = computed(() => {
  const expenseItems = filteredTransactions.value.filter(t => t.category_type === 'EXPENSE')
  const categories = {}
  
  expenseItems.forEach(item => {
    categories[item.category_name] = (categories[item.category_name] || 0) + item.amount
  })

  return {
    labels: Object.keys(categories),
    datasets: [{
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'],
      data: Object.values(categories)
    }]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { position: 'bottom' } }
}
</script>

<style scoped>
.chart-container { height: 300px; position: relative; }
.table th { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; }
.card { transition: transform 0.2s; }
.bg-success-subtle { background-color: #e1f5ea; }
.bg-danger-subtle { background-color: #fbe9e9; }
</style>