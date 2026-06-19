import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 添加Token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    const res = response.data
    
    // 统一处理响应
    if (res.code === 200 || res.code === 201) {
      return res
    } else {
      ElMessage.error(res.message || '请求失败')
      return Promise.reject(new Error(res.message || '请求失败'))
    }
  },
  error => {
    // 处理HTTP错误
    if (error.response) {
      const { status, data } = error.response
      
      if (status === 401) {
        ElMessage.error('未授权，请重新登录')
        localStorage.removeItem('token')
        localStorage.removeItem('username')
        window.location.href = '/login'
      } else if (status === 404) {
        ElMessage.error(data.message || '资源不存在')
      } else if (status === 500) {
        ElMessage.error('服务器错误')
      } else {
        ElMessage.error(data.message || '请求失败')
      }
    } else if (error.request) {
      ElMessage.error('网络错误，请检查连接')
    } else {
      ElMessage.error('请求配置错误')
    }
    
    return Promise.reject(error)
  }
)

export default api
