<template>
  <div class="publication-form">
    <div class="form-container">
      <h1>Create a Publication</h1>
      <form @submit.prevent="submitForm">
        <!-- Title Field -->
        <div class="form-group">
          <input type="text" v-model="form.title" placeholder="Title" required @input="validateTitle"/>
          <span v-if="formErrors.title" class="error-icon" @mouseover="showTooltip('title')" @mouseleave="hideTooltip">
            <img src="../assets/error_icon.png" alt="Error" />
            <div v-if="tooltipVisible && currentTooltip === 'title'" class="tooltip">{{ formErrors.title }}</div>
          </span>
          <span v-else-if="formValidations.title" class="success-icon">
            <img src="../assets/check_icon.png" alt="Success" />
          </span>
        </div>

        <!-- Author Field -->
        <div class="form-group">
          <input type="text" v-model="form.author" placeholder="Author" required @input="validateAuthor"/>
          <span v-if="formErrors.author" class="error-icon" @mouseover="showTooltip('author')" @mouseleave="hideTooltip">
            <img src="../assets/error_icon.png" alt="Error" />
            <div v-if="tooltipVisible && currentTooltip === 'author'" class="tooltip">{{ formErrors.author }}</div>
          </span>
          <span v-else-if="formValidations.author" class="success-icon">
            <img src="../assets/check_icon.png" alt="Success" />
          </span>
        </div>

        <!-- Editorial Field -->
        <div class="form-group">
          <input type="text" v-model="form.editorial" placeholder="Editorial" required @input="validateEditorial"/>
          <span v-if="formErrors.editorial" class="error-icon" @mouseover="showTooltip('editorial')" @mouseleave="hideTooltip">
            <img src="../assets/error_icon.png" alt="Error" />
            <div v-if="tooltipVisible && currentTooltip === 'editorial'" class="tooltip">{{ formErrors.editorial }}</div>
          </span>
          <span v-else-if="formValidations.editorial" class="success-icon">
            <img src="../assets/check_icon.png" alt="Success" />
          </span>
        </div>

        <!-- Genre Field -->
        <div class="form-group genre-group">
          <div class="genre-selection">
            <p class="genre-title">Genres</p>
            <div v-for="genre in genres" :key="genre" class="genre-item">
              <label>{{ genre }}</label>
              <input type="checkbox" :value="genre" v-model="form.genre" @change="validateGenreSelection" />
            </div>
          </div>
          <small v-if="errorGenre" class="error-message">{{ errorGenre }}</small>
        </div>

        <!-- Year Field -->
        <div class="form-group">
          <input type="number" v-model="form.year" placeholder="Year of Publication" min="0" required @input="validateYear"/>
          <span v-if="formErrors.year" class="error-icon" @mouseover="showTooltip('year')" @mouseleave="hideTooltip">
            <img src="../assets/error_icon.png" alt="Error" />
            <div v-if="tooltipVisible && currentTooltip === 'year'" class="tooltip">{{ formErrors.year }}</div>
          </span>
          <span v-else-if="formValidations.year" class="success-icon">
            <img src="../assets/check_icon.png" alt="Success" />
          </span>
        </div>

        <!-- ISBN Field -->
        <div class="form-group">
          <input type="text" v-model="form.isbn" placeholder="ISBN" required @input="validateISBN"/>
          <span v-if="formErrors.isbn" class="error-icon" @mouseover="showTooltip('isbn')" @mouseleave="hideTooltip">
            <img src="../assets/error_icon.png" alt="Error" />
            <div v-if="tooltipVisible && currentTooltip === 'isbn'" class="tooltip">{{ formErrors.isbn }}</div>
          </span>
          <span v-else-if="formValidations.isbn" class="success-icon">
            <img src="../assets/check_icon.png" alt="Success" />
          </span>
        </div>

        <!-- Price Field -->
        <div class="form-group">
          <input type="number" v-model="form.price" placeholder="Minimum Price" min="0" step="0.01" required @input="validatePrice"/>
          <span v-if="formErrors.price" class="error-icon" @mouseover="showTooltip('price')" @mouseleave="hideTooltip">
            <img src="../assets/error_icon.png" alt="Error" />
            <div v-if="tooltipVisible && currentTooltip === 'price'" class="tooltip">{{ formErrors.price }}</div>
          </span>
          <span v-else-if="formValidations.price" class="success-icon">
            <img src="../assets/check_icon.png" alt="Success" />
          </span>
        </div>

        <!-- Synopsis Field -->
        <div class="form-group">
          <textarea v-model="form.synopsis" placeholder="Synopsis" class="synopsis-textarea" required @input="validateSynopsis"></textarea>
          <span v-if="formErrors.synopsis" class="error-icon" @mouseover="showTooltip('synopsis')" @mouseleave="hideTooltip">
            <img src="../assets/error_icon.png" alt="Error" />
            <div v-if="tooltipVisible && currentTooltip === 'synopsis'" class="tooltip">{{ formErrors.synopsis }}</div>
          </span>
          <span v-else-if="formValidations.synopsis" class="success-icon">
            <img src="../assets/check_icon.png" alt="Success" />
          </span>
        </div>

        <!-- Add Purchase Link Section -->
        <div class="form-group">
          <p>Add Purchase Link</p>
          <div v-for="(link, index) in form.purchaseLinks" :key="index" class="link-group">
            <input type="url" v-model="form.purchaseLinks[index]" placeholder="Purchase link" />
            <button type="button" @click="removePurchaseLink(index)">-</button>
          </div>
          <button type="button" @click="addPurchaseLink" v-if="form.purchaseLinks.length < 3">+</button>
        </div>

        <button type="submit">Submit</button>
      </form>
    </div>

    <!-- Image Upload Section -->
    <div class="image-container">
      <div v-if="previewImage" class="image-preview">
        <img :src="previewImage" alt="Book cover preview" />
      </div>
      <div v-else class="image-placeholder">
        Book cover image preview
      </div>

      <div class="image-upload">
        <label class="image-label" @click="triggerImageInput">Choose Image</label>
        <input type="file" ref="imageInput" class="image-input" @change="handleImageUpload" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      form: {
        title: '',
        author: '',
        editorial: '',
        genre: [],
        year: '',
        isbn: '',
        price: '',
        synopsis: '',
        image: null,
        purchaseLinks: []
      },
      previewImage: null,
      errorGenre: '',
      formErrors: {
        title: '',
        author: '',
        editorial: '',
        year: '',
        isbn: '',
        price: '',
        synopsis: ''
      },
      formValidations: {
        title: false,
        author: false,
        editorial: false,
        year: false,
        isbn: false,
        price: false,
        synopsis: false
      },
      existingISBNs: ['9781234567890', '9781234567891'],
      genres: ['Action', 'Love', 'Drama', 'Terror', 'Fantasy', 'Sci-Fi', 'Mystery', 'Adventure', 'Historical', 'Romance', 'Thriller', 'Biography', 'Poetry'],
      tooltipVisible: false,
      currentTooltip: '' // Para saber qué tooltip mostrar
    }
  },
  methods: {
    // Método para mostrar el tooltip
    showTooltip (field) {
      this.tooltipVisible = true
      this.currentTooltip = field // Asigna el campo para mostrar el mensaje
    },
    // Método para ocultar el tooltip
    hideTooltip () {
      this.tooltipVisible = false
      this.currentTooltip = '' // Resetea el campo
    },
    validateTitle () {
      const regex = /^[a-zA-Z0-9\s\W]+$/
      this.formValidations.title = regex.test(this.form.title)
      this.formErrors.title = this.formValidations.title ? '' : 'Title can only contain letters, numbers, and symbols.'
    },
    validateAuthor () {
      const regex = /^[a-zA-Z\s]+$/
      this.formValidations.author = regex.test(this.form.author)
      this.formErrors.author = this.formValidations.author ? '' : 'Author name must only contain letters.'
    },
    validateEditorial () {
      const regex = /^[a-zA-Z0-9\s]+$/
      this.formValidations.editorial = regex.test(this.form.editorial)
      this.formErrors.editorial = this.formValidations.editorial ? '' : 'Editorial can only contain letters and numbers.'
    },
    validateYear () {
      const regex = /^(19|20)\d{2}$/
      this.formValidations.year = regex.test(this.form.year)
      this.formErrors.year = this.formValidations.year ? '' : 'Please enter a valid year.'
    },
    validateISBN () {
      this.formValidations.isbn = !this.existingISBNs.includes(this.form.isbn)
      this.formErrors.isbn = this.formValidations.isbn ? '' : 'ISBN already exists.'
    },
    validatePrice () {
      this.formValidations.price = this.form.price > 0
      this.formErrors.price = this.formValidations.price ? '' : 'Price must be greater than zero.'
    },
    validateSynopsis () {
      this.formValidations.synopsis = this.form.synopsis.length > 10
      this.formErrors.synopsis = this.formValidations.synopsis ? '' : 'Synopsis must be at least 10 characters.'
    },
    validateGenreSelection () {
      this.errorGenre = this.form.genre.length === 0 ? 'At least one genre must be selected.' : ''
    },
    addPurchaseLink () {
      this.form.purchaseLinks.push('')
    },
    removePurchaseLink (index) {
      this.form.purchaseLinks.splice(index, 1)
    },
    submitForm () {
      // Lógica para enviar el formulario
    },
    triggerImageInput () {
      this.$refs.imageInput.click()
    },
    handleImageUpload (event) {
      const file = event.target.files[0]
      if (file) {
        this.previewImage = URL.createObjectURL(file)
        this.form.image = file
      }
    }
  }
}
</script>

