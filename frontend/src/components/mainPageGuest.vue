<template>
  <div class="background-container">
    <!-- Header con campo de búsqueda y botón de inicio de sesión -->
    <header class="header">
      <!--<input type="text" placeholder="Search for a publication" class="search-bar" /> -->
      <router-link to="/login" class="sign-in-btn">Sign in</router-link>
    </header>

    <!-- Título principal -->
    <main class="content">
      <h1 class="main-title">Publications</h1>

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
      books: []

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
  width: 200px;
  font-size: 1em;
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

.carousel-container {
  margin-top: 100px;
  display: flex;
  align-items: center;
  gap: 15px;
  width: 100%;
  max-width: 1200px;
  overflow: hidden;
  /* Fondo de color claro */
  padding: 20px; /* Espacio interno */
  border-radius: 15px; /* Bordes redondeados */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3); /* Sombra para darle profundidad */
  border: 5px solid ; /* Borde sutil */
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
