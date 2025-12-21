<template>
  <div>
    <h3>예금 목록</h3>
    <ul>
      <li v-for="deposit in deposits" :key="deposit.id">
        <router-link :to="`/deposit/${deposit.id}`">
          {{ deposit.kor_co_nm }} - {{ deposit.fin_prdt_nm }}
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  deposits: {
    type: Array,
    required: true
  }
})
</script>
