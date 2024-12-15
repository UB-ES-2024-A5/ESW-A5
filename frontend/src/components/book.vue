<template>
  <div class="background-container">
    <div v-if="loading" class="loading-container">
      <p>Loading data, please wait...</p>
    </div>
    <div v-else class="book-details">
      <!-- Back Button -->
      <div class="back-button">
        <button @click="$router.go(-1)" class="back-button-style">Back</button>
      </div>

      <!-- Main Content -->
      <div class="content">
        <!-- Left Section -->
        <div class="left-section">
          <div class="image-container">
            <img :src="book.img || '/default-image.png'" alt="Book Cover" />
          </div>
          <div class="star-rating" v-if="!user_me.is_editor">
            <span  v-for="star in 5" :key="star" class="star" :class="{ active: star <= rating }" @click="rate_stars(star)">★</span>
            <span class="rating-average">({{ mediaValoracion.toFixed(1) }})</span>
          </div>
        </div>

        <!-- Right Section (Info) -->
        <div class="info">
          <div class="title-container">
            <h1 class="title">{{ book.title || 'Title of the publication' }}</h1>
            <!-- Wishlist Star -->
            <div
              v-if="!user_me.is_editor"
              class="star"
              @click="toggleStar(wishlistId, bookid2)"
              :class="{ selected: starSelected }"
            >
              ★
            </div>
          </div>
          <p><strong>Author:</strong> {{ book.author || 'Author example' }}</p>
          <p><strong>Genre:</strong> {{ book.gender_main || 'Genre1, Genre2' }}</p>
          <p><strong>Publisher:</strong> {{ user.name || 'Publisher' }}</p>
          <p><strong>Year of the publication:</strong> {{ book.publication_year || 'Year example' }}</p>
          <p><strong>ISBN:</strong> {{ book.isbn || 'ISBN example' }}</p>
          <p><strong>Minimum Price:</strong> {{ book.price || 'Price example' }}</p>
          <p><strong>Synopsis:</strong> {{ book.synopsis || 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla quam velit, vulputate.' }}</p>
          <strong>Purchase Links:</strong>
          <ul>
            <li
              v-for="(link, index) in book.list_links"
              :key="link"
              class="link-item"
            >
              <a :href="link" target="_blank" rel="noopener noreferrer">
                <button class="link-button">Link {{ index + 1 }}</button>
              </a>
            </li>
          </ul>
        </div>
      </div>

      <!-- Comments Section -->
      <div class="rating-section" v-if="!user_me.is_editor">
        <h2 class="comment-title">Leave a comment</h2>
        <textarea
          v-model="comment"
          placeholder="Share your thoughts about this book..."
          class="comment-box"
        ></textarea>
        <button  class="submit-button" @click="submitReview()">Submit Review</button>
      </div>
      <div class="comments-section">
  <h2 class="comments-title">Comments</h2>
  <div v-if="Object.keys(comments).length" class="comments-list" :key="componentKey">
    <!-- Iteramos sobre los comentarios por su ID -->
    <div v-for="(commentData, username) in comments" :key="username">
      <!-- Iteramos sobre cada comentario dentro de list_comments -->
      <div
        v-for="(text, index) in commentData.list_comments"
        :key="index"
        class="comment-box"
      >
        <div class="comment-header">
          <p class="comment-author">{{ username }}</p>
          <div class="comment-rating">
            <!-- Mostramos la valoración en estrellas -->
            <span
              v-for="star in 5"
              :key="star"
              class="star"
              :class="{ active: star <= commentData.rating }"
            >
              ★
            </span>
          </div>
        </div>
        <div class="comment-content">
          <p>{{ text }}</p>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="no-comments">No comments yet. Be the first to comment!</div>
</div>

    </div>
  </div>
</template>

<script>
import WishlistService from '../services/WishlistServices'
import UserServices from '../services/UserServices'
import BookServices from '../services/BookServices'
import Swal from 'sweetalert2'

export default {
  name: 'BookDetails',
  data () {
    return {
      book: {},
      userRating: 4,
      averageRating: 3,
      comment: '',
      starSelected: false,
      wishlistId: null,
      bookid2: '',
      user: {},
      user_id: '',
      user_me: {},
      rating: 0,
      comments: {},
      loading: true,
      mediaValoracion: 0,
      valoracioUsuari: false,
      componentKey: 0
    }
  },
  methods: {
    async fetchBookDetails () {
      const bookId = this.$route.query.bookId
      this.bookid2 = bookId
      BookServices.getBookById(bookId).then((res) => {
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
        this.fetchBookPublisher()
      })
        .catch(error => {
          console.error(error)
        })
    },
    fetchBookPublisher () {
      BookServices.getBookPublisher(this.user_id).then((res) => {
        this.user = {
          name: res.data.name
        }
      })
        .catch(error => {
          console.error(error)
        })
    },

    fetchComments2 (BookId) {
      BookServices.getReviews(BookId).then((reviewsResponse) => {
        let contador = 0
        let sumaValoracion = 0
        reviewsResponse.data.forEach((review) => {
          if (review.account_id === this.user_me.id) {
            this.valoracioUsuari = true
          }
          contador += 1
          sumaValoracion += review.point_book
          UserServices.getUserById2(review.account_id).then((user) => {
            const nameEntero = user.name + ' ' + user.surname
            console.warn(review.list_comments)
            this.comments[nameEntero] = {
              rating: review.point_book,
              list_comments: review.list_comments
            }
          })
            .catch((error) => {
              console.error(`Error al obtener el usuario con ID: ${review.account_id}: `, error)
            })
        })
        if (sumaValoracion === 0 || contador === 0) {
          this.mediaValoracion = 0
        } else {
          sumaValoracion = sumaValoracion / contador
          this.mediaValoracion = sumaValoracion
        }
        this.componentKey += 1
      })
        .catch((error) => {
          console.error('Error al obtener los comentarios', error)
          throw error
        })
    },

    async getUser () {
      try {
        this.user_me = await UserServices.getActualUser()
      } catch (error) {
        console.error('Error al obtener el usuario:', error)
      }
    },
    async getWishlistId () {
      try {
        const wishlistResponse = await WishlistService.getMyWishlists()
        if (wishlistResponse && wishlistResponse.data.length > 0) {
          this.wishlistId = wishlistResponse.data[0].id
          await this.checkifBookinWishlist(this.wishlistId)
        }
      } catch (error) {
        console.error('Error al obtener o crear wishlist', error)
        throw error
      }
    },
    async checkifBookinWishlist (id) {
      try {
        const wishlistResponse = await WishlistService.getWishlistsBooks(id)
        wishlistResponse.data.forEach(book => {
          if (book.isbn === this.book.isbn) {
            this.starSelected = true
          }
        })
      } catch (error) {
        console.error('Error al saber si el libro está en la wishlist', error)
      }
    },
    async toggleStar (wishlistId, bookid) {
      this.starSelected = !this.starSelected
      try {
        if (this.starSelected) {
          await WishlistService.addBookWishlist(wishlistId, bookid)
        } else {
          await WishlistService.deleteBookWishlist(wishlistId, bookid)
        }
      } catch (error) {
        console.error('Error al modificar la wishlist', error)
        this.starSelected = !this.starSelected
      }
    },
    rate_stars (star) {
      this.rating = star
      console.warn(`Puntuación seleccionada: ${this.rating}`)
    },
    submitReview () {
      if (this.rating !== 0 && !this.valoracioUsuari) {
        if (this.comment.trim() !== '') {
          const data = {
            text: this.comment
          }
          BookServices.createReviewComments(data, this.bookid2)
          this.comment = ''
        }
        const data2 = {
          point_book: this.rating
        }
        BookServices.createReviewPoints(data2, this.bookid2)
        Swal.fire({
          icon: 'success',
          title: 'Success!',
          text: 'Grácies per la teva valoració!'
        })
        this.rating = 0
      } else {
        if (this.valoracioUsuari) {
          Swal.fire({
            icon: 'warning',
            title: 'Valoració ja registrada',
            text: 'Aquest usuari ja te una valoració en aquest llibre.'
          })
        } else {
          Swal.fire({
            icon: 'warning',
            title: 'Valoració Incompleta',
            text: 'No es pot crear la valoració sense indicar el nombre de estrelles.'
          })
        }
      }
    }
  },
  async mounted () {
    try {
      this.loading = true
      await this.getUser()
      await this.fetchBookDetails()
      this.fetchComments2(this.bookid2)
      await this.getWishlistId()
    } catch (error) {
      console.error('Error al cargar algun componente: ', error)
    } finally {
      await new Promise(resolve => setTimeout(resolve, 250))
      this.componentKey += 1
      this.loading = false
      console.log(`Number of comments: ${this.comments.length}`)
    }
  }
}
</script>

<style scoped>

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 18px;
  color: #555;
}
.background-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100%;
  background: url('../assets/fondo_carrousel2.png') no-repeat center center fixed;
  background-size: cover;
  font-family: 'Georgia', serif;
  background-position: center bottom;
  color: #333;
  position: relative;
  padding-top: 20px;
}

