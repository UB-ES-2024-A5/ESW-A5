import http from '../http-common'

class WishlistService {
  getMyWishlists () {
    const token = localStorage.getItem('token')
    return http.get(`/api/v1/wishlists/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
  }
  readBooksOfWishlist (id) {
    return http.get(`/api/v1/wishlists/${id}/books`)
  }
}
export default new WishlistService()
