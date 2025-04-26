import { createRouter, createWebHistory } from 'vue-router';
import ChatView from '../views/ChatView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import QuestionnaireView from '../views/QuestionnaireView.vue';
import JournalView from '../views/JournalView.vue'; // Import the new view
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
    },
    { // Add the new route for the journal
      path: '/journal',
      name: 'journal',
      component: JournalView,
      meta: { requiresAuth: true } // Assuming journal requires login
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
    // If logged in user tries to access login/register, redirect based on questionnaire status
    const questionnaireStore = useQuestionnaireStore();
    // Ensure status is checked if userId exists
    if (authStore.userId) {
        await questionnaireStore.checkCompletionStatus(authStore.userId);
    }

    if (questionnaireStore.isCompleted) {
        next({ name: 'chat' }); // Go to chat if questionnaire is done
    } else {
        next({ name: 'questionnaire' }); // Go to questionnaire if not done
    }
    return;
  }


  // Handle questionnaire redirects ONLY if requiresQuestionnaire is set
  if (requiresQuestionnaire && authStore.isLoggedIn) {
    // Check if user has completed the questionnaire
    const questionnaireStore = useQuestionnaireStore();
    // Ensure status is checked if userId exists
    if (authStore.userId) {
        await questionnaireStore.checkCompletionStatus(authStore.userId);
    }

    if (!questionnaireStore.isCompleted) {
      next({ name: 'questionnaire' });
      return;
    }
  }

  // If trying to access questionnaire directly after completing it, redirect to chat
  if (to.name === 'questionnaire' && authStore.isLoggedIn) {
      const questionnaireStore = useQuestionnaireStore();
      if (authStore.userId) {
          await questionnaireStore.checkCompletionStatus(authStore.userId);
      }
      if (questionnaireStore.isCompleted) {
          next({ name: 'chat' });
          return;
      }
  }


  next(); // Proceed to the route if no redirects happened
});

export default router;