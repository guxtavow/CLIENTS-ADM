<template>
  <div class="container">
    <UserTable />
  </div>
</template>

<script>
import UserTable from '@/components/UserTable.vue'

export default {
  components: {
    UserTable
  }
}
</script>

<style>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style>