import http from '../http-common'

class LoginService {
  login (data) {
    return http.post('/api/v1/login/access-token', data, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
      .then((res) => {
        return res
      })
  }
}
export default new LoginService()
