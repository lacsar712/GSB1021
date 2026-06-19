<template>
  <div class="login-container">
    <!-- 左侧区域 -->
    <div class="login-left">
      <div class="brand-content">
        <div class="logo-container">
          <el-icon :size="80" color="#fff">
            <Money />
          </el-icon>
        </div>
        <h1 class="brand-title">工资管理系统</h1>
        <p class="brand-subtitle">Salary Management System</p>
        <p class="brand-description">高效、安全、便捷的企业工资管理解决方案</p>
      </div>
    </div>

    <!-- 右侧区域 -->
    <div class="login-right">
      <div class="login-box">
        <h2 class="login-title">欢迎登录</h2>
        <p class="login-subtitle">请输入您的账号和密码</p>

        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="rules"
          class="login-form"
          @keyup.enter="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              size="large"
              :prefix-icon="User"
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              :prefix-icon="Lock"
              show-password
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              class="login-button"
              @click="handleLogin"
            >
              {{ loading ? '登录中...' : '登 录' }}
            </el-button>
          </el-form-item>
        </el-form>

        <div class="default-account">
          <el-icon><InfoFilled /></el-icon>
          <span>默认账号：admin / 123456</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Money, InfoFilled } from '@element-plus/icons-vue'
import api from '../utils/api'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    try {
      const res = await api.post('/auth/login', loginForm)
      
      // 保存Token和用户信息
      localStorage.setItem('token', res.data.access_token)
      localStorage.setItem('username', res.data.username)
      
      ElMessage.success('登录成功')
      router.push('/')
    } catch (error) {
      console.error('Login failed:', error)
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.login-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-left {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.login-left::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: move 20s linear infinite;
}

@keyframes move {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

.brand-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
}

.logo-container {
  margin-bottom: 30px;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

.brand-title {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 15px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.brand-subtitle {
  font-size: 20px;
  margin-bottom: 20px;
  opacity: 0.9;
}

.brand-description {
  font-size: 16px;
  opacity: 0.8;
  max-width: 400px;
  margin: 0 auto;
  line-height: 1.6;
}

.login-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  padding: 60px;
}

.login-box {
  width: 100%;
  max-width: 420px;
  background: white;
  padding: 50px 40px;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.login-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.15);
}

.login-title {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 10px;
  text-align: center;
}

.login-subtitle {
  font-size: 14px;
  color: #909399;
  margin-bottom: 40px;
  text-align: center;
}

.login-form {
  margin-bottom: 20px;
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: bold;
  border-radius: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s ease;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.login-button:active {
  transform: translateY(0);
}

.default-account {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: #f0f9ff;
  border-radius: 8px;
  color: #409eff;
  font-size: 14px;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 0 0 1px #dcdfe6 inset;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #c0c4cc inset;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #409eff inset !important;
}
</style>
