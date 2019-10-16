<template>
  <div id="app">
    <Bugit/>
  </div>
</template>

<script>
import Bugit from './components/Bugit.vue'

export default {
  name: 'app',
  components: {
    Bugit
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
