import axios from 'axios'

// Crear una instancia de Axios
const http = axios.create({
  baseURL: process.env.API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para agregar el token de autorización a cada solicitud
http.interceptors.request.use(
  (config) => {
    // Obtener el token desde localStorage
    const token = localStorage.getItem('token')

    // Si el token existe, agrégalo al encabezado de Authorization
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    // Manejo de errores de solicitud
    return Promise.reject(error)
  }
)

export default http
