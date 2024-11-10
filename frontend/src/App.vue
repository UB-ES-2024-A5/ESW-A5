<template>
  <div id="app">
    <router-link to="/">
      <img :src="logo" alt="Logo" class="app-logo" />
    </router-link>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
      logo: require('@/assets/logo_book1.png') // Ruta hacia el logo en assets
    }
  }
}
</script>

<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0;
  padding-top: 20px; /* Aumenta si necesitas espacio adicional alrededor del logo */
}

/* Posiciona el logo en la esquina superior izquierda */
.app-logo {
  position: absolute;
  top: 20px; /* Ajusta para posicionarlo correctamente en la página */
  left: 20px; /* Ajusta para tu diseño */
  height: 150px; /* Tamaño del logo */
  cursor: pointer;
  z-index: 1000; /* Asegura que esté sobre otros elementos */
}
</style>
