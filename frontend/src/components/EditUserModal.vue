<template>
  <div v-if="isVisible" class="modal-overlay">
    <div class="modal-content">
      <h3>Edit User</h3>

      <!-- Edit Username -->
      <div class="p-mb-3">
        <label for="username">Username</label>
        <input v-model="editedUser.username" id="username" type="text" disabled class="p-inputtext" />
      </div>

      <!-- Roles -->
      <div class="p-mb-3">
        <label>Select Roles</label>
        <div v-for="role in roles" :key="role.name">
          <input 
            type="checkbox" 
            :id="role.name" 
            :value="role.name"
            v-model="editedUser.roles" 
          />
          <label :for="role.name">{{ role.name }}</label>
        </div>
      </div>

      <!-- Timezone -->
      <div class="p-mb-3">
        <label for="timezone">Select Timezone</label>
        <select v-model="editedUser.preferences.timezone" id="timezone">
          <option v-for="timezone in timezones" :key="timezone.code" :value="timezone.code ">
            {{ timezone.name }}
          </option>
        </select>
      </div>

      <!-- Active Status -->
      <div class="p-mb-3">
        <label for="active">Active</label>
        <input type="checkbox" v-model="editedUser.active" id="active" />
      </div>

      <!-- Buttons -->
      <div class="modal-actions">
        <button 
        style="cursor: pointer; color: white; background-color: green; border: none; border-radius: 30px; width:80px;height: 40px;" 
        @click="updateUser()">Save</button>
        <button 
        style="cursor: pointer; color: white; background-color: red; border: none; border-radius: 30px; width:80px; height: 40px;" 
        @click="closeDialog">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch, type PropType } from 'vue'

export default defineComponent({
  props: {
    isVisible: Boolean,
    user: Object as PropType<any>,
    roles: Array as PropType<{ name: string }[]>,
    timezones: Array as PropType<{ code: string; name: string }[]>
  },
  emits: ['closeDialog', 'updateUser'],
  setup(props, { emit }) {
    const editedUser = ref({ ...props.user });

    watch(() => props.user, (newUser) => {
      if (newUser) {
        editedUser.value = { ...newUser };
      }
    }, { deep: true });

    const closeDialog = () => {
      emit('closeDialog');
    };

    const updateUser = () => {
      emit('updateUser', editedUser.value);
    };

    return { editedUser, closeDialog, updateUser };
  },
});
</script>

<style scoped>
label{
  font-weight: bold;
  margin: 5px;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: rgb(35, 76, 95);
  color: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
}

.modal-actions {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  
}

.p-mb-3 {
  margin-bottom: 1rem;
  gap:5px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin: auto;
  width: 70%;
}

</style>
