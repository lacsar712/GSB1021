import { createRouter, createWebHistory } from 'vue-router'
import Login from './views/Login.vue'
import Layout from './views/Layout.vue'
import Employees from './views/Employees.vue'
import Salaries from './views/Salaries.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    component: Layout,
    redirect: '/employees',
    children: [
      {
        path: 'employees',
        name: 'Employees',
        component: Employees,
        meta: { title: '员工管理' }
      },
      {
        path: 'salaries',
        name: 'Salaries',
        component: Salaries,
        meta: { title: '工资管理' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.path === '/login') {
    // 已登录跳转到首页
    if (token) {
      next('/')
    } else {
      next()
    }
  } else {
    // 未登录跳转到登录页
    if (!token) {
      next('/login')
    } else {
      next()
    }
  }
})

export default router
