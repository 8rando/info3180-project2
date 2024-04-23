import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import HomePage from '../views/HomeView.vue';
import RegistrationView from '@/views/RegistrationView.vue';
import ExploreView from '../views/ExploreView.vue';
import LoginView from '../views/LoginView.vue';
import NewPostView from '../views/NewPostView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',

      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: RegistrationView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },

    {
      path: '/explore',
      name: 'explore',
      component: ExploreView
    },
 
    {
      path: '/posts/new',
      name: 'newPost',
      component: NewPostView
    }
  ]
})

export default router