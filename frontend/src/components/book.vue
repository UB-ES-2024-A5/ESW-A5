<template>
  <div class="background-container">
    <div class="book-details">
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
          <div class="star-rating">
            <span v-for="star in 5" :key="star" class="star">★</span>
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
      <div class="rating-section">
        <h2 class="comment-title">Leave a comment</h2>
        <textarea
          placeholder="Share your thoughts about this book..."
          class="comment-box"
        ></textarea>
        <button class="submit-button">Submit Review</button>
      </div>
    </div>
  </div>
</template>

<script>
import WishlistService from '../services/WishlistServices'
import axios from 'axios'
import UserServices from '../services/UserServices'

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
      user_id: '',
      user_me: {}
    }
  },
  methods: {
    fetchBookDetails () {
      const bookId = this.$route.query.bookId
      this.bookid2 = bookId
      const path = process.env.API_URL + '/api/v1/books/search_id/' + bookId

      axios.get(path)
        .then(res => {
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
        .catch(error => {
          console.error(error)
        })
    },
    fetchBookPublisher () {
      const path = process.env.API_URL + '/api/v1/users/by_id/' + this.user_id
      axios.get(path)
        .then(res => {
          this.user = {
            name: res.data.name
          }
        })
        .catch(error => {
          console.error(error)
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
    }
  },
  async mounted () {
    this.fetchBookDetails()
    await this.getWishlistId()
    await this.getUser()
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
  height: 100px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  resize: vertical;
  margin-bottom: 10px;
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
