// filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\src\router\index.ts
import { createRouter, createWebHistory } from 'vue-router'
// We will create this ChatView component in the next step
import ChatView from '../views/ChatView.vue' // <-- Uncomment this line

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'chat',
      // Temporarily comment out the component until we create it
      component: ChatView // <-- Use the imported ChatView here
      // For now, let's add a placeholder component just to avoid errors
      // component: { template: '<div>Loading Chat...</div>' } // <-- Remove or comment out this line
    }
    // Removed the default '/' (HomeView) and '/about' routes
  ]
})

export default router