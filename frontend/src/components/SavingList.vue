<template>
  <div>
    <h3>적금 목록</h3>
    <ul>
      <li 
        v-for="saving in savings" 
        :key="saving.id"
      >
        {{ saving.kor_co_nm }} - {{ saving.fin_prdt_nm }}
      </li>
    </ul>
  </div>
</template>

<script setup>
// ✅ store 제거
defineProps({
  savings: {
    type: Array,
    required: true
  }
})
</script>
