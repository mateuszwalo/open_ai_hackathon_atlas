import { createRouter, createWebHistory } from 'vue-router';
import ChatView from '../views/ChatView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import QuestionnaireView from '../views/QuestionnaireView.vue';
import { useAuthStore } from '@/stores/authStore';
import { useQuestionnaireStore } from '@/stores/questionnaireStore';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'chat',
      component: ChatView,
      meta: { requiresAuth: true, requiresQuestionnaire: true }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { requiresGuest: true }
    },
    {
      path: '/questionnaire',
      name: 'questionnaire',
      component: QuestionnaireView,
      meta: { requiresAuth: true }
    }
  ]
});

// Navigation Guard
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiresGuest = to.matched.some(record => record.meta.requiresGuest);
  const requiresQuestionnaire = to.matched.some(record => record.meta.requiresQuestionnaire);

  // Handle authentication redirects
  if (requiresAuth && !authStore.isLoggedIn) {
    next({ name: 'login' });
    return;
  }
  
  if (requiresGuest && authStore.isLoggedIn) {
    next({ name: 'chat' });
    return;
  }

  // Handle questionnaire redirects
  if (requiresQuestionnaire && authStore.isLoggedIn) {
    // Check if user has completed the questionnaire
    const questionnaireStore = useQuestionnaireStore();
    await questionnaireStore.checkCompletionStatus(authStore.userId);
    
    if (!questionnaireStore.isCompleted) {
      next({ name: 'questionnaire' });
      return;
    }
  }

  next();
});

export default router;