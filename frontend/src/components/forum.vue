<template>
  <div class="forum-background">
    <div class="forum-container">
      <!-- Back Button -->
      <button @click="goBack" class="back-button-forum">Back</button>

      <h1 class="forum-title">BookNet Forum</h1>

      <!-- Topic List -->
      <div>
        <div class="forum-header">
          <h2 class="forum-subtitle">Posts</h2>
          <button @click="addNewTopic()" class="new-topic-button">New Post</button>
        </div>

        <div class="topic-list-container">
          <ul class="topic-list">
            <topic-item
              v-for="(topic, index) in topics"
              :key="index"
              :topic="topic"
              :currentUserId="current_user.id"
              @respond="respondToPost"
              @like="likePost"
              @dislike="dislikePost"
              @view-profile="viewProfilePost"
              @view-responses="viewResponsesPost"
              @delete="deleteMyPost"
            />
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Swal from 'sweetalert2'
import TopicItem from '../components/postForumItem.vue'
import ForumServices from '../services/ForumServices.js'
import UserServices from '../services/UserServices.js'
import AccountServices from '../services/AccountServices.js'

export default {
  components: {
    TopicItem
  },
  data () {
    return {
      topics: [],
      current_topic: null,
      current_user: {id: '1'},
      topics_selected: [],
      image: null,
      imagePreview: null,
      imageError: null
    }
  },
  methods: {
    async getMyReaction (postId) {
      try {
        const myReact = await ForumServices.getReactionByPostId(postId)
        return myReact ? myReact.type : null // Devolver el tipo de reacción o null
      } catch (e) {
        return null
      }
    },
    async getPostMyFollowing () {
      try {
        const posts = await ForumServices.getAllPostsFromFollowings()
        console.log('Resultados:', posts.data)
        // Mapear y agregar atributos adicionales
        this.topics = await Promise.all(
          posts.data.map(async (post) => {
            // Obtener datos del usuario y la cuenta
            // eslint-disable-next-line camelcase
            const resultMyReaction = await this.getMyReaction(post.id)
            const account = await AccountServices.getAccountById(post.account_id) // `account_id` debe estar en el post
            const user = await UserServices.getUserById(account.id) // Asumiendo que `account` tiene `user_id`
            const responses = await ForumServices.getResponsesForPost(post.id)
            // Agregar nuevos atributos al post
            return {
              // Copiar los atributos originales del post
              id: post.id,
              text: post.text,
              image: post.img,
              likes: post.likes,
              dislikes: post.dislikes,
              date: post.date,
              responses: [],
              num_responses: responses.count,
              profileImg: account.photo || 'default_account_icon.png', // Imagen de perfil
              name: user.name || 'Unknown User', // Nombre de usuario
              isEditor: user.is_editor || false, // Si el usuario es editor
              account_id: post.account_id,
              my_reaction: resultMyReaction
            }
          })
        )
        this.topics.sort((a, b) => new Date(b.date) - new Date(a.date))
      } catch (error) {
        console.error('Error al buscar:', error)
      }
    },
    async getMyPosts () {
      try {
        const posts = await ForumServices.getAllMyPosts()
        console.log('Resultados:', posts.data)
        // Mapear y agregar atributos adicionales
        const myTopics = await Promise.all(
          posts.data
            .filter(post => post.parent_forum_id === null) // Excluir el usuario logueado
            .map(async (post) => {
              // Obtener datos del usuario y la cuenta
              // eslint-disable-next-line camelcase
              const resultMyReaction = await this.getMyReaction(post.id)
              const account = await AccountServices.getAccountById(post.account_id) // `account_id` debe estar en el post
              const user = await UserServices.getUserById(account.id) // Asumiendo que `account` tiene `user_id`
              const responses = await ForumServices.getResponsesForPost(post.id)
              // Agregar nuevos atributos al post
              return {
                // Copiar los atributos originales del post
                id: post.id,
                text: post.text,
                image: post.img,
                likes: post.likes,
                dislikes: post.dislikes,
                date: post.date,
                responses: [],
                num_responses: responses.count,
                profileImg: account.photo || 'default_account_icon.png', // Imagen de perfil
                name: user.name || 'Unknown User', // Nombre de usuario
                isEditor: user.is_editor || false, // Si el usuario es editor
                account_id: post.account_id,
                my_reaction: resultMyReaction
              }
            })
        )
        myTopics.sort((a, b) => new Date(b.date) - new Date(a.date))
        this.topics = [...this.topics, ...myTopics]
      } catch (error) {
        console.error('Error al buscar:', error)
      }
    },
    async goBack () {
      try {
        const userInfo = await UserServices.getActualUser()
        if (userInfo.is_editor) {
          this.$router.push({path: '/mainPage_publisher'})
        } else {
          this.$router.push({path: '/mainPage_user'})
        }
      } catch (error) {
        console.error('Error redirecting:', error)
        Swal.fire({
          icon: 'error',
          title: 'Oops!',
          text: 'Something went wrong. Please try again later.'
        })
      }
    },
    addNewTopic () {
      Swal.fire({
        title: 'Add New Post',
        html: `
          <textarea id="message" class="swal2-textarea" placeholder="Enter your message" style="width: 80%; height: 150px;"></textarea>
          <div class="input-group">
            <input
              type="file"
              accept="image/jpeg"
              id="image-upload"
              style="margin-bottom: 10px" "margin-top: 10px" "text-align: center"
            />
            <div id="image-preview-container" class="image-preview"></div>
            <span id="image-error-message" class="error-message"></span>
          </div>
        `,
        showCancelButton: true,
        preConfirm: () => {
          const message = document.getElementById('message').value
          if (!message) {
            Swal.showValidationMessage('Please enter a message')
          } else {
            return {message}
          }
        }
      }).then(async (result) => {
        if (result.isConfirmed) {
          const {message} = result.value
          console.warn(this.imagePreview)
          const imgBase64 = this.image ? await this.convertImageToBase64(this.image) : null
          const newTopic = {
            text: message,
            ...(this.imagePreview != null ? {img: imgBase64} : {})
          }
          await ForumServices.createPost(newTopic)
          Swal.fire({
            icon: 'success',
            title: 'Success!',
            text: 'Post created successfully!'
          })
        }
      })
      // Declarar `this.imagePreview` aquí para asegurar que sea accesible
      this.imagePreview = null // Initializer como null
      // Vincular el evento de cambio de imagen
      const imageInput = document.getElementById('image-upload')
      imageInput.addEventListener('change', (event) => {
        const file = event.target.files[0]
        const previewContainer = document.getElementById('image-preview-container')
        const errorMessageContainer = document.getElementById('image-error-message')
        if (file && file.type === 'image/jpeg') {
          this.imagePreview = URL.createObjectURL(file) // Assign la URL de la imagen a `this.imagePreview`
          this.image = file
          console.warn(this.image)
          // Actualizar el DOM con la vista previa de la imagen
          previewContainer.innerHTML = `<img src="${this.imagePreview}" alt="Image Preview" style="max-width: 80%; height: auto;" />`
          // Limpiar mensajes de error
          errorMessageContainer.textContent = ''
        } else {
          // Mostrar mensaje de error si el archivo no es válido
          previewContainer.innerHTML = ''
          errorMessageContainer.textContent = 'Por favor, selecciona una imagen en formato JPEG.'
        }
      })
    },
    respondToPost (topic) {
      this.current_topic = topic
      Swal.fire({
        title: 'Respond New Post',
        html: `
          <textarea id="message" class="swal2-textarea" placeholder="Enter your message" style="width: 80%; height: 150px;"></textarea>
          <div class="input-group">
            <input
              type="file"
              accept="image/jpeg"
              id="image-upload"
              style="margin-bottom: 10px" "margin-top: 10px" "text-align: center"
            />
            <div id="image-preview-container" class="image-preview"></div>
            <span id="image-error-message" class="error-message"></span>
          </div>
        `,
        showCancelButton: true,
        preConfirm: () => {
          const message = document.getElementById('message').value
          if (!message) {
            Swal.showValidationMessage('Please enter a message')
          } else {
            return {message}
          }
        }
      }).then(async (result) => {
        if (result.isConfirmed) {
          const {message} = result.value
          const imgBase64 = this.image ? await this.convertImageToBase64(this.image) : null
          const newTopic = {
            text: message,
            ...(this.imagePreview != null ? {img: imgBase64} : {})
          }
          await ForumServices.createResponse(this.current_topic.id, newTopic)
          this.current_topic.num_responses += 1
          Swal.fire({
            icon: 'success',
            title: 'Success!',
            text: 'Respond created successfully!'
          })
        }
      })
      // Declarar `this.imagePreview` aquí para asegurar que sea accesible
      this.imagePreview = null // Initializer como null
      // Vincular el evento de cambio de imagen
      const imageInput = document.getElementById('image-upload')
      imageInput.addEventListener('change', (event) => {
        const file = event.target.files[0]
        const previewContainer = document.getElementById('image-preview-container')
        const errorMessageContainer = document.getElementById('image-error-message')
        if (file && file.type === 'image/jpeg') {
          this.imagePreview = URL.createObjectURL(file) // Assign la URL de la imagen a `this.imagePreview`
          this.image = file
          // Actualizar el DOM con la vista previa de la imagen
          previewContainer.innerHTML = `<img src="${this.imagePreview}" alt="Image Preview" style="max-width: 80%; height: auto;" />`
          // Limpiar mensajes de error
          errorMessageContainer.textContent = ''
        } else {
          // Mostrar mensaje de error si el archivo no es válido
          previewContainer.innerHTML = ''
          errorMessageContainer.textContent = 'Por favor, selecciona una imagen en formato JPEG.'
        }
      })
    },
    checkIfActive (topic) {
      if (topic.isActive === false) {
        topic.isActive = true
      } else if (topic.isActive === true) {
        topic.isActive = false
      }
    },
    async viewProfilePost (topic) {
      try {
        // Verificar que el topic y el id existan
        if (!topic || !topic.account_id) {
          console.error('El topic o account_id es inválido')
          return 0
        }
        if (topic.is_editor) {
          if (topic.account_id !== this.current_user.id) {
            await this.$router.push({path: '/search_publisher_profile', query: {userID: topic.account_id}}) // Redirigir al perfil de user
          } else {
            await this.$router.push({path: '/publisher_profile'}) // Redirigir al perfil del current_user
          }
        } else {
          if (topic.account_id !== this.current_user.id) {
            await this.$router.push({path: '/search_user_profile', query: {userID: topic.account_id}}) // Redirigir al perfil de user
          } else {
            await this.$router.push({path: '/user_profile'}) // Redirigir al perfil del current_user
          }
        }
      } catch (error) {
        console.error('Error fetching responses:', error)
      }
    },
    async viewResponsesPost (topic) {
      try {
        if (topic.responses.length === 0) {
          const responses = await ForumServices.getResponsesForPost(topic.id)
          topic.responses = await Promise.all(
            responses.data.map(async (response) => {
              // Obtener datos del usuario y la cuenta
              // eslint-disable-next-line camelcase
              const resultMyReaction = await this.getMyReaction(response.id)
              const account = await AccountServices.getAccountById(response.account_id) // `account_id` debe estar en el post
              const user = await UserServices.getUserById(account.id) // Asumiendo que `account` tiene `user_id`
              const reResponses = await ForumServices.getResponsesForPost(response.id)
              // Agregar nuevos atributos al post
              return {
                // Copiar los atributos originales del post
                id: response.id,
                text: response.text,
                image: response.img,
                likes: response.likes,
                dislikes: response.dislikes,
                date: response.date,
                responses: [],
                num_responses: reResponses.count,
                profileImg: account.photo || 'default_account_icon.png', // Imagen de perfil
                name: user.name || 'Unknown User', // Nombre de usuario
                isEditor: user.is_editor || false, // Si el usuario es editor
                account_id: response.account_id,
                my_reaction: resultMyReaction,
                isActive: false
              }
            })
          )
          topic.responses.sort((a, b) => new Date(b.date) - new Date(a.date))
          this.topics_selected.push(topic.id)
        } else {
          topic.responses = []
          this.topics_selected = this.topics_selected.filter(id => id !== topic.id)
        }
        this.checkIfActive(topic)
      } catch (error) {
        console.error('Error fetching responses:', error)
      }
    },
    async deleteMyPost (topic) {
      await ForumServices.deletePost(topic.id)
      await this.getdata()
    },
    async getdata () {
      this.current_user = await UserServices.getActualUser()
      await this.getPostMyFollowing()
      await this.getMyPosts()
    },
    async toggleReaction (topic, type) {
      try {
        let newReaction
        if (type === true) {
          newReaction = { type: true } // Like
        } else if (type === false) {
          newReaction = { type: false } // Dislike
        }
        if (topic.my_reaction === type) {
          // Eliminar la reacción si ya está activa
          await ForumServices.deleteReaction(topic.id)
          topic.my_reaction = null
          if (type === true) {
            topic.likes -= 1
          } else {
            topic.dislikes -= 1
          }
        } else if (topic.my_reaction === null) {
          // Crear nueva reacción (like o dislike)
          await ForumServices.createReaction(topic.id, newReaction)
          topic.my_reaction = type
          if (type === true) {
            topic.likes += 1
          } else {
            topic.dislikes += 1
          }
        } else {
          // Actualizar la reacción si estaba en el estado contrario
          await ForumServices.updateReaction(topic.id, newReaction)
          topic.my_reaction = type
          if (type === true) {
            topic.likes += 1
            topic.dislikes -= 1
          } else {
            topic.likes -= 1
            topic.dislikes += 1
          }
        }
      } catch (error) {
        console.error('Error al manejar la reacción:', error)
      }
    },
    async likePost (topic) {
      await this.toggleReaction(topic, true)
    },
    async dislikePost (topic) {
      await this.toggleReaction(topic, false)
    },
    convertImageToBase64 (image) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onloadend = () => resolve(reader.result)
        reader.onerror = (error) => reject(error)
        reader.readAsDataURL(image)
      })
    }
  },
  mounted () {
    this.getdata()
  }
}
</script>

