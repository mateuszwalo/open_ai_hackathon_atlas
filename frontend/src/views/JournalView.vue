// filepath: c:\Users\maksk\Desktop\TheHack\open_ai_hackathon_atlas\frontend\src\views\JournalView.vue
<script setup lang="ts">
import { ref, computed } from 'vue';

// --- Dummy Data ---
// Structure: { 'YYYY-MM': { 'DD': 'good' | 'mid' | 'bad' } }
const dummyRatings = ref({
  '2025-04': { // Current month (April 2025)
    '01': 'good', '03': 'mid', '05': 'bad', '07': 'good', '10': 'mid',
    '12': 'good', '15': 'bad', '18': 'good', '20': 'mid', '22': 'good',
    '25': 'bad', '26': 'good',
  },
  '2025-03': { // Previous month (March 2025)
    '02': 'mid', '04': 'good', '06': 'bad', '08': 'mid', '11': 'good',
    '13': 'bad', '16': 'good', '19': 'mid', '21': 'bad', '23': 'good',
    '26': 'mid', '28': 'good', '30': 'bad',
  },
  '2025-02': { // Two months ago (February 2025)
    '01': 'bad', '03': 'good', '05': 'mid', '07': 'bad', '09': 'good',
    '11': 'mid', '14': 'good', '17': 'bad', '20': 'mid', '22': 'good',
    '25': 'bad', '27': 'good',
  },
});

// --- Calendar Logic ---
const currentDate = ref(new Date(2025, 3, 26)); // Start with April 2025

const currentMonth = computed(() => currentDate.value.getMonth());
const currentYear = computed(() => currentDate.value.getFullYear());

const monthName = computed(() => {
  return currentDate.value.toLocaleString('default', { month: 'long', year: 'numeric' });
});

const daysInMonth = computed(() => {
  return new Date(currentYear.value, currentMonth.value + 1, 0).getDate();
});

const firstDayOfMonth = computed(() => {
  // Get the day of the week (0=Sun, 1=Mon, ..., 6=Sat)
  const day = new Date(currentYear.value, currentMonth.value, 1).getDay();
  // Adjust so Monday is 0, Sunday is 6
  return (day === 0) ? 6 : day - 1;
});

const calendarDays = computed(() => {
  const days = [];
  // Add empty placeholders for days before the 1st
  for (let i = 0; i < firstDayOfMonth.value; i++) {
    days.push({ key: `prev-${i}`, day: null, rating: null });
  }
  // Add actual days of the month
  const monthKey = `${currentYear.value}-${String(currentMonth.value + 1).padStart(2, '0')}`;
  const monthRatings = dummyRatings.value[monthKey] || {};
  for (let day = 1; day <= daysInMonth.value; day++) {
    const dayKey = String(day).padStart(2, '0');
    days.push({
      key: `day-${day}`,
      day: day,
      rating: monthRatings[dayKey] || null, // Get rating from dummy data
    });
  }
  return days;
});

function prevMonth() {
  currentDate.value = new Date(currentYear.value, currentMonth.value - 1, 1);
}

function nextMonth() {
  currentDate.value = new Date(currentYear.value, currentMonth.value + 1, 1);
}

function getDayClass(rating: string | null) {
  if (!rating) return '';
  return `day-${rating}`; // e.g., 'day-good', 'day-mid', 'day-bad'
}

const weekDays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

</script>

<template>
  <div class="journal-view">
    <h1>Daily Journal</h1>

    <div class="calendar-container">
      <div class="calendar-header">
        <button @click="prevMonth" class="nav-button">&lt;</button>
        <h2>{{ monthName }}</h2>
        <button @click="nextMonth" class="nav-button">&gt;</button>
      </div>

      <div class="calendar-grid">
        <div v-for="dayName in weekDays" :key="dayName" class="weekday-header">
          {{ dayName }}
        </div>
        <div
          v-for="calDay in calendarDays"
          :key="calDay.key"
          class="calendar-day"
          :class="[{ 'empty-day': !calDay.day }, getDayClass(calDay.rating)]"
        >
          <span v-if="calDay.day">{{ calDay.day }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.journal-view {
  padding: 1rem;
  font-family: 'Switzer', sans-serif;
  max-width: 900px;
  margin: 0 auto;
}

h1 {
  font-family: 'Nohemi', sans-serif;
  color: #3c8a38;
  text-align: center;
  margin-bottom: 2rem;
}

.calendar-container {
  background-color: #ffffff;
  border: 1px solid #a2e59f;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.calendar-header h2 {
  font-family: 'Nohemi', sans-serif;
  font-size: 1.4rem;
  color: #333;
  margin: 0;
  text-align: center;
  flex-grow: 1;
}

.nav-button {
  background: none;
  border: 1px solid #a2e59f;
  color: #3c8a38;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-bottom: 2px; /* Adjust vertical alignment */
}

.nav-button:hover {
  background-color: #e8f5e9;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px; /* Gap between cells */
}

.weekday-header {
  text-align: center;
  font-weight: 600;
  color: #555;
  font-size: 0.85rem;
  padding-bottom: 0.5rem;
  font-family: 'Nohemi', sans-serif;
}

.calendar-day {
  border: 1px solid #eee;
  border-radius: 4px;
  height: 80px; /* Adjust height as needed */
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  position: relative;
  transition: background-color 0.2s;
}

.calendar-day span {
  z-index: 1; /* Ensure number is above background color */
}

.empty-day {
  background-color: #f9f9f9;
  border-color: #f0f0f0;
}

/* Day rating colors */
.day-good {
  background-color: rgba(162, 229, 159, 0.6); /* Light green with opacity */
  border-color: rgba(162, 229, 159, 0.8);
}
.day-mid {
  background-color: rgba(255, 241, 118, 0.6); /* Light yellow with opacity */
  border-color: rgba(255, 241, 118, 0.8);
}
.day-bad {
  background-color: rgba(255, 182, 193, 0.6); /* Light red/pink with opacity */
  border-color: rgba(255, 182, 193, 0.8);
}

/* Optional: Hover effect for days */
.calendar-day:not(.empty-day):hover {
  background-color: #e8f5e9;
  cursor: pointer; /* Indicate clickability (for future) */
}
</style>