import http from '../http-common'

class BookService {
  getBooksByEditorial () {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/books/my_books`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        console.log(res.data)
        const count = res.data.count
        return count
      })
      .catch(error => {
        console.error('Error al obtener los libros', error)
      })
  }
  getAllBooks () {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/books/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        console.log(res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error al obtener los libros', error)
      })
  }
}

export default new BookService()
