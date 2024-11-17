
<template>
  <div class="profile-container" :style="{ backgroundImage: 'url(' + backgroundImage + ')' }">
    <div class="profile-box">
      <div class="profile-info">
        <h1>Publisher Profile</h1>
        <div class="profile-image">
          <img :src="userProfileImage" alt="Profile Picture" />
        </div>
        <div class="profile-details">
          <p><strong>Name:</strong> {{ user.name }}</p>
          <p><strong>Email:</strong> {{ user.email }}</p>
          <p><strong>CIF:</strong> {{ user.cif }}</p>
          <p><strong>Publications:</strong> {{ user.publications }}</p>
        </div>
      </div>

      <div v-if="wishlistVisible" class="wishlist-popup">
        <div class="wishlist-content">
          <h2>Your Wishlist</h2>
          <ul>
            <li v-for="book in user.wishlist" :key="book.id">{{ book.title }}</li>
          </ul>
          <button @click="closeWishlist" class="close-button">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import userServices from '../services/UserServices.js'
import bookServices from '../services/BookServices.js'
export default {
  data () {
    return {
      backgroundImage: require('@/assets/fondo_profile.png'),
      userProfileImage: require('@/assets/placeholder_image.png'), // Default placeholder image
      user: {
        name: '',
        email: '',
        cif: '',
        publications: null
      },
      wishlistVisible: false
    }
  },
  methods: {
    showWishlist () {
      this.wishlistVisible = true
    },
    closeWishlist () {
      this.wishlistVisible = false
    },
    async fetchUserProfile () {
      console.log('Fetching user profile...')
      try {
        const userData = await userServices.getActualUser()
        console.log('User data:', userData)
        this.user.name = userData.name
        this.user.email = userData.email
        this.user.cif = userData.cif
        this.user.publications = await bookServices.getBooksByEditorial()
      } catch (error) {
        console.error('Error al obtener los datos del usuario:', error)
      }
    }
  },
  mounted () {
    console.log('Componente montado')
    this.fetchUserProfile()
  }
}
</script>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-color: #f5ece0;
  padding: 0;
  margin: 0;
}

/* Profile box style */
.profile-box {
  display: flex;
  width: 600px; /* Ajustar el ancho si es necesario */
  height: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
  position: relative;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.profile-info {
  width: 100%;
}

.profile-info h1 {
  font-size: 28px;
  margin-bottom: 20px;
  color: #333;
}

.profile-image img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin-bottom: 20px;
}

.profile-details {
  font-size: 18px;
  color: #333;
  margin-bottom: 20px;
}

.profile-details p {
  margin: 10px 0;
}

/* Wishlist button */
.wishlist-button {
  padding: 12px;
  background-color: #007bff;
  border: none;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

/* Wishlist popup */
.wishlist-popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.wishlist-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  width: 400px;
}

.wishlist-content h2 {
  font-size: 24px;
  margin-bottom: 20px;
}

.wishlist-content ul {
  list-style-type: none;
  padding: 0;
  font-size: 18px;
  margin-bottom: 20px;
}

.wishlist-content li {
  margin: 10px 0;
}

.close-button {
  padding: 10px 20px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.close-button:hover {
  background-color: #d32f2f;
}
</style>
