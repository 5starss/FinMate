import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useSavingStore = defineStore('saving', () => {
  const API_URL = import.meta.env.VITE_API_URL
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
