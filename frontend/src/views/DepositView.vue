<template>
    <div>
      <h1>예금</h1>
    </div>
    <DepositList />
</template>

<script setup>
  import { onMounted } from 'vue'
  import { useDepositStore } from '@/stores/deposits'
  import DepositList from '@/components/DepositList.vue'

  const store = useDepositStore()

  onMounted(() => {
    store.getDeposits()
  })
</script>

<style>

</style>