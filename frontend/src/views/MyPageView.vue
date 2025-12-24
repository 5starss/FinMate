<template>
  <div class="view-container">
    <div class="header-section">
      <h1 class="page-title">마이 페이지</h1>
      <p class="subtitle">나의 자산 현황과 포트폴리오를 한눈에 관리하세요.</p>
    </div>

    <div class="profile-section">
      <div class="profile-card">
        <div class="profile-header">
          <div class="avatar-area">
            <div 
              class="avatar-circle" 
              :class="{ 'editable': isEditing }"
              @click="triggerFileInput"
            >
              <img v-if="displayImageUrl" :src="displayImageUrl" class="profile-img" alt="profile" />
              <i v-else class="bi bi-person-fill default-icon"></i>

              <div v-if="isEditing" class="camera-overlay">
                <i class="bi bi-camera-fill"></i>
              </div>
            </div>

            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              style="display:none"
              @change="onFileChange"
            />
          </div>
          <div class="user-info">
            <div class="name-row">
              <h2 class="username">{{ userInfo?.username }}님</h2>
              <span class="user-badge">FinMate Member</span>
            </div>
            <p class="email">{{ userInfo?.email }}</p>
          </div>
          <div class="edit-btn-area">
            <button v-if="!isEditing" @click="toggleEdit" class="edit-btn">
              <i class="bi bi-pencil-square"></i> 정보 수정
            </button>
            <div v-else class="action-buttons">
              <button @click="saveProfile" class="save-btn">저장</button>
              <button @click="toggleEdit" class="cancel-btn">취소</button>
            </div>
          </div>
        </div>

        <div class="profile-details">
          <div class="detail-item">
            <span class="label">나이</span>
            <div v-if="!isEditing" class="value">{{ userInfo?.profile?.age || '-' }}세</div>
            <input v-else type="number" v-model="editData.profile.age" class="edit-input" placeholder="나이">
          </div>
          <div class="detail-item">
            <span class="label">성별</span>
            <div v-if="!isEditing" class="value">{{ genderDisplay }}</div>
            <select v-else v-model="editData.profile.gender" class="edit-select">
              <option value="M">남성</option>
              <option value="F">여성</option>
            </select>
          </div>
          <div class="detail-item">
            <span class="label">연소득</span>
            <div v-if="!isEditing" class="value">{{ formatIncome(userInfo?.profile?.income) }}</div>
            <input v-else type="number" v-model="editData.profile.income" class="edit-input" placeholder="연소득">
          </div>
          <div class="detail-item">
            <span class="label">투자 성향</span>
            <div v-if="!isEditing" class="value highlight">{{ userInfo?.profile?.spending_habits || '미설정' }}</div>
            <select v-else v-model="editData.profile.spending_habits" class="edit-select">
              <option value="보수적">보수적 (안정 추구)</option>
              <option value="공격적">공격적 (수익 추구)</option>
              <option value="균형 잡힌">균형 잡힌 소비</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <div class="dashboard-section">
      <div class="asset-card total-asset">
        <div class="card-content">
          <span class="card-label">나의 총 자산</span>
          <h1 class="total-amount">{{ formatIncome(totalAssets) }}</h1>
          <i class="bi bi-wallet2 bg-icon"></i>
        </div>
      </div>

      <div class="sub-asset-grid">
        <div class="asset-card sub-card cash">
          <div class="icon-box"><i class="bi bi-cash-coin"></i></div>
          <div class="text-group">
            <span class="sub-label">현금 (가계부 잔액)</span>
            <span class="sub-amount">{{ formatIncome(cashBalance) }}</span>
          </div>
        </div>
        <div class="asset-card sub-card deposit">
          <div class="icon-box"><i class="bi bi-piggy-bank"></i></div>
          <div class="text-group">
            <span class="sub-label">총 예금액</span>
            <span class="sub-amount">{{ formatIncome(totalDepositAmount) }}</span>
          </div>
        </div>
        <div class="asset-card sub-card saving">
          <div class="icon-box"><i class="bi bi-graph-up-arrow"></i></div>
          <div class="text-group">
            <span class="sub-label">총 적금액</span>
            <span class="sub-amount">{{ formatIncome(totalSavingAmount) }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="subscription-section">
      <div class="section-header">
        <h3 class="section-title">내 포트폴리오 <span class="count-badge">{{ totalCount }}</span></h3>
      </div>

      <div v-if="totalCount > 0" class="product-grid">
        <div 
          v-for="sub in subscriptions.deposits" 
          :key="'d-'+sub.id" 
          @click="openModal(sub, 'deposit')" 
          class="product-card deposit-theme"
        >
          <div class="card-top">
            <span class="bank-badge">{{ sub.bank_name }}</span>
            <span class="type-badge">예금</span>
          </div>
          <h4 class="product-name">{{ sub.product_name }}</h4>
          <div class="card-bottom">
            <div class="info-group">
              <span class="info-label">금리</span>
              <span class="info-value">{{ sub.option_details.intr_rate }}%</span>
            </div>
            <div class="info-group right">
              <span class="info-label">기간</span>
              <span class="info-value">{{ sub.option_details.save_trm }}개월</span>
            </div>
          </div>
        </div>

        <div 
          v-for="sub in subscriptions.savings" 
          :key="'s-'+sub.id" 
          @click="openModal(sub, 'saving')" 
          class="product-card saving-theme"
        >
          <div class="card-top">
            <span class="bank-badge">{{ sub.bank_name }}</span>
            <span class="type-badge saving">적금</span>
          </div>
          <h4 class="product-name">{{ sub.product_name }}</h4>
          <div class="card-bottom">
            <div class="info-group">
              <span class="info-label">금리</span>
              <span class="info-value text-green">{{ sub.option_details.intr_rate }}%</span>
            </div>
            <div class="info-group right">
              <span class="info-label">기간</span>
              <span class="info-value">{{ sub.option_details.save_trm }}개월</span>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <i class="bi bi-inbox"></i>
        <p>아직 가입한 금융 상품이 없습니다.<br>AI 추천을 받아보세요!</p>
        <router-link to="/recommend" class="recommend-link">AI 추천 받으러 가기</router-link>
      </div>
    </div>

    <div v-if="selectedProduct" class="modal-overlay" @click.self="closeModal">
      <div class="custom-modal animate-up">
        <div class="modal-header">
          <h4>상품 상세 정보</h4>
          <button @click="closeModal" class="close-btn"><i class="bi bi-x-lg"></i></button>
        </div>
        <div class="modal-body">
          <div class="product-summary">
            <span class="bank-label">{{ selectedProduct.bank_name }}</span>
            <h3 class="modal-product-name">{{ selectedProduct.product_name }}</h3>
            <div class="amount-display">
              <span class="label">가입 금액</span>
              <span class="amount">{{ formatIncome(selectedProduct.amount) }}</span>
            </div>
          </div>

          <div class="detail-grid">
            <div class="grid-item">
              <span class="label">기간</span>
              <span class="val">{{ selectedProduct.option_details.save_trm }}개월</span>
            </div>
            <div class="grid-item">
              <span class="label">기본 금리</span>
              <span class="val primary">{{ selectedProduct.option_details.intr_rate }}%</span>
            </div>
            <div class="grid-item">
              <span class="label">최고 금리</span>
              <span class="val highlight">{{ selectedProduct.option_details.intr_rate2 }}%</span>
            </div>
          </div>

          <div class="condition-box">
            <span class="box-title">📢 우대 조건</span>
            <p>{{ selectedProduct.special_condition }}</p>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="confirmUnsubscribe" class="unsubscribe-btn">
            해지하기
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'
import { useLedgerStore } from '@/stores/ledgers'

const ledgerStore = useLedgerStore()
const accountStore = useAccountStore()
// --- 이미지 관련 상태 추가 (Script 상단에 넣어주세요) ---
const fileInput = ref(null)      // input 태그 연결용
const selectedFile = ref(null)   // 서버 전송용 파일 객체
const previewUrl = ref(null)     // 화면 미리보기용 URL
const userInfo = ref(null)
const isEditing = ref(false)
const editData = ref(null)
const subscriptions = ref({ deposits: [], savings: [] })
const selectedProduct = ref(null)

const API_URL = 'http://127.0.0.1:8000'

// --- 데이터 로드 ---
const fetchProfile = async () => {
  try {
    const res = await axios.get(`${API_URL}/accounts/profile/`, {
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    userInfo.value = res.data
    // 깊은 복사로 초기화
    editData.value = JSON.parse(JSON.stringify(res.data))
    // 프로필 데이터가 없을 경우를 대비해 초기화
    if (!editData.value.profile) {
      editData.value.profile = { age: null, gender: 'M', income: 0, spending_habits: '보수적' }
    }
  } catch (err) { console.error(err) }
}

const fetchSubscriptions = async () => {
  try {
    const res = await axios.get(`${API_URL}/products/user-subscriptions/`, {
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    subscriptions.value = res.data
  } catch (err) { console.error(err) }
}

// --- 자산 계산 로직 ---
const cashBalance = computed(() => {
  if (!ledgerStore.transactions) return 0
  const income = ledgerStore.transactions
    .filter(t => t.category_type === 'INCOME')
    .reduce((acc, cur) => acc + cur.amount, 0)
  const expense = ledgerStore.transactions
    .filter(t => t.category_type === 'EXPENSE')
    .reduce((acc, cur) => acc + cur.amount, 0)
  return income - expense
})

const totalDepositAmount = computed(() => {
  return (subscriptions.value.deposits || []).reduce((acc, cur) => acc + (cur.amount || 0), 0)
})

const totalSavingAmount = computed(() => {
  return (subscriptions.value.savings || []).reduce((acc, cur) => acc + (cur.amount || 0), 0)
})

const totalAssets = computed(() => {
  return cashBalance.value + totalDepositAmount.value + totalSavingAmount.value
})

// 이미지 경로 계산 (중요: 서버 주소와 합치기)
const displayImageUrl = computed(() => {
  if (previewUrl.value) return previewUrl.value
  const path = userInfo.value?.profile?.image
  if (!path) return null
  return path.startsWith('http') ? path : `${API_URL}${path}`
})

// 이미지 클릭 시 파일 창 열기
const triggerFileInput = () => {
  if (isEditing.value) fileInput.value.click()
}

// 파일 선택 시 미리보기 생성
const onFileChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    selectedFile.value = file
    previewUrl.value = URL.createObjectURL(file)
  }
}

// --- 프로필 수정 로직 (기존 saveProfile을 이 코드로 교체하세요) ---
const saveProfile = async () => {
  try {
    // 이미지를 보내기 위해 FormData 객체 생성
    const formData = new FormData()
    
    // 텍스트 데이터 추가
    formData.append('nickname', editData.value.nickname || '')
    formData.append('age', editData.value.profile.age || '')
    formData.append('gender', editData.value.profile.gender || 'M')
    formData.append('income', editData.value.profile.income || 0)
    formData.append('spending_habits', editData.value.profile.spending_habits || '보수적')

    // 새로 선택한 이미지가 있을 때만 formData에 추가
    if (selectedFile.value) {
      formData.append('profile.image', selectedFile.value)
    }

    const res = await axios.put(`${API_URL}/accounts/profile/`, formData, {
      headers: { 
        Authorization: `Token ${accountStore.token}`,
        'Content-Type': 'multipart/form-data' // 파일 전송 시 필수
      }
    })
    
    userInfo.value = res.data
    isEditing.value = false
    selectedFile.value = null // 초기화
    previewUrl.value = null  // 초기화
    alert('정보가 수정되었습니다.')
    fetchProfile() // 최신 정보 다시 가져오기
  } catch (err) { 
    console.error(err)
    alert('수정 실패: ' + (err.response?.data?.detail || '오류 발생')) 
  }
}

// toggleEdit 함수도 초기화 로직 추가 (선택사항)
const toggleEdit = () => {
  if (isEditing.value) {
    editData.value = JSON.parse(JSON.stringify(userInfo.value))
    previewUrl.value = null   // 취소 시 미리보기 삭제
    selectedFile.value = null // 취소 시 선택 파일 삭제
  }
  isEditing.value = !isEditing.value
}

// --- 모달 로직 ---
const openModal = (product, type) => { selectedProduct.value = { ...product, type } }
const closeModal = () => { selectedProduct.value = null }

const confirmUnsubscribe = async () => {
  if (confirm('정말 해지하시겠습니까? 해당 상품의 가입 정보가 삭제됩니다.')) {
    try {
      const typePath = selectedProduct.value.type === 'deposit' ? 'deposits' : 'savings'
      // URL 경로 주의: /financial/deposit-products/unsubscribe/... 등 백엔드 URL에 맞게 수정 필요
      // 여기서는 사용자가 제공한 코드의 패턴을 따름
      await axios.delete(`${API_URL}/products/${typePath}/unsubscribe/${selectedProduct.value.id}/`, {
        headers: { Authorization: `Token ${accountStore.token}` }
      })
      alert('해지되었습니다.')
      closeModal()
      fetchSubscriptions()
    } catch (err) { 
      console.error(err)
      alert('오류가 발생했습니다.') 
    }
  }
}

// --- 유틸 ---
const totalCount = computed(() => {
  return (subscriptions.value.deposits?.length || 0) + (subscriptions.value.savings?.length || 0)
})

const genderDisplay = computed(() => {
  const g = userInfo.value?.profile?.gender
  return g === 'M' ? '남성' : g === 'F' ? '여성' : '미설정'
})

const formatIncome = (value) => {
  return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' }).format(value || 0)
}

onMounted(() => {
  fetchProfile()
  fetchSubscriptions()
  ledgerStore.getTransactions()
})
</script>

<style scoped>
.view-container {
  max-width: 1200px;
  margin: 50px auto;
  padding: 0 20px;
  min-height: 800px;
}

/* 헤더 */
.header-section { margin-bottom: 40px; }
.page-title { font-size: 2rem; font-weight: 800; color: #333; margin-bottom: 10px; }
.subtitle { color: #666; font-size: 1.1rem; }

/* 1. 프로필 섹션 */
.profile-section { margin-bottom: 40px; }
.profile-card {
  background: white; border-radius: 24px; padding: 40px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  display: flex; gap: 50px; align-items: center; flex-wrap: wrap;
}
.profile-header {
  display: flex; flex-direction: column; align-items: center; text-align: center;
  border-right: 1px solid #eee; padding-right: 50px; min-width: 250px;
}
.avatar-circle {
  width: 100px; height: 100px;
  background: #f0f4ff; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  position: relative; overflow: hidden; /* 이미지가 원을 넘지 않게 함 */
  margin-bottom: 15px;
  transition: 0.3s;
}
.avatar-circle.editable { cursor: pointer; border: 2px solid #2F65F6; }
/* 실제 이미지 스타일 */
.profile-img {
  width: 100%; height: 100%;
  object-fit: cover; /* 사진 비율 유지하며 꽉 채움 */
}

/* 이미지 위 카메라 오버레이 */
.camera-overlay {
  position: absolute; top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.3);
  display: flex; align-items: center; justify-content: center;
  color: white; font-size: 1.5rem;
}

/* 기존 bi-person-fill 색상 유지 */
.default-icon { font-size: 3rem; color: #2F65F6; }

.username { font-size: 1.5rem; font-weight: 800; margin-bottom: 5px; }
.user-badge { background: #eef4ff; color: #2F65F6; font-size: 0.8rem; padding: 4px 10px; border-radius: 20px; font-weight: 700; }
.email { color: #888; font-size: 0.95rem; margin-top: 10px; }
.edit-btn-area { margin-top: 20px; }
.edit-btn, .save-btn, .cancel-btn {
  padding: 8px 20px; border-radius: 20px; font-size: 0.9rem; font-weight: 600; cursor: pointer; transition: 0.2s; border: none;
}
.edit-btn { background: #f8f9fa; color: #555; }
.edit-btn:hover { background: #e9ecef; }
.save-btn { background: #2F65F6; color: white; margin-right: 10px; }
.cancel-btn { background: #eee; color: #555; }

.profile-details { flex-grow: 1; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 30px; }
.detail-item { display: flex; flex-direction: column; }
.detail-item .label { font-size: 0.9rem; color: #888; margin-bottom: 8px; font-weight: 600; }
.detail-item .value { font-size: 1.2rem; font-weight: 700; color: #333; }
.detail-item .value.highlight { color: #2F65F6; }
.edit-input, .edit-select {
  padding: 10px; border: 1px solid #ddd; border-radius: 10px; outline: none; font-size: 1rem;
}
.edit-input:focus, .edit-select:focus { border-color: #2F65F6; }

/* 2. 대시보드 (자산) */
.dashboard-section { margin-bottom: 50px; }
.asset-card {
  background: white; border-radius: 24px; padding: 30px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.03); position: relative; overflow: hidden;
}
/* 총 자산 카드 */
.total-asset {
  background: linear-gradient(135deg, #2F65F6 0%, #5C8AF8 100%);
  color: white; margin-bottom: 20px; padding: 40px;
}
.card-content { position: relative; z-index: 1; }
.total-asset .card-label { font-size: 1.1rem; opacity: 0.9; display: block; margin-bottom: 10px; }
.total-asset .total-amount { font-size: 3rem; font-weight: 800; margin: 0; }
.bg-icon {
  position: absolute; right: 30px; bottom: -10px; font-size: 8rem;
  color: white; opacity: 0.15; transform: rotate(-15deg);
}

/* 서브 자산 그리드 */
.sub-asset-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
.sub-card { display: flex; align-items: center; gap: 20px; transition: transform 0.2s; }
.sub-card:hover { transform: translateY(-5px); }
.icon-box {
  width: 50px; height: 50px; border-radius: 15px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem;
}
.cash .icon-box { background: #eef4ff; color: #2F65F6; }
.deposit .icon-box { background: #e3f2fd; color: #0288d1; }
.saving .icon-box { background: #e8f5e9; color: #198754; }

.text-group { display: flex; flex-direction: column; }
.sub-label { font-size: 0.9rem; color: #888; font-weight: 600; margin-bottom: 5px; }
.sub-amount { font-size: 1.3rem; font-weight: 800; color: #333; }

/* 3. 상품 리스트 */
.subscription-section { margin-bottom: 50px; }
.section-header { margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
.section-title { font-size: 1.5rem; font-weight: 800; color: #333; margin: 0; }
.count-badge { background: #2F65F6; color: white; padding: 2px 10px; border-radius: 12px; font-size: 1rem; }

.product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 20px; }
.product-card {
  background: white; border-radius: 20px; padding: 25px; cursor: pointer;
  border: 1px solid #f0f0f0; transition: all 0.2s; position: relative;
}
.product-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.08); }

/* 테마별 스타일 */
.deposit-theme { border-top: 5px solid #2F65F6; }
.saving-theme { border-top: 5px solid #198754; }

.card-top { display: flex; justify-content: space-between; margin-bottom: 15px; }
.bank-badge { font-weight: 700; color: #666; font-size: 0.9rem; }
.type-badge { background: #eef4ff; color: #2F65F6; padding: 4px 10px; border-radius: 8px; font-size: 0.8rem; font-weight: 700; }
.type-badge.saving { background: #e8f5e9; color: #198754; }

.product-name { font-size: 1.2rem; font-weight: 800; color: #333; margin-bottom: 20px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.card-bottom { display: flex; justify-content: space-between; align-items: flex-end; }
.info-group { display: flex; flex-direction: column; }
.info-label { font-size: 0.8rem; color: #999; margin-bottom: 2px; }
.info-value { font-size: 1.4rem; font-weight: 800; color: #2F65F6; }
.info-value.text-green { color: #198754; }
.info-group.right { text-align: right; }
.info-group.right .info-value { font-size: 1.2rem; color: #555; }

.empty-state {
  text-align: center; padding: 60px 0; background: white; border-radius: 24px; border: 2px dashed #eee;
}
.empty-state i { font-size: 3rem; color: #ddd; margin-bottom: 15px; display: block; }
.empty-state p { color: #888; margin-bottom: 20px; }
.recommend-link { color: #2F65F6; font-weight: 700; text-decoration: none; }

/* 모달 */
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; z-index: 1000;
}
.custom-modal {
  background: white; width: 450px; max-width: 90%; border-radius: 24px; padding: 30px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.2); animation: slideUp 0.3s ease-out;
}
@keyframes slideUp { from { transform: translateY(50px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
.modal-header h4 { margin: 0; font-weight: 800; color: #333; }
.close-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #999; }

.product-summary { text-align: center; margin-bottom: 30px; }
.bank-label { display: inline-block; background: #f5f5f5; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; color: #666; margin-bottom: 10px; font-weight: 600; }
.modal-product-name { font-size: 1.6rem; font-weight: 800; color: #333; margin-bottom: 15px; line-height: 1.3; }
.amount-display { background: #f8fbff; padding: 15px; border-radius: 15px; display: inline-block; width: 100%; }
.amount-display .label { display: block; font-size: 0.9rem; color: #666; margin-bottom: 5px; }
.amount-display .amount { font-size: 1.5rem; font-weight: 800; color: #2F65F6; }

.detail-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 30px; text-align: center; }
.grid-item { background: #fff; border: 1px solid #eee; padding: 15px 5px; border-radius: 12px; }
.grid-item .label { display: block; font-size: 0.8rem; color: #999; margin-bottom: 5px; }
.grid-item .val { font-size: 1.1rem; font-weight: 700; color: #333; }
.grid-item .val.primary { color: #2F65F6; }
.grid-item .val.highlight { color: #f44336; }

.condition-box { background: #f9fafb; padding: 20px; border-radius: 15px; margin-bottom: 30px; }
.box-title { font-weight: 700; font-size: 0.95rem; color: #333; display: block; margin-bottom: 8px; }
.condition-box p { font-size: 0.9rem; color: #555; line-height: 1.6; margin: 0; white-space: pre-line; }

.unsubscribe-btn {
  width: 100%; padding: 15px; border-radius: 15px; border: 1px solid #ffcdd2; background: #ffebee;
  color: #d32f2f; font-weight: 700; cursor: pointer; transition: 0.2s;
}
.unsubscribe-btn:hover { background: #ffcdd2; }

/* 반응형 */
@media (max-width: 768px) {
  .profile-card { flex-direction: column; text-align: center; gap: 30px; padding: 30px; }
  .profile-header { border-right: none; border-bottom: 1px solid #eee; padding-right: 0; padding-bottom: 30px; width: 100%; }
  .profile-details { width: 100%; }
  .total-asset { text-align: center; }
  .bg-icon { display: none; }
}
</style>