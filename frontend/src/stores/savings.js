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
  
  // ✅ 적금 가입 함수 수정
  const subscribeSaving = function (payload, token) {
    const { product_id, option_id } = payload // payload에서 상품ID와 옵션ID 추출
    
    return axios({
      method: 'post',
      url: `${API_URL}/products/savings/${product_id}/subscribe/`, // Django URL 설정에 따라 수정 가능
      data: {
        option_id: option_id // 서버의 request.data.get('option_id')로 전달됨
      },
      headers: {
        Authorization: `Token ${token}`
      }
  })
  }

// return 객체에 subscribeSaving 추가 필수!
  return { savings, getSavings, getSavingDetail, subscribeSaving, API_URL }
}, { persist: true })
