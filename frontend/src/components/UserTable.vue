<template>
  <div>
    <div class="flex justify-content-between align-items-center mb-4">
      <h1 class="text-3xl font-bold">User Management</h1>
      <Button
        label="Create User"
        icon="pi pi-plus"
        @click="openCreateDialog"
      />
    </div>

    <DataTable
      :value="users"
      :paginator="true"
      :rows="5"
      :loading="loading"
      paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
      :rowsPerPageOptions="[5,10]"
      currentPageReportTemplate="Showing {first} to {last} of {totalRecords} users"
      class="tableData"
    >
      <Column field="username" header="Username" :sortable="true">
        <template #body="{ data }">
          <router-link :to="`/user/${data.username}`">{{ data.username }}</router-link>
        </template>
      </Column>
      <Column field="roles" header="Roles" :sortable="true" class="text-center">
        <template #body="{ data }">
          <span 
          v-for="(role, index) in data.roles" 
          :key="role"
          class="role-badge"
        >
            {{ role.toUpperCase() }}
            <span v-if="index < data.roles.length - 1">, </span>
          </span>
        </template>
      </Column>
      <Column field="preferences.timezone" header="Timezone" :sortable="true" class="text-center" />
      <Column field="active" header="Active" :sortable="true" class="text-center">
        <template #body="{ data }">
          <i
            class="pi"
            :class="data.active ? 'pi-check-circle text-green-500' : 'pi-times-circle text-red-500'"
          />
        </template>
      </Column>
      <Column field="last_updated_at" header="Last Updated" :sortable="true" class="text-center">
        <template #body="{ data }">
          {{ formatDate(data.last_updated_at) }}
        </template>
      </Column>
      <Column field="created_ts" header="Created At" :sortable="true">
        <template #body="{ data }">
          <span class="date-text">
          {{ formatDate(data.created_ts) }}
        </span>
        </template>
      </Column>
    </DataTable>

    <UserDialog
      v-model:visible="showDialog"
      :user="selectedUser"
      :isEdit="isEdit"
      @close="closeDialog"
      @save="handleSave"
    />

    <ConfirmDialog />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useConfirm } from 'primevue/useconfirm'
import { useToast } from 'primevue/usetoast'
import api from '../services/api'
import UserDialog from './UserDialog.vue'

export default {
  components: {
    UserDialog
  },
  setup() {
    const confirm = useConfirm()
    const toast = useToast()
    const users = ref([])
    const loading = ref(false)
    const showDialog = ref(false)
    const selectedUser = ref(null)
    const isEdit = ref(false)

    const fetchUsers = async () => {
      loading.value = true
      try {
        users.value = await api.getUsers()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to fetch users',
          life: 3000
        })
      } finally {
        loading.value = false
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString()
    }

    const openCreateDialog = () => {
      selectedUser.value = null
      isEdit.value = false
      showDialog.value = true
    }

    const openEditDialog = (user) => {
      selectedUser.value = { ...user }
      isEdit.value = true
      showDialog.value = true
    }

    const closeDialog = () => {
      showDialog.value = false
    }

    const handleSave = async (userData) => {
      try {
        if (isEdit.value) {
          await api.updateUser(selectedUser.value.username, userData)
          toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'User updated successfully',
            life: 3000
          })
        } else {
          await api.createUser(userData)
          toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'User created successfully',
            life: 3000
          })
        }
        fetchUsers()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: isEdit.value ? 'Failed to update user' : 'Failed to create user',
          life: 3000
        })
      }
    }

    const confirmDelete = (username) => {
      confirm.require({
        message: 'Are you sure you want to delete this user?',
        header: 'Confirmation',
        icon: 'pi pi-exclamation-triangle',
        accept: () => {
          deleteUser(username)
        }
      })
    }

    const deleteUser = async (username) => {
      try {
        await api.deleteUser(username)
        toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'User deleted successfully',
          life: 3000
        })
        fetchUsers()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to delete user',
          life: 3000
        })
      }
    }

    onMounted(() => {
      fetchUsers()
    })

    return {
      users,
      loading,
      showDialog,
      selectedUser,
      isEdit,
      formatDate,
      openCreateDialog,
      openEditDialog,
      closeDialog,
      handleSave,
      confirmDelete
    }
  }
}
</script>

<style scoped>
.p-button {
  margin-right: 10px;
  margin: 10px;
  gap: 15px;
  width: 105px;
  height: 40px;
  border-radius:30px ;
  background-color: #007BFF;
  color: white;
}
.role-badge{
  margin: 10px;
}
.date-text{
  margin: 30px;
}
.pi{
  margin: 20px;
}

</style>