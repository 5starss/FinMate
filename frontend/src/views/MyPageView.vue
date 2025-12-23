<template>
  <div class="container mt-5">
    <div class="card shadow-sm border-0 mb-4">
      <div class="card-header bg-white py-3 d-flex justify-content-between align-items-center border-bottom">
        <h4 class="mb-0 fw-bold"><i class="bi bi-person-badge me-2 text-primary"></i>내 프로필</h4>
        <div v-if="!isEditing">
          <button @click="toggleEdit" class="btn btn-outline-primary btn-sm rounded-pill px-3">
            <i class="bi bi-pencil me-1"></i>정보 수정
          </button>
        </div>
        <div v-else>
          <button @click="saveProfile" class="btn btn-primary btn-sm me-2 rounded-pill px-3">저장</button>
          <button @click="toggleEdit" class="btn btn-outline-secondary btn-sm rounded-pill px-3">취소</button>
        </div>
      </div>

      <div class="card-body p-4">
        <div class="row" v-if="userInfo">
          <div class="col-md-4 border-end d-flex flex-column align-items-center justify-content-center">
            <div class="rounded-circle bg-light d-inline-flex align-items-center justify-content-center mb-3" style="width: 100px; height: 100px;">
              <i class="bi bi-person-fill text-secondary" style="font-size: 3rem;"></i>
            </div>
            <h5 class="fw-bold mb-1">{{ userInfo.username }}</h5>
            <p class="text-muted small mb-0">{{ userInfo.email }}</p>
          </div>

          <div class="col-md-8 ps-md-5">
            <div class="row g-3">
              <div class="col-6">
                <label class="form-label text-muted small fw-bold">나이</label>
                <div v-if="!isEditing" class="fs-5 fw-semibold">{{ userInfo.profile?.age || '미설정' }}세</div>
                <input v-else type="number" v-model="editData.profile.age" class="form-control form-control-sm">
              </div>
              <div class="col-6">
                <label class="form-label text-muted small fw-bold">성별</label>
                <div v-if="!isEditing" class="fs-5 fw-semibold">{{ genderDisplay }}</div>
                <select v-else v-model="editData.profile.gender" class="form-select form-select-sm">
                  <option value="M">남성</option>
                  <option value="F">여성</option>
                </select>
              </div>
              <div class="col-12">
                <label class="form-label text-muted small fw-bold">연소득</label>
                <div v-if="!isEditing" class="fs-5 fw-semibold">{{ formatIncome(userInfo.profile?.income) }}</div>
                <input v-else type="number" v-model="editData.profile.income" class="form-control form-control-sm" placeholder="숫자만 입력">
              </div>
              <div class="col-12">
                <label class="form-label text-muted small fw-bold">소비 성향</label>
                <div v-if="!isEditing" class="fs-5 fw-semibold text-primary">{{ userInfo.profile?.spending_habits || '미설정' }}</div>
                <select v-else v-model="editData.profile.spending_habits" class="form-select form-select-sm">
                  <option value="보수적">보수적 (안정 추구)</option>
                  <option value="공격적">공격적 (수익 추구)</option>
                  <option value="균형 잡힌">균형 잡힌 소비</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-3 mb-5">
      <div class="col-12">
        <div class="card border-0 shadow-sm bg-primary text-white overflow-hidden">
          <div class="card-body p-4 position-relative">
            <div class="position-relative z-1">
              <h6 class="text-white-50 fw-bold mb-1">나의 총 자산 현황</h6>
              <h1 class="display-5 fw-bold mb-0">{{ formatIncome(totalAssets) }}</h1>
            </div>
            <i class="bi bi-wallet2 position-absolute end-0 bottom-0 text-white-50 m-3" style="font-size: 5rem; opacity: 0.2;"></i>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex align-items-center mb-2">
              <div class="p-2 bg-info-subtle text-info rounded-3 me-2">
                <i class="bi bi-cash-coin"></i>
              </div>
              <span class="text-muted small fw-bold">현금 (가계부 잔액)</span>
            </div>
            <h4 class="fw-bold mb-0 text-dark">{{ formatIncome(cashBalance) }}</h4>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex align-items-center mb-2">
              <div class="p-2 bg-success-subtle text-success rounded-3 me-2">
                <i class="bi bi-piggy-bank"></i>
              </div>
              <span class="text-muted small fw-bold">총 예금액</span>
            </div>
            <h4 class="fw-bold mb-0 text-dark">{{ formatIncome(totalDepositAmount) }}</h4>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body">
            <div class="d-flex align-items-center mb-2">
              <div class="p-2 bg-warning-subtle text-warning rounded-3 me-2">
                <i class="bi bi-graph-up-arrow"></i>
              </div>
              <span class="text-muted small fw-bold">총 적금액</span>
            </div>
            <h4 class="fw-bold mb-0 text-dark">{{ formatIncome(totalSavingAmount) }}</h4>
          </div>
        </div>
      </div>
    </div>

    <section class="mt-4 pb-5">
      <h5 class="fw-bold mb-3">가입 중인 상품 <span class="badge bg-primary ms-1">{{ totalCount }}</span></h5>
      <div class="row g-3">
        <div v-for="sub in subscriptions.deposits" :key="'d-'+sub.id" 
             @click="openModal(sub, 'deposit')" class="col-md-6">
          <div class="card border-0 shadow-sm h-100 hover-card">
            <div class="card-body d-flex align-items-center">
              <div class="icon-box me-3 bg-primary-subtle text-primary rounded-circle">
                <i class="bi bi-piggy-bank fs-4"></i>
              </div>
              <div class="flex-grow-1 overflow-hidden">
                <div class="small text-muted text-truncate">{{ sub.bank_name }}</div>
                <div class="fw-bold text-truncate">{{ sub.product_name }}</div>
              </div>
              <div class="text-end ms-2">
                <div class="text-primary fw-bold">{{ sub.option_details.intr_rate }}%</div>
                <div class="small text-muted">{{ sub.option_details.save_trm }}개월</div>
              </div>
            </div>
          </div>
        </div>
        <div v-for="sub in subscriptions.savings" :key="'s-'+sub.id" 
             @click="openModal(sub, 'saving')" class="col-md-6">
          <div class="card border-0 shadow-sm h-100 hover-card border-start border-success border-4">
            <div class="card-body d-flex align-items-center">
              <div class="icon-box me-3 bg-success-subtle text-success rounded-circle">
                <i class="bi bi-graph-up-arrow fs-4"></i>
              </div>
              <div class="flex-grow-1 overflow-hidden">
                <div class="small text-muted text-truncate">{{ sub.bank_name }}</div>
                <div class="fw-bold text-truncate">{{ sub.product_name }}</div>
              </div>
              <div class="text-end ms-2">
                <div class="text-success fw-bold">{{ sub.option_details.intr_rate }}%</div>
                <div class="small text-muted">{{ sub.option_details.save_trm }}개월</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="totalCount === 0" class="text-center py-5 bg-light rounded border-dashed mt-2">
        <p class="text-muted mb-0">아직 가입한 금융 상품이 없습니다.</p>
      </div>
    </section>
    
    <div v-if="selectedProduct" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content border-0 shadow animate__animated animate__fadeInUp">
        <div class="modal-header border-0">
          <h5 class="fw-bold mb-0">상품 상세 정보</h5>
          <button @click="closeModal" class="btn-close"></button>
        </div>
        <div class="modal-body">
          <div class="text-center mb-4">
            <h4 class="fw-bold text-primary mb-1">{{ selectedProduct.product_name }}</h4>
            <span class="badge bg-light text-dark border">{{ selectedProduct.bank_name }}</span>
          </div>
          <div class="mb-4 text-center">
            <label class="fw-bold small mb-1 text-secondary d-block">가입 금액</label>
              <div class="fs-4 fw-bold text-dark">
                {{ formatIncome(selectedProduct.amount) }}
              </div>
          </div>
          <div class="row g-2 text-center bg-light p-3 rounded-3 mb-4">
            <div class="col-4 border-end">
              <small class="text-muted d-block">기간</small>
              <span class="fw-bold">{{ selectedProduct.option_details.save_trm }}개월</span>
            </div>
            <div class="col-4 border-end">
              <small class="text-muted d-block">기본 금리</small>
              <span class="fw-bold text-primary">{{ selectedProduct.option_details.intr_rate }}%</span>
            </div>
            <div class="col-4">
              <small class="text-muted d-block">최고 금리</small>
              <span class="fw-bold text-danger">{{ selectedProduct.option_details.intr_rate2 }}%</span>
            </div>
          </div>
          <div class="mb-3 px-1">
            <label class="fw-bold small mb-2 text-secondary"><i class="bi bi-info-circle me-1"></i>우대 조건</label>
            <div class="small p-2 bg-light rounded border-start border-3 border-primary" style="max-height: 120px; overflow-y: auto; white-space: pre-line;">
              {{ selectedProduct.special_condition }}
            </div>
          </div>
        </div>
        <div class="modal-footer border-0">
          <button @click="confirmUnsubscribe" class="btn btn-outline-danger w-100 py-2 rounded-pill fw-bold">가입 해지하기</button>
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
    editData.value = JSON.parse(JSON.stringify(res.data))
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

