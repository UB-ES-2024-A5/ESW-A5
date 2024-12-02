import http from '../http-common'

class AccountService {
  create (data) {
    const accountData = { id: data }
    return http.post('/api/v1/accounts/', accountData)
      .then((res) => {
        return res.data
      })
  }

  getActualAccount () {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/accounts/me`, {
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

  getAccountById (accountId) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/accounts/${accountId}`, {
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

  updateAccount (data) {
    const token = localStorage.getItem('token')
    return http.patch(`/api/v1/accounts/me`, data, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then((res) => res.data)
      .catch((error) => {
        console.error('Error al actualizar los datos del usuario:', error)
        throw error
      })
  }

  followAccount (accountId) {
    const token = localStorage.getItem('token')
    return http.post(`/api/v1/followers/${accountId}`, {}, { // Nota el objeto vacío para el body
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then((res) => res.data)
      .catch((error) => {
        console.error('Error al seguir al usuario:', error.response?.data || error.message)
        throw error
      })
  }

  unfollowAccount (accountId) {
    const token = localStorage.getItem('token')
    return http.delete(`/api/v1/followers/${accountId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then((res) => res.data)
      .catch((error) => {
        console.error('Error al dejar de seguir al usuario:', error.response?.data || error.message)
        throw error
      })
  }

  getFollowingAccounts () {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/followers/me_following`, {
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
}
export default new AccountService()
