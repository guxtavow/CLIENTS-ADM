<template>
  <div id="app">
    <Toast />
    <router-view />
  </div>
</template>

<script>
import Toast from 'primevue/toast'

export default {
  components: {
    Toast
  }
}
</script>

<style>
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: white;
  background-color: #2c3e50;
  height:100vh ;
  width: 94vw;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.p-card {
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.p-datatable .p-datatable-thead > tr > th {
  background-color: lightblue;
  color: black;
  font-weight: bold;
  font-size: 16px;
  padding: 10px;
  justify-content: center;
  align-items: center;
  text-align: center;
  margin: auto;
  height: 10px;
}

.p-button {
  font-weight: 500;
  transition: all 0.2s;
}

.p-button.p-button-success {
  background: #16a34a;
  border-color: #16a34a;
  
}

.p-button.p-button-success:hover {
  background: #15803d;
  border-color: #15803d;
}

.p-button.p-button-danger {
  background: #dc2626;
  border-color: #dc2626;
}

.p-button.p-button-danger:hover {
  background: #b91c1c;
  border-color: #b91c1c;
}

.p-button.p-button-info {
  background: #2563eb;
  border-color: #2563eb;
}

.p-button.p-button-info:hover {
  background: #1d4ed8;
  border-color: #1d4ed8;
}

.action-buttons .p-button {
  width: 36px;
  height: 36px;
}
</style>