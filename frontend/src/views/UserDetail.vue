<template>
    <div v-if="user">
      <h1>User Details</h1>
      <p><strong>Username:</strong> {{ user.username }}</p>
      <p><strong>Roles:</strong> {{ user.roles ? user.roles.join(', ') : '-' }}</p>
      <p><strong>Timezone:</strong> {{ user.preferences?.timezone || 'N/A' }}</p>
      <p><strong>Is Active?</strong> {{ user.active ? 'Yes' : 'No' }}</p>

  
      <button
      style="background-color: transparent; border: none; cursor: pointer; font-size:80px; font-weight: bolder; color: gray; " 
      @click="$router.go(-1)">back</button>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue'
  import axios from 'axios'
  import { useRoute } from 'vue-router'

  
  export default defineComponent({
    setup() {
      const route = useRoute()
      const user = ref(null)
  
      const fetchUser = async () => {
        try {
          const response = await axios.get(`http://localhost:5000/user/${route.params.username}`)
          user.value = response.data
        } catch (error) {
          console.error('Erro ao buscar usuário:', error)
        }
      }

      onMounted(fetchUser)
  
      return { user }
    },
  })
  </script>
  
  <style scoped>
    p{
        display: flex;
        flex-direction: column;
        gap:10px;
    }
    .user-details {
        overflow-x: hidden;
    }
    strong{
        text-decoration: underline;
    }


</style>