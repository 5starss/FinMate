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
  box-sizing: border-box;
}
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* 화면 전체 높이 사용 */
}

/* 헤더 밑에 들어가는 콘텐츠 영역 */
.content-wrapper {
  flex: 1; /* 남은 공간을 모두 차지함 (핵심!) */
  display: flex;
  flex-direction: column;
}

</style>

