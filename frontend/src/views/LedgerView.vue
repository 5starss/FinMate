<template>
  <div class="view-container">
    <div class="header-section animate-fade-in">
      <h2 class="page-title"><i class="bi bi-wallet2 text-primary"></i> 나의 가계부</h2>
      <div class="date-controller">
        <button @click="changeMonth(-1)" class="nav-btn">&lt;</button> 
        <span class="current-date">{{ currentYear }}년 {{ currentMonth }}월</span>
        <button @click="changeMonth(1)" class="nav-btn">&gt;</button>
        <button @click="resetToToday" class="today-btn">Today</button>
      </div>
    </div>

    <div class="stats-grid animate-slide-up">
      <div class="stat-card income">
        <div class="icon-circle bg-green"><i class="bi bi-arrow-down-left"></i></div>
        <div class="text-group">
          <span class="label">이달의 수입</span>
          <h3 class="amount text-green">+ {{ formatPrice(totalIncome) }}원</h3>
        </div>
      </div>
      <div class="stat-card expense">
        <div class="icon-circle bg-red"><i class="bi bi-arrow-up-right"></i></div>
        <div class="text-group">
          <span class="label">이달의 지출</span>
          <h3 class="amount text-red">- {{ formatPrice(totalExpense) }}원</h3>
        </div>
      </div>
      <div class="stat-card balance">
        <div class="icon-circle bg-blue"><i class="bi bi-wallet-fill"></i></div>
        <div class="text-group">
          <span class="label">현재 잔액</span>
          <h3 class="amount text-blue">{{ formatPrice(totalBalance) }}원</h3>
        </div>
      </div>
    </div>

    <div class="content-grid">
      <div class="left-column animate-slide-up delay-1">
        
        <div class="input-card" :class="{ 'edit-mode': isEditing }">
          <div class="card-header-custom">
            <h5 class="card-title">
              {{ isEditing ? '✏️ 내역 수정하기' : '📝 새 내역 쓰기' }}
            </h5>
            <div class="type-toggle">
              <label class="toggle-btn" :class="{ active: transactionType === 'EXPENSE' }">
                <input type="radio" value="EXPENSE" v-model="transactionType" @change="onTypeChange"> 지출
              </label>
              <label class="toggle-btn" :class="{ active: transactionType === 'INCOME' }">
                <input type="radio" value="INCOME" v-model="transactionType" @change="onTypeChange"> 수입
              </label>
            </div>
          </div>

          <form @submit.prevent="handleSaveTransaction" class="transaction-form">
            <div class="form-row">
              <div class="input-group date-group">
                <label>📅 날짜</label>
                <input type="date" v-model="newTransaction.date" required>
              </div>
              <div class="input-group category-group">
                <label>📂 카테고리</label>
                <div class="select-wrapper">
                  <select v-model="selectedCategoryId" required>
                    <option value="" disabled>선택하세요</option>
                    <option v-for="cat in store.categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
                    <option value="new">+ 직접 입력</option>
                  </select>
                  <button 
                    v-if="selectedCategoryId && selectedCategoryId !== 'new'" 
                    type="button" 
                    @click.stop="deleteCategory(selectedCategoryId)" 
                    class="del-cat-btn"
                    title="카테고리 삭제"
                  >
                    <i class="bi bi-x"></i>
                  </button>
                </div>
              </div>
            </div>

            <div v-if="selectedCategoryId === 'new'" class="form-row">
              <div class="input-group">
                <label>✨ 새 카테고리 이름</label>
                <input type="text" v-model="customCategoryName" class="full-input" placeholder="예: 경조사비" required>
              </div>
            </div>

            <div class="form-row">
              <div class="input-group title-group">
                <label>🖊️ 내역</label>
                <input type="text" v-model="newTransaction.title" placeholder="예: 점심 식사" required>
              </div>
              <div class="input-group amount-group">
                <label>💰 금액</label>
                <div class="amount-wrapper">
                  <input type="number" v-model="newTransaction.amount" placeholder="0" required>
                  <span class="unit">원</span>
                </div>
              </div>
            </div>

            <div class="form-row">
              <div class="input-group">
                <label>📝 메모 (선택)</label>
                <input type="text" v-model="newTransaction.memo" class="full-input" placeholder="추가 설명을 적어주세요">
              </div>
            </div>

            <div class="form-actions">
              <button v-if="isEditing" type="button" @click="cancelEdit" class="cancel-btn">취소</button>
              <button type="submit" class="submit-btn" :class="isEditing ? 'edit' : 'save'">
                {{ isEditing ? '수정 완료' : '등록하기' }}
              </button>
            </div>
          </form>
        </div>

        <div class="list-card">
          <div class="list-header">
            <h5>상세 내역 <span class="count-badge">{{ filteredTransactions.length }}</span></h5>
          </div>
          
          <div v-if="filteredTransactions.length > 0" class="transaction-list">
            <div 
              v-for="item in filteredTransactions" 
              :key="item.id" 
              class="list-item"
              @click="startEdit(item)"
            >
              <div class="item-date">
                <span class="day">{{ item.date.slice(8, 10) }}</span>
                <span class="month-sm">{{ item.date.slice(5, 7) }}월</span>
              </div>
              <div class="item-info">
                <div class="info-top">
                  <span class="cat-badge" :class="item.category_type === 'INCOME' ? 'income' : 'expense'">
                    {{ getCategoryName(item) }}
                  </span>
                  <span class="item-title">{{ item.title }}</span>
                </div>
                <div v-if="item.memo" class="item-memo">{{ item.memo }}</div>
              </div>
              <div class="item-amount" :class="item.category_type === 'INCOME' ? 'text-green' : 'text-red'">
                {{ item.category_type === 'INCOME' ? '+' : '-' }} {{ formatPrice(item.amount) }}
              </div>
              <button @click.stop="confirmDelete(item.id)" class="item-del-btn">
                <i class="bi bi-trash"></i>
              </button>
            </div>
          </div>

          <div v-else class="empty-state">
            <i class="bi bi-receipt"></i>
            <p>이달의 내역이 없습니다.</p>
          </div>
        </div>
      </div>

      <div class="right-column animate-slide-up delay-2">
        <div class="chart-card">
          <div class="chart-header">
            <h5>{{ chartMode === 'EXPENSE' ? '지출' : '수입' }} 분석</h5>
            <button @click="toggleChartMode" class="chart-toggle-btn">
              {{ chartMode === 'EXPENSE' ? '수입 보기' : '지출 보기' }}
            </button>
          </div>
          
          <div v-if="hasChartData" class="chart-wrapper">
            <Pie :data="chartData" :options="chartOptions" />
          </div>
          <div v-else class="empty-chart">
            <i class="bi bi-pie-chart"></i>
            <p>분석할 데이터가 없습니다.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useLedgerStore } from '@/stores/ledgers'
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'

