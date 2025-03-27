<template>
    <div v-if="isVisible" class="modal-overlay">
      <div class="modal-content">
        <h3>Create User</h3>
  
        <!-- Username -->
        <div class="p-mb-3">
          <label for="username">Username</label>
          <input v-model="newUser.username" id="username" type="text" required />
        </div>
  
        <!-- Roles -->
        <div class="p-mb-3">
          <label>Select Role</label>
          <div v-for="role in roles" :key="role.name">
            <input 
              type="checkbox"
              :id="role.name"
              :value="role.name"
              v-model="newUser.roles" 
            />
            <label :for="role.name">{{ role.name }}</label>
          </div>
        </div>
  
        <!-- Timezone -->
        <div class="p-mb-3">
          <label for="timezone">Select Timezone</label>
          <select v-model="newUser.preferences.timezone" id="timezone">
            <option v-for="timezone in timezones" :key="timezone.code" :value="timezone.code">
              {{ timezone.name }}
            </option>
          </select>
        </div>
  
        <!-- Active Status -->
        <div class="p-mb-3">
          <label for="active">Active</label>
          <input type="checkbox" v-model="newUser.active" id="active" />
        </div>
  
        <!-- Buttons -->
        <div class="modal-actions">
          <Button 
          style="cursor: pointer; color: white; background-color: green; border: none; border-radius: 30px; width:80px; height: 40px;" 
          label="Create" @click="createUser" />
          <Button 
          style="cursor: pointer; color: white; background-color: red; border: none; border-radius: 30px; width:80px; height: 40px;" 
          label="Cancel"  @click="closeDialog" />
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, defineEmits, type PropType } from 'vue';
  
  export default defineComponent({
    props: {
      isVisible: Boolean,
      roles: Array as PropType<{ name: string }[]>,
      timezones: Array as PropType<{ code: string; name: string }[]>,
    },
    emits: ['closeDialog', 'userCreated'],
    setup(_, { emit }) {
      const newUser = ref({
        username: '',
        roles: [],
        preferences: { timezone: '' },
        active: false,
      });
  
      const closeDialog = () => {
        emit('closeDialog');
      };
  
      const createUser = () => {
        if (!newUser.value.username.trim()) {
          alert('Username is required!');
          return;
        }
        emit('userCreated', newUser.value);
        closeDialog();
      };
  
      return { newUser, closeDialog, createUser };
    },
  });
  </script>
  
  <style scoped>
  .p-mb-3 {
    margin: auto;
    margin-bottom: 10px;
    font-weight: bolder;
    display: flex;
    flex-direction: column;
    width: 60%;
   }
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .modal-content {
    width: 400px;
    padding: 20px;
    background-color: rgb(17, 83, 158);
    border-radius: 8px;
  }
  
  .modal-actions {
    margin-top: 20px;
    display: flex;
    justify-content: space-between;
  }
  </style>
  