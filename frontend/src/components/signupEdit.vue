<template>
  <div class="signup-container" :style="{ backgroundImage: 'url(' + backgroundImage + ')' }">
    <div class="signup-box">
      <div class="signup-form">
        <h1>PUBLISHER SIGN UP</h1>
        <form @submit.prevent="register_user">
          <!-- Campo de CIF -->
          <div class="input-group">
            <span class="input-icon">
              <img :src="cifIcon" alt="CIF icon" />
            </span>
            <input
              v-model="cif"
              type="text"
              placeholder="CIF"
              required
              @input="validateCIF"
            />
            <span v-if="cif && cifValid !== null" class="validation-icon">
              <img
                :src="cifValid ? checkIcon : errorIcon"
                :alt="cifValid ? 'Valid' : 'Invalid'"
                :title="cifValid ? '' : cifErrorMessage"
              />
            </span>
          </div>

          <!-- Campo de Nombre de la Editorial -->
          <div class="input-group">
            <span class="input-icon">
              <img :src="accountIcon" alt="Account icon" />
            </span>
            <input
              v-model="name"
              type="text"
              placeholder="Name"
              required
              @input="validateName"
            />
            <span v-if="name && nameValid !== null" class="validation-icon">
              <img
                :src="nameValid ? checkIcon : errorIcon"
                :alt="nameValid ? 'Valid' : 'Invalid'"
                :title="nameValid ? '' : nameErrorMessage"
              />
            </span>
          </div>

          <!-- Campo de Email -->
          <div class="input-group">
            <span class="input-icon">
              <img :src="mailIcon" alt="Mail icon" />
            </span>
            <input
              v-model="email"
              type="email"
              placeholder="Email"
              required
              @input="validateEmail"
            />
            <span v-if="email && emailValid !== null" class="validation-icon">
              <img
                :src="emailValid ? checkIcon : errorIcon"
                :alt="emailValid ? 'Valid' : 'Invalid'"
                :title="emailValid ? '' : emailErrorMessage"
              />
            </span>
          </div>

          <!-- Campo de Contraseña -->
          <div class="input-group">
            <span class="input-icon">
              <img :src="lockIcon" alt="Lock icon" />
            </span>
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              placeholder="Password"
              required
              @input="validatePassword"
            />
            <span class="toggle-password" @click="toggleShowPassword">
              <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
            </span>
            <span v-if="password && passwordValid !== null" class="validation-icon">
              <img
                :src="passwordValid ? checkIcon : errorIcon"
                :alt="passwordValid ? 'Valid' : 'Invalid'"
                :title="passwordValid ? '' : passwordErrorMessage"
              />
            </span>
          </div>

          <!-- Campo de Confirmar Contraseña -->
          <div class="input-group">
            <span class="input-icon">
              <img :src="keyIcon" alt="Key icon" />
            </span>
            <input
              :type="showConfirmPassword ? 'text' : 'password'"
              v-model="confirmPassword"
              placeholder="Confirm Password"
              required
              @input="validateConfirmPassword"
            />
            <span class="toggle-password" @click="toggleShowConfirmPassword">
              <i :class="showConfirmPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
            </span>
            <span v-if="confirmPassword && confirmPasswordValid !== null" class="validation-icon">
              <img
                :src="confirmPasswordValid ? checkIcon : errorIcon"
                :alt="confirmPasswordValid ? 'Valid' : 'Invalid'"
                :title="confirmPasswordValid ? '' : confirmPasswordErrorMessage"
              />
            </span>
          </div>

          <!-- Términos y Condiciones -->
          <div class="terms-conditions">
            <input type="checkbox" v-model="agreedToTerms" required />
            <label>I agree to all statements in <span class="terms-link">terms and conditions</span></label>
          </div>
          <button type="submit" class="signup-button">Register</button>
        </form>

        <!-- Enlace para Iniciar Sesión -->
        <p class="login-link">
          Already have an account?
          <router-link to="/login" class="login-link-text">Sign In</router-link>
        </p>
      </div>
      <div class="signup-image">
        <img :src="boxEditImage" alt="Signup illustration" />
      </div>
    </div>
  </div>
</template>

<script>
import Swal from 'sweetalert2'
import UserService from '../services/UserServices'
import AccountService from '../services/AccountServices'