// [중요] Chart.js 컴포넌트 등록
ChartJS.register(ArcElement, Tooltip, Legend)

const store = useLedgerStore()

// --- 상태 관리 ---
const viewDate = ref(new Date())
const currentYear = computed(() => viewDate.value.getFullYear())
const currentMonth = computed(() => viewDate.value.getMonth() + 1)

const isEditing = ref(false)
const editingId = ref(null)

const transactionType = ref('EXPENSE')
const selectedCategoryId = ref('')
const customCategoryName = ref('')
const chartMode = ref('EXPENSE')

const newTransaction = ref({
  date: new Date().toISOString().substr(0, 10),
  title: '',
  amount: null,
  memo: ''
})

onMounted(async () => {
  await store.getTransactions()
  await store.getCategories(transactionType.value)
})

// [추가] 카테고리 이름을 안전하게 가져오는 헬퍼 함수
// 백엔드에서 category_name을 안 보내주거나, category(ID)만 있을 경우 대비
const getCategoryName = (item) => {
  if (item.category_name) return item.category_name
  const cat = store.categories.find(c => c.id === item.category)
  return cat ? cat.name : '기타'
}

// --- 차트 데이터 로직 (수정됨) ---
const filteredTransactions = computed(() => {
  return store.transactions.filter(item => {
    const itemDate = new Date(item.date)
    return itemDate.getFullYear() === currentYear.value && 
           itemDate.getMonth() + 1 === currentMonth.value
  }).sort((a, b) => new Date(b.date) - new Date(a.date))
})

// 차트 데이터 유무 확인
const hasChartData = computed(() => {
  const items = filteredTransactions.value.filter(t => t.category_type === chartMode.value)
  return items.length > 0 && items.reduce((acc, cur) => acc + cur.amount, 0) > 0
})

