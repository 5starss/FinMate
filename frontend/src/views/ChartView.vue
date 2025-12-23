<template>
  <div class="page-wrapper">
    <div class="content-container">
      <div class="page-header">
        <h2 class="title">현물 상품 시세 조회</h2>
        <p class="subtitle">국제 금/은 시세의 과거 데이터를 조회하고 변동 추이를 확인하세요.</p>
      </div>

      <div class="control-panel">
        <div class="date-controls">
          <div class="input-group">
            <label>시작일</label>
            <input type="date" v-model="startDate" @change="updateChart" class="custom-input">
          </div>
          <span class="tilde">~</span>
          <div class="input-group">
            <label>종료일</label>
            <input type="date" v-model="endDate" @change="updateChart" class="custom-input">
          </div>
        </div>

        <div class="asset-toggle">
          <button 
            @click="changeAsset('gold')" 
            :class="['toggle-btn', { active: currentAsset === 'gold' }]"
          >
            <span class="icon">🟡</span> 금 (Gold)
          </button>
          <button 
            @click="changeAsset('silver')" 
            :class="['toggle-btn', { active: currentAsset === 'silver' }]"
          >
            <span class="icon">⚪</span> 은 (Silver)
          </button>
        </div>
      </div>
      
      <div class="divider"></div>

      <div class="chart-section">
        <div v-if="isLoading" class="status-msg">
          데이터를 불러오는 중입니다...
        </div>
        
        <div v-else class="chart-wrapper">
          <canvas v-show="hasData" id="spotChart"></canvas>
          
          <div v-if="!hasData" class="status-msg no-data">
            <p>선택된 기간에 해당하는 데이터가 없습니다.</p>
            <small>날짜 범위를 변경해 보세요.</small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'

// 1. 상태 변수
const currentAsset = ref('gold')
const startDate = ref('') 
const endDate = ref('')
const goldData = ref([])
const silverData = ref([])
const isLoading = ref(true)
let chartInstance = null

// 2. Computed
const hasData = computed(() => {
  const data = getFilteredData()
  return data.length > 0
})

// 3. 데이터 로드
onMounted(async () => {
  await loadData()
  renderChart()
})

const loadData = async () => {
  isLoading.value = true
  try {
    // [주의] 실제 파일 경로가 public 폴더에 있는지 확인해주세요.
    const goldRes = await axios.get('/Gold_prices.json') 
    const silverRes = await axios.get('/Silver_prices.json')
    
    goldData.value = processRawData(goldRes.data)
    silverData.value = processRawData(silverRes.data)
    
  } catch (error) {
    console.error("데이터 로드 실패:", error)
  } finally {
    isLoading.value = false
  }
}

const processRawData = (rawData) => {
  const processed = rawData.map(item => {
    const dateObj = new Date(item.Date)
    const dateStr = !isNaN(dateObj) ? dateObj.toISOString().split('T')[0] : item.Date
    const priceStr = String(item['Close/Last']).replace(/,/g, '')
    
    return {
      date: dateStr,
      price: parseFloat(priceStr)
    }
  })
  
  return processed.sort((a, b) => new Date(a.date) - new Date(b.date))
}

const changeAsset = (asset) => {
  currentAsset.value = asset
  updateChart()
}

const getFilteredData = () => {
  let targetData = currentAsset.value === 'gold' ? goldData.value : silverData.value
  
  if (!startDate.value && !endDate.value) {
    return targetData
  }

  return targetData.filter(item => {
    const itemDate = new Date(item.date)
    const start = startDate.value ? new Date(startDate.value) : new Date('1900-01-01')
    const end = endDate.value ? new Date(endDate.value) : new Date('2999-12-31')
    return itemDate >= start && itemDate <= end
  })
}

const updateChart = () => {
  if (!chartInstance) return
  
  const filtered = getFilteredData()
  if (filtered.length === 0) return

  filtered.sort((a, b) => new Date(a.date) - new Date(b.date))

  chartInstance.data.labels = filtered.map(item => item.date)
  chartInstance.data.datasets[0].data = filtered.map(item => item.price)
  chartInstance.data.datasets[0].label = currentAsset.value === 'gold' ? 'Gold Price (USD)' : 'Silver Price (USD)'
  chartInstance.data.datasets[0].borderColor = currentAsset.value === 'gold' ? '#FFD700' : '#C0C0C0'
  chartInstance.data.datasets[0].backgroundColor = currentAsset.value === 'gold' ? 'rgba(255, 215, 0, 0.1)' : 'rgba(192, 192, 192, 0.1)'
  
  chartInstance.update()
}

