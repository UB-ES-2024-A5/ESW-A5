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
          <button @click="addNewTopic" class="new-topic-button">New Post</button>
        </div>

        <div class="topic-list-container">
          <ul class="topic-list">
            <li v-for="topic in topics" :key="topic.id" class="topic-item">
              <h3 class="topic-title">{{ topic.title }}</h3>
              <p class="topic-message">{{ topic.message }}</p>
              <p class="topic-info">{{ topic.date }}</p>

              <!-- Like/Dislike Buttons -->
              <div class="reaction-buttons">
                <button @click="likePost(topic)" class="reaction-button thumbs-up">
                  👍 {{ topic.likes }}
                </button>
                <button @click="dislikePost(topic)" class="reaction-button thumbs-down">
                  👎 {{ topic.dislikes }}
                </button>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Swal from 'sweetalert2'
import userServices from '../services/UserServices.js'

export default {
  data () {
    return {
      topics: [
        { id: 1, title: 'Welcome to Vue Forum', message: 'This is the welcome post where we can discuss the basics of the forum.', date: new Date().toLocaleDateString('es-ES'), likes: 0, dislikes: 0 },
        { id: 1, title: 'Welcome to Vue Forum', message: 'This is the welcome post where we can discuss the basics of the forum.', date: new Date().toLocaleDateString('es-ES'), likes: 0, dislikes: 0 },
        { id: 1, title: 'Welcome to Vue Forum', message: 'This is the welcome post where we can discuss the basics of the forum.', date: new Date().toLocaleDateString('es-ES'), likes: 0, dislikes: 0 }
      ]
    }
  },
  methods: {
    async goBack () {
      try {
        const userInfo = await userServices.getActualUser()
        if (userInfo.is_editor) {
          this.$router.push({ path: '/mainPage_publisher' })
        } else {
          this.$router.push({ path: '/mainPage_user' })
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
          <input id="title" class="swal2-input" placeholder="Post Title">
          <textarea id="message" class="swal2-textarea" placeholder="Enter your message"></textarea>
        `,
        showCancelButton: true,
        preConfirm: () => {
          const title = document.getElementById('title').value
          const message = document.getElementById('message').value
          if (!title || !message) {
            Swal.showValidationMessage('Please enter both a title and a message')
          } else {
            return { title, message }
          }
        }
      }).then((result) => {
        if (result.isConfirmed) {
          const { title, message } = result.value
          const newTopic = {
            id: this.topics.length + 1,
            title,
            message,
            date: new Date().toLocaleDateString('es-ES')
          }
          this.topics.push(newTopic)
        }
      })
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
  height: 60vh; /* Keeps the container height fixed */
  padding: 4rem;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* Prevent content from overflowing */
}

.topic-list-container {
  flex-grow: 1;
  max-height: 400px; /* Set a fixed height for the container */
  overflow-y: scroll; /* Enable vertical scrolling */
  padding-right: 0.5rem; /* Prevent scrollbar overlap with content */
  margin-top: 1rem; /* Add some spacing above */
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
  margin-bottom: 1.5rem;
  text-align: center;
  color: #333;
}

.forum-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
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
  padding: 0;
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
  position: relative; /* Add this to position child elements absolutely */
}

.topic-item:hover {
  background-color: #f3f4f6;
}

.topic-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0 0 0.5rem;
  color: #222;
  text-align: left;
}

/* Position the date at the bottom-left of the post */
.topic-info {
  font-size: 0.9rem;
  color: #777;
  position: absolute;
  bottom: 0;
  left: 0;
  margin: 10px; /* Add some margin for spacing */
}

/* Add styling for the reaction buttons */
.reaction-buttons {
  display: flex;
  justify-content: flex-end;
  position: absolute;
  bottom: 0;
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
</style>