// --- 자산 계산 로직 (신규) ---

// 1. 현금 잔액 (가계부 수입 - 지출)
const cashBalance = computed(() => {
  const income = ledgerStore.transactions
    .filter(t => t.category_type === 'INCOME')
    .reduce((acc, cur) => acc + cur.amount, 0)
  const expense = ledgerStore.transactions
    .filter(t => t.category_type === 'EXPENSE')
    .reduce((acc, cur) => acc + cur.amount, 0)
  return income - expense
})

// 2. 총 예금액
const totalDepositAmount = computed(() => {
  return (subscriptions.value.deposits || []).reduce((acc, cur) => acc + (cur.amount || 0), 0)
})

// 3. 총 적금액
const totalSavingAmount = computed(() => {
  return (subscriptions.value.savings || []).reduce((acc, cur) => acc + (cur.amount || 0), 0)
})

// 4. 합산 총 자산
const totalAssets = computed(() => {
  return cashBalance.value + totalDepositAmount.value + totalSavingAmount.value
})

// --- 프로필 수정/해지/유틸 로직 (기존 유지) ---
const toggleEdit = () => {
  if (isEditing.value) editData.value = JSON.parse(JSON.stringify(userInfo.value))
  isEditing.value = !isEditing.value
}

const saveProfile = async () => {
  try {
    const res = await axios.put(`${API_URL}/accounts/profile/`, editData.value, {
      headers: { Authorization: `Token ${accountStore.token}` }
    })
    userInfo.value = res.data
    isEditing.value = false
    alert('정보가 수정되었습니다.')
  } catch (err) { alert('수정 실패') }
}

