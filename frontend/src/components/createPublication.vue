<template>
  <div class="publication-container" :style="{ backgroundImage: 'url(' + backgroundImage + ')' }">
    <div class="publication-box">
      <div class="fields-container">
        <div class="publication-form">
          <h1>Create a Publication</h1>
          <form @submit.prevent="submitPublication">
            <!-- Campo de Título -->
            <div class="input-group">
              <input
                v-model="title"
                type="text"
                placeholder="Title"
                required
                @input="validateTitle"
              />
              <!-- Icono de validación fuera del campo -->
              <span v-if="title && titleValid !== null" class="validation-icon">
                <img
                  :src="titleValid ? checkIcon : errorIcon"
                  :alt="titleValid ? 'Valid' : 'Invalid'"
                  :title="titleValid ? '' : titleErrorMessage"
                />
              </span>
            </div>

            <!-- Campo de Autor -->
            <div class="input-group">
              <input
                v-model="author"
                type="text"
                placeholder="Author"
                required
                @input="validateAuthor"
              />
              <span v-if="author && authorValid !== null" class="validation-icon">
                <img
                  :src="authorValid ? checkIcon : errorIcon"
                  :alt="authorValid ? 'Valid' : 'Invalid'"
                  :title="authorValid ? '' : authorErrorMessage"
                />
              </span>
            </div>

            <!-- Campo de Editorial -->
            <div class="input-group">
              <input
                v-model="editorial"
                type="text"
                placeholder="Editorial"
                required
                @input="validateEditorial"
              />
              <span v-if="editorial && editorialValid !== null" class="validation-icon">
                <img
                  :src="editorialValid ? checkIcon : errorIcon"
                  :alt="editorialValid ? 'Valid' : 'Invalid'"
                  :title="editorialValid ? '' : editorialErrorMessage"
                />
              </span>
            </div>

            <!-- Campo de Géneros -->
            <div class="input-group">
              <p class="genre-title">Genres</p>
              <div class="genre-selection">
                <div class="genre-box">
                  <div v-for="genre in genres" :key="genre" class="genre-item">
                    <label>{{ genre }}</label>
                    <input
                      type="checkbox"
                      :value="genre"
                      v-model="selectedGenres"
                      @change="validateGenreSelection"
                    />
                  </div>
                </div>
                <span v-if="errorGenre" class="error-message">{{ errorGenre }}</span>
              </div>
            </div>

            <!-- Campo de Año de Publicación -->
            <div class="input-group">
              <input
                v-model="year"
                type="number"
                placeholder="Year of Publication"
                min="0"
                required
                @input="validateYear"
              />
              <span v-if="year && yearValid !== null" class="validation-icon">
                <img
                  :src="yearValid ? checkIcon : errorIcon"
                  :alt="yearValid ? 'Valid' : 'Invalid'"
                  :title="yearValid ? '' : yearErrorMessage"
                />
              </span>
            </div>

            <!-- Campo de ISBN -->
            <div class="input-group">
              <input
                v-model="isbn"
                type="text"
                placeholder="ISBN"
                required
                @input="validateISBN"
                maxlength="13"
              />
              <span v-if="isbn && isbnValid !== null" class="validation-icon">
                <img
                  :src="isbnValid ? checkIcon : errorIcon"
                  :alt="isbnValid ? 'Valid' : 'Invalid'"
                  :title="isbnValid ? '' : isbnErrorMessage"
                />
              </span>
            </div>

            <!-- Campo de Precio -->
            <div class="input-group">
              <input
                v-model="price"
                type="number"
                placeholder="Price"
                min="0"
                step="0.01"
                required
                @input="validatePrice"
              />
              <span v-if="price && priceValid !== null" class="validation-icon">
                <img
                  :src="priceValid ? checkIcon : errorIcon"
                  :alt="priceValid ? 'Valid' : 'Invalid'"
                  :title="priceValid ? '' : priceErrorMessage"
                />
              </span>
            </div>

            <!-- Campo de Sinopsis -->
            <div class="input-group">
              <textarea
                v-model="synopsis"
                placeholder="Synopsis"
                class="synopsis-textarea"
                required
                @input="validateSynopsis"
                maxlength="200"
              ></textarea>
              <span v-if="synopsis && synopsisValid !== null" class="validation-icon">
                <img
                  :src="synopsisValid ? checkIcon : errorIcon"
                  :alt="synopsisValid ? 'Valid' : 'Invalid'"
                  :title="synopsisValid ? '' : synopsisErrorMessage"
                />
              </span>
            </div>

            <!-- Campo de Enlaces de Compra -->
            <div class="input-group">
              <p class="genre-title">Purchase Links</p>
              <div class="link-selection">
                <div v-for="(link, index) in publisherLinks" :key="index" class="link-item">
                  <input
                    v-model="publisherLinks[index]"
                    type="url"
                    placeholder="Enter purchase link"
                    :required="index < 3"
                  />
                  <!-- Mostrar botón de eliminar solo si hay más de un enlace -->
                  <button
                    v-if="publisherLinks.length >= 1"
                    type="button"
                    @click="removeLink(index)"
                    class="remove-link-btn"
                  >
                    -
                  </button>
                </div>
                <!-- Botón para agregar enlaces, visible solo si hay menos de 3 enlaces -->
                <button
                  v-if="publisherLinks.length < 3"
                  type="button"
                  @click="addLink"
                  class="add-link-btn"
                >
                  +
                </button>
              </div>
              <!-- Mensaje cuando no hay enlaces -->
              <span v-if="publisherLinks.length === 0" class="error-message">You can add up to 3 links.</span>
            </div>
            <!-- Campo de Imagen -->
            <div class="input-group">
              <input
                type="file"
                accept="image/jpeg"
                @change="handleImageUpload"
              />
              <span v-if="image && imagePreview" class="image-preview">
                <img :src="imagePreview" alt="Image Preview" />
              </span>
              <span v-if="image && imageError" class="error-message">{{ imageError }}</span>
            </div>

            <!-- Botón para Enviar -->
            <button type="submit" class="publication-button">Create Publication</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import BookServices from '../services/BookServices.js'
