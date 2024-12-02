<template>
  <div class="user-profile" :style="{ backgroundImage: `url(${backgroundImage})` }">
    <div class="content-box">
      <!-- Botón de "Back" -->
      <button class="back-button" @click="goBack" aria-label="Go back">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon">
          <path d="M19 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H19v-2z"/>
        </svg>
      </button>
      <div class="profile-image-container">
        <img :src="userProfileImage" alt="Profile Icon" class="profile-image">
      </div>
      <div class="user-info">
        <h1>{{ user.name }}</h1>
        <button
          class="follow-button"
          :class="{ 'following': isFollowing, 'disabled': !isLoggedIn }"
          @click="toggleFollow"
          :disabled="!isLoggedIn"
        >
          {{ isFollowing ? 'Unfollow' : 'Follow' }}
        </button>
        <p>{{ user.email }}</p>
        <p>cif {{ user.cif }}</p>
      </div>
      <div class="follow-info">
        <div class="follow-item">
          <!-- Ícono de varias personas para seguidores -->
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon">
            <path d="M16 11c1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3 1.34 3 3 3zm-8 0c1.66 0 3-1.34 3-3S9.66 5 8 5 5 6.34 5 8s1.34 3 3 3zm8 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4zM8 13c-2.67 0-8 1.34-8 4v2h6v-2c0-.73.38-1.41 1-2-.68-.06-1-.94-1-2z" />
          </svg>
          <span>{{ account.num_followers }} followers</span>
        </div>
        <div class="follow-item">
          <!-- Ícono de una persona con un "+" para siguiendo -->
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon">
            <path d="M16 11c1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3 1.34 3 3 3zm-8 0c1.66 0 3-1.34 3-3S9.66 5 8 5 5 6.34 5 8s1.34 3 3 3zm8 2c-2.67 0-8 1.34-8 4v2h3v-2h10v2h3v-2c0-2.66-5.33-4-8-4zm2 3v-2h2v2h-2z" />
          </svg>
          <span>{{ account.num_following }} followed</span>
        </div>
      </div>
      <div class="biography-section">
        <h2>Biography</h2>
        <p>{{ account.bio }}</p>
      </div>

      <!-- Carrusel de publicaciones: Solo visible si estás logueado y sigues la cuenta -->
      <div v-if="isLoggedIn && isFollowing" class="carousel-container">
        <button class="carousel-btn left-btn" @click="previousSlide">‹</button>
        <div class="carousel">
          <div class="carousel-track" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
            <img
              v-for="(book, index) in books"
              :key="index"
              :src="book.img"
              class="carousel-image"
              @click="goToBook(book.id)"
              alt="Book Cover"
            />
          </div>
        </div>
        <button class="carousel-btn right-btn" @click="nextSlide">›</button>
      </div>

    </div>
  </div>
</template>

<script>
import userServices from '../services/UserServices.js'
import accountServices from '../services/AccountServices.js'
import BookServices from '../services/BookServices.js'
export default {
  data () {
    return {
      profileIcon: require('@/assets/account_icon.png'),
      backgroundImage: require('@/assets/fondo_profile.png'),
      userProfileImage: require('@/assets/placeholder_image.png'), // Default placeholder image
      user: {
        name: '',
        surname: '',
        email: '',
        wishlist: [],
        wishlistId: ''
      },
      account: {
        num_followers: '',
        num_following: '',
        photo: '',
        bio: ''
      },
      currentIndex: 0,
      imagesPerSlide: 5,
      books: [],
      isFollowing: false, // Estado de seguimiento
      isLoggedIn: false // Estado de inicio de sesión
    }
  },
  computed: {
    maxIndex () {
      return Math.ceil(this.images.length / this.imagesPerSlide) - 1
    }
  },
  methods: {
    async fetchUserProfile () {
      console.log('Fetching user profile...')
      const userID = this.$route.query.userID // Obtén el userID desde la query string
      try {
        const userData = await userServices.getUserById(userID)
        const accountData = await accountServices.getAccountById(userID)
        console.log('User data:', userData)
        this.user.name = userData.name
        this.user.cif = userData.cif
        this.user.email = userData.email
        this.account.num_followers = accountData.num_followers || '0'
        this.account.num_following = accountData.num_following || '0'
        this.account.bio = accountData.bio
        // Mostrar placeholder si no hay foto de perfil
        this.userProfileImage = accountData.photo || this.profileIcon
        // Verifica si ya sigues al usuario
        await this.checkIfFollowing()
      } catch (error) {
        console.error('Error al obtener los datos del usuario:', error)
      }
    },
    goBack () {
      this.$router.push('/mainPage_user')
    },
    async checkIfFollowing () {
      try {
        const userID = this.$route.query.userID // Obtén el userID desde la query string
        const followingData = await accountServices.getFollowingAccounts() // Obtén la lista de seguidos
        this.isFollowing = followingData.data.some(
          (data) => data.following_id.toString().trim() === userID.toString().trim()
        )
      } catch (error) {
        console.error('Error al verificar el estado de seguimiento:', error)
      }
    },
    async toggleFollow () {
      const userID = this.$route.query.userID // Obtén el userID desde la query string
      try {
        if (this.isFollowing) {
          // Si ya sigues, deja de seguir
          await accountServices.unfollowAccount(userID)
        } else {
          // Si no sigues, empieza a seguir
          await accountServices.followAccount(userID)
        }
        // Actualiza el estado de seguimiento
        await this.fetchUserProfile()
      } catch (error) {
        console.error('Error al alternar el estado de seguimiento:', error)
      }
    },
    isUserLoggedIn () {
      // Verifica si hay un token presente
      return !!localStorage.getItem('token')
    },
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
      this.$router.push({ path: '/book', query: { bookId: index } })
    },
    async getAllBooks () {
      try {
        const userID = this.$route.query.userID // Obtén el userID desde la query string
        const response = await BookServices.getBooksByEditorialId(userID)
        this.books = response.data
        this.maxIndex = Math.ceil(this.books.length / 3) - 1 // Ajustar según el número de libros visibles
      } catch (error) {
        console.error('Error al obtener libros:', error)
      }
    }
  },
  mounted () {
    this.isLoggedIn = this.isUserLoggedIn() // Establece el estado de inicio de sesión
    this.fetchUserProfile().then(() => {
      this.checkIfFollowing() // Solo se llama después de cargar el perfil
    })
    this.getAllBooks()
  }
}
</script>

