import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/Home.vue'
import MovieDetails from '../views/MovieDetails.vue'

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage
  },
  {
    path: '/movie/:id',
    name: 'MovieDetails',
    component: MovieDetails
  }
]

const router = createRouter({
  history: createWebHistory(), //process.env.BASE_URL
  routes
})

export default router