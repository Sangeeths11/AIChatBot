import { createRouter, createWebHistory } from 'vue-router';
import UserRegister from './components/UserRegister.vue'
// import UserLogin from '../components/UserLogin.vue'
import UserLogin from './components/UserLogin.vue'

const routes = [
  {
    path: '/UserRegister',
    name: 'UserRegister',
    component: UserRegister
  },
  {
    path: '/UserLogin',
    name: 'UserLogin',
    component: UserLogin
  }
  // ... you can add more routes here
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
