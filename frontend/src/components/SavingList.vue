<template>
  <div>
    <h3>적금 목록</h3>
    <ul>
      <li 
        v-for="saving in savings" 
        :key="saving.id"
      >
        <router-link :to="`/saving/${saving.id}`">
          {{ saving.kor_co_nm }} - {{ saving.fin_prdt_nm }}
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  savings: {
    type: Array,
    required: true
  }
})
</script>