.book-details {
  display: flex;
  flex-direction: column;
  align-items: center; /* Asegura que el título y la estrella estén alineados verticalmente */
  justify-content: flex-start; /* Evita espacio innecesario */
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 15px;
  padding: 20px;
  max-width: 3000px;
  width: 700px;
  margin: 0 auto;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.content {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 20px;
  align-items: flex-start;
  width: 100%;
}

.image-container img {
  width: 275px;
  height: 350px;
  object-fit: fill;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin-right: 0px;
  margin-top: 20px;
}

.info {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  margin-left: 0;
  padding-left: 10px;
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
  align-items: center; /* Asegura que el título y la estrella estén alineados verticalmente */
  justify-content: center; /* Evita espacio innecesario */
  width: 100%;
  margin-bottom: 15px;
}

.left-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
}

.info p {
  font-size: 1rem;
  margin: 5px 0;
}

.back-button {
  display: flex;
  justify-content: flex-start;
  width: 100%;
  margin-bottom: 15px;
}

.back-button button {
  top: 1rem;
  left: 1rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  font-weight: bold;
  background-color: #2563eb;
  color: white;
  border: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
  cursor: pointer;
}

.back-button button:hover {
  background-color: #333;
  color: #fff;
}

.star {
  font-size: 2.5rem;
  color: #9f9f9f;
  cursor: pointer;
  transition: transform 0.2s, color 0.2s;
}

