<template>
  <div class="app-container">
    <HeaderNavbar />

    <div class="content-wrapper">
      <RouterView />
    </div>

    <FooterSection />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import HeaderNavbar from '@/components/HeaderNavbar.vue'
import FooterSection from '@/components/FooterSection.vue' 
</script>

<style>
/* 전역 스타일 (이미 적용되어 있다면 그대로 두세요) */
body, html {
  margin: 0;
  padding: 0;
  height: 100%;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* 화면 꽉 채우기 */
}

.content-wrapper {
  flex: 1; /* 남은 공간 모두 차지 */
  display: flex;
  flex-direction: column;
}
</style>