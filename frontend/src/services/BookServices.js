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

  getBooksByEditorialId (accountId) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/books/${accountId}`, {
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
      }) // Ensure this line ends with a semicolon
  }

  createBook (data) {
    const token = localStorage.getItem('token')
    if (!token) {
      console.error('No token found in localStorage')
      throw new Error('User not authenticated')
    }

    // Log para verificar la estructura de datos
    console.log('Data being sent to the backend:', JSON.stringify(data, null, 2))

    return http.post(
      '/api/v1/books/',
      data,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    )
      .then(res => {
        console.log('Book created successfully:', res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error al crear el libro:', error.response ? error.response.data : error.message)
        throw error
      })
  }

  getBooksByGenre (genre) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/books/by_genre/${genre}`, {
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

  getBooksByPriceMax (price) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/books/by_price_max/${price}`, {
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

  getBooksByPriceMin (price) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/books/by_price_min/${price}`, {
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

  getBooksByDateMax (date) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/books/by_date_max/${date}`, {
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

  getBooksByDateMin (date) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/books/by_date_min/${date}`, {
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
