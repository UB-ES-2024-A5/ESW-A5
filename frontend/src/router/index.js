import Vue from 'vue'
import Router from 'vue-router'
import Login from '../components/login.vue'
import Signup from '../components/signup.vue'
import GuessAccess from '../components/welcomePage.vue'
import SignupEdit from '../components/signupEdit.vue'
import MainPageGuest from '../components/mainPageGuest.vue'
import MainPageUser from '../components/mainPageUser.vue'
import MainPagePublisher from '../components/mainPagePublisher.vue'
import UserProfile from '../components/userProfile.vue'
import PublisherProfile from '../components/publisherProfile.vue'
import Book from '../components/book.vue'
import CreatePublication from '../components/createPublication.vue'
import searchUserProfile from '../components/searchUserProfile.vue'
import searchPublisherProfile from '../components/searchPublisherProfile.vue'

import axios from 'axios'
import userServices from '../services/UserServices.js'

Vue.use(Router)
const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'guestaccess',
      component: GuessAccess,
      meta: { requiresAuth: false } // Ruta pública
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { requiresAuth: false } // Ruta pública
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup,
      meta: { requiresAuth: false } // Ruta pública
    },
    {
      path: '/signupEdit',
      name: 'signupEdit',
      component: SignupEdit,
      meta: { requiresAuth: false } // Ruta pública
    },
    {
      path: '/mainPage_guest',
      name: 'mainPage_guest',
      component: MainPageGuest,
      meta: { requiresAuth: false } // Ruta pública
    },
    {
      path: '/mainPage_user',
      name: 'mainPage_user',
      component: MainPageUser,
      meta: { requiresAuth: true } // Requiere autenticación
    },
    {
      path: '/mainPage_publisher',
      name: 'mainPage_publisher',
      component: MainPagePublisher,
      meta: { requiresAuth: true } // Requiere autenticación
    },
    {
      path: '/user_profile',
      name: 'user_profile',
      component: UserProfile,
      meta: { requiresAuth: true } // Requiere autenticación
    },
    {
      path: '/publisher_profile',
      name: 'publisher_profile',
      component: PublisherProfile,
      meta: { requiresAuth: true } // Requiere autenticación
    },
    {
      path: '/book',
      name: 'book',
      component: Book,
      meta: { requiresAuth: true } // Requiere autenticación
    },
    {
      path: '/create_publication',
      name: 'create_publication',
      component: CreatePublication,
      meta: { requiresAuth: true } // Requiere autenticación
    },
    {
      path: '/search_user_profile',
      name: 'search_user_profile',
      component: searchUserProfile
    },
    {
      path: '/search_publisher_profile',
      name: 'search_publisher_profile',
      component: searchPublisherProfile
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  // Obtenemos el token del localStorage
  const token = localStorage.getItem('token')
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  // Si la ruta requiere autenticación y no hay token, redirigimos al login
  if (requiresAuth && !token) {
    console.log('Redirigiendo a /login...')
    return next('/login')
  }

  // Si hay un token, configuramos axios para usarlo
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`

    try {
      // Obtenemos la información del usuario
      const userInfo = await userServices.getActualUser()

      // Restricción de acceso según el rol del usuario
      if (userInfo) {
        // Rutas prohibidas para usuarios no editores
        const editorOnlyRoutes = ['/create_publication', '/mainPage_publisher', '/publisher_profile']
        if (!userInfo.is_editor && editorOnlyRoutes.includes(to.path)) {
          console.log('Acceso denegado: Usuario no es editor.')
          return next('/mainPage_user') // Redirigir al área del usuario normal
        }

        // Rutas prohibidas para editores
        const userOnlyRoutes = ['/user_profile', '/mainPage_user']
        if (userInfo.is_editor && userOnlyRoutes.includes(to.path)) {
          console.log('Acceso denegado: Usuario es editor.')
          return next('/mainPage_publisher') // Redirigir al área del editor
        }
      }

      // Si el usuario ya está autenticado y trata de acceder a login, signup, o mainPage_guest, redirigimos a su página principal
      if (
        (to.path === '/login' || to.path === '/signup' || to.path === '/signupEdit' || to.path === '/mainpage_guest' || to.path === '/') &&
        userInfo
      ) {
        if (userInfo.is_editor) {
          console.log('Usuario autenticado como editor, redirigiendo a /mainPage_publisher...')
          return next('/mainPage_publisher')
        } else {
          console.log('Usuario autenticado como usuario normal, redirigiendo a /mainPage_user...')
          return next('/mainPage_user')
        }
      }
    } catch (error) {
      // Si hay un error al obtener la información del usuario, limpiamos el token
      console.error('Error al obtener información del usuario:', error)
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']

      // Redirigimos al login si hay error
      if (requiresAuth) {
        return next('/login')
      }
    }
  }

  // Continuar con la navegación si no hay problemas
  next()
})

export default router
