<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="app-container">
    <RouterView />
  </div>
</template>

<style scoped>
/* Add some basic layout/background styles based on styling.md */
#app-container {
  min-height: 100vh; /* Ensure it takes full viewport height */
  background-color: #f8fbef; /* light ivory */
  color: #212121; /* dark gray */
  padding: 1rem; /* Add some padding around the content */
  box-sizing: border-box;
}

/* You might add more global styles here or keep them component-specific */
</style>