import http from '../http-common'

class AccountService {
  create (data) {
    const accountData = { id: data }
    return http.post('/api/v1/accounts/', accountData)
      .then((res) => {
        return res.data
      })
  }
}
export default new AccountService()