<style scoped>
.user-profile {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  padding: 2rem;
  font-family: 'Arial', sans-serif;
}

.content-box {
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 400px;
  width: 100%;
  position: relative; /* Esto es clave para posicionar el botón relativo a este contenedor */
}

.profile-image-container {
  position: relative;
  margin-bottom: 1.5rem;
}

.profile-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-info {
  text-align: center;
  margin-bottom: 1rem;
}

.user-info h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 500;
  color: #333;
}

.user-info p {
  margin: 0.5rem 0 0;
  color: #666;
}

.follow-info {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.follow-item {
  display: flex;
  align-items: center;
  color: #555;
  font-size: 0.9rem;
}

.follow-item .icon {
  width: 16px;
  height: 16px;
  margin-right: 0.3rem;
}

.biography-section {
  width: 100%;
  margin-bottom: 1.5rem;
  text-align: center;
  max-height: 300px; /* Opcional: limitar la altura máxima */
  overflow-y: auto; /* Permite desplazarse si el texto supera la altura */
}

.biography-section h2 {
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.biography-section p {
  color: #555;
  font-size: 0.9rem;
  line-height: 1.4;
  margin: 0; /* Evita márgenes inesperados */
  word-wrap: break-word; /* Asegura que las palabras largas no rompan el diseño */
  white-space: pre-wrap; /* Mantiene los saltos de línea escritos por el usuario */
}

@media (max-width: 480px) {
  .content-box {
    padding: 1.5rem;
  }

  .user-info h1 {
    font-size: 1.2rem;
  }

  .follow-info {
    flex-direction: column;
    gap: 0.5rem;
  }

}

.follow-button.disabled {
  background-color: #ccc;
  border: 1px solid #ccc;
  cursor: not-allowed;
  color: #666;
}

.follow-button.disabled:hover {
  background-color: #ccc;
  color: #666;
}

input[type="file"] {
  display: none; /* Oculta el input */
}

.back-button {
  position: absolute; /* Para colocarlo en una esquina del contenedor */
  top: 10px;
  right: 10px;
  background-color: transparent;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  transition: background-color 0.3s;
}

.back-button .icon {
  width: 24px;
  height: 24px;
  fill: #333;
}

.back-button:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.back-button:active {
  background-color: rgba(0, 0, 0, 0.2);
}

.follow-button {
  margin-left: 10px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  border-radius: 20px;
  border: 1px solid #007bff;
  background-color: white;
  color: #007bff;
  cursor: pointer;
  transition: all 0.3s;
}

.follow-button.following {
  background-color: #f1f1f1;
  color: #666;
  border-color: #ccc;
}

.follow-button:hover {
  background-color: #007bff;
  color: white;
}

.carousel-container {
  width: 100%;
  position: relative;
  overflow: hidden;
  margin: 20px 0;
}

.carousel {
  display: flex;
  overflow: hidden;
}

.carousel-track {
  display: flex;
  transition: transform 0.5s ease-in-out;
}

.carousel-image {
  width: 100px;
  height: 150px;
  margin: 0 5px;
  cursor: pointer;
  border-radius: 8px;
  object-fit: cover;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(0, 0, 0, 0.5);
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  z-index: 10;
}

.left-btn {
  left: 10px;
}

.right-btn {
  right: 10px;
}
</style>
