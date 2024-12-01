<template>
  <div class="background-container">
    <div class="book-details">
      <div class="back-button">
      </div>

      <div class="content">
        <div class="left-section">
          <div class="title-container">
            <h1 class="title">{{ book.title || 'Title of the publication' }}</h1>
            <div class="star" @click="toggleStar(wishlistId, bookid2)" :class="{ selected: starSelected }"> ★
            </div>
          </div>
          <div class="image-container">
            <img :src="book.img || '/default-image.png'" alt="Book Cover" />
          </div>
        </div>

        <div class="info">
          <p><strong>Author:</strong> {{ book.author || 'Author example' }}</p>
          <p><strong>Genre:</strong> {{ book.gender_main || 'Genre1, Genre2' }}</p>
          <p><strong>Publisher:</strong> {{ user.name || this.user_id }}</p>
          <p><strong>Year of the publication:</strong> {{ book.publication_year || 'Year example' }}</p>
          <p><strong>ISBN:</strong> {{ book.isbn || 'ISBN example' }}</p>
          <p><strong>Minimum Price:</strong> {{ book.price || 'Price example' }}</p>
          <p><strong>Synopsis:</strong> {{ book.synopsis || 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla quam velit, vulputate.' }}</p>
          <strong>Links de compra:</strong> <ul>
          <li v-for="(link,index) in book.list_links" :key="link" class="link-item">
                <a :href="link" target="_blank" rel="noopener noreferrer">
                  <button class="link-button">Link {{ index + 1}}</button>
                </a>
              </li>
        </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import WishlistService from '../services/WishlistServices'
import axios from 'axios'

export default {
  name: 'BookDetails',
  data () {
    return {
      book: {},
      userRating: 4,
      averageRating: 3,
      comments: [],
      starSelected: false,
      wishlistId: null,
      bookid2: '',
      user: {},
      user_id: ''
    }
  },
  methods: {
    fetchBookDetails () {
      const bookId = this.$route.query.bookId
      this.bookid2 = bookId
      const path = process.env.API_URL + '/api/v1/books/search_id/' + bookId

      axios.get(path)
        .then((res) => {
          this.book = {
            title: res.data.title,
            author: res.data.author,
            gender_main: res.data.gender_main,
            publication_year: res.data.publication_year,
            isbn: res.data.isbn,
            price: res.data.price,
            synopsis: res.data.synopsis,
            img: res.data.img,
            list_links: res.data.list_links || [],
            account_id: res.data.account_id
          }
          this.user_id = this.book.account_id
          this.comments = res.data.comments || []
          this.fetchBookPublisher()
        })
        .catch((error) => {
          console.error(error)
          alert('Failed to load book details')
        })
    },
    fetchBookPublisher () {
      const path = process.env.API_URL + '/api/v1/users/by_id/' + this.user_id
      axios.get(path)
        .then((res) => {
          this.user = {
            name: res.data.name
          }
        })
        .catch((error) => {
          console.error(error)
          alert('Failed to load book details')
        })
    },
    checkIfBookInWishlist (isbn) {
      // Verifica si el libro está en la wishlist
      const path = process.env.API_URL + '/api/v1/wishlists/' + this.wishlistId + '/books'
      axios.get(path)
        .then((res) => {
          const bookInWishlist = res.data.some(book => book.isbn === isbn)
          this.starSelected = bookInWishlist
        })
        .catch((error) => {
          console.error(error)
        })
    },
    loadMoreComments () {
      console.log('Load more comments')
    },
    async getWishlistId () {
      try {
        const wishlistResponse = await WishlistService.getMyWishlists()
        console.log(wishlistResponse)

        // Si se crea una nueva wishlist, asignamos su ID
        if (wishlistResponse && wishlistResponse.data.length > 0) {
          this.wishlistId = wishlistResponse.data[0].id
        }
      } catch (error) {
        console.error('Error al obtener o crear wishlist', error)
      }
    },
    async toggleStar (wishlistId, bookid) {
      this.starSelected = !this.starSelected
      if (this.starSelected) {
        try {
          // Agregar el libro a la wishlist
          await WishlistService.addBookWishlist(wishlistId, bookid)
        } catch (error) {
          console.error('Error al agregar libro a la wishlist', error)
        }
      } else {
        try {
          // Eliminar el libro de la wishlist
          await WishlistService.deleteBookWishlist(wishlistId, bookid)
        } catch (error) {
          console.error('Error al eliminar libro de la wishlist', error)
        }
      }
    }
  },
  mounted () {
    this.fetchBookDetails()
    // this.getWishlistId()
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
  background-size: cover; /* Ensures the image fits within the container */
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
  align-items: flex-start;
  width: 100%;
}

.image-container img {
  width: 175px;
  height: 250px;
  object-fit: fill;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin-right: 0px;
}

.info {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  margin-left: 0;
  padding-left: 10px;
  margin-top: 50px;
}

.info p {
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
  width: 100%;
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

.back-button {
  display: flex;
  justify-content: flex-start;
  width: 100%; /* Ocupa todo el ancho para alineación */
  margin-bottom: 15px; /* Espaciado debajo del botón */
}

.back-button button {
  background-color: transparent;
  border: 2px solid #333;
  color: #333;
  font-size: 1.2rem;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.back-button button:hover {
  background-color: #333;
  color: #fff;
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
.link-item{
  color: #0073e6; /* Un azul profesional */
  text-decoration: none; /* Elimina el subrayado por defecto */
  font-weight: bold; /* Da énfasis al texto */
  padding: 5px; /* Espaciado alrededor del texto */
  border-radius: 5px; /* Bordes redondeados */
  transition: all 0.4s ease; /* Suaviza las animaciones */
  display: inline-block; /* Asegura que respeta el padding */
  text-align: left;

}

.link-button {
  background-color: #007bff; /* Fondo azul */
  color: white; /* Texto blanco */
  border: none; /* Sin bordes */
  border-radius: 10px; /* Bordes redondeados */
  padding: 10px 15px; /* Espaciado interno */
  font-size: 16px; /* Tamaño de la fuente */
  font-weight: bold; /* Texto en negrita */
  cursor: pointer; /* Mostrar el cursor de mano */
  transition: background-color 0.3s, transform 0.2s; /* Animación suave */
  text-align: left;

}
.link-button:hover {
  background-color: #0056b3; /* Azul más oscuro al pasar el ratón */
  transform: scale(1.10); /* Efecto de zoom */
}

.link-button:active {
  transform: scale(1); /* Reducir zoom al hacer clic */
  background-color: #004494; /* Fondo aún más oscuro */
}

</style>
