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

Vue.use(Router)
export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'guestaccess',
      component: GuessAccess
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup
    },
    {
      path: '/signupEdit',
      name: 'signupEdit',
      component: SignupEdit
    },
    {
      path: '/mainPage_guest',
      name: 'mainPage_guest',
      component: MainPageGuest
    },
    {
      path: '/mainPage_user',
      name: 'mainPage_user',
      component: MainPageUser
    },
    {
      path: '/mainPage_publisher',
      name: 'mainPage_publisher',
      component: MainPagePublisher
    },
    {
      path: '/user_profile',
      name: 'user_profile',
      component: UserProfile
    },
    {
      path: '/publisher_profile',
      name: 'publisher_profile',
      component: PublisherProfile
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
    },
    {
      path: '/book',
      name: 'book',
      component: Book
    },
    {
      path: '/create_publication',
      name: 'create_publication',
      component: CreatePublication
    }
  ]
})
