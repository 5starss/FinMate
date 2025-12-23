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
  
  const subscribeSaving = function (productId, token) {
  return axios({
    method: 'post',
    url: `${API_URL}/products/savings/${productId}/subscribe/`,
    headers: {
      Authorization: `Token ${token}`
    }
  })
  }

// return 객체에 subscribeSaving 추가 필수!
  return { savings, getSavings, getSavingDetail, subscribeSaving, API_URL }
}, { persist: true })
