<template>
  <HeaderNavbar />

  <div class="app-container">
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import HeaderNavbar from '@/components/HeaderNavbar.vue'

  const accountStore = useAccountStore()
  const logOut = function () {
    accountStore.logOut()
  }
</script>

<style>
body {
  margin: 0;
  padding: 0;
}
.app-container {
  /* 헤더 높이만큼 띄우거나, 전체 레이아웃 잡을 때 사용 */
  width: 100%;
  min-height: 100vh;
}
</style>
