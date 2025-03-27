<template>
  <div id="app">
    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin: 20px;
}

header {
  background: #007ad9;
  color: white;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 20px;
}

main {
  padding: 20px;
}
</style>
