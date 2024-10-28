<template>
  <div class="signup-container" :style="{ backgroundImage: 'url(' + backgroundImage + ')' }">
    <div class="signup-box">
      <div class="signup-form">
        <h1>USER SIGN UP</h1>
        <form @submit.prevent="handleSignUp">
          <!-- Campo de Nombre -->
          <div class="input-group">
            <span class="input-icon">
              <img :src="accountIcon" alt="Account icon" />
            </span>
            <input v-model="name" type="text" placeholder="Name" required />
          </div>

          <!-- Campo de Apellido -->
          <div class="input-group">
            <span class="input-icon">
              <img :src="accountIcon" alt="Account icon" />
            </span>
            <input v-model="surname" type="text" placeholder="Surname" required />
          </div>

          <!-- Campo de Email -->
          <div class="input-group">
            <span class="input-icon">
              <img :src="mailIcon" alt="Mail icon" />
            </span>
            <input v-model="email" type="email" placeholder="Email" required />
          </div>

          <!-- Campo de Contraseña -->
          <div class="input-group">
            <span class="input-icon">
              <img :src="lockIcon" alt="Lock icon" />
            </span>
            <input :type="showPassword ? 'text' : 'password'" v-model="password" placeholder="Password" required />
            <span class="toggle-password" @click="toggleShowPassword">
              <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i> <!-- Asegúrate de que esto esté correcto -->
            </span>
          </div>

          <!-- Campo de Confirmar Contraseña -->
          <div class="input-group">
            <span class="input-icon">
              <img :src="keyIcon" alt="Key icon" />
            </span>
            <input :type="showConfirmPassword ? 'text' : 'password'" v-model="confirmPassword" placeholder="Confirm Password" required />
            <span class="toggle-password" @click="toggleShowConfirmPassword">
              <i :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
            </span>
          </div>

          <!-- Términos y Condiciones -->
          <div class="terms-conditions">
            <input type="checkbox" v-model="agreedToTerms" required />
            <label>I agree to all statements in <span class="terms-link">terms and conditions</span></label>
          </div>
          <button type="submit" @click="register_user" class="signup-button">sign in</button>
        </form>

        <!-- Enlace para Iniciar Sesión -->
        <p class="login-link">
          Already have an account?
          <router-link to="/login" class="login-link-text">Sign In</router-link>
        </p>
      </div>
      <div class="signup-image">
        <img :src="boxImage" alt="Signup illustration" />
      </div>
    </div>
  </div>
</template>

<script>
import UserService from '../services/UserServices'
export default {
  data () {
    return {
      username: null,
      password: null,
      token: null,
      is_authenticated: false,
      name: null,
      surname: null,
      email: null,
      confirmPassword: null,
      agreedToTerms: false,
      showPassword: false,
      showConfirmPassword: false,
      accountIcon: require('@/assets/account_icon.png'),
      mailIcon: require('@/assets/mail_icon.png'),
      lockIcon: require('@/assets/lock_icon.png'),
      keyIcon: require('@/assets/key_icon.png'),
      boxImage: require('@/assets/foto_signup.png'), // Replace with your signup illustration path
      backgroundImage: require('@/assets/foto_fondo_login.png') // Replace with your signup background path
    }
  },
  methods: {
    validateFields () {
      if (!this.name || !this.surname || !this.email || !this.password || !this.confirmPassword) {
        alert('Please fill in all fields.')
        return false
      }

      if (!this.email.includes('@')) {
        alert('Please enter a valid email address.')
        return false
      }

      if (this.password !== this.confirmPassword) {
        alert('Passwords do not match.')
        return false
      }

      if (!this.agreedToTerms) {
        alert('You must agree to the terms and conditions.')
        return false
      }

      return true
    },

    register_user () {
      if (this.validateFields()) {
        const data = {
          name: this.name,
          surname: this.surname,
          email: this.email,
          password: this.password
        }

        UserService.create(data)
          .then(() => {
            alert('La cuenta se ha creado correctamente. Por favor inicie sesión.')
            this.$router.push({ path: '/login' })
          })
          .catch((error) => {
            console.error(error)
            alert('Hubo un error al crear la cuenta.')
          })
      }
    },
    toggleShowPassword () {
      this.showPassword = !this.showPassword
    },
    toggleShowConfirmPassword () {
      this.showConfirmPassword = !this.showConfirmPassword
    }
  }
}
</script>

<style scoped>
/* Fullscreen container with background */
.signup-container {
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

/* Increased Signup box width */
.signup-box {
  display: flex;
  width: 1000px; /* Adjusted width to fit all fields */
  padding: 30px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
  position: relative;
  justify-content: space-between;
}

/* Signup form styling (left side) */
.signup-form {
  width: 45%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
  padding-right: 30px;
}

/* Sign Up title */
h1 {
  text-align: center;
  font-size: 28px;
  margin-bottom: 20px;
  color: #333;
}

/* Input field styles */
.input-group {
  position: relative;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.input-group input {
  width: 100%;
  padding: 12px 40px 12px 40px; /* Padding for the icon */
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
  box-sizing: border-box;
}

/* Icon on the left of each field */
.input-icon {
  position: absolute;
  left: 10px;
  font-size: 18px;
  color: #777;
}

.input-icon img {
  width: 24px;
  height: 24px;
}

.toggle-password {
  position: absolute;
  right: 10px; /* Ajusta el valor según sea necesario */
  cursor: pointer;
  font-size: 18px;
  color: #000; /* Puedes cambiar el color si es necesario */
  z-index: 1; /* Asegúrate de que el icono esté por encima del campo */
}

/* Terms and Conditions */
.terms-conditions {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  font-size: 14px;
  color: #555;
}

.terms-link {
  color: #007bff;
  cursor: pointer;
  text-decoration: underline;
}

/* Signup button */
.signup-button {
  width: 100%;
  padding: 12px;
  background-color: #007bff;
  border: none;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 20px;
}

/* Login link under the signup form */
.login-link {
  text-align: center;
  margin-top: 10px;
}

.login-link-text {
  color: #007bff;
  text-decoration: none;
}

.login-link-text:hover {
  text-decoration: underline;
}

/* Image styling (right side) */
.signup-image {
  width: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.signup-image img {
  width: 100%;
  height: auto;
  border-radius: 10px;
}

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Arial', sans-serif;
}
</style>
