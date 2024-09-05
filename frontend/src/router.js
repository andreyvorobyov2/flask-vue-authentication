import { createRouter, createWebHistory } from 'vue-router';
import store from './store.js';
import HomePage from './components/HomePage.vue';
import AboutPage from './components/AboutPage.vue';
import LoginPage from './components/LoginPage.vue';
import SignupPage from './components/SignupPage.vue';
import MyProjectsPage from './components/MyProjectsPage.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
        path: '/about',
        name: 'about',
        component: AboutPage
    },
    {
        path: '/login',
        name: 'login',
        component: LoginPage
    },
    {
        path: '/signup',
        name: 'signup',
        component: SignupPage
    },
    {
        path: '/myprojects',
        name: 'myprojects',
        component: MyProjectsPage,
        meta: {requiresAuth: true}
    },
  ]
})

router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth) {
      const username = store.state.username;
      if (username) {
        next();
      } else {
        next('/login');
      }
    } else {
      next();
    }
  });

export default router