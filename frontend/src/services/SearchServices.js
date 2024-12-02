import http from '../http-common'

class SearchServices {
  search (query, limit) {
    return http.get('/api/v1/search/' + query + '?limit=' + limit)
      .then((res) => {
        return res
      })
  }
}
export default new SearchServices()
