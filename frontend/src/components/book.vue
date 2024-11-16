<template>
  <div class="background-container">
    <div class="book-details">
      <div class="content">
        <!-- Imagen de la publicación -->
        <div class="left-section">
          <div class="title-container">
            <h1 class="title">{{ book.title || 'Title of the publication' }}</h1>
            <!-- Estrella pulsable -->
            <div class="star" @click="toogleStar(wishlistId, bookid2)" :class="{ selected: starSelected }"> ★

            </div>
          </div>
          <div class="image-container">
            <img :src="book.img || '/default-image.png'" alt="Book Cover" />
          </div>
        </div>

        <!-- Información del libro -->
        <div class="info">
          <p><strong>Author:</strong> {{ book.author || 'Author example' }}</p>
          <p><strong>Genre:</strong> {{ book.gender_main || 'Genre1, Genre2' }}</p>
          <p><strong>Publisher:</strong> {{ book.publisher || 'WillyRex' }}</p>
          <p><strong>Year of the publication:</strong> {{ book.publication_year || 'Year example' }}</p>
          <p><strong>ISBN:</strong> {{ book.isbn || 'ISBN example' }}</p>
          <p><strong>Minimum Price:</strong> {{ book.price || 'Price example' }}</p>
          <p><strong>Synopsis:</strong> {{ book.synopsis || 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla quam velit, vulputate.' }}</p>

        </div>
      </div>

        <!-- Valoración del usuario
        <div class="rating">
          <p>Your valorization</p>
          <div class="user-rating">
             Estrellas de valoración del usuario
            <span v-for="star in 5" :key="star" :class="{ filled: star <= userRating }">★</span>
          </div>
          <p>Users valoration</p>
          <div class="average-rating">
             Estrellas de valoración de usuarios
            <span v-for="star in 5" :key="star" :class="{ filled: star <= averageRating }">★</span>
          </div>
        </div>-->

      <!-- Sección de comentarios
      <div class="comments">
        <h2>Comments</h2>
        <div v-for="comment in comments" :key="comment.id" class="comment-box">
          <p><strong>{{ comment.user || 'Name user' }}</strong></p>
          <p>{{ comment.text || 'User comment' }}</p>
        </div>

        <button @click="loadMoreComments">→</button>
      </div>-->
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import WishlistServices from '../services/WishlistServices'

export default {
  name: 'BookDetails',
  data () {
    return {
      book: {},
      userRating: 4, // Valoración del usuario
      averageRating: 3, // Valoración promedio de los usuarios
      comments: [], // Lista de comentarios
      starSelected: false,
      whishlist: [],
      wishlistId: null,
      bookid2: ''
    }
  },
  methods: {
    fetchBookDetails () {
      const bookId = this.$route.query.bookId // Obtener el ID del libro desde la URL
      this.bookid2 = bookId
      const path = process.env.API_URL + '/api/v1/books/search_id/' + bookId

      axios.get(path)
        .then((res) => {
          console.log(res) // Verificar la respuesta
          // Asignar los datos del libro al objeto `book`
          this.book = {
            title: res.data.title,
            author: res.data.author,
            gender_main: res.data.gender_main,
            publisher: res.data.publisher,
            publication_year: res.data.publication_year,
            isbn: res.data.isbn,
            price: res.data.price,
            synopsis: res.data.synopsis,
            img: res.data.img
          }

          // Asignar comentarios si están disponibles
          this.comments = res.data.comments || []
        })
        .catch((error) => {
          console.error(error)
          alert('Failed to load book details')
        })
    },
    loadMoreComments () {
      // Implementar lógica para cargar más comentarios si es necesario
      console.log('Load more comments')
    },
    async getWhishlistId () {
      WishlistServices.getMyWishlists().then(async res => {
        console.log(res)
        this.wishlistId = res.data[0].id
        console.log(this.wishlistId)
      }).catch(error => {
        console.error('Error obteniendo los datos', error)
      })
    },
    toogleStar (wishid, bookid) {
      this.starSelected = !this.starSelected
      if (this.starSelected) {
        WishlistServices.addBookWishlist(wishid, bookid)
      } else {
        WishlistServices.deleteBookWishlist(wishid, bookid)
      }
    }
  },
  mounted () {
    this.fetchBookDetails()
    this.getWhishlistId()
  }
}
</script>

<style scoped>
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
.book-details {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 15px;
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.content {
  display: grid;
  grid-template-columns: 150px auto; /* Columna de la imagen y columna del texto */
  gap: 20px; /* Espaciado entre la imagen y el texto */
  align-items: flex-start; /* Asegura que todo comience en la parte superior */
  width: 100%;
}
.image-container img {
  width: 150px;
  height: 200px;
  object-fit: cover;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin-right: 0px;
}
.info {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  margin-left: 0;
  padding-left: 10px;
  margin-top: 50px
}
.info p{
  margin: 4px 0;
}

.title {
  font-size: 1.5em;
  font-weight: bold;
  margin-bottom: 10px;
}
.title-container {
  display: flex;
  align-items: center; /* Alinea el título y la estrella en una fila */
  flex-direction: row;
  justify-content: space-between; /* Espacia el título y la estrella */
  width: 100%; /* Asegura que ocupen todo el ancho disponible */
}
.left-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: space-between;
  width: 100%;
}
.info p {
  font-size: 1rem;
  margin: 5px 0;
}

.comments {
  width: 100%;
  margin-top: 20px;
}

.comment-box {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 10px;
}

button {
  background-color: transparent;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
}
.star {
  margin-left: auto;
  font-size: 2rem; /* Tamaño de la estrella */
  color: #9f9f9f; /* Color dorado para la estrella */
  cursor: pointer;
  transition: transform 0.2s, color 0.2s; /* Animaciones */
}

.star:hover {
  transform: scale(1.2); /* Efecto de agrandamiento al pasar el ratón */
  color: #8a8a8a; /* Color más brillante al pasar el ratón */
}
.star.selected {
  color: goldenrod;
}
</style>
