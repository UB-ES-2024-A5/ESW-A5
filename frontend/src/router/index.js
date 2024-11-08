import Vue from 'vue'
import Router from 'vue-router'
import Login from '../components/login.vue'
import signup from '../components/signup.vue'
import guessaccess from '../components/welcomePage.vue'
import signupEdit from '../components/signupEdit.vue'
import mainpageGuest from '../components/mainPageGuest.vue'
import mainpageUser from '../components/mainPageUser.vue'
import mainpagePublisher from '../components/mainPagePublisher.vue'

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
    },
    {
      path: '/mainPage_guest',
      name: 'mainPage_guest',
      component: mainpageGuest
    },
    {
      path: '/mainPage_user',
      name: 'mainPage_user',
      component: mainpageUser
    },
    {
      path: '/mainPage_publisher',
      name: 'mainPage_publisher',
      component: mainpagePublisher
    }
  ]
})
