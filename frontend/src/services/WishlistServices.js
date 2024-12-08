import http from '../http-common'

class WishlistService {
  getMyWishlists () {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/wishlists/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        console.log(res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error al obtener las wishlists', error)
      })
  }
  getWishlistsBooks (id) {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/wishlists/${id}/books`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        console.log(res.data)
        console.log('AQUI VA LA VUELTA')
        return res.data
      })
      .catch(error => {
        console.error('Error al obtener los libros de la  wishlists', error)
      })
  }

  addBookWishlist (whishlistid, bookid) {
    const token = localStorage.getItem('token')
    return http.patch(`/api/v1/wishlists/${whishlistid}/${bookid}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        console.log(res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error al añadir libro a la wishlist', error)
      })
  }
  deleteBookWishlist (whishlistid, bookid) {
    const token = localStorage.getItem('token')
    return http.delete(`/api/v1/wishlists/${whishlistid}/${bookid}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        console.log(res.data)
        return res.data
      })
      .catch(error => {
        console.error('Error al borrar libro a la wishlist', error)
      })
  }
  readBooksOfWishlist (id) {
    return http.get(`/api/v1/wishlists/${id}/books`)
  }
  //  create-wishlist-on-login
  async createWishlistOnLogin () {
    const response = await this.getMyWishlists()
    console.log(response.count)
    if (response.count < 1) {
      const token = localStorage.getItem('token')
      const data = {name: 'Wishlist'}
      return http.post(`/api/v1/wishlists/`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
    }
  }
  async getUserWishlist (userId) {
    const response = await http.get(`/wishlists/user/${userId}`)
    return response.data
  }

  async getWishlistByUserId (userId) {
    const response = await http.get(`/api/v1/wishlists/by_account/${userId}`)
    return response.data
  }
}
export default new WishlistService()
