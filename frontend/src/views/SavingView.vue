<template>
    <div>
      <h1>적금</h1>
    </div>
    <SavingList />
</template>

<script setup>
  import { onMounted } from 'vue'
  import { useSavingStore } from '@/stores/savings'
  import SavingList from '@/components/SavingList.vue'

  const store = useSavingStore()

  onMounted(() => {
    store.getSavings()
  })
</script>

<style>

</style>