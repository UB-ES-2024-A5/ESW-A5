import http from '../http-common'

class ForumServices {
  getAllMyPosts (skip = 0, limit = 100) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/forums/all_posts_me/?skip=${skip}&limit=${limit}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        console.log(res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error fetching my posts', error)
        throw error
      })
  }

  getAllPostsByAccountId (accountId, skip = 0, limit = 100) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/forums/all_posts/${accountId}?skip=${skip}&limit=${limit}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        console.log(res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error fetching posts by account ID', error)
        throw error
      })
  }

  getPostById (postId) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/forums/post_by_id/${postId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        console.log(res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error fetching post by ID', error)
        throw error
      })
  }

  getAllPostsFromFollowings (skip = 0, limit = 100) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/forums/all_post_my_following/?skip=${skip}&limit=${limit}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        console.log(res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error fetching posts from followings', error)
        throw error
      })
  }

  getResponsesForPost (postId, skip = 0, limit = 100) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/forums/responses/${postId}?skip=${skip}&limit=${limit}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        console.log(res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error fetching responses for post', error)
        throw error
      })
  }

  createPost (data) {
    const token = localStorage.getItem('token')
    if (!token) {
      console.error('No token found in localStorage')
      throw new Error('User not authenticated')
    }

    console.log('Data being sent to create post:', JSON.stringify(data, null, 2))

    return http.post(
      '/api/v1/forums/',
      data,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    )
      .then(res => {
        console.log('Post created successfully:', res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error creating post:', error.response ? error.response.data : error.message)
        throw error
      })
  }

  createResponse (parentPostId, data) {
    const token = localStorage.getItem('token')
    if (!token) {
      console.error('No token found in localStorage')
      throw new Error('User not authenticated')
    }

    console.log('Data being sent to create response:', JSON.stringify(data, null, 2))

    return http.post(
      `/api/v1/forums/${parentPostId}`,
      data,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    )
      .then(res => {
        console.log('Response created successfully:', res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error creating response:', error.response ? error.response.data : error.message)
        throw error
      })
  }

  deletePost (postId) {
    const token = localStorage.getItem('token')
    return http.delete(`/api/v1/forums/delete_post/${postId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        console.log('Post deleted successfully:', res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error deleting post', error)
        throw error
      })
  }

  createReaction (postId, reactionData) {
    const token = localStorage.getItem('token')
    if (!token) {
      console.error('No token found in localStorage')
      throw new Error('User not authenticated')
    }

    console.log('Reaction data being sent:', JSON.stringify(reactionData, null, 2))

    return http.post(
      `/api/v1/forums/create_reaction/${postId}`,
      reactionData,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    )
      .then(res => {
        console.log('Reaction created successfully:', res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error creating reaction:', error.response ? error.response.data : error.message)
        throw error
      })
  }

  updateReaction (postId, reactionData) {
    const token = localStorage.getItem('token')
    if (!token) {
      console.error('No token found in localStorage')
      throw new Error('User not authenticated')
    }

    console.log('Reaction data being updated:', JSON.stringify(reactionData, null, 2))

    return http.patch(
      `/api/v1/forums/update_reaction/${postId}`,
      reactionData,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    )
      .then(res => {
        console.log('Reaction updated successfully:', res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error updating reaction:', error.response ? error.response.data : error.message)
        throw error
      })
  }

  deleteReaction (postId) {
    const token = localStorage.getItem('token')
    return http.delete(`/api/v1/forums/delete_reaction/${postId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        console.log('Reaction deleted successfully:', res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error deleting reaction', error)
        throw error
      })
  }

  getMyLikedPosts (skip = 0, limit = 100) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/forums/posts_me_like/?skip=${skip}&limit=${limit}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        console.log(res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error fetching liked posts', error)
        throw error
      })
  }

  getMyDislikedPosts (skip = 0, limit = 100) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/forums/posts_me_dislike/?skip=${skip}&limit=${limit}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        console.log(res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error fetching disliked posts', error)
        throw error
      })
  }

  getLikedPostsByAccount (accountId, skip = 0, limit = 100) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/forums/posts_like/${accountId}?skip=${skip}&limit=${limit}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        console.log(res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error fetching liked posts by account', error)
        throw error
      })
  }

  getDislikedPostsByAccount (accountId, skip = 0, limit = 100) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/forums/posts_dislike/${accountId}?skip=${skip}&limit=${limit}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        console.log(res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error fetching disliked posts by account', error)
        throw error
      })
  }
  getReactionByPostId (postId) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/forums/get_reaction_by_post_id/${postId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        console.log('Reaction data:', res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error fetching reaction:', error)
        throw error
      })
  }
}

export default new ForumServices()
