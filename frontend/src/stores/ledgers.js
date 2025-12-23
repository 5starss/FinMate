import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from '@/stores/accounts'

export const useLedgerStore = defineStore('ledger', () => {
  const API_URL = import.meta.env.VITE_API_URL
  const accountStore = useAccountStore()
  
  const transactions = ref([])
  const categories = ref([])

  // ✅ 1. 카테고리 목록 가져오기 (입력 폼의 Select 박스용)
  const getCategories = function () {
    return axios({
      method: 'get',
      url: `${API_URL}/ledgers/categories/`,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then(res => {
        categories.value = res.data
      })
      .catch(err => console.error('카테고리 로드 실패:', err))
  }

  // ✅ 2. 내역 목록 가져오기
  const getTransactions = function () {
    return axios({
      method: 'get',
      url: `${API_URL}/ledgers/transactions/`,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then(res => {
        transactions.value = res.data
      })
      .catch(err => console.error('내역 로드 실패:', err))
  }

  // ✅ 3. 새로운 내역 기록하기 (Create)
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
        // 저장이 성공하면 목록을 다시 불러와서 화면을 갱신합니다.
        getTransactions()
        return res
      })
      .catch(err => {
        console.error('내역 저장 실패:', err)
        throw err
      })
  }

  // 4. 삭제 기능 추가
  const deleteTransaction = function (transactionId) {
    return axios({
      method: 'delete',
      url: `${API_URL}/ledgers/transactions/${transactionId}/`,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then(res => {
        // 삭제 성공 후 목록을 다시 불러와서 화면 동기화
        getTransactions()
      })
      .catch(err => console.error('삭제 실패:', err))
  }
  return { 
    transactions, 
    categories, 
    getCategories, 
    getTransactions, 
    createTransaction,
    deleteTransaction
  }
}, { persist: true })