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
        <h1>{{ user.name }} {{ user.surname }}</h1>
        <button
          class="follow-button"
          :class="{ 'following': isFollowing, 'disabled': !isLoggedIn }"
          @click="toggleFollow"
          :disabled="!isLoggedIn"
        >
          {{ isFollowing ? 'Unfollow' : 'Follow' }}
        </button>
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
        <p>{{ account.bio }}</p>
      </div>

      <button
        v-if="isFollowing"
        @click="showWishlist"
        class="wishlist-btn"
        :disabled="!isLoggedIn"
        :class="{ 'disabled': !isLoggedIn }"
        title="You must be logged in to see the wishlist"
      >
        <!-- Ícono de estrella para la wishlist -->
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon">
          <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
        </svg>
        <span>Wishlist</span>
      </button>

      <button
        v-else
        class="wishlist-btn disabled"
        disabled
        title="You must follow this user to see their wishlist"
      >
        <!-- Ícono de estrella para indicar inaccesible -->
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon">
          <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
        </svg>
        <span>Wishlist</span>
      </button>

      <button @click="showForum" class="forum-btn">
        <!-- Ícono de mensaje cuadrado -->
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="icon">
          <path d="M3 3h18c1.1 0 1.99.89 1.99 1.99v14.02c0 1.1-.89 2-1.99 2H3c-1.1 0-1.99-.89-1.99-1.99V4.99C1.01 3.89 1.89 3 3 3zm0 2v14h18V5H3zm5 3h8v2H8V8z"/>
        </svg>
        <span>Forum</span>
      </button>

      <!-- Wishlist Popup -->
      <div v-if="wishlistVisible" class="wishlist-popup">
        <div class="wishlist-content">
          <h2>{{ user.name }} Wishlist</h2>
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

      <!-- Forum Popup -->
      <div v-if="forumVisible" class="forum-popup">
        <div class="forum-content">
          <div class="forum-header">
            <h2>{{ user.name }}  forum posts</h2>
            <select v-model="forumFilter" @change="filterPosts">
              <option value="participated">Participated</option>
              <option value="liked">Liked</option>
              <option value="disliked">Disliked</option>
            </select>
          </div>
          <!-- Contenedor de tarjetas -->
          <div class="forum-list">
            <div v-for="post in filteredPosts" :key="post.id" class="forum-card">
              <!-- Condicional para mostrar imagen o placeholder -->
              <!-- Verificación para mostrar imagen o placeholder -->
              <img :src="post.img || placeholderImage"
                   alt="Post Image"
                   class="post-image">
              <div class="post-details">
                <p class="post-text">{{ post.text }}</p>
                <div class="post-meta">
                  <span class="post-date">{{ new Date(post.date).toLocaleString() }}</span>
                  <div class="post-reactions">
                    <span>{{ post.likes }} 👍</span>
                    <span>{{ post.dislikes }} 👎</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <button @click="closeForum" class="close-button">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import userServices from '../services/UserServices.js'
