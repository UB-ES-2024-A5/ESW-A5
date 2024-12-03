<template>
  <div class="background-container">
    <!-- Header con campo de búsqueda y botón de inicio de sesión -->
    <header class="header">
      <input type="text" placeholder="Search for a publication or user" class="search-bar" v-model="searchQuery" @input="search" @focus="showDropdown = true"  @blur="hideDropdown"/>
      <div v-if="showDropdown && searchResults.length > 0" class="dropdown">
        <ul>
          <li v-for="(result, index) in searchResults" :key="index" @mousedown="selectResult(result)" class="dropdown-item">
            <img :src="result.img" alt="Result Image" class="result-image"/>
            <!-- Título o Nombre en el centro -->
            <div class="result-content"><p class="result-title">{{ result.title || result.name }}</p></div>
            <!-- Tipo (book o user) a la derecha -->
            <span class="result-type">{{ result.title ? 'Book' : 'User' }}</span>
          </li>
        </ul>
      </div>
      <!-- Cambiamos el router-link por un botón que ejecuta la función logout -->
      <button @click="logout" class="sign-in-btn">Log out</button>

      <!-- Enlace al perfil de usuario con icono de imagen -->
      <router-link to="/publisher_profile" class="profile-link">
        <img src="@/assets/user_icon.png" alt="User Profile" class="user-icon" />
      </router-link>
    </header>

    <!-- Título principal -->
    <main class="content">
      <h1 class="main-title">Publications</h1>

      <!-- Carrusel de imágenes -->
      <div class="carousel-container">
        <!-- Botón de agregar publicación -->
        <router-link to="/create_publication" class="add-button">+</router-link>

        <button class="carousel-btn left-btn" @click="previousSlide">‹</button>
        <div class="carousel">
          <div class="carousel-track" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
           <img v-for="(book, index) in books" :key="index" :src="book.img" class="carousel-image" @click="goToBook(book.id)" />
          </div>
        </div>
        <button class="carousel-btn right-btn" @click="nextSlide">›</button>
      </div>
    </main>
  </div>
</template>

<script>
import BookServices from '../services/BookServices'
import SearchServices from '../services/SearchServices'
import AccountServices from '../services/AccountServices'
import UserServices from '../services/UserServices'

export default {
  name: 'mainPageGuest',
  data () {
    return {
      images: [
        require('@/assets/19557g.png'),
        require('@/assets/19557g.png'),
        require('@/assets/19557g.png'),
        require('@/assets/19557g.png'),
        require('@/assets/19557g.png'),
        require('@/assets/19557g.png'),
        require('@/assets/19557g.png')
      ],
      currentIndex: 0,
      imagesPerSlide: 5,
      books: [],
      searchQuery: '',
      searchResults: [],
      showDropdown: false,
      current_user: null
    }
  },
  computed: {
    maxIndex () {
      return Math.ceil(this.images.length / this.imagesPerSlide) - 1
    }
  },
  methods: {
    nextSlide () {
      if (this.currentIndex < this.maxIndex) {
        this.currentIndex++
      }
    },
    previousSlide () {
      if (this.currentIndex > 0) {
        this.currentIndex--
      }
    },
    goToBook (index) {
      this.$router.push({path: '/book', query: {bookId: index}})
    },

    async getAllBooks () {
      BookServices.getAllBooks().then(async data => {
        this.books = data.data
      })
      UserServices.getActualUser().then(async data => {
        this.current_user = data
      })
    },
    logout () {
      // Eliminamos el token del localStorage
      localStorage.removeItem('token')

      // Redirigimos al usuario a la página de inicio
      this.$router.push('/')
    },
    async search () {
      if (this.searchQuery.trim() === '') {
        this.searchResults = []
        return
      }
      try {
        const res = await SearchServices.search(this.searchQuery, 20)
        console.log('Resultados:', res.data)
        const userId = this.current_user.id
        this.searchResults = await Promise.all(
          res.data
            .filter(result => !(userId && !result.title && result.id === userId)) // Excluir el usuario logueado
            .map(async result => {
              if (!result.title) { // Es un usuario
                const account = await AccountServices.getAccountById(result.id)
                result.img = account.photo || 'default_account_icon.png'
              }
              return result
            })
        )
      } catch (error) {
        console.error('Error al buscar:', error)
      }
    },
    selectResult (result) {
      if (result.title) {
        // Es un libro
        console.log('Seleccionaste un libro:', result.title)
        this.navigateToBookDetail(result.id) // Por ejemplo, ir a detalle del libro
      } else if (result.name) {
        // Es un usuario
        console.log('Seleccionaste un usuario:', result.name)
        this.navigateToUserProfile(result) // Por ejemplo, ir al perfil del usuario
      }
    },
    navigateToBookDetail (bookId) {
      this.$router.push({path: '/book', query: {bookId: bookId}}) // Redirigir al detalle del libro
    },
    navigateToUserProfile (user) {
      if (user.is_editor) {
        this.$router.push({path: '/search_publisher_profile', query: {userID: user.id}}) // Redirigir al perfil del usuario
      } else {
        this.$router.push({path: '/search_user_profile', query: {userID: user.id}}) // Redirigir al perfil del usuario
      }
    },
    hideDropdown () {
      setTimeout(() => {
        this.showDropdown = false
      }, 200) // Retrasa el cierre para permitir la selección
    }
  },
  mounted () {
    this.getAllBooks()
  }
}
</script>

