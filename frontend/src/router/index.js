import Vue from 'vue'
import Router from 'vue-router'
import Login from '../components/login.vue'
import signup from '../components/signup.vue'
import guessaccess from '../components/guestaccess.vue'
import signupEdit from '../components/signupEdit.vue'

Vue.use(Router)
export default new Router({
  routes: [
    {
      path: '/',
      name: 'guestaccess',
      component: guessaccess
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/signup',
      name: 'signup',
      component: signup
    },
    {
      path: '/signupEdit',
      name: 'signupEdit',
      component: signupEdit
    }
  ]
})
