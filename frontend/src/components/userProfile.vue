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
        <button @click="selectImage" class="change-icon-btn" aria-label="Change profile icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon">
            <path d="M5 20h4l11-11-4-4L5 16v4zm14-14l-4-4 2-2 4 4-2 2z" />
          </svg>
        </button>
        <input type="file" accept="image/jpeg" ref="fileInput" style="display: none;" @change="handleFileChange">
      </div>
      <div class="user-info">
        <h1>{{ user.name }} {{ user.surname }}</h1>
        <p>{{ user.email }}</p>
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
        <p v-if="!isEditingBio">{{ account.bio }}</p>
        <textarea v-else v-model="editedBiography" rows="4" class="bio-textarea"></textarea>
        <button @click="toggleEditBio" class="edit-bio-btn">
          {{ isEditingBio ? 'Save' : 'Edit Biography' }}
        </button>
      </div>

      <button @click="showWishlist" class="wishlist-btn">
        <!-- Ícono de estrella para la wishlist -->
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon">
          <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
        </svg>
        <span>Wishlist</span>
      </button>

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
    </div>
  </div>
</template>

<script>
import userServices from '../services/UserServices.js'
import accountServices from '../services/AccountServices.js'
import Swal from 'sweetalert2'
import wishlistServices from '../services/WishlistServices.js'
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
      wishlistVisible: false,
      isEditingBio: false, // Estado de edición de la biografía
      editedBiography: '' // Biografía temporal mientras se edita
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
    async fetchUserProfile () {
      console.log('Fetching user profile...')
      try {
        const userData = await userServices.getActualUser()
        const accountData = await accountServices.getActualAccount()
        console.log('User data:', userData)
        this.user.name = userData.name
        this.user.surname = userData.surname
        this.user.email = userData.email
        this.account.num_followers = accountData.num_followers || '0'
        this.account.num_following = accountData.num_following || '0'
        this.account.bio = accountData.bio
        // Mostrar placeholder si no hay foto de perfil
        this.userProfileImage = accountData.photo || this.profileIcon
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
    },
    async toggleEditBio () {
      if (this.isEditingBio) {
        // Validar la biografía antes de guardar
        const trimmedBio = this.editedBiography.trim()
        if (trimmedBio.length > 200) {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'The biography cannot exceed 200 characters.',
            timer: 2000,
            showConfirmButton: false
          })
          return // No guardar si no cumple con la validación
        }

        if (this.editedBiography !== trimmedBio) {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'The biography cannot have any blank spaces at the beginning or end.',
            timer: 2000,
            showConfirmButton: false
          })
          return // No guardar si no cumple con la validación
        }
        // Guardar en el servidor
        const data = {
          bio: trimmedBio
        }
        await accountServices.updateAccount(data)
        await this.fetchUserProfile()
      } else {
        // Entrar en modo edición
        this.editedBiography = this.account.bio
      }
      this.isEditingBio = !this.isEditingBio
    },
    selectImage () {
      this.$refs.fileInput.click()
    },
    async handleFileChange (event) {
      const file = event.target.files[0]
      if (!file || file.type !== 'image/jpeg') {
        Swal.fire({
          icon: 'error',
          title: 'Invalid format',
          text: 'Por favor selecciona un archivo JPEG.',
          timer: 2000,
          showConfirmButton: false
        })
        return
      }

      try {
        const imageBase64 = await this.convertImageToBase64(file)
        this.userProfileImage = imageBase64

        // Guardar en el servidor
        const data = {
          photo: imageBase64
        }
        await accountServices.updateAccount(data)
        await this.fetchUserProfile()
        Swal.fire({
          icon: 'success',
          title: 'Photo updated',
          text: 'Your profile photo has been updated successfully.',
          timer: 2000,
          showConfirmButton: false
        })
      } catch (error) {
        console.error('Error al actualizar la foto:', error)
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'The profile picture could not be updated.',
          timer: 2000,
          showConfirmButton: false
        })
      }
    },
    convertImageToBase64 (image) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onloadend = () => resolve(reader.result)
        reader.onerror = reject
        reader.readAsDataURL(image)
      })
    },
    goBack () {
      this.$router.push('/mainPage_user')
    }
  },
  mounted () {
    this.fetchUserProfile()
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

.change-icon-btn {
  position: absolute;
  bottom: 0;
  right: 0;
  background-color: white;
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s;
}

.change-icon-btn:hover {
  background-color: #f0f0f0;
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

.bio-textarea {
  width: 100%;
  padding: 0.5rem;
  font-size: 0.9rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: vertical; /* Permite al usuario ajustar el tamaño mientras edita */
  margin-bottom: 0.5rem;
  max-height: 150px; /* Altura máxima ajustable */
}

.edit-bio-btn {
  background-color: #f0f0f0;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.edit-bio-btn:hover {
  background-color: #e0e0e0;
}

.wishlist-btn {
  display: flex;
  align-items: center;
  background-color: transparent;
  color: #007bff;
  border: 1px solid #007bff;
  border-radius: 20px;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
}

.wishlist-btn:hover {
  background-color: #007bff;
  color: white;
}

.wishlist-btn .icon {
  width: 18px;
  height: 18px;
  margin-right: 0.5rem;
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

  .wishlist-btn {
    font-size: 0.9rem;
  }
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
</style>
