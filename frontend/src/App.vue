<script setup>
// App.vue 作为根组件，路由配置已在 main.js 中设置
</script>

<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<style>
/* 全局样式 */
body {
  margin: 0;
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
}

#app {
  min-height: 100vh;
}
</style>
