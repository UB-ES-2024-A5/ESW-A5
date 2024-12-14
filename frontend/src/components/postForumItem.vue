<template>
  <li :class="['topic-item', { 'active-topic': isActive }]">
    <!-- Name, ImagePerfl and date -->
    <div class="topic-header" @click="$emit('view-profile', topic)">
      <div class="profile-info">
        <img :src="topic.profileImg" alt="Profile" class="profile-img" />
        <span class="profile-name">{{ topic.name }}</span>
      </div>
      <span class="post-date">{{ timeAgo(topic.date) }}</span>
    </div>

    <!-- Optional Text -->
    <div class="topic-content" @click="$emit('view-responses', topic)">
      <div>
        <p v-if="topic.text" class="topic-text" style="margin-left: 10px">
          {{ topic.text }}
        </p>
      </div>

      <!-- Optional Image -->
      <div v-if="topic.image" class="image-container">
        <img
          :src="topic.image"
          alt="Post Image"
          class="post-image"
        />
      </div>
    </div>

    <!-- Respond Button -->
    <div class="topic-reaction">
      <button @click="$emit('respond', topic)" class="response-button">Respond</button>
      <p class="num-responses" style="margin-left: 10px"> {{ topic.num_responses + ' respnses'}} </p>
      <!-- Like/Dislike Buttons -->
      <div class="reaction-buttons">
        <button @click="$emit('like', topic)" class="reaction-button thumbs-up">
          👍 {{ formatLikes(topic.likes) }}
        </button>
        <button @click="$emit('dislike', topic)" class="reaction-button thumbs-down">
          👎 {{ formatLikes(topic.dislikes) }}
        </button>
      </div>
    </div>
    <!-- Responses -->
    <ul v-if="topic.responses && topic.responses.length" class="responses-list">
      <topic-item
        v-for="(response, index) in topic.responses"
        :key="index"
        :topic="response"
        @respond="$emit('respond', $event)"
        @like="$emit('like', $event)"
        @dislike="$emit('dislike', $event)"
        @view-profile="$emit('view-profile', $event)"
        @view-responses="$emit('view-responses', $event)"
      />
    </ul>
  </li>
</template>

<script>
export default {
  name: 'TopicItem',
  props: {
    topic: {
      type: Object,
      required: true
    },
    isActive: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    timeAgo (dateString) {
      const postDate = new Date(dateString)
      const now = new Date()
      const diffInSeconds = Math.floor((now - postDate) / 1000)
      if (diffInSeconds < 60) {
        return `${diffInSeconds} sec ago`
      } else if (diffInSeconds < 3600) {
        const minutes = Math.floor(diffInSeconds / 60)
        return `${minutes} min${minutes !== 1 ? 's' : ''} ago`
      } else if (diffInSeconds < 86400) {
        const hours = Math.floor(diffInSeconds / 3600)
        return `${hours} h${hours !== 1 ? 's' : ''} ago`
      } else if (diffInSeconds < 2592000) { // Less than a month (30 days)
        const days = Math.floor(diffInSeconds / 86400)
        return `${days} day${days !== 1 ? 's' : ''} ago`
      } else if (diffInSeconds < 31536000) { // Less than a year (365 days)
        const months = Math.floor(diffInSeconds / 2592000) // 30 days per month
        return `${months} month${months !== 1 ? 's' : ''} ago`
      } else {
        const years = Math.floor(diffInSeconds / 31536000) // 365 days per year
        return `${years} year${years !== 1 ? 's' : ''} ago`
      }
    },
    formatLikes (likes) {
      if (likes >= 100000000) {
        // Más de 100 millones, formato 100M
        return (likes / 1000000).toFixed(1) + 'M'
      } else if (likes >= 100000) {
        // Más de 100 mil, formato 100k (sin decimales)
        return Math.floor(likes / 1000) + 'k'
      } else if (likes >= 1000) {
        // Más de 999, formato 1k con decimales
        return (likes / 1000).toFixed(1) + 'k'
      } else {
        // Menos de 1000, número normal
        return likes.toString()
      }
    }
  }
}
</script>

<style scoped>
.forum-background {
  background: url('../assets/fondo_forum.png') no-repeat center fixed;
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
  max-height: 525px; /* Set a fixed height for the container */
  overflow-y: scroll; /* Enable vertical scrolling */
  padding-right: 0.5rem; /* Prevent scrollbar overlap with content */
  margin-top: 0.5rem; /* Add some spacing above */
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

.topic-list-container {
  flex-grow: 1;
  overflow-y: auto;
}

.topic-list {
  list-style: none;
  padding: 10px;
  margin: 0;
}

.topic-item {
  background-color: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease;
  cursor: pointer;
  margin-bottom: 1rem;
  margin-top: 15px;
  position: relative; /* Add this to position child elements absolutely */
}

.topic-item:hover {
  background-color: #e0e0e0; /* Tono gris claro para el hover */
}

.topic-item.active-topic {
  background-color: #c5c5c5; /* Cambia a tu preferencia */
}

.topic-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ccc; /* Línea fina */
  padding: 10px;
  background-color: #ffffff;
  cursor: pointer;
  transition: background-color 0.3s;
}

.topic-header:hover {
  background-color: #f0f0f0; /* Tono diferente al hover del header */
}

/* Hover para el contenido */
.topic-content {
  background-color: #ffffff;
  padding: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.topic-content:hover {
  background-color: #f0f0f0; /* Tono diferente al hover del header */
}

.profile-info {
  display: flex;
  align-items: center;
}

.profile-img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 20px;
}

.profile-name {
  font-size: 16px;
  font-weight: bold;
}

.post-date {
  font-size: 14px;
  color: #888;
  text-align: right;
  white-space: nowrap;
}

.num-responses {
  font-size: 14px;
  color: #888;
  text-align: right;
  white-space: nowrap;
  margin-top: 20px;
}

.topic-item {
  text-align: left;
  margin-bottom: 0px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 180px; /* Ajusta según el tamaño máximo que deseas para la imagen */
  width: 100%; /* Para que ocupe to do el ancho disponible */
  margin-bottom: 10px;
  overflow: hidden; /* Asegura que las imágenes no se salgan del contenedor */
}

.image-container img {
  width: auto; /* La anchura se ajustará automáticamente */
  height: 100%; /* La imagen ocupará to do el alto del contenedor */
  object-fit: contain; /* Mantiene la proporción de la imagen */
}

.post-image {
  width: 15%;
  height: auto;
  margin-top: 0;
  cursor: pointer;
}

.topic-reaction {
  background-color: #ffffff;
  margin-top: 0;
  display: flex;
}

.response-button {
  margin-top: 10px;
  margin-left: 10px;
  width: calc(100% - 225px);
  height: 40px;
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
  flex-wrap: wrap;
}

.response-button:hover {
  background-color: #0056b3;
}

/* Add styling for the reaction buttons */
.reaction-buttons {
  display: flex;
  justify-content: center;
  right: 0;
  margin: 10px; /* Add some margin for spacing */
}

.reaction-button {
  padding: 0.5rem;
  font-size: 1rem;
  background-color: transparent;
  border: 1px solid #ccc;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 0px;
  gap: 5px;
}

.reaction-button:hover {
  background-color: #f0f0f0;
}

.thumbs-up {
  color: green;
}

.thumbs-down {
  color: red;
}

/* Estilo para las respuestas */
.responses-list {
  list-style-type: none;
  margin-top:5px;
  padding-left: 0;
}

.response-item {
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 10px;
  transition: background-color 0.3s;
}

.response-item:hover {
  background-color: #f9f9f9; /* Cambia de color al pasar el ratón */
}

</style>
