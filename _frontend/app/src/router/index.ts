import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import EmployeeOnboardingPage from '@/pages/EmployeeOnboardingPage.vue'

const routes = [
    { path: '/', name: 'home', component: HomePage },
    { path: '/employee/onboarding', name: 'onboarding', component: EmployeeOnboardingPage },
  // add more routes here
]

export const router = createRouter({
    history: createWebHistory(),
    routes,
})