<style scoped>
.publication-form {
  display: flex;
  justify-content: space-between;
  padding: 20px;
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 1200px;
  margin: 0 auto;
}

/* Estilos para las imágenes */
.success-icon img, .error-icon img {
  width: 20px;
  height: 20px;
}

.error-icon img:hover {
  cursor: pointer;
}

.form-container {
  width: 50%;
  margin: auto;
}

h1 {
  font-size: 1.5em;
  color: #333;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 1rem;
  position: relative;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;
  font-size: 0.9em;
}

.form-group select {
  height: 40px;
}

.form-group input::placeholder,
.form-group select::placeholder,
.form-group textarea::placeholder {
  color: #999;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #4CAF50;
}

.genre-group {
  position: relative;
}

.genre-selection {
  max-height: 100px; /* Nuevo alto más pequeño */
  overflow-y: auto;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 30px 8px 8px;
  margin-top: 10px;
  width: 100%;
}

.genre-title {
  position: absolute;
  top: 0px;
  left: 4px;
  font-size: 0.9em;
  color: #999;
  background-color: #fff;
  padding: 0 5px;
}

.genre-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 0;
}

.genre-item label {
  flex-grow: 1;
}

.genre-item input {
  margin-left: auto;
  transform: translateX(100%); /* Mueve el checkbox a la derecha */
}

