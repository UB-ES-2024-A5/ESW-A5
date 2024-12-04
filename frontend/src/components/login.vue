<template>
  <div class="login-container" :style="{ backgroundImage: 'url(' + backgroundImage + ')' }">
    <div class="login-box">
      <div class="login-form">
        <h1>SIGN IN</h1>
        <form @submit.prevent="login_user">
          <div class="input-group">
            <input v-model="email" type="email" placeholder="Email" required />
          </div>
          <div class="input-group">
            <input v-model="password" type="password" placeholder="Password" required />
          </div>
          <button type="submit" class="login-button">Sign in</button>
        </form>
        <!-- Sign Up link under the form -->
        <p class="signup-link">
          Don't have an account?
          <router-link to="/signup" class="signup-link-text">Sign Up</router-link>
        </p>
      </div>
      <div class="login-image">
        <img :src="boxImage" alt="Login illustration" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Swal from 'sweetalert2'
import userServices from '../services/UserServices.js'
import WishlistServices from '../services/WishlistServices.js'

export default {
  data () {
    return {
      email: null,
      password: null,
      token: null,
      is_authenticated: false,
      boxImage: require('../assets/foto_box.png'),
      backgroundImage: require('../assets/foto_fondo_login.png')
    }
  },
  methods: {
    async login_user (event) {
      /*
      const data = `username=${this.email}&password=${this.password}`
      const path = 'https://esa05-cyc9agehcmd3gudg.francecentral-01.azurewebsites.net/api/v1/login/access-token'
      */
      const data = `username=${this.email}&password=${this.password}`
      const path = process.env.API_URL + '/api/v1/login/access-token'

      try {
        const res = await axios.post(path, data, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })
        console.log(res)
        this.is_authenticated = true
        this.token = res.data.access_token

        // Guardamos el token en localStorage
        localStorage.setItem('token', this.token)

        // Configuramos Axios para que use el token automáticamente en futuras solicitudes
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`

        // Llamamos a getActualUser y esperamos la respuesta
        const userInfo = await userServices.getActualUser()

        // Verificamos si el usuario es editor y redirige en consecuencia
        if (userInfo.is_editor) {
          Swal.fire({
            icon: 'success',
            title: 'Welcome!',
            text: 'Redirecting to the publisher\'s page...',
            timer: 2000,
            showConfirmButton: false
          })
          this.$router.push({ path: '/mainPage_publisher' })
        } else {
          await this.createWishlist()
          Swal.fire({
            icon: 'success',
            title: 'Welcome!',
            text: 'Redirecting to the user\'s page...',
            timer: 2000,
            showConfirmButton: false
          })
          this.$router.push({ path: '/mainPage_user' })
        }
      } catch (error) {
        console.error(error)
        Swal.fire({
          icon: 'error',
          title: 'Login Failed',
          text: 'Email or Password incorrect. Please try again.'
        })
      }
    },
    async createWishlist () {
      await WishlistServices.createWishlistOnLogin()
    }
  }
}
</script>

<style scoped>
/* Fullscreen container with background */
.login-container {
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

/* Login box style */
.login-box {
  display: flex; /* Use flexbox to place form and image side by side */
  width: 900px; /* Increased width to allow space */
  padding: 30px; /* Add padding for a larger feel */
  background: rgba(255, 255, 255, 0.6); /* Slight transparency */
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2); /* Deeper shadow for depth */
  position: relative;
  justify-content: space-between; /* Ensure space between form and image */
}

/* Login form styling (left side) */
.login-form {
  width: 45%; /* Form takes 45% width */
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center; /* Center text horizontally */
  padding-right: 30px; /* Add space between the form and the image */
}

/* Sign In title */
h1 {
  text-align: center;
  font-size: 28px;
  margin-bottom: 20px;
  color: #333; /* Darker text for contrast */
}

/* Input field styles */
.input-group {
  margin-bottom: 15px;
}

.input-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px; /* Larger input font size */
  box-sizing: border-box;
}

/* Login button */
.login-button {
  font-family: 'Roboto', sans-serif; /* Nueva fuente */
  font-weight: bold; /* Negrita */
  font-size: 16px;
  width: 100%;
  padding: 12px;
  background-color: #007bff;
  border: none;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 20px;
}

/* Sign-up link under the login form */
.signup-link {
  text-align: center; /* Center the text under the form */
  margin-top: 10px;
}

.signup-link-text {
  color: #007bff;
  text-decoration: none;
}

.signup-link-text:hover {
  text-decoration: underline;
}

/* Image styling (right side) */
.login-image {
  width: 50%; /* Image takes 50% width */
  display: flex;
  justify-content: center;
  align-items: center; /* Center the image vertically */
}

.login-image img {
  width: 100%;
  height: auto;
  border-radius: 10px;
}

/* Ensure there's no margin around the body and html */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Arial', sans-serif;
}
</style>
