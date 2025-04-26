import { createRouter, createWebHistory } from 'vue-router';
import ChatView from '../views/ChatView.vue';
import LoginView from '../views/LoginView.vue'; // Import LoginView
import RegisterView from '../views/RegisterView.vue'; // Import RegisterView
import { useAuthStore } from '@/stores/authStore'; // Import auth store

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'chat',
      component: ChatView,
      meta: { requiresAuth: true } // Add meta field to indicate this route needs login
    },
    {
      path: '/login', // Add login route
      name: 'login',
      component: LoginView,
      meta: { requiresGuest: true } // Add meta field for routes only accessible to guests (not logged in)
    },
    {
      path: '/register', // Add register route
      name: 'register',
      component: RegisterView,
      meta: { requiresGuest: true } // Also only accessible to guests
    }
    // Removed the default '/' (HomeView) and '/about' routes if they were there
  ]
});

// Navigation Guard: This function runs before each navigation attempt
router.beforeEach((to, from, next) => {
  // It's okay to get the store instance here, Pinia handles it
  const authStore = useAuthStore();

  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiresGuest = to.matched.some(record => record.meta.requiresGuest);

  if (requiresAuth && !authStore.isLoggedIn) {
    // If the route requires login (like '/chat') AND the user is NOT logged in...
    // Redirect them to the login page
    next({ name: 'login' });
  } else if (requiresGuest && authStore.isLoggedIn) {
    // If the route requires the user to be a guest (like '/login' or '/register') AND the user IS logged in...
    // Redirect them to the main chat page
    next({ name: 'chat' });
  } else {
    // Otherwise (route doesn't require auth/guest, or user status matches requirement)...
    // Allow navigation to proceed
    next();
  }
});

export default router;