import accountServices from '../services/AccountServices.js'
import wishlistServices from '../services/WishlistServices.js'
import forumServices from '../services/ForumServices'
export default {
  data () {
    return {
      profileIcon: require('@/assets/account_icon.png'),
      backgroundImage: require('@/assets/fondo_profile.png'),
      userProfileImage: require('@/assets/placeholder_image.png'), // Default placeholder image
      placeholderImage: require('@/assets/placeholder_image.png'),
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
      isFollowing: false, // Estado de seguimiento
      isLoggedIn: false, // Estado de inicio de sesión
      forumVisible: false,
      forumFilter: 'participated',
      posts: [],
      filteredPosts: []
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
      const userID = this.$route.query.userID // Obtén el userID desde la query string
      try {
        const userData = await userServices.getUserById(userID)
        const accountData = await accountServices.getAccountById(userID)
        this.user.name = userData.name
        this.user.surname = userData.surname
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
    async fetchWishlistsInformation () {
      const userId = this.$route.query.userID
      try {
        const res = await wishlistServices.getWishlistByUserId(userId)
        this.wishlistId = res.id
        await this.fetchBooksInWishlist(this.wishlistId)
      } catch (error) {
        console.error('Error al obtener la wishlist:', error)
      }
    },
    async fetchBooksInWishlist (id) {
      const res = await wishlistServices.readBooksOfWishlist(id)
      this.user.wishlist = res.data
    },
    goBack () {
      this.$router.push('/mainPage_user')
    },
    async checkIfFollowing () {
      try {
        const userID = this.$route.query.userID // Obtén el userID desde la query string
        const followingData = await accountServices.getFollowingAccounts()
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
    showForum () {
      this.fetchForumPosts()
      this.forumVisible = true
    },
    closeForum () {
      this.forumVisible = false
    },
    async fetchForumPosts () {
      try {
        const { data } = {}
        this.posts = data
        this.filterPosts()
      } catch (error) {
        console.error('Error fetching forum posts:', error)
      }
    },
    async filterPosts () {
      const userID = this.$route.query.userID // Obtén el userID desde la query string
      try {
        let data
        if (this.forumFilter === 'participated') {
          // Obtener posts participated
          const response = await forumServices.getAllPostsByAccountId(userID)
          data = response.data
        } else if (this.forumFilter === 'liked') {
          // Obtener posts liked
          const response = await forumServices.getLikedPostsByAccount(userID)
          data = response.data
        } else if (this.forumFilter === 'disliked') {
          // Obtener posts disliked
          const response = await forumServices.getDislikedPostsByAccount(userID)
          data = response.data
        } else {
          data = []
        }
        this.filteredPosts = data
      } catch (error) {
        console.error(`Error fetching ${this.forumFilter} posts:`, error)
      }
    }
  },
  mounted () {
    this.isLoggedIn = this.isUserLoggedIn() // Establece el estado de inicio de sesión
    this.fetchUserProfile()
    this.checkIfFollowing() // Llama después de cargar el perfil
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

.follow-button.disabled,
.wishlist-btn.disabled {
  background-color: #ccc;
  border: 1px solid #ccc;
  cursor: not-allowed;
  color: #666;
}

.follow-button.disabled:hover,
.wishlist-btn.disabled:hover {
  background-color: #ccc;
  color: #666;
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

/* Contenedor principal del foro */
.forum-popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.forum-content {
  background: white;
  width: 90%;
  max-width: 800px;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  max-height: 80%;
}

/* Encabezado del foro */
.forum-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.forum-header h2 {
  font-size: 1.5em;
  color: #333;
}

.forum-header select {
  padding: 8px 12px;
  font-size: 1em;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;
}

/* Contenedor de la lista de posts */
.forum-list {
  display: flex;
  flex-direction: column;
  gap: 1rem; /* Espaciado entre tarjetas */
  max-height: 400px; /* Altura máxima para permitir desplazamiento */
  overflow-y: auto; /* Habilitar scroll vertical si hay muchos posts */
  padding: 1rem;
}

/* Estilos para las tarjetas */
.forum-card {
  display: flex;
  align-items: flex-start;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  gap: 1rem; /* Espaciado entre imagen y contenido */
  position: relative; /* Para facilitar el control del contenido */
}

/* Imagen del post */
.post-image {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  object-fit: cover;
  flex-shrink: 0;
}

/* Detalles del post */
.post-details {
  flex-grow: 1;
}

/* Texto del post */
.post-text {
  font-size: 1rem;
  color: #333;
  margin-bottom: 0.5rem;
  word-wrap: break-word; /* Ajustar palabras largas */
}

/* Meta información (fecha y reacciones) */
.post-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  color: #666;
}

.post-meta span {
  display: flex;
  align-items: center;
  gap: 5px;
}

.post-meta span svg {
  width: 14px;
  height: 14px;
}

/* Botón para cerrar */
.close-button {
  display: block;
  margin: 20px auto 0;
  padding: 10px 20px;
  background: #ff5f5f;
  color: white;
  font-size: 1em;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.close-button:hover {
  background: #e04e4e;
}

.post-date {
  font-style: italic;
  margin-top: 0.5rem;
  align-self: flex-start; /* Alinea la fecha a la izquierda */
  color: #777;
  font-size: 0.75rem;
}

.post-reactions {
  display: flex;
  gap: 1rem; /* Espaciado entre likes y dislikes */
}

/* Scrollbar estilizado (opcional, solo para navegadores compatibles) */
.forum-list::-webkit-scrollbar {
  width: 8px;
}
.forum-list::-webkit-scrollbar-thumb {
  background-color: #bbb;
  border-radius: 4px;
}
.forum-list::-webkit-scrollbar-thumb:hover {
  background-color: #999;
}

.forum-btn {
  margin-top: 10px;
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

.forum-btn:hover {
  background-color: #007bff;
  color: white;
}

.forum-btn .icon {
  width: 18px;
  height: 18px;
  margin-right: 0.5rem;
}

@media (max-width: 480px) {
  .forum-btn {
    font-size: 0.9rem;
  }
}
</style>
