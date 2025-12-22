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
      url: `${API_URL}/products/saving/`,
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
      url: `${API_URL}/products/api/savings/${id}/`,
    })
  }
  
  return {
    savings,
    getSavings,
    getSavingDetail,
    API_URL,
  }
}, { persist: true })
