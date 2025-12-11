import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useDepositStore = defineStore('deposit', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const deposits = ref([])

  const getDeposits = function () {
    axios({
      method: 'get',
      url: `${API_URL}/products/deposit/`,
    })
      .then(res => {
        console.log(res.data)
        deposits.value = res.data
      })
      .catch(err => console.log(err))
  }

  return { deposits, getDeposits, API_URL }
}, { persist: true })