<style scoped>
/* Fondo principal */
.background-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100vh;
  background: url('../assets/fondo_carrousel2.png') no-repeat center center fixed;
  background-size: cover; /* Ensures the image fits within the container */
  font-family: 'Georgia', serif;
  background-position: center bottom; /* Align the image to the top, showing more of the top part */
  color: #333;
  position: relative;
  padding-top: 20px;
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
  width: 300px;
  font-size: 1em;
  background-color: #f5e8d8;
}

.dropdown {
  position: absolute; /* Posiciona el dropdown relativo al contenedor */
  top: 100%; /* Colócalo justo debajo del campo de búsqueda */
  left: 0; /* Alineado al borde izquierdo del input */
  background-color: white; /* Fondo blanco */
  border: 1px solid #ddd; /* Borde */
  border-radius: 4px; /* Bordes redondeados */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2); /* Sombra para resaltar */
  max-height: 200px; /* Altura máxima con scroll */
  overflow-y: auto; /* Scroll vertical */
  z-index: 1000; /* Asegura que esté por encima de otros elementos */
  width: 100%; /* Alineado con el ancho del input */
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.2s;
}

.dropdown-item:hover {
  background-color: #e1e1e1;
}

.result-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 15px;
}

.result-content {
  flex-grow: 1;
}

.result-title {
  font-size: 16px;
  font-weight: bold;
  margin: 0;
}

.result-type {
  font-size: 14px;
  color: #8a8a8a;
  text-align: right;
}

.dropdown-item:last-child {
  border-bottom: none;
}

ul {
  margin: 5px;
  padding: 0;
  list-style: none;
}

li {
  margin: 0;
  padding: 0;
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

.profile-link:hover {
  transform: scale(1.1); /* Efecto de zoom al pasar el ratón */
}

/* Contenido principal */
.content {
  text-align: center;
  padding-top: 110px;
}

/* Título principal */
.main-title {
  font-size: 3em;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

/* Contenedor del carrusel */
.carousel-container {
  margin-top: 100px;
  display: flex;
  align-items: center;
  gap: 15px;
  width: 100%;
  max-width: 1200px;
  overflow: hidden;
  padding: 20px; /* Espacio interno */
  border-radius: 15px; /* Bordes redondeados */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3); /* Sombra para darle profundidad */
  position: relative; /* Para posicionar el botón flotante */
}

/* Botón de agregar publicación en el carrusel */
.add-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #333;
  color: #fff;
  font-size: 1.5em;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  transition: background-color 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  cursor: pointer;
}

.add-button:hover {
  background-color: #555;
}

.carousel {
  overflow: hidden;
  width: 100%;
  position: relative;
}

.carousel-track {
  display: flex;
  transition: transform 0.5s ease;
}

.carousel-image {
  width: calc(100% / 5); /* Ajuste para mostrar cinco imágenes a la vez */
  flex-shrink: 0;
  margin-right: 15px; /* Adds space between images */
  border-radius: 10px; /* Bordes redondeados */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 1); /* Sombra para efecto 3D */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.carousel-btn {
  font-size: 6em;
  background: none;
  border: none;
  cursor: pointer;
  color: #000000;
  transition: color 0.3s ease;
}

.carousel-btn:hover {
  color: #555;
}
</style>
