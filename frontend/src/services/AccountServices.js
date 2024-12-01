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
}
export default new AccountService()