<style scoped>
.forum-background {
  background: url('../assets/fondo_forum.png') no-repeat center fixed;
  background-size: cover; /* La imagen cubre toda el área */
  width: 100%;
  height: 100%;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}

.forum-container {
  max-width: 1500px;
  width: 80%;
  height: 83vh; /* Keeps the container height fixed */
  padding: 2.5rem;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* Prevent content from overflowing */
  margin-top: 50px;
}

.topic-list-container {
  flex-grow: 1;
  max-height: 65vh; /* Ajusta la altura máxima en función del tamaño de la pantalla */
  overflow-y: scroll; /* Habilita el desplazamiento vertical si el contenido excede la altura */
  padding-right: 0.5rem; /* Evita que el scrollbar se solape con el contenido */
  margin-top: 0.5rem; /* Añade un margen superior para separar de otros elementos */
}

/* Optional: Customize scrollbar for modern browsers */
.topic-list-container::-webkit-scrollbar {
  width: 8px; /* Adjust scrollbar width */
}

.topic-list-container::-webkit-scrollbar-track {
  background: #f1f1f1; /* Scrollbar track color */
  border-radius: 10px; /* Rounded corners */
}

.topic-list-container::-webkit-scrollbar-thumb {
  background: #888; /* Scrollbar color */
  border-radius: 10px;
}

.topic-list-container::-webkit-scrollbar-thumb:hover {
  background: #555; /* Hover color for scrollbar */
}

.back-button-forum {
  position: absolute;
  top: 1rem;
  left: 1rem;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  font-weight: bold;
  background-color: #2563eb;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.back-button-forum:hover {
  background-color: #1d4ed8;
}

.forum-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 1rem;
  text-align: center;
  color: #333;
}

.forum-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.forum-subtitle {
  font-size: 1.5rem;
  font-weight: 600;
  color: #555;
}

.new-topic-button {
  padding: 0.5rem 1rem;
  margin-right: 10px;
  font-size: 0.9rem;
  font-weight: bold;
  background-color: #2563eb;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.new-topic-button:hover {
  background-color: #1d4ed8;
}

.topic-list {
  list-style: none;
  padding: 10px;
  margin: 0;
}

</style>