const chartData = computed(() => {
  const items = filteredTransactions.value.filter(t => t.category_type === chartMode.value)
  
  // 카테고리별 합계 계산
  const categorySums = {}
  items.forEach(item => {
    // 안전한 이름 가져오기
    const name = getCategoryName(item)
    categorySums[name] = (categorySums[name] || 0) + item.amount
  })
  
  // 데이터 정렬 (금액 큰 순서)
  const sortedEntries = Object.entries(categorySums).sort((a, b) => b[1] - a[1])
  
  return {
    labels: sortedEntries.map(e => e[0]),
    datasets: [{
      backgroundColor: chartMode.value === 'EXPENSE' 
        ? ['#ff6b6b', '#ff9f43', '#feca57', '#48dbfb', '#5f27cd', '#ff9ff3', '#54a0ff']
        : ['#1dd1a1', '#10ac84', '#00d2d3', '#222f3e', '#576574', '#8395a7'],
      data: sortedEntries.map(e => e[1]),
      hoverOffset: 4
    }]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        usePointStyle: true,
        padding: 20,
        font: { size: 12 }
      }
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          let label = context.label || '';
          if (label) {
            label += ': ';
          }
          if (context.parsed !== null) {
            label += new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' }).format(context.parsed);
          }
          return label;
        }
      }
    }
  }
}

// --- 기타 로직 (기존 유지) ---
const totalIncome = computed(() => filteredTransactions.value
  .filter(t => t.category_type === 'INCOME').reduce((acc, cur) => acc + cur.amount, 0))

const totalExpense = computed(() => filteredTransactions.value
  .filter(t => t.category_type === 'EXPENSE').reduce((acc, cur) => acc + cur.amount, 0))

const totalBalance = computed(() => totalIncome.value - totalExpense.value)

