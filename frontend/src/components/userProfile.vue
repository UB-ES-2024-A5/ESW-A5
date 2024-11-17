<template>
  <div class="profile-container" :style="{ backgroundImage: 'url(' + backgroundImage + ')' }">
    <div class="profile-box">
      <div class="profile-info">
        <h1>User Profile</h1>

        <!-- Profile Image with a click to upload -->
        <div class="profile-image" @click="selectImage">
          <img :src="userProfileImage" alt="Profile Picture" />
        </div>

        <!-- Profile Details -->
        <div class="profile-details">
          <p><strong>Name:</strong> {{ user.name }}</p>
          <p><strong>Surname:</strong> {{ user.surname }}</p>
          <p><strong>Email:</strong> {{ user.email }}</p>
        </div>

        <!-- Wishlist Button -->
        <button @click="showWishlist" class="wishlist-button">View Wishlist</button>

        <!-- Back Button -->
        <router-link to="/mainpage_user">
          <button class="back-button">Back</button>
        </router-link>
      </div>

      <!-- Wishlist Popup -->
      <div v-if="wishlistVisible" class="wishlist-popup">
        <div class="wishlist-content">
          <h2>Your Wishlist</h2>
          <ul>
            <li v-for="book in user.wishlist.data" :key="book.id">
              <router-link :to="{ path: '/book', query: { bookId: book.id } }">
                <strong>{{ book.title }}</strong>
              </router-link>
              - {{ book.author }}
            </li>
          </ul>
          <button @click="closeWishlist" class="close-button">Close</button>
        </div>
      </div>

      <!-- File Input for Image Selection (hidden) -->
      <input type="file" ref="fileInput" @change="handleFileChange" accept="image/*" hidden />
    </div>
  </div>
</template>
<script>
import userServices from '../services/UserServices.js'
import wishlistServices from '../services/WishlistServices.js'
export default {
  data () {
    return {
      backgroundImage: require('@/assets/fondo_profile.png'),
      userProfileImage: require('@/assets/placeholder_image.png'), // Default placeholder image
      user: {
        name: '',
        surname: '',
        email: '',
        wishlist: [],
        wishlistId: ''
      },
      wishlistVisible: false
    }
  },
  methods: {
    showWishlist () {
      this.wishlistVisible = true
      this.fetchWishlistsInformation()
    },
    closeWishlist () {
      this.wishlistVisible = false
    },
    selectImage () {
      // Trigger the file input when the profile image is clicked
      this.$refs.fileInput.click()
    },
    handleFileChange (event) {
      const file = event.target.files[0]
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader()
        reader.onload = () => {
          this.userProfileImage = reader.result
        }
        reader.readAsDataURL(file)
      }
    },
    async fetchUserProfile () {
      console.log('Fetching user profile...')
      try {
        const userData = await userServices.getActualUser()
        console.log('User data:', userData)
        this.user.name = userData.name
        this.user.surname = userData.surname
        this.user.email = userData.email
      } catch (error) {
        console.error('Error al obtener los datos del usuario:', error)
      }
    },
    async fetchWishlistsInformation () {
      const res = await wishlistServices.getMyWishlists()
      this.wishlistId = res.data[0].id
      this.fetchBooksInWishlist(this.wishlistId)
    },
    async fetchBooksInWishlist (id) {
      const res = await wishlistServices.readBooksOfWishlist(id)
      console.log(res)
      this.user.wishlist = res.data
    }
  },
  mounted () {
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

/* Ajuste de tamaño para centrar la caja */
.profile-box {
  display: flex;
  width: 600px; /* Ajustar el ancho si es necesario */
  height: 500px;
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
  font-size: 32px;
  margin-bottom: 20px;
  color: #333;
}

/* Center the profile image */
.profile-image {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 250px;
  height: 250px;
  margin-bottom: 20px;
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
  margin-left: 175px;
}

.profile-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Profile details */
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
  margin-bottom: 10px;
}

/* Back button */
.back-button {
  padding: 12px;
  background-color: #6c757d;
  border: none;
  color: white;
  border-radius: 5px;
  cursor: pointer;
}

.back-button:hover {
  background-color: #5a6268;
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
