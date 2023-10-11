import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

import App from './App.vue'
import UserLogin from './components/UserLogin.vue'
import UserRegister from './components/UserRegister.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/login', component: UserLogin, name: 'login' },
        { path: '/', component: UserLogin, name: 'home' },
        { path: '/register', component: UserRegister, name: 'register' },
    ]
});

const app = createApp(App)

app.use(router);
app.mount('#app')