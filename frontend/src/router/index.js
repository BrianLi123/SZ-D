import { createRouter, createWebHistory } from 'vue-router'
import ChatWindow from '@/components/ChatWindow.vue'

const routes = [
  {
    path: '/',
    name: 'Chat',
    component: ChatWindow
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('@/views/History.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router