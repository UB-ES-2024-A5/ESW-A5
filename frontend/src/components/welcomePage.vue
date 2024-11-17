<template>
  <div class="background-container">
    <!-- Header con campo de búsqueda y botón de inicio de sesión en la esquina superior derecha -->
    <header class="header">
      <router-link to="/login" class="sign-in-btn">Sign in</router-link>
    </header>

    <!-- Contenido principal con texto alineado a la izquierda y botones de registro -->
    <main class="content">
      <h1 class="main-title">Start your book life</h1>
      <p class="subtitle">The most complete reading social network in the world</p>
      <div class="buttons">
        <router-link to="/signup" class="sign-up-btn">Sign up as user</router-link>
        <router-link to="/signupEdit" class="sign-up-btn">Sign up as publisher</router-link>
        <router-link to="/mainpage_guest" class="sign-up-btn">Guest access</router-link>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'BookLife'
}
</script>

<script>
export default {
  name: 'BookLife'
}
</script>

<style scoped>
/* Estilo global para evitar subrayados en los enlaces */
a {
  text-decoration: none; /* Elimina el subrayado de todos los enlaces */
}
/* Fondo principal */
html, body {
  height: 100%; /* Asegura que el body ocupe toda la altura de la ventana */
  margin: 0; /* Elimina el margen predeterminado */
  overflow: hidden; /* Evita que aparezca la barra de desplazamiento */
}

/* Fondo principal */
.background-container {
  display: flex;
  align-items: center;
  justify-content: center; /* Cambia 'center' a 'flex-start' para alinear todo a la izquierda */
  height: 100vh;
  background: url('../assets/foto_guest_access.png') no-repeat center center fixed;
  background-size: cover;
  font-family: 'Georgia', serif;
  color: #333;
  position: relative;
  padding-right: 600px; /* Agrega padding para mover el contenido hacia la izquierda */
}

/* Header */
.header {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Campo de búsqueda */
.search-bar {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 20px;
  width: 180px;
  font-size: 0.9em;
  color: #333;
  background-color: #f5e8d8;
}

/* Botón de inicio de sesión */
.sign-in-btn {
  padding: 8px 16px;
  background-color: transparent;
  border: 1px solid #333;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9em;
  color: #333;
  transition: background-color 0.3s ease;
}

.sign-in-btn:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

/* Contenido principal */
.content {
  text-align: left; /* Asegura que el texto esté alineado a la izquierda */
  max-width: 800px; /* Aumenta el ancho máximo del contenedor */
  padding-left: 20px; /* Lleva el texto más a la izquierda */
  margin-top: -150px; /* Ajusta el margen para desplazar el bloque hacia arriba */
}

/* Estilo del título */
.main-title {
  font-size: 7em; /* Aumenta el tamaño del título */
  font-weight: bold;
  color: #000;
  margin-bottom: 10px; /* Separación entre el título y el subtítulo */
  text-shadow: 0px 1px 1px rgba(0, 0, 0, 0.1);
  white-space: nowrap; /* Evita que el texto se divida en varias líneas */
}

/* Estilo del subtítulo */
.subtitle {
  font-size: 3em; /* Aumenta el tamaño del subtítulo */
  color: #333;
  margin-bottom: 30px; /* Separación entre el subtítulo y los botones */
  white-space: nowrap; /* Evita que el texto se divida en varias líneas */
}

/* Botones de registro */
.buttons {
  display: flex;
  gap: 15px; /* Espacio entre los botones */
}

.sign-up-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 5px;
  background-color: #000;
  color: #fff;
  cursor: pointer;
  font-size: 1.3em;
  transition: background-color 0.3s ease;
}

.sign-up-btn:hover {
  background-color: #333;
}
</style>
