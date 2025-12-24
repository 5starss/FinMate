import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

export const useLedgerStore = defineStore('ledger', () => {
  const API_URL = import.meta.env.VITE_API_URL
  const accountStore = useAccountStore()
  
  const transactions = ref([])
  const categories = ref([])

  // ✅ 1. 카테고리 목록 가져오기 (필터링 추가)
  // type: 'INCOME', 'EXPENSE' 또는 null(전체)
  const getCategories = function (type = null) {
    let url = `${API_URL}/ledgers/categories/`
    if (type) url += `?type=${type}`

    return axios({
      method: 'get',
      url: url,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then(res => {
        categories.value = res.data
      })
      .catch(err => console.error('카테고리 로드 실패:', err))
  }

  // ✅ 2. 새로운 카테고리 생성 (A방식: 직접 입력 시 백엔드 등록)
  const createCategory = function (payload) {
    // payload 예시: { name: '테니스', type: 'EXPENSE' }
    return axios({
      method: 'post',
      url: `${API_URL}/ledgers/categories/`,
      data: payload,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then(res => {
        // 생성 후 목록을 다시 불러오거나 현재 배열에 추가
        categories.value.push(res.data)
        return res.data // 생성된 카테고리(id 포함)를 반환하여 즉시 선택 가능케 함
      })
      .catch(err => {
        console.error('카테고리 생성 실패:', err)
        throw err
      })
  }

  // ✅ 특정 카테고리 삭제하기 (리뷰 반영)
  const deleteCategory = function (categoryId) {
    return axios({
      method: 'delete',
      url: `${API_URL}/ledgers/categories/${categoryId}/`,
      headers: { Authorization: `Token ${accountStore.token}` }
    })
      .then(() => {
        getCategories() // 삭제 후 카테고리 목록 갱신
      })
      .catch(err => {
        alert('이 카테고리를 사용하는 내역이 있어 삭제할 수 없습니다.')
        console.error(err)
      })
  }

  // ✅ 3. 내역 목록 가져오기 (차트/필터링용 type 추가)
  const getTransactions = function (type = null) {
    let url = `${API_URL}/ledgers/transactions/`
    if (type) url += `?type=${type}`

    return axios({
      method: 'get',
      url: url,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then(res => {
        transactions.value = res.data
      })
      .catch(err => console.error('내역 로드 실패:', err))
  }

  // ✅ 4. 새로운 내역 기록하기
  const createTransaction = function (payload) {
    return axios({
      method: 'post',
      url: `${API_URL}/ledgers/transactions/`,
      data: payload,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then(res => {
        // 저장이 성공하면 목록 갱신
        getTransactions()
        return res
      })
      .catch(err => {
        console.error('내역 저장 실패:', err)
        throw err
      })
  }

  // ✅ 특정 내역 수정하기 (PATCH/PUT)
  const updateTransaction = function (transactionId, payload) {
    return axios({
      method: 'put',
      url: `${API_URL}/ledgers/transactions/${transactionId}/`,
      data: payload,
      headers: { Authorization: `Token ${accountStore.token}` }
    })
      .then(res => {
        getTransactions() // 수정 후 목록 갱신
        return res.data
      })
  }

  // ✅ 5. 삭제 기능
  const deleteTransaction = function (transactionId) {
    return axios({
      method: 'delete',
      url: `${API_URL}/ledgers/transactions/${transactionId}/`,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then(res => {
        getTransactions()
      })
      .catch(err => console.error('삭제 실패:', err))
  }

  return { 
    transactions, 
    categories, 
    getCategories, 
    createCategory,
    getTransactions, 
    createTransaction,
    deleteTransaction,
    updateTransaction,
    deleteCategory,
  }
}, { persist: true })