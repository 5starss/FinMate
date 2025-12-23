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

  const subscribeDeposit = function (payload, token) {
  const { product_id, option_id } = payload
  
  return axios({
    method: 'post',
    url: `${API_URL}/products/deposits/${product_id}/subscribe/`,
    data: {
      option_id: option_id
    },
    headers: {
      Authorization: `Token ${token}`
    }
  })
}

  return { deposits, getDeposits, getDepositDetail, subscribeDeposit, API_URL }
}, { persist: true })