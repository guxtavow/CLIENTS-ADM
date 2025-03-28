<template>
  <div class="container" v-if="user">
    <div class="flex justify-content-between align-items-center mb-4">
      <h1>User Details: {{ user.username }}</h1>
      <div>
        <Button
          label="Edit"
          icon="pi pi-pencil"
          class="p-button-text mr-2"
          @click="openEditDialog"
        />
        <Button
          label="Delete"
          icon="pi pi-trash"
          class="p-button-text p-button-danger"
          @click="confirmDelete"
        />
      </div>
    </div>

    <div class="p-card">
      <div class="p-card-body">
        <div class="grid p-fluid">
          <div class="col-12 md:col-6">
            <div class="p-field">
              <label>Username</label>
              <p>{{ user.username }}</p>
            </div>
          </div>
          <div class="col-12 md:col-6">
            <div class="p-field">
              <label>Active</label>
              <p>
                <i
                  class="pi"
                  :class="user.active ? 'pi-check-circle text-green-500' : 'pi-times-circle text-red-500'"
                />
                {{ user.active ? 'Yes' : 'No' }}
              </p>
            </div>
          </div>
          <div class="col-12 md:col-6">
            <div class="p-field">
              <label>Roles</label>
              <div>
                <Tag
                  v-for="role in user.roles"
                  :key="role"
                  :value="role"
                  class="mr-2"
                />
              </div>
            </div>
          </div>
          <div class="col-12 md:col-6">
            <div class="p-field">
              <label>Timezone</label>
              <p>{{ user.preferences.timezone }}</p>
            </div>
          </div>
          <div class="col-12 md:col-6">
            <div class="p-field">
              <label>Created At</label>
              <p>{{ formatDate(user.created_ts) }}</p>
            </div>
          </div>
          <div class="col-12 md:col-6">
            <div class="p-field">
              <label>Last Updated</label>
              <p>{{ formatDate(user.last_updated_at) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <Button
      label="Back to Users"
      icon="pi pi-arrow-left"
      class="p-button-text mt-4"
      @click="$router.push('/')"
    />

    <UserDialog
      v-model:visible="showDialog"
      :user="user"
      :isEdit="true"
      @close="closeDialog"
      @save="handleSave"
    />

    <ConfirmDialog />
    <Toast />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useConfirm } from 'primevue/useconfirm'
import { useToast } from 'primevue/usetoast'
import api from '@/services/api'
import UserDialog from '@/components/UserDialog.vue'

export default {
  components: {
    UserDialog
  },
  props: {
    username: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const route = useRoute()
    const router = useRouter()
    const confirm = useConfirm()
    const toast = useToast()
    const user = ref(null)
    const loading = ref(false)
    const showDialog = ref(false)

    const fetchUser = async () => {
      loading.value = true
      try {
        const username = props.username || route.params.username
        user.value = await api.getUser(username)
        if (!user.value) {
          router.push('/')
          toast.add({
            severity: 'warn',
            summary: 'Not Found',
            detail: 'User not found',
            life: 3000
          })
        }
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to fetch user',
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

    const openEditDialog = () => {
      showDialog.value = true
    }

    const closeDialog = () => {
      showDialog.value = false
    }

    const handleSave = async (userData) => {
      try {
        await api.updateUser(user.value.username, userData)
        toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'User updated successfully',
          life: 3000
        })
        fetchUser()
      } catch (error) {
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Failed to update user',
          life: 3000
        })
      }
    }

    const confirmDelete = () => {
      confirm.require({
        message: 'Are you sure you want to delete this user?',
        header: 'Confirmation',
        icon: 'pi pi-exclamation-triangle',
        accept: () => {
          deleteUser()
        }
      })
    }

    const deleteUser = async () => {
      try {
        await api.deleteUser(user.value.username)
        toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'User deleted successfully',
          life: 3000
        })
        router.push('/')
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
      fetchUser()
    })

    return {
      user,
      loading,
      showDialog,
      formatDate,
      openEditDialog,
      closeDialog,
      handleSave,
      confirmDelete
    }
  }
}
</script>

<style scoped>
.p-field {
  margin-bottom: 1.5rem;
}

.p-field label {
  font-weight: bold;
  display: block;
  margin-bottom: 0.5rem;
}

.p-card {
  margin-bottom: 2rem;
}
</style>