const startEdit = (item) => {
  isEditing.value = true
  editingId.value = item.id
  transactionType.value = item.category_type
  store.getCategories(item.category_type).then(() => {
    selectedCategoryId.value = item.category
  })
  newTransaction.value = {
    date: item.date,
    title: item.title,
    amount: item.amount,
    memo: item.memo || ''
  }
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const cancelEdit = () => {
  isEditing.value = false
  editingId.value = null
  resetForm()
}

const resetForm = () => {
  newTransaction.value = { 
    date: new Date().toISOString().substr(0, 10), 
    title: '', 
    amount: null, 
    memo: '' 
  }
  selectedCategoryId.value = ''
  customCategoryName.value = ''
}

const onTypeChange = () => {
  selectedCategoryId.value = ''
  store.getCategories(transactionType.value)
  // 차트 모드도 같이 변경해주면 사용자 경험이 좋음 (선택사항)
  // chartMode.value = transactionType.value 
}

const handleSaveTransaction = async () => {
  try {
    let finalCategoryId = selectedCategoryId.value
    if (selectedCategoryId.value === 'new') {
      const newCat = await store.createCategory({
        name: customCategoryName.value,
        type: transactionType.value
      })
      finalCategoryId = newCat.id
    }

    if (isEditing.value) {
      await store.updateTransaction(editingId.value, {
        ...newTransaction.value,
        category: finalCategoryId
      })
      alert('수정되었습니다.')
    } else {
      await store.createTransaction({
        ...newTransaction.value,
        category: finalCategoryId
      })
    }
    cancelEdit()
  } catch (err) {
    console.error(err)
    alert('저장 중 오류가 발생했습니다. 입력값을 확인해주세요.')
  }
}

const confirmDelete = async (id) => {
  if (confirm('삭제하시겠습니까?')) await store.deleteTransaction(id)
}

const deleteCategory = async (catId) => {
  if (confirm('이 카테고리를 삭제하시겠습니까?')) {
    try {
      await store.deleteCategory(catId)
      selectedCategoryId.value = ''
    } catch (err) { 
      alert('삭제할 수 없는 카테고리입니다.') 
    }
  }
}

const toggleChartMode = () => {
  chartMode.value = chartMode.value === 'EXPENSE' ? 'INCOME' : 'EXPENSE'
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
  /* [필수] 박스 크기 계산 기준 통일 (삐져나옴 방지) */
  * { box-sizing: border-box; }
  
  /* 애니메이션 */
  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
  .animate-fade-in { animation: fadeIn 0.8s ease-out; }
  .animate-slide-up { animation: slideUp 0.8s ease-out forwards; opacity: 0; }
  .delay-1 { animation-delay: 0.1s; }
  .delay-2 { animation-delay: 0.2s; }
  
  .view-container { max-width: 1200px; margin: 40px auto; padding: 0 20px; min-height: 800px; }
  
  /* 헤더 */
  .header-section { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
  .page-title { font-size: 1.8rem; font-weight: 800; color: #333; margin: 0; }
  
  /* 날짜 컨트롤러 */
  .date-controller { 
    display: flex; align-items: center; background: white; padding: 8px 20px; 
    border-radius: 50px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #f8f9fa;
  }
  .nav-btn { 
    background: none; border: none; font-family: sans-serif; font-size: 1.5rem; 
    font-weight: 300; line-height: 1; padding-bottom: 3px; color: #adb5bd;    
    cursor: pointer; padding: 0 15px; transition: all 0.2s; display: flex; align-items: center;
  }
  .nav-btn:hover { color: #2F65F6; transform: scale(1.2); font-weight: 700; }
  .current-date { font-size: 1.3rem; font-weight: 800; margin: 0 5px; color: #333; width: 140px; text-align: center; user-select: none; }
  .today-btn { 
    background: #f1f3f5; color: #666; border: none; padding: 6px 14px; 
    border-radius: 20px; font-size: 0.8rem; font-weight: 700; cursor: pointer; margin-left: 10px; transition: all 0.2s;
  }
  .today-btn:hover { background: #2F65F6; color: white; }
  
  /* 1. 상단 통계 카드 */
  .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px; }
  .stat-card { background: white; border-radius: 20px; padding: 25px; display: flex; align-items: center; gap: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.03); border: 1px solid #f0f0f0; }
  .icon-circle { width: 50px; height: 50px; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; flex-shrink: 0; }
  .bg-green { background: #e8f5e9; color: #198754; }
  .bg-red { background: #ffebee; color: #e53935; }
  .bg-blue { background: #e3f2fd; color: #0288d1; }
  .text-group { display: flex; flex-direction: column; overflow: hidden; }
  .label { font-size: 0.85rem; color: #888; font-weight: 600; margin-bottom: 5px; }
  .amount { font-size: 1.5rem; font-weight: 800; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .text-green { color: #198754; }
  .text-red { color: #e53935; }
  .text-blue { color: #333; }
  
  /* 레이아웃 그리드 */
  .content-grid { 
    display: grid; 
    /* 입력창(2) : 차트(1) 비율 유지하되, 차트는 최소 350px 확보 */
    grid-template-columns: minmax(0, 2fr) minmax(350px, 1fr); 
    gap: 25px; align-items: start; 
  }
  
  /* 2. 입력 폼 (왼쪽) */
  .input-card { 
    background: white; border-radius: 20px; padding: 30px; 
    box-shadow: 0 5px 20px rgba(0,0,0,0.03); margin-bottom: 25px; 
    border: 2px solid transparent; transition: border-color 0.3s; 
  }
  .input-card.edit-mode { border-color: #ffca28; background: #fffdf5; }
  
  .card-header-custom { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
  .card-title { font-size: 1.2rem; font-weight: 800; color: #333; margin: 0; }
  .type-toggle { background: #f1f3f5; padding: 4px; border-radius: 12px; display: flex; }
  .toggle-btn { padding: 6px 15px; border-radius: 8px; font-size: 0.9rem; font-weight: 700; color: #888; cursor: pointer; transition: 0.2s; }
  .toggle-btn.active { background: white; color: #333; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
  .toggle-btn input { display: none; }
  
  /* [핵심 수정] 입력 폼 레이아웃: Grid 사용으로 겹침 방지 */
  .transaction-form .form-row { 
    display: grid; 
    grid-template-columns: 1fr 1fr; /* 정확히 반반 나누기 */
    gap: 20px; 
    margin-bottom: 20px; 
  }
  
  /* 메모 입력창처럼 혼자 있는 행은 1열로 통합 */
  .transaction-form .form-row:has(.full-input),
  .transaction-form .form-row:has(.input-group:only-child) {
    grid-template-columns: 1fr;
  }
  
  .input-group { 
    display: flex; flex-direction: column; width: 100%;
  }
  
  .input-group label { 
    font-size: 0.8rem; font-weight: 700; color: #666; margin-bottom: 8px; 
  }
  
  /* 입력창 기본 스타일 */
  .input-group input, 
  .select-wrapper select,
  .full-input { 
    width: 100%; 
    padding: 12px; 
    border: 1px solid #e0e0e0; 
    border-radius: 10px; font-size: 0.95rem; outline: none; background: #fff;
  }
  .input-group input:focus, .select-wrapper select:focus { border-color: #2F65F6; }
  
  /* 카테고리 셀렉트: 오른쪽 여백(X버튼용) */
  .select-wrapper { position: relative; width: 100%; }
  .select-wrapper select { padding-right: 40px; }
  
  .del-cat-btn { 
    position: absolute; right: 8px; top: 50%; transform: translateY(-50%); 
    background: white; border: 1px solid #eee; border-radius: 50%; width: 24px; height: 24px;
    display: flex; align-items: center; justify-content: center;
    color: #ff6b6b; font-size: 1rem; cursor: pointer; z-index: 2;
  }
  
  /* 금액 입력칸: 오른쪽 여백('원'용) */
  .amount-wrapper { position: relative; width: 100%; }
  .amount-wrapper input { padding-right: 40px; text-align: right; font-weight: 700; }
  .amount-wrapper .unit { position: absolute; right: 15px; top: 50%; transform: translateY(-50%); font-weight: 700; color: #888; pointer-events: none; }
  
  /* [수정] 메모 입력창은 오른쪽 여백 제거 */
  .full-input { padding-right: 12px; }
  
  .form-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 10px; }
  .submit-btn { background: #2F65F6; color: white; border: none; padding: 12px 30px; border-radius: 12px; font-weight: 700; cursor: pointer; transition: 0.2s; }
  .submit-btn:hover { background: #1c50d8; }
  .submit-btn.edit { background: #ffa000; }
  .cancel-btn { background: #eee; color: #555; border: none; padding: 12px 20px; border-radius: 12px; font-weight: 700; cursor: pointer; }
  
  /* 내역 리스트 */
  .list-card { background: white; border-radius: 20px; padding: 25px; box-shadow: 0 5px 20px rgba(0,0,0,0.03); }
  .list-header { margin-bottom: 20px; }
  .list-header h5 { font-weight: 800; font-size: 1.1rem; }
  .count-badge { background: #eee; color: #555; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem; margin-left: 5px; }
  
  .transaction-list { display: flex; flex-direction: column; gap: 10px; }
  .list-item { display: flex; align-items: center; padding: 15px; border-radius: 15px; background: #fcfcfc; border: 1px solid #f0f0f0; cursor: pointer; transition: all 0.2s; }
  .list-item:hover { transform: translateX(5px); background: #f8fbff; border-color: #eef4ff; }
  
  .item-date { display: flex; flex-direction: column; align-items: center; margin-right: 15px; min-width: 40px; }
  .item-date .day { font-size: 1.1rem; font-weight: 800; color: #333; }
  .item-date .month-sm { font-size: 0.7rem; color: #999; }
  .item-info { flex: 1; display: flex; flex-direction: column; }
  .info-top { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
  .cat-badge { font-size: 0.75rem; padding: 3px 8px; border-radius: 6px; font-weight: 700; }
  .cat-badge.income { background: #e8f5e9; color: #198754; }
  .cat-badge.expense { background: #ffebee; color: #e53935; }
  .item-title { font-weight: 700; color: #333; font-size: 0.95rem; }
  .item-memo { font-size: 0.8rem; color: #888; }
  .item-amount { font-weight: 800; font-size: 1.1rem; margin-right: 15px; }
  .item-del-btn { background: none; border: none; color: #ccc; cursor: pointer; font-size: 1.1rem; }
  .item-del-btn:hover { color: #ff6b6b; }
  .empty-state { text-align: center; padding: 40px 0; color: #888; }
  .empty-state i { font-size: 2rem; margin-bottom: 10px; display: block; }
  
  /* 3. 차트 영역 */
  .right-column { position: sticky; top: 100px; }
  .chart-card { background: white; border-radius: 20px; padding: 25px; box-shadow: 0 5px 20px rgba(0,0,0,0.03); height: 500px; display: flex; flex-direction: column; }
  .chart-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
  .chart-header h5 { font-weight: 800; margin: 0; }
  .chart-toggle-btn { border: 1px solid #ddd; background: white; padding: 5px 12px; border-radius: 15px; font-size: 0.8rem; cursor: pointer; }
  .chart-wrapper { flex: 1; position: relative; width: 100%; overflow: hidden; }
  .empty-chart { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #ccc; }
  .empty-chart i { font-size: 3rem; margin-bottom: 10px; }
  
  /* 반응형 */
  @media (max-width: 900px) {
    .stats-grid { grid-template-columns: 1fr; }
    .content-grid { grid-template-columns: 1fr; } 
    .right-column { position: static; } 
    .chart-card { height: auto; min-height: 400px; }
    
    /* 모바일에서는 1열로 변경 */
    .transaction-form .form-row { grid-template-columns: 1fr; }
  }
  </style>