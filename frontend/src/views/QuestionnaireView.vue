<script setup lang="ts">
import { ref } from 'vue';
import { useQuestionnaireStore } from '@/stores/questionnaireStore';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';

const questionnaireStore = useQuestionnaireStore();
const authStore = useAuthStore();
const router = useRouter();

const currentQuestionIndex = ref(0);
const showError = ref(false);

const handleNext = () => {
  if (currentQuestionIndex.value < questionnaireStore.questions.length - 1) {
    currentQuestionIndex.value++;
  } else {
    submitQuestionnaire();
  }
};

const handlePrev = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--;
  }
};

const submitQuestionnaire = async () => {
  // Check if all questions are answered
  if (!questionnaireStore.isComplete()) {
    showError.value = true;
    return;
  }
  
  await questionnaireStore.submitQuestionnaire();
  if (!questionnaireStore.error) {
    router.push('/');
  }
};
</script>

<template>
  <div class="questionnaire-view">
    <h1>Personality Assessment</h1>
    <p class="instructions">Please answer these questions to help us provide personalized support.</p>
    
    <div class="question-container">
      <div class="progress">
        Question {{ currentQuestionIndex + 1 }} of {{ questionnaireStore.questions.length }}
      </div>
      
      <div class="question">
        <h2>{{ questionnaireStore.questions[currentQuestionIndex].text }}</h2>
        
        <div class="likert-scale">
          <div 
            v-for="value in 5" 
            :key="value" 
            class="likert-option" 
            :class="{ selected: questionnaireStore.questions[currentQuestionIndex].answer === value }"
            @click="questionnaireStore.questions[currentQuestionIndex].answer = value"
          >
            <div class="likert-circle"></div>
            <span class="likert-label">
              {{ value === 1 ? 'Strongly disagree' : 
                 value === 2 ? 'Disagree' : 
                 value === 3 ? 'Neutral' : 
                 value === 4 ? 'Agree' : 
                 'Strongly agree' }}
            </span>
          </div>
        </div>
      </div>
      
      <div class="navigation">
        <button 
          @click="handlePrev" 
          :disabled="currentQuestionIndex === 0"
          class="prev-button"
        >
          Previous
        </button>
        <button 
          v-if="currentQuestionIndex < questionnaireStore.questions.length - 1" 
          @click="handleNext"
          :disabled="questionnaireStore.questions[currentQuestionIndex].answer === null"
          class="next-button"
        >
          Next
        </button>
        <button 
          v-else 
          @click="submitQuestionnaire"
          :disabled="questionnaireStore.isLoading"
          class="submit-button"
        >
          {{ questionnaireStore.isLoading ? 'Submitting...' : 'Submit' }}
        </button>
      </div>
      
      <div v-if="showError" class="error">
        Please answer all questions before submitting.
      </div>
      
      <div v-if="questionnaireStore.error" class="error">
        {{ questionnaireStore.error }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.questionnaire-view {
  max-width: 700px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #a2e59f;
  border-radius: 8px;
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  font-family: 'Nohemi', sans-serif;
  color: #3c8a38;
  text-align: center;
  margin-bottom: 1rem;
}

.instructions {
  text-align: center;
  margin-bottom: 2rem;
  color: #555;
}

.progress {
  text-align: right;
  margin-bottom: 1.5rem;
  color: #666;
  font-size: 0.9rem;
}

.question {
  margin-bottom: 2rem;
}

h2 {
  font-family: 'Switzer', sans-serif;
  font-weight: 400;
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
  color: #212121;
}

.likert-scale {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.likert-option {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.likert-option:hover {
  background-color: #f0f8f0;
}

.likert-option.selected {
  background-color: #e8f5e9;
}

.likert-circle {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid #a2e59f;
  margin-right: 12px;
  position: relative;
}

.likert-option.selected .likert-circle::after {
  content: "";
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #3c8a38;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.navigation {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
}

button {
  padding: 0.7rem 1.2rem;
  border: none;
  border-radius: 8px;
  font-family: 'Nohemi', sans-serif;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.prev-button {
  background-color: #f1f8e9;
  color: #3c8a38;
  border: 1px solid #a2e59f;
}

.prev-button:hover:not(:disabled) {
  background-color: #e8f5e9;
}

.next-button {
  background-color: #3c8a38;
  color: white;
}

.next-button:hover {
  background-color: #2e6b2c;
}

.submit-button {
  background-color: #3c8a38;
  color: white;
}

.submit-button:hover:not(:disabled) {
  background-color: #2e6b2c;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  color: #d32f2f;
  background-color: #ffebee;
  border: 1px solid #ef9a9a;
  padding: 0.75rem;
  border-radius: 8px;
  margin-top: 1.5rem;
  text-align: center;
}
</style>