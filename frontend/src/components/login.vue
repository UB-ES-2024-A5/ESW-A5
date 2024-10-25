<template>
  <div class="login-container" :style="{ backgroundImage: 'url(' + backgroundImage + ')' }">
    <div class="login-box">
      <div class="login-form">
        <h1>SIGN IN</h1>
        <form @submit.prevent="handleLogin">
          <div class="input-group">
            <input v-model="email" type="email" placeholder="Email" required />
          </div>
          <div class="input-group">
            <input v-model="password" type="password" placeholder="Password" required />
          </div>
          <button type="submit" class="login-button">Login</button>
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
export default {
  data () {
    return {
      email: '',
      password: '',
      // Set your images here
      boxImage: require('@/assets/foto_box.png'),
      backgroundImage: require('@/assets/foto_fondo_login.png')
    }
  },
  methods: {
    handleLogin () {
      // Handle login logic here
      console.log(`Email: ${this.email}, Password: ${this.password}`)
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
