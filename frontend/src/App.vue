<template>
  <header>
    <nav>
      <RouterLink :to="{ name: 'HomeView' }">홈으로</RouterLink>
      <RouterLink :to="{ name: 'DepositView' }">예금</RouterLink>
      <RouterLink :to="{ name: 'SavingView' }">적금</RouterLink>
    </nav>
  </header>
  <RouterView />
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router'
</script>

<style>

</style>
