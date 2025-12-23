import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useDepositStore = defineStore('deposit', () => {
  const API_URL = import.meta.env.VITE_API_URL
  const deposits = ref([])

  const getDeposits = function () {
    return axios({
      method: 'get',
      url: `${API_URL}/products/deposit-list/`,
    })
      .then(res => {
        deposits.value = res.data
        return res
      })
      .catch(err => {
        console.log('getDeposits error:', err)
        throw err
      })
  }

  const getDepositDetail = function (id) {
    return axios({
      method: 'get',
      url: `${API_URL}/products/deposits/${id}/`,
    })
  }

  // ✅ 예금 가입 함수 수정
  const subscribeDeposit = function (payload, token) {
    // 1. payload에서 amount를 추가로 꺼내옵니다.
    const { product_id, option_id, amount } = payload
  
    return axios({
      method: 'post',
      url: `${API_URL}/products/deposits/${product_id}/subscribe/`,
      data: {
        option_id: option_id,
        amount: amount // ✅ 2. 서버로 가입 금액을 함께 보냅니다.
      },
      headers: {
        Authorization: `Token ${token}`
      }
    })
  }

  return { deposits, getDeposits, getDepositDetail, subscribeDeposit, API_URL }
}, { persist: true })