const renderChart = () => {
  const ctx = document.getElementById('spotChart')
  if (!ctx) return

  if (chartInstance) chartInstance.destroy()

  const filtered = getFilteredData()
  filtered.sort((a, b) => new Date(a.date) - new Date(b.date))
  
  const isGold = currentAsset.value === 'gold'

  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: filtered.map(item => item.date),
      datasets: [{
        label: isGold ? 'Gold Price (USD)' : 'Silver Price (USD)',
        data: filtered.map(item => item.price),
        borderColor: isGold ? '#FFD700' : '#C0C0C0',
        backgroundColor: isGold ? 'rgba(255, 215, 0, 0.1)' : 'rgba(192, 192, 192, 0.1)',
        borderWidth: 2,
        tension: 0.1, // 선을 약간 부드럽게 (0이면 직선)
        pointRadius: 2, // 평소엔 점 숨김
        pointHoverRadius: 4, // 호버 시 점 표시
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { 
        legend: { 
          position: 'top',
          labels: {
            font: { family: "'Noto Sans KR', sans-serif", size: 14 }
          }
        },
        tooltip: {
          mode: 'index',
          intersect: false,
        }
      },
      scales: { 
        x: {
          grid: { display: false } // X축 격자 숨김 (깔끔하게)
        },
        y: { 
          beginAtZero: false,
          grid: { color: '#f0f0f0' } // Y축 격자 연하게
        } 
      },
      interaction: {
        mode: 'nearest',
        axis: 'x',
        intersect: false
      }
    }
  })
}
</script>

<style scoped>
/* 페이지 전체 래퍼 (배경색 및 여백) */
.page-wrapper {
  background-color: white;
  min-height: calc(100vh - 70px);
  padding: 40px 20px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

/* 콘텐츠 컨테이너 (흰색 카드) */
.content-container {
  background-color: white;
  width: 100%;
  max-width: 1100px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  padding: 30px;
  border: 1px solid #eee;
}

/* 헤더 스타일 */
.page-header {
  margin-bottom: 30px;
}

.title {
  font-size: 26px;
  font-weight: 800;
  color: #333;
  margin: 8px;
}

.subtitle {
  font-size: 15px;
  color: #666;
}

/* 컨트롤 패널 */
.control-panel {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: flex-end;
  gap: 20px;
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 12px;
}

.date-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.input-group label {
  font-size: 13px;
  font-weight: 600;
  color: #555;
  margin-left: 4px;
}

.custom-input {
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  color: #333;
  outline: none;
  transition: all 0.2s;
}

.custom-input:focus {
  border-color: #2F65F6;
  box-shadow: 0 0 0 3px rgba(47, 101, 246, 0.1);
}

.tilde {
  margin-top: 24px; /* 라벨 높이만큼 내림 */
  color: #888;
  font-weight: bold;
}

/* 토글 버튼 그룹 */
.asset-toggle {
  display: flex;
  background-color: #e9ecef;
  padding: 4px;
  border-radius: 8px;
}

.toggle-btn {
  padding: 10px 24px;
  border: none;
  background: transparent;
  color: #666;
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.toggle-btn:hover {
  color: #333;
}

/* 활성화된 버튼 스타일 */
.toggle-btn.active {
  background-color: white;
  color: #2F65F6;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.icon {
  font-size: 14px;
}

.divider {
  height: 1px;
  background-color: #eee;
  margin: 30px 0;
}

/* 차트 영역 */
.chart-section {
  position: relative;
  min-height: 400px;
}

.chart-wrapper {
  height: 500px;
  width: 100%;
}

.status-msg {
  text-align: center;
  padding: 100px 0;
  color: #666;
  font-size: 16px;
}

.no-data {
  background-color: #f9f9f9;
  border-radius: 8px;
}

.no-data p {
  margin: 0 0 8px 0;
  font-weight: bold;
  color: #555;
}

.no-data small {
  color: #999;
}
</style>