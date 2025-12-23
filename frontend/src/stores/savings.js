import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useSavingStore = defineStore('saving', () => {
  const API_URL = import.meta.env.VITE_API_URL
  const savings = ref([])

  // ✅ 목록 조회
  const getSavings = function () {
    return axios({
      method: 'get',
      url: `${API_URL}/products/saving-list/`,
    })
      .then(res => {
        savings.value = res.data
        return res
      })
      .catch(err => {
        console.log(err)
        throw err
      })
  }

  // ✅ 상세 조회
  const getSavingDetail = function (id) {
    return axios({
      method: 'get',
      url: `${API_URL}/products/savings/${id}/`,
    })
  }
  
  // ✅ 적금 가입 함수 (수정됨)
  const subscribeSaving = function (payload, token) {
    // 1. payload에서 필요한 모든 값을 추출 (amount 추가!)
    const { product_id, option_id, amount } = payload 
    
    return axios({
      method: 'post',
      url: `${API_URL}/products/savings/${product_id}/subscribe/`,
      data: {
        option_id: option_id,
        amount: amount // ✅ 2. 쉼표(,) 추가 및 데이터 매칭 완료
      },
      headers: {
        Authorization: `Token ${token}`
      }
    })
  }

// return 객체에 subscribeSaving 추가 필수!
  return { savings, getSavings, getSavingDetail, subscribeSaving, API_URL }
}, { persist: true })