export default {
  data () {
    return {
      name: '',
      cif: '',
      email: '',
      password: '',
      confirmPassword: '',
      nameValid: null,
      cifValid: null,
      surnameValid: null,
      emailValid: null,
      passwordValid: null,
      confirmPasswordValid: null,
      agreedToTerms: false,
      nameErrorMessage: 'Only letters are allowed.',
      surnameErrorMessage: 'Only letters are allowed.',
      emailErrorMessage: 'Please enter a valid email address -> example@gmail.com',
      passwordErrorMessage: 'Password must be at least 8 characters, contain a symbol and an uppercase letter.',
      confirmPasswordErrorMessage: 'Passwords do not match.',
      showPassword: false,
      showConfirmPassword: false,
      accountIcon: require('@/assets/account_icon.png'),
      cifIcon: require('@/assets/cif_icon.png'),
      boxEditImage: require('@/assets/signupEditImage.png'),
      mailIcon: require('@/assets/mail_icon.png'),
      lockIcon: require('@/assets/lock_icon.png'),
      keyIcon: require('@/assets/key_icon.png'),
      checkIcon: require('@/assets/check_icon.png'),
      errorIcon: require('@/assets/error_icon.png'),
      boxImage: require('@/assets/foto_signup.png'),
      backgroundImage: require('@/assets/foto_fondo_login.png')
    }
  },
  computed: {
    canRegister () {
      return (
        this.nameValid &&
        this.emailValid &&
        this.passwordValid &&
        this.confirmPasswordValid &&
        this.agreedToTerms &&
        this.cifValid
      )
    }
  },
  methods: {
    validateName () {
      const nameRegex = /^[a-zA-ZÀ-ÿ\s]+$/ // solo letras y espacios permitidos
      this.nameValid = nameRegex.test(this.name) && this.name.trim().length > 0
    },
    validateCIF () {
      const cifRegex = /^[A-Za-z]\d{8}$/ // CIF format: starts with a letter followed by 8 digits
      this.cifValid = cifRegex.test(this.cif)
    },
    validateEmail () {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      this.emailValid = emailRegex.test(this.email)
    },
    validatePassword () {
      const length = /^.{8,40}$/
      const hasUppercase = /[A-Z]/
      const hasSymbol = /[\W_]/

      const isValidLength = length.test(this.password)
      const containsUppercase = hasUppercase.test(this.password)
      const containsSymbol = hasSymbol.test(this.password)
      this.passwordValid = isValidLength && containsUppercase && containsSymbol
    },
    validateConfirmPassword () {
      this.confirmPasswordValid = this.password === this.confirmPassword
    },
    toggleShowPassword () {
      this.showPassword = !this.showPassword
    },
    toggleShowConfirmPassword () {
      this.showConfirmPassword = !this.showConfirmPassword
    },
    register_user () {
      if (this.canRegister) {
        const data = {
          name: this.name,
          email: this.email,
          password: this.password,
          is_editor: true,
          cif: this.cif
        }
        UserService.create(data)
          .then((res) => {
            const userId = res.id
            Swal.fire({
              title: 'Account Created!',
              text: 'La cuenta se ha creado correctamente. Por favor inicie sesión.',
              icon: 'success',
              confirmButtonText: 'OK'
            })
            AccountService.create(userId).then(() => {})
            this.$router.push({ path: '/login' })
          })
          .catch((error) => {
            console.error(error)
            Swal.fire({
              title: 'Error',
              text: 'Hubo un error al crear la cuenta.',
              icon: 'error',
              confirmButtonText: 'Try Again'
            })
          })
      } else {
        Swal.fire({
          title: 'Form Errors',
          text: 'Please correct the errors in the form.',
          icon: 'warning',
          confirmButtonText: 'Review'
        })
      }
    }
  }
}
</script>

<style scoped>

.signup-button {
  font-family: 'Roboto', sans-serif; /* Nueva fuente */
  font-weight: bold;
  font-size: 16px;
}

.input-group {
  position: relative;
  margin-bottom: 15px;
}

.validation-icon {
  position: absolute;
  right: -30px;
  top: 50%;
  transform: translateY(-50%);
}

.validation-icon img {
  width: 20px;
  height: 20px;
}

.validation-icon img[title] {
  position: relative;
}

.validation-icon img[title]:hover:after {
  content: attr(title);
  position: absolute;
  bottom: 100%;
  right: 0;
  background-color: #f44336;
  color: white;
  padding: 5px;
  border-radius: 5px;
  font-size: 12px;
  white-space: nowrap;
}

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
  padding: 12px 40px 12px 40px;
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
  right: 10px;
  cursor: pointer;
  font-size: 18px;
  color: #000;
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