export default {
  data () {
    return {
      title: '',
      author: '',
      editorial: '',
      year: '',
      isbn: '',
      price: '',
      synopsis: '',
      selectedGenres: [],
      image: null,
      imagePreview: null,
      imageError: '',
      titleValid: null,
      authorValid: null,
      editorialValid: null,
      yearValid: null,
      isbnValid: null,
      priceValid: null,
      synopsisValid: null,
      errorGenre: '',
      genres: ['Fiction', 'Non-Fiction', 'Fantasy', 'Science Fiction', 'Romance'],
      publisherLinks: [ ],
      titleErrorMessage: 'Title is required.',
      authorErrorMessage: 'Author is required.',
      editorialErrorMessage: 'Editorial is required.',
      yearErrorMessage: 'Enter a valid year.',
      isbnErrorMessage: 'Enter a valid ISBN.',
      priceErrorMessage: 'Enter a valid price.',
      synopsisErrorMessage: 'Synopsis is required.',
      checkIcon: require('../assets/check_icon.png'),
      errorIcon: require('../assets/error_icon.png'),
      backgroundImage: require('../assets/fondo_carrousel2.png')
    }
  },
  computed: {
    canSubmit () {
      return (
        this.titleValid &&
        this.authorValid &&
        this.editorialValid &&
        this.yearValid &&
        this.isbnValid &&
        this.priceValid &&
        this.synopsisValid &&
        this.selectedGenres.length >= 1 &&
        this.selectedGenres.length <= 2 &&
        !this.imageError &&
        this.publisherLinks.every(link => link.trim() === '' || /^(ftp|http|https):\/\/[^ "]+$/.test(link))
      )
    }
  },
  methods: {
    handleImageUpload (event) {
      const file = event.target.files[0]
      if (file && file.type === 'image/jpeg') {
        this.imageError = ''
        this.image = file
        this.imagePreview = URL.createObjectURL(file)
      } else {
        this.imageError = 'Only JPEG images are allowed.'
        this.imagePreview = null
      }
    },
    validateTitle () {
      this.titleValid = this.title.trim().length > 0
    },
    validateAuthor () {
      const regex = /^[A-Za-z\s]+$/
      this.authorValid = regex.test(this.author)
    },
    validateEditorial () {
      const regex = /^[A-Za-z\s]+$/
      this.editorialValid = regex.test(this.editorial)
    },
    validateYear () {
      const currentYear = new Date().getFullYear()
      this.yearValid = this.year >= 1000 && this.year <= currentYear
    },
    validateISBN () {
      // Validar que el ISBN tenga entre 10 y 13 dígitos numéricos
      const regex = /^\d{10,13}$/
      this.isbnValid = regex.test(this.isbn)
    },
    validatePrice () {
      this.priceValid = this.price >= 0 && !isNaN(this.price)
    },
    validateGenreSelection () {
      // Verificar que haya entre 1 y 2 géneros seleccionados
      if (this.selectedGenres.length === 0) {
        this.errorGenre = 'Please select at least one genre.'
      } else if (this.selectedGenres.length > 2) {
        this.errorGenre = 'You can select up to two genres.'
      } else {
        this.errorGenre = ''
      }
    },
    validateSynopsis () {
      this.synopsisValid = this.synopsis.trim().length > 0
    },
    addLink () {
      if (this.publisherLinks.length < 3) {
        this.publisherLinks.push('')
      }
    },
    removeLink (index) {
      // Eliminar el enlace solo si hay más de un enlace
      if (this.publisherLinks.length > 1) {
        this.publisherLinks.splice(index, 1)
      } else {
        // Si es el único enlace, lo eliminamos completamente
        this.publisherLinks = []
      }
    },
    async submitPublication () {
      if (this.canSubmit) {
        try {
          // Convertir la imagen a Base64 de forma asíncrona
          const imageBase64 = await this.convertImageToBase64(this.image)

          // Preparar los datos con las correcciones necesarias
          const data = {
            title: this.title,
            author: this.author,
            gender_main: this.selectedGenres[0] || '',
            gender_secondary: this.selectedGenres[1] || null,
            synopsis: this.synopsis,
            publication_year: parseInt(this.year, 10), // Cambiar a 'publication_year'
            isbn: this.isbn,
            price: parseFloat(this.price) || null,
            img: imageBase64, // Asegurarse de que es una cadena Base64 válida
            links: this.publisherLinks.filter(link => link.trim() !== '')
          }

          console.log('Data sent to server:', data)

          // Enviar los datos al backend
          await BookServices.createBook(data)
          alert('Publication created successfully!')
          this.$router.push({ path: '/mainPage_publisher', query: { token: localStorage.getItem('token') } })
        } catch (error) {
          console.error('Error while creating book:', error)
          alert('Failed to create publication. Please try again.')
        }
      } else {
        alert('Please correct the errors in the form.')
      }
    },
    convertImageToBase64 (image) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onloadend = () => resolve(reader.result)
        reader.onerror = reject
        reader.readAsDataURL(image)
      })
    }
  }
}
</script>

