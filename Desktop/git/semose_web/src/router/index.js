import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../components/MainPage.vue'
import Intro from '../components/Intro.vue'

const routes = [
  {
    path: '/',
    name: 'IntroComponent',
    component: Intro
  },
  {
    path: '/main',
    name: 'MainPageComponent',
    component: MainPage
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
