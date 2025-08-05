import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import EmployeesPage from '@/pages/EmployeesPage.vue'

const routes = [
    { path: '/', name: 'home', component: HomePage },
    { path: '/employees', name: 'employees', component: EmployeesPage },
  // add more routes here
]

export const router = createRouter({
    history: createWebHistory(),
    routes,
})