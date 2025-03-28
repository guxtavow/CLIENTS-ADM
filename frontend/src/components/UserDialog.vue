<template>
  <Dialog
    v-model:visible="visible"
    :header="isEdit ? 'Edit User' : 'Create User'"
    :modal="true"
    :style="{ width: '50vw' }"
    :breakpoints="{ '960px': '75vw', '641px': '90vw' }"
    class="dialog-container"
  >
    <div class="p-fluid">
      <div class="p-field">
        <label for="username">Username</label>
        <InputText
          id="username"
          v-model="userData.username"
          :disabled="isEdit"
          placeholder="Enter username"
          required
        />
      </div>

      <div class="p-field">
        <label for="timezone">Timezone</label>
        <select
          id="timezone"
          v-model="userData.preferences.timezone"
          class="custom-select"
          required
        >
          <option value="" disabled>Select a timezone</option>
          <option
            v-for="tz in timezones"
            :key="tz.value"
            :value="tz.value"
          >
            {{ tz.label }}
          </option>
        </select>
      </div>

      <div class="p-field">
      <label for="roles">User Roles</label>
      <div class="select-wrapper">
        <select
          id="roles"
          v-model="userData.roles"
          class="role-select"
          multiple
          size="4"
        >
          <option
            v-for="role in availableRoles"
            :key="role.value"
            :value="role.value"
            class="role-option"
          >
            {{ role.label }}
          </option>
        </select>
        <div class="selected-roles" v-if="userData.roles.length > 0">
          Selected: {{ selectedRolesLabels.join(', ') }}
        </div>
      </div>
    </div>

      <div class="p-field-checkbox">
        <Checkbox
          id="active"
          v-model="userData.active"
          :binary="true"
        />
        <label for="active">Active user</label>
      </div>
    </div>

    <template #footer>
      <Button
        label="Cancel"
        icon="pi pi-times"
        @click="closeDialog"
        class="p-button-text"
      />
      <Button
        label="Save"
        icon="pi pi-check"
        @click="submitForm"
        autofocus
      />
    </template>
  </Dialog>
</template>

<script lang="ts">
import { defineComponent, type PropType, ref, watch } from 'vue'
import { useToast } from 'primevue/usetoast'
import type { User, UserFormData } from '@/interface/user.interface'

interface TimezoneOption {
  label: string
  value: string
}

interface RoleOption {
  label: string
  value: string
}

export default defineComponent({
  name: 'UserDialog',
  props: {
    visible: {
      type: Boolean,
      required: true,
    },
    user: {
      type: Object as PropType<User | null>,
      default: null,
    },
    isEdit: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['close', 'save'],
  setup(props, { emit }) {
    const toast = useToast()
    const timezones: TimezoneOption[] = [
      { label: 'America/New_York', value: 'America/New_York' },
      { label: 'Europe/London', value: 'Europe/London' },
      { label: 'Asia/Tokyo', value: 'Asia/Tokyo' },
      { label: 'Australia/Sydney', value: 'Australia/Sydney' },
    ]
    const availableRoles: RoleOption[] = [
      { label: 'Admin', value: 'admin' },
      { label: 'Manager', value: 'manager' },
      { label: 'User', value: 'user' },
    ]

    const defaultUserData: UserFormData = {
      username: '',
      password: '', // Mantido no modelo mas não será usado no formulário
      active: true,
      roles: [],
      preferences: {
        timezone: 'America/New_York',
      },
    }

    const userData = ref<UserFormData>({ ...defaultUserData })

    watch(
      () => props.user,
      (newUser) => {
        if (newUser) {
          userData.value = {
            username: newUser.username,
            password: newUser.password || '', // Mantém a senha existente para edição
            active: newUser.active,
            roles: [...newUser.roles],
            preferences: {
              timezone: newUser.preferences.timezone,
            },
          }
        } else {
          userData.value = { ...defaultUserData }
        }
      }
    )

    const closeDialog = () => {
      emit('close')
    }

    const submitForm = () => {
      if (!userData.value.username) {
        toast.add({
          severity: 'error',
          summary: 'Validation Error',
          detail: 'Username is required',
          life: 3000,
        })
        return
      }

      emit('save', { ...userData.value })
      closeDialog()
    }

    return {
      userData,
      timezones,
      availableRoles,
      closeDialog,
      submitForm,
    }
  },
})
</script>

<style scoped>
.dialog-container ::v-deep(.p-dialog-content) {
  background: black;
  padding: 2rem;
}

.p-fluid {
  background: white;
  padding: 1rem;
  border-radius: 8px;
}

.p-field {
  margin-bottom: 1.5rem;
  color: black;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: black;
  font-weight: 500;
}

.custom-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid black;
  border-radius: 6px;
  background-color: #f8fafc;
  color: #1a202c;
}

.custom-select[multiple] {
  min-height: 120px;
}

.p-field-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: black;
}

.p-button {
  transition: all 0.2s;
  color: #1a202c;
}
.dialog-container{
  background-color: white;
}
</style>