.star:hover {
  transform: scale(1.2);
  color: #8a8a8a;
}

.star.selected {
  color: goldenrod;
}

.link-item {
  color: #0073e6;
  text-decoration: none;
  font-weight: bold;
  padding: 5px;
  border-radius: 5px;
  transition: all 0.4s ease;
  display: inline-block;
  text-align: left;
}

.link-button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 10px 15px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
  text-align: left;
}

.link-button:hover {
  background-color: #0056b3;
  transform: scale(1.10);
}

.link-button:active {
  transform: scale(1);
  background-color: #004494;
}

.star-rating {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.star.active {
  color: gold;
}

.rating-average {
  margin-left: 10px;
  font-size: 1.5rem;
  font-weight: bold;
  color: black;
  margin-top: 18px;
  font-family: 'serif';
}
.rating-section {
  width: 100%;
  margin-top: 20px;
}

.comment-title {
  font-size: 1.2em;
  margin-bottom: 10px;
}

.comment-box {
  width: 98%;
  max_width: 700px;
  height: 100px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  resize: vertical;
  margin-bottom: 10px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}
.comments-section {
  margin-top: 20px;
  padding: 10px;
  border-top: 1px solid #ddd;
}

.comments-title {
  font-size: 20px;
  margin-bottom: 10px;
  text-align: left;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-box {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.comment-author {
  font-weight: bold;
  color: #333;
}
.comment-rating {
  display: flex;
}

.comment-content {
  font-size: 14px;
  line-height: 1.4;
}

.no-comments {
  font-size: 14px;
  color: #999;
  text-align: center;
}

.submit-button {
  font-family: 'Roboto', sans-serif; /* Nueva fuente */
  font-weight: bold; /* Negrita */
  font-size: 16px;
  padding: 12px;
  background-color: #007bff;
  border: none;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 20px;
}

.submit-button:hover {
  background-color: #0056b3;
}

</style>
