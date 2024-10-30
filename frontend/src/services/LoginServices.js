import http from '../http-common'

class LoginService {
  login (data) {
    return http.post('/api/v1/login/access-token', data)
      .then((res) => {
        return res.data
      })
  }
}

export default new LoginService()
