<template>
    <div>
      <h3>적금 목록</h3>
      <!-- <ArticleListItem 
        v-for="article in store.articles"
        :key="article.id"
        :article="article"
      /> -->
      <ul>
          <li 
          v-for="saving in store.savings" 
          :key="saving.id"
          >
          {{ saving.kor_co_nm }} - {{ saving.fin_prdt_nm }}
          </li>
      </ul>
    </div>
  </template>
  
  <script setup>
    import { useSavingStore } from '@/stores/savings'
  
    const store = useSavingStore()
    console.log(store.savings)
  
  </script>