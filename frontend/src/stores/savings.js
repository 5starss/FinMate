import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useSavingStore = defineStore('saving', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const savings = ref([])

  const getSavings = function () {
    axios({
      method: 'get',
      url: `${API_URL}/products/saving/`,
    })
      .then(res => {
        console.log(res.data)
        savings.value = res.data
      })
      .catch(err => console.log(err))
  }

  return { savings, getSavings, API_URL }
}, { persist: true })
