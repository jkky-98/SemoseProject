import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../components/MainPage.vue'
import Intro from '../components/Intro.vue'
import MapComponent from '../components/MapComponent.vue'

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
  {
    path: '/test',
    name: 'MapComponent',
    component: MapComponent
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