.image-label {
  display: inline-block;
  padding: 8px 12px;
  background-color: #4CAF50;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px; /* Espacio entre el botón y el recuadro */
}

.image-input {
  display: none;
}

.image-container {
  width: 30%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.image-placeholder {
  width: 100%;
  height: 200px;
  background-color: #000;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9em;
  text-align: center;
  border-radius: 8px;
}

.image-preview img {
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.synopsis-textarea {
  min-height: 150px;
  resize: none;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;
  font-size: 0.9em;
}

.synopsis-textarea::placeholder {
  color: #999;
}

.synopsis-textarea:focus {
  border-color: #4CAF50;
}

.checkbox-group label {
  display: block;
  font-weight: normal;
  color: #555;
  margin-bottom: 5px;
}

.link-group {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.link-group input {
  flex: 1;
}

.link-group button {
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 5px;
  margin-left: 5px;
  cursor: pointer;
}

button[type="button"],
button[type="submit"] {
  padding: 8px 12px;
  font-size: 0.9em;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button[type="button"] {
  background-color: #f44336;
  color: white;
}

button[type="submit"] {
  background-color: #4CAF50;
  color: white;
  margin-top: 10px;
  width: 100%;
  font-size: 1.1em;
}

.tooltip {
  position: absolute;
  top: 50%;
  left: 110%; /* Alinea el tooltip a la derecha */
  transform: translateY(-50%); /* Centra el tooltip verticalmente */
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 5px;
  border-radius: 5px;
  font-size: 12px;
  z-index: 1;
  white-space: nowrap;
  display: none;
}

.error-icon:hover .tooltip {
  display: block;
}

.error-icon {
  position: relative;
  display: inline-block;
}

.image-preview {
  margin-top: 20px;
}

.image-upload {
  display: flex;
  justify-content: center;
}

.image-label {
  cursor: pointer;
  background-color: #ddd;
  padding: 10px;
  border-radius: 5px;
}

.image-input {
  display: none;
}
</style>
