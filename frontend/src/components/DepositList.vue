<template>
    <div>
      <h3>예금 목록</h3>
      <!-- <ArticleListItem 
        v-for="article in store.articles"
        :key="article.id"
        :article="article"
      /> -->
      <ul>
          <li 
          v-for="deposit in store.deposits" 
          :key="deposit.id"
          >
          {{ deposit.kor_co_nm }} - {{ deposit.fin_prdt_nm }}
          </li>
      </ul>
    </div>
  </template>
  
  <script setup>
    import { useDepositStore } from '@/stores/deposits'
    // import ArticleListItem from '@/components/ArticleListItem.vue'
  
    const store = useDepositStore()
    console.log(store.deposits)
  
  </script>