const openModal = (product, type) => { selectedProduct.value = { ...product, type } }
const closeModal = () => { selectedProduct.value = null }

const confirmUnsubscribe = async () => {
  if (confirm('정말 해지하시겠습니까?')) {
    try {
      const typePath = selectedProduct.value.type === 'deposit' ? 'deposits' : 'savings'
      await axios.delete(`${API_URL}/products/${typePath}/unsubscribe/${selectedProduct.value.id}/`, {
        headers: { Authorization: `Token ${accountStore.token}` }
      })
      alert('해지되었습니다.')
      closeModal()
      fetchSubscriptions()
    } catch (err) { alert('오류 발생') }
  }
}

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
  ledgerStore.getTransactions() // 가계부 데이터도 로드
})
</script>

<style scoped>
/* 기존 스타일 유지 + 보강 */
.hover-card { transition: all 0.2s ease; cursor: pointer; }
.hover-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important; }
.icon-box { width: 45px; height: 45px; display: flex; align-items: center; justify-content: center; }
.border-dashed { border: 2px dashed #dee2e6; }
.z-1 { z-index: 1; }

.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.4); display: flex; align-items: center; justify-content: center; z-index: 2000;
}
.modal-content { background: white; width: 90%; max-width: 400px; border-radius: 24px; padding: 20px; }
.animate__fadeInUp { animation: fadeInUp 0.4s ease; }
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>