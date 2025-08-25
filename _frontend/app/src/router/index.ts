import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import EmployeeOnboardingPage from '@/pages/EmployeeOnboardingPage.vue'
import ManageEmployeesPage from '@/pages/ManageEmployeesPage.vue'
import ContractorAdd from '@/pages/ContractorAdd.vue'
import ContractorsManage from '@/pages/ContractorsManage.vue'

const routes = [
    { path: '/', name: 'home', component: HomePage },
    { path: '/employee/onboarding', name: 'onboarding', component: EmployeeOnboardingPage },
    {path: '/employee/manage-employees', name:'manage-employee', component: ManageEmployeesPage},
    {path: '/contractor/add-contractor', name: 'add-contractor', component: ContractorAdd},
    {path: '/contractor/manage-contractors', name: 'manage-contractor', component: ContractorsManage}

  // add more routes here
]

export const router = createRouter({
    history: createWebHistory(),
    routes,
})