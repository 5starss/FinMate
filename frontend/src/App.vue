<template>
  <header>
    <nav>
      <RouterLink :to="{ name: 'HomeView' }">홈으로</RouterLink> |
      <RouterLink :to="{ name: 'DepositView' }">예금</RouterLink> |
      <RouterLink :to="{ name: 'SavingView' }">적금</RouterLink> |
      <RouterLink :to="{ name: 'SignUpView' }">SignUpPage</RouterLink> |
      <RouterLink :to="{ name: 'LogInView' }">LogInPage</RouterLink> | 
      <RouterLink :to="{ name: 'SearchView' }">비디오 검색</RouterLink> |
      <RouterLink :to="{ name: 'MapView' }">지도</RouterLink> |
      <form @submit.prevent="logOut">
        <input type="submit" value="LogOut">
      </form>
    </nav>
  </header>
  <RouterView />
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

  const accountStore = useAccountStore()
  const logOut = function () {
    accountStore.logOut()
  }
</script>

<style>

</style>
