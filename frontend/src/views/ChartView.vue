<template>
  <div class="spot-container">
    <div class="header">
      <h2>현물 상품 비교</h2>
    </div>

    <div class="control-panel">
      <h3>금/은 가격 변동</h3>
      
      <div class="controls">
        <div class="date-group">
          <div class="date-input">
            <label>시작일:</label>
            <input type="date" v-model="startDate" @change="updateChart" class="form-control">
          </div>
          <div class="date-input">
            <label>종료일:</label>
            <input type="date" v-model="endDate" @change="updateChart" class="form-control">
          </div>
        </div>

        <div class="btn-group">
          <button 
            @click="changeAsset('gold')" 
            :class="['toggle-btn', { active: currentAsset === 'gold' }]"
          >금</button>
          <button 
            @click="changeAsset('silver')" 
            :class="['toggle-btn', { active: currentAsset === 'silver' }]"
          >은</button>
        </div>
      </div>
      
      <hr>

      <div class="chart-wrapper">
        <canvas v-show="hasData" id="spotChart"></canvas>
        
        <div v-if="!hasData" class="no-data-msg">
          <p>선택된 조건에 해당하는 데이터가 없습니다.</p>
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
const startDate = ref('') // 처음에 비워두면 전체 기간으로 인식됨
const endDate = ref('')
const goldData = ref([])
const silverData = ref([])
const isLoading = ref(true) // 로딩 상태 추가
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
  isLoading.value = true // 로딩 시작
  try {
    const goldRes = await axios.get('/Gold_prices.json') 
    const silverRes = await axios.get('/Silver_prices.json')
    
    // 가져온 Raw 데이터를 깔끔하게 변환해서 저장
    goldData.value = processRawData(goldRes.data)
    silverData.value = processRawData(silverRes.data)
    
  } catch (error) {
    console.error("데이터 로드 실패:", error)
  } finally {
    isLoading.value = false // 로딩 종료
  }
}

// 데이터 전처리 (날짜 변환 및 정렬)
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
  
  // 날짜 오름차순 정렬 (과거 -> 현재)
  return processed.sort((a, b) => new Date(a.date) - new Date(b.date))
}

// 4. 자산 변경
const changeAsset = (asset) => {
  currentAsset.value = asset
  updateChart()
}

// 필터링 로직
const getFilteredData = () => {
  let targetData = currentAsset.value === 'gold' ? goldData.value : silverData.value
  
  // 시작일과 종료일이 모두 비어있으면 -> 전체 데이터 반환
  if (!startDate.value && !endDate.value) {
    return targetData
  }

  // 하나라도 선택되었으면 필터링
  return targetData.filter(item => {
    const itemDate = new Date(item.date)
    const start = startDate.value ? new Date(startDate.value) : new Date('1900-01-01')
    const end = endDate.value ? new Date(endDate.value) : new Date('2999-12-31')
    return itemDate >= start && itemDate <= end
  })
}

// 6. 차트 업데이트
const updateChart = () => {
  if (!chartInstance) return
  
  const filtered = getFilteredData()
  if (filtered.length === 0) return

  // 데이터 시간순 정렬
  filtered.sort((a, b) => new Date(a.date) - new Date(b.date))

  chartInstance.data.labels = filtered.map(item => item.date)
  chartInstance.data.datasets[0].data = filtered.map(item => item.price)
  chartInstance.data.datasets[0].label = currentAsset.value === 'gold' ? 'Gold Price (USD)' : 'Silver Price (USD)'
  chartInstance.data.datasets[0].borderColor = currentAsset.value === 'gold' ? '#FFD700' : '#C0C0C0'
  chartInstance.data.datasets[0].backgroundColor = currentAsset.value === 'gold' ? 'rgba(255, 215, 0, 0.2)' : 'rgba(192, 192, 192, 0.2)'
  
  chartInstance.update()
}

// 7. 차트 렌더링
const renderChart = () => {
  const ctx = document.getElementById('spotChart')
  if (!ctx) return

  if (chartInstance) chartInstance.destroy()

  const filtered = getFilteredData()
  // 데이터 정렬
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
        backgroundColor: isGold ? 'rgba(255, 215, 0, 0.2)' : 'rgba(192, 192, 192, 0.2)',
        borderWidth: 2,
        tension: 0.1,
        pointRadius: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'top' } },
      scales: { y: { beginAtZero: false } }
    }
  })
}
</script>

<style scoped>
.spot-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Noto Sans KR', sans-serif;
}

.header {
  background-color: #5cb85c; 
  color: white;
  padding: 15px;
  text-align: center;
  border-radius: 5px 5px 0 0;
  margin-bottom: 20px;
}

.control-panel {
  border: 1px solid #ddd;
  padding: 20px;
  border-radius: 5px;
  background-color: white;
}

.controls {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-wrap: wrap;
  margin-bottom: 10px;
}

.date-group {
  display: flex;
  gap: 20px;
}

.date-input {
  display: flex;
  flex-direction: column;
}

.date-input label {
  font-size: 12px;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-control {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn-group {
  display: flex;
  gap: 5px;
}

.toggle-btn {
  padding: 8px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  background-color: #eee;
  color: #333;
}

.toggle-btn.active {
  background-color: #5cb85c;
  color: white;
}

.chart-wrapper {
  position: relative;
  height: 400px;
  width: 100%;
}

.no-data-msg, .loading-msg {
  padding: 50px;
  text-align: center;
  color: #666;
  font-weight: bold;
  border: 1px dashed #ccc;
  border-radius: 5px;
  margin-top: 20px;
}
</style>