<style scoped>
/* Contenedor general más ancho */
.publication-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}

/* Caja del formulario más ancha y menos alta */
.publication-box {
  width: 80%; /* Aumentamos el ancho del contenedor */
  max-width: 900px; /* Limitar el ancho máximo */
  max-height: 80vh; /* Reducimos la altura máxima al 80% de la ventana */
  background-color: white;
  padding: 20px; /* Reducimos el padding para hacer el recuadro más compacto */
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  overflow-y: auto; /* Habilitar el desplazamiento vertical */
  display: flex;
  flex-direction: column;
}

/* Opcional: Ajustar los márgenes para un espaciado más compacto */
.input-group {
  position: relative;
  margin-bottom: 15px; /* Reducimos el margen entre los campos */
}

/* Contenedor de los campos de entrada */
.fields-container {
  flex: 1; /* Esto permite que el formulario ocupe el espacio disponible */
  overflow-y: auto; /* Habilitar el desplazamiento en caso de que los campos sobrepasen */
}

.input-group input[type="file"] {
  display: block;
  margin: 10px 0;
}

/* Campos de entrada */
.input-group input,
.input-group textarea {
  width: 100%;              /* Ocupa todo el ancho disponible */
  max-width: 100%;          /* Asegura que no se agrande más allá del 100% */
  padding: 10px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ccc;
  box-sizing: border-box;
  resize: none;             /* Impide que los campos se agranden manualmente */
}

/* Ajustes específicos para los textarea */
.input-group textarea {
  min-height: 120px;        /* Establece una altura mínima */
  resize: vertical;         /* Permite solo el ajuste vertical, no horizontal */
}

.input-group textarea {
  min-height: 120px;
}

/* Estilo de los iconos de validación */
.validation-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
}

.validation-icon img {
  width: 100%;
  height: auto;
  cursor: pointer;
}

/* Ajustes de mensaje de error */
.error-message {
  color: red;
  font-size: 12px;
  margin-top: 5px;
}

/* Botón de envío */
.publication-button {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.publication-button:hover {
  background-color: #0056b3;
}

/* Títulos */
.genre-title {
  font-weight: bold;
}
.input-group input[type="file"] {
  display: block;
  margin: 10px 0;
}

.image-preview img {
  max-width: 100%;
  max-height: 200px;
  margin-top: 10px;
}

/* Estilo para el campo de los enlaces de compra */
.link-selection {
  display: flex;
  flex-direction: column;
}

.link-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.link-item input {
  width: 80%;
  padding: 8px;
  font-size: 14px;
  margin-right: 10px;
}

.add-link-btn,
.remove-link-btn {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  cursor: pointer;
  font-size: 14px;
}

.add-link-btn:hover,
.remove-link-btn:hover {
  background-color: #0056b3;
}
</style>
