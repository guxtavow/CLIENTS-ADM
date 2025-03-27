import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue'
import UserDetail from '@/views/UserDetail.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/user/:username', component: UserDetail, props: true }
]

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
