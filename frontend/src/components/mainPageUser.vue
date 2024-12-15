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
      <router-link to="/forum" class="profile-link">
        <img src="@/assets/forum_icon.png" alt="Forum" class="user-icon" data-testid="forum-icon" />
      </router-link>
      <router-link to="/user_profile" class="profile-link">
        <img src="@/assets/user_icon.png" alt="User Profile" class="user-icon" data-testid="user-profile-icon" />
      </router-link>
    </header>

    <!-- Título principal -->
    <main class="content">
      <h1 class="main-title">Publications</h1>

      <!-- Contenedor de filtros -->
      <div class="filters-container">
        <label>
          Genre:
          <select v-model="filters.genre" @change="clearFiltersExcept('genre'); applyFilters">
            <option value="">All</option>
            <option value="Fiction">Fiction</option>
            <option value="Non-Fiction">Non-Fiction</option>
            <option value="Fantasy">Fantasy</option>
            <option value="Science Fiction">Science Fiction</option>
            <option value="Romance">Romance</option>
          </select>
        </label>
        <label>
          Min Price:
          <input type="number" v-model.number="filters.minPrice" @input="clearFiltersExcept('minPrice'); applyFilters" placeholder="Min Price" />
        </label>
        <label>
          Max Price:
          <input type="number" v-model.number="filters.maxPrice" @input="clearFiltersExcept('maxPrice'); applyFilters" placeholder="Max Price" />
        </label>
        <label>
          Min Year:
          <input type="number" v-model.number="filters.minYear" @input="clearFiltersExcept('minYear'); applyFilters" placeholder="Min Year" />
        </label>
        <label>
          Max Year:
          <input type="number" v-model.number="filters.maxYear" @input="clearFiltersExcept('maxYear'); applyFilters" placeholder="Max Year" />
        </label>
      </div>

      <!-- Carrusel de imágenes -->
      <div class="carousel-container">
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
// import axios from 'axios'
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
      filteredBooks: [],
      imagesPerSlide: 5,
      books: [],
      searchQuery: '',
      searchResults: [],
      showDropdown: false,
      current_user: null,
      filters: {
        genre: '',
        minPrice: null,
        maxPrice: null,
        minYear: null,
        maxYear: null
      }
    }
  },
  computed: {
    maxIndex () {
      return Math.ceil(this.images.length / this.imagesPerSlide) - 1
    }
  },
  watch: {
    'filters.genre' (newVal) {
      if (newVal) {
        this.clearFiltersExcept('genre')
      }
      this.applyFilters() // Siempre aplica filtros después de cambiar uno
    },
    'filters.minPrice' (newVal) {
      if (newVal !== null) {
        this.clearFiltersExcept('minPrice')
      }
      this.applyFilters() // Siempre aplica filtros después de cambiar uno
    },
    'filters.maxPrice' (newVal) {
      if (newVal === null || newVal === '') {
        this.filters.maxPrice = null // Asegúrate de convertir cadenas vacías a null
      }
      this.applyFilters()
    },
    'filters.minYear' (newVal) {
      if (newVal !== null) {
        this.clearFiltersExcept('minYear')
      }
      this.applyFilters() // Siempre aplica filtros después de cambiar uno
    },
    'filters.maxYear' (newVal) {
      if (newVal === null || newVal === '') {
        this.filters.maxYear = null // Asegúrate de convertir cadenas vacías a null
      }
      this.applyFilters()
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
        console.log(user)
        this.$router.push({path: '/search_publisher_profile', query: {userID: user.id}}) // Redirigir al perfil del usuario
      } else {
        this.$router.push({path: '/search_user_profile', query: {userID: user.id}}) // Redirigir al perfil del usuario
      }
    },
    hideDropdown () {
      setTimeout(() => {
        this.showDropdown = false
      }, 200) // Retrasa el cierre para permitir la selección
    },
    async applyFilters () {
      const { genre, minPrice, maxPrice, minYear, maxYear } = this.filters

      // Si todos los filtros están vacíos, carga todos los libros
      // Carga todos los libros si no hay filtros aplicados
      if (!genre && !minPrice && !maxPrice && !minYear && !maxYear) {
        await this.fetchAllBooks()
        return
      }

      // Aplicar el filtro basado en el campo rellenado
      if (genre) {
        await this.applyGenreFilter(genre)
      } else if (minPrice !== null) {
        await this.applyMinPriceFilter(minPrice)
      } else if (maxPrice !== null) {
        await this.applyMaxPriceFilter(maxPrice)
      } else if (minYear !== null) {
        await this.applyMinYearFilter(minYear)
      } else if (maxYear !== null) {
        await this.applyMaxYearFilter(maxYear)
      }
    },
    async applyGenreFilter (genre) {
      try {
        const filteredBooks = await BookServices.getBooksByGenre(genre)
        this.updateBooks(filteredBooks)
      } catch (error) {
        console.error('Error al filtrar por género:', error)
      }
    },

    async applyMinPriceFilter (minPrice) {
      try {
        const filteredBooks = await BookServices.getBooksByPriceMin(minPrice)
        this.updateBooks(filteredBooks)
      } catch (error) {
        console.error('Error al filtrar por precio mínimo:', error)
      }
    },

    async applyMaxPriceFilter (maxPrice) {
      try {
        const filteredBooks = await BookServices.getBooksByPriceMax(maxPrice)
        this.updateBooks(filteredBooks)
      } catch (error) {
        console.error('Error al filtrar por precio máximo:', error)
      }
    },

    async applyMinYearFilter (minYear) {
      try {
        const filteredBooks = await BookServices.getBooksByDateMin(minYear)
        this.updateBooks(filteredBooks)
      } catch (error) {
        console.error('Error al filtrar por año mínimo:', error)
      }
    },

    async applyMaxYearFilter (maxYear) {
      try {
        const filteredBooks = await BookServices.getBooksByDateMax(maxYear)
        this.updateBooks(filteredBooks)
      } catch (error) {
        console.error('Error al filtrar por año máximo:', error)
      }
    },

    // Restablecer filtros excepto el actualmente modificado
    resetFilters (activeFilter) {
      Object.keys(this.filters).forEach(filter => {
        if (filter !== activeFilter) {
          this.filters[filter] = null
        }
      })
    },

    // Método genérico para actualizar los libros en el carrusel
    updateBooks (filteredBooks) {
      this.books = filteredBooks.data // Actualizar los libros filtrados
      this.currentIndex = 0 // Reiniciar el índice del carrusel
    },

    // Método para obtener todos los libros en caso de que no haya filtros activos
    async fetchAllBooks () {
      try {
        const allBooks = await BookServices.getAllBooks()
        this.updateBooks(allBooks)
      } catch (error) {
        console.error('Error al obtener todos los libros:', error)
      }
    },
    clearFiltersExcept (activeFilter) {
      Object.keys(this.filters).forEach((filter) => {
        if (filter !== activeFilter) {
          this.filters[filter] = filter === 'genre' ? '' : null // Vaciar select o inputs
        }
      })
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
  background-size: cover;  /* Ensures the image fits within the container */
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

/* Filtros */
.filters-container {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 30px;
  background: rgba(255, 255, 255, 0.8); /* Fondo translúcido */
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Sombra sutil */
  border: 2px solid #ccc; /* Borde suave */
  min-height: 70px; /* Altura mínima fija */
  align-items: center; /* Centra los elementos verticalmente */
}

.filters-container label {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  font-size: 1em;
  font-weight: bold;
  color: #333;
}

.filters-container input,
.filters-container select {
  margin-top: 5px;
  padding: 10px;
  font-size: 1em;
  border: 1px solid #ccc;
  border-radius: 10px;
  outline: none;
  transition: border-color 0.3s ease;
  background-color: #f8f8f8; /* Fondo claro */
}

.filters-container input:focus,
.filters-container select:focus {
  border-color: #8a8a8a; /* Color destacado en foco */
}

.filters-container select {
  appearance: none; /* Oculta la flecha por defecto */
  background-image: url('data:image/svg+xml;charset=UTF-8,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="%238a8a8a"%3E%3Cpath fill-rule="evenodd" d="M10 12a.75.75 0 01-.53-.22l-3.75-3.75a.75.75 0 111.06-1.06L10 10.44l3.22-3.22a.75.75 0 111.06 1.06l-3.75 3.75A.75.75 0 0110 12z" clip-rule="evenodd"/%3E%3C/svg%3E');
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 16px 16px;
}

.filters-container input[type='number'] {
  -moz-appearance: textfield; /* Oculta las flechas en Firefox */
}

.filters-container input[type='number']::-webkit-inner-spin-button,
.filters-container input[type='number']::-webkit-outer-spin-button {
  -webkit-appearance: none; /* Oculta las flechas en Chrome */
}

/* Botón de aplicar filtros (opcional) */
.filters-container button {
  padding: 10px 20px;
  font-size: 1em;
  font-weight: bold;
  color: white;
  background-color: #333;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.filters-container button:hover {
  background-color: #555;
}

/* Carrusel */
.carousel-container {
  margin-top: 50px; /* Reduce el margen superior */
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1110px; /* Reduce el ancho máximo */
  min-width: 250px;
  overflow: hidden;
  padding: 10px;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Reduce la sombra */
  border: 3px solid; /* Reduce el grosor del borde */
  height: 280px; /* Reduce la altura */
  position: relative;
  gap: 20px; /* Aumenta el espacio entre las flechas y las imágenes */
  padding-left: 40px;
  padding-right: 40px;
}

/* Pista del carrusel */
.carousel {
  overflow: hidden;
  width: 100%;
  height: 100%;
}

.carousel-track {
  display: flex;
  transition: transform 0.5s ease;
  height: 100%;
}

/* Imágenes del carrusel */
.carousel-image {
  width: 150px; /* Reduce el ancho */
  height: 100%; /* Ajusta la altura a la del contenedor */
  flex-shrink: 0;
  margin-right: 10px; /* Reduce el espacio entre imágenes */
  border-radius: 10px; /* Bordes redondeados para las imágenes */
  object-fit: cover; /* Asegura que las imágenes mantengan su proporción */
  border: 2px solid #ccc; /* Añade un borde fino */
}

/* Botones del carrusel */
.carousel-btn {
  background-color: rgba(0, 0, 0, 0.5); /* Fondo translúcido */
  color: white;
  border: none;
  border-radius: 50%;
  width: 35px; /* Reduce el tamaño */
  height: 35px;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin: 0 20px; /* Añadir más margen para aumentar la separación */
}

.carousel-btn:hover {
  background-color: rgba(0, 0, 0, 0.7); /* Oscurece al pasar el mouse */
}

/* Botón izquierdo */
.left-btn {
  position: absolute;
  left: 10px; /* Ajusta la posición */
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
}

/* Botón derecho */
.right-btn {
  position: absolute;
  right: 10px; /* Ajusta la posición */
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
}
</style>
