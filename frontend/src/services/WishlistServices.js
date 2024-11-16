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
create-wishlist-on-login
  async createWishlistOnLogin () {
    const response = await this.getMyWishlists()
    console.log(response.data.count)
    if (response.data.count < 1) {
      const token = localStorage.getItem('token')
      const data = {name: 'Wishlist'}
      return http.post(`/api/v1/wishlists/`, data, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
    }
  }
dev
}
export default new WishlistService()
