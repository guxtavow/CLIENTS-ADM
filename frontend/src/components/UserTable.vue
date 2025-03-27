<template>
    <div>
      <Button label="Criar Usuário" icon="pi pi-plus" class="p-button-success mb-3" @click="openCreatingUser" />
      
      <table v-if="users.length > 0" class="p-datatable p-component">
        <thead>
          <tr>
            <th>Username</th>
            <th>Roles</th>
            <th>Timezone</th>
            <th>Is Active?</th>
            <th>Last Updated At</th>
            <th>Created At</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(user, index) in users" :key="user.username">
            <td>
              <router-link :to="'/user/' + user.username"
              style="color: green; text-decoration: none;"
              >
              {{ user.username }}
              </router-link>
            </td>
            <td>{{ user.roles ? user.roles.join(', ') : '-' }}</td>
            <td>{{ user.preferences?.timezone || 'N/A' }}</td>
            <td>
              <i 
                :class="user.active ? 'pi pi-check-circle' : 'pi pi-times-circle'"
                :style="{ color: user.active ? 'green' : 'red' }"
              ></i>
            </td>
            <td>{{ formatDate(user.last_updated_at) }}</td>
            <td>{{ formatDate(user.created_ts) }}</td>
            <td>
              <Button icon="pi pi-pencil" @click="editUser(user)" ></Button>
              <Button icon="pi pi-trash" class="p-button-danger" @click="deleteUser(user.username)" ></Button>
            </td>
          </tr>
        </tbody>
      </table>
  
      <p v-else>Carregando usuários...</p>
  
      <!-- Edit User Modal -->
      <EditUserModal 
        :isVisible="isDialogVisible"
        :user="editedUser"
        :roles="roles"
        :timezones="timezones"
        @updateUser="updateUser"
        @closeDialog="closeDialog"
      />

      <!-- Create User Modal -->
      <CreateUserModal
        :isVisible="isDialogVisibleCreate"
        :roles="roles"
        :timezones="timezones"
        @userCreated="createUser"
        @closeDialog="closeCreateDialog"
      />
    </div>
  </template>
  
  <script lang="ts">
  import axios from 'axios'
  import { ref, onMounted } from 'vue'
  import EditUserModal from './EditUserModal.vue'
  import CreateUserModal from './CreateUserModal.vue'
  
  export default {
    components: {
      EditUserModal,
      CreateUserModal
    },
    setup() {
      const users = ref([])
      const roles = ref([
        { name: 'admin' },
        { name: 'user' },
        { name: 'manager' },
      ])
       // timezones
      const timezones = ref([
        { code: 'America/New_York', name: 'America/New_York' },
        { code: 'America/Los_Angeles', name: 'America/Los_Angeles' },
        { code: 'Europe/London', name: 'Europe/London' },
        { code: 'Asia/Tokyo', name: 'Asia/Tokyo' },
        { code: 'Europe/Berlin', name: 'Europe/Berlin' },
        { code: 'Australia/Sydney', name: 'Australia/Sydney' },
        { code: 'America/Los_Angeles', name: 'America/Los_Angeles' },
        { code: 'Asia/Singapore', name: 'Asia/Singapore' },
        { code: 'America/Chicago', name: 'America/Chicago' },
        { code: 'Europe/Paris', name: 'Europe/Paris' },
        { code: 'Asia/Dubai', name: 'Asia/Dubai' },
        { code: 'America/Toronto', name: 'America/Toronto' },
        { code: 'Europe/Rome', name: 'Europe/Rome' },
        { code: 'Asia/Hong_Kong', name: 'Asia/Hong_Kong' },
        { code: 'America/Denver', name: 'America/Denver' },
        { code: 'Europe/Amsterdam', name: 'Europe/Amsterdam' },
        { code: 'Australia/Melbourne', name: 'Australia/Melbourne' },
        { code: 'America/Phoenix', name: 'America/Phoenix' },
        { code: 'Europe/Moscow', name: 'Europe/Moscow' },
        { code: 'Asia/Seoul', name: 'Asia/Seoul' },
        { code: 'America/Sao_Paulo', name: 'America/Sao_Paulo' },
        { code: 'Europe/Vienna', name: 'Europe/Vienna' },
        { code: 'Asia/Bangkok', name: 'Asia/Bangkok' },
        { code: 'America/Vancouver', name: 'America/Vancouver' },
        { code: 'Australia/Perth', name: 'Australia/Perth' },
        { code: 'America/Mexico_City', name: 'America/Mexico_City' },
        { code: 'Europe/Stockholm', name: 'Europe/Stockholm' },
        { code: 'Asia/Kolkata', name: 'Asia/Kolkata' },
        { code: 'America/Buenos_Aires', name: 'America/Buenos_Aires' },
      ])
      const isDialogVisible = ref(false)
      const isDialogVisibleCreate = ref(false)
      const editedUser = ref(null)
      
  
      const fetchUsers = async () => {
      try {
        console.log("Buscando usuários...");  // 🔍 Debug
        const response = await axios.get('http://localhost:5000/users');
        
        if (response.data.length === 0) {
          console.warn("⚠️ Nenhum usuário encontrado!");
        } else {
          users.value = response.data.map((user: any) => ({
            ...user,
            created_ts: user.created_ts || 'N/A',
            last_updated_at: user.last_updated_at || 'N/A',
            roles: Array.isArray(user.roles) ? user.roles : [], 
            preferences: user.preferences || {},
          }));
          console.log("Usuários carregados:", users.value);
        }
      } catch (error) {
        console.error('Erro ao buscar usuários:', error);
      }
    }

      const formatDate = (timestamp: number) => {
        if (!timestamp) return 'N/A'
        return new Date(timestamp).toLocaleString()
      };
  
      const deleteUser = async (username: string) => {
        try {
          await axios.delete(`http://localhost:5000/users/${username}`)
          fetchUsers()
        } catch (error) {
          console.error('Erro ao deletar usuário:', error)
        }
      }
      const openCreatingUser = () => {
        isDialogVisibleCreate.value = true
      }

      const closeCreateDialog = () => {
        isDialogVisibleCreate.value = false
      }
  
      const editUser = (user: any) => {
        editedUser.value = { ...user }
        isDialogVisible.value = true
      }

      const closeDialog = () => {
        isDialogVisible.value = false
      }
  
      //update user function
      const updateUser = async (user:any) => {
        try {
          await axios.put(`http://localhost:5000/update_users/${user.username}`, user)
          fetchUsers()
          closeDialog()
        } catch (error) {
          console.error('Erro ao atualizar usuário:', error)
        }
      }
  
      // create user function
      const createUser = async(user: any) =>{
        try {
          await axios.post('http://localhost:5000/new_users', user,{
            headers: { 'Content-Type': 'application/json' }
          })
          await fetchUsers()
          closeDialog()
        } catch (error) {
          console.error('Erro ao criar usuário:', error)
        }
      }
      onMounted(fetchUsers);
  
      return {       
        users, fetchUsers, deleteUser, isDialogVisibleCreate, closeCreateDialog, editUser, formatDate, openCreatingUser, isDialogVisible, editedUser, createUser, roles, timezones, updateUser, closeDialog };
    }
  };
  </script>
  
  <style scoped>
  
  .p-button {
    margin: 10px;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th, td {
    padding: 10px;
    text-align: center;
  }
  
  td {
    color: white;
    font-size: medium;
  }
  
  th {
    background-color: #4076a0;
    font-weight: bolder;
    font-size: larger;
  }
  
  tr:nth-child(even) {
    background-color: #272424;
  }
  
  tr:hover {
    background-color: #5c835b;
  }
  </style>
  