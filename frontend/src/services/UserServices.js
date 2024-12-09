import http from '../http-common'

class UserService {
  getAll () {
    return http.get('/api/v1/users/')
      .then((res) => {
        return res.data
      })
  }

  get (id) {
    return http.get(`/api/v1/users/${id}`)
      .then((res) => {
        return res.data
      })
  }

  getActualUser () {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/users/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then((res) => res.data)
      .catch((error) => {
        console.error('Error al obtener los datos del usuario:', error)
        throw error
      })
  }

  getUserById (userId) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/users/by_id/${userId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then((res) => res.data)
      .catch((error) => {
        console.error('Error al obtener los datos del usuario:', error)
        throw error
      })
  }
  async getUserById2 (userId) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/users/by_id/${userId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then((res) => res.data)
      .catch((error) => {
        console.error('Error al obtener los datos del usuario:', error)
        throw error
      })
  }

  getUserEmail (email) {
    return http.get(`/api/v1/users/${email}`)
      .then((res) => {
        return res.data
      })
  }

  create (data) {
    return http.post('/api/v1/users/', data)
      .then((res) => {
        return res.data
      })
  }

  update (id, data) {
    return http.put(`/api/v1/users/${id}`, data)
      .then((res) => {
        return res.data
      })
  }

  delete (id) {
    return http.delete(`/api/v1/users/${id}`)
      .then((res) => {
        return res.data
      })
  }
}

export default new UserService()
