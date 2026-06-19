<template>
  <el-container class="layout-container">
    <!-- 顶部导航栏 -->
    <el-header class="layout-header">
      <div class="header-left">
        <el-icon :size="28" color="#409eff">
          <Money />
        </el-icon>
        <h1 class="header-title">工资管理系统</h1>
      </div>
      <div class="header-right">
        <span class="username">{{ username }}</span>
        <el-button type="danger" @click="handleLogout" :icon="SwitchButton">
          退出登录
        </el-button>
      </div>
    </el-header>

    <el-container>
      <!-- 侧边菜单 -->
      <el-aside width="220px" class="layout-aside">
        <el-menu
          :default-active="activeMenu"
          router
          class="sidebar-menu"
        >
          <el-menu-item index="/employees">
            <el-icon><User /></el-icon>
            <span>员工管理</span>
          </el-menu-item>
          <el-menu-item index="/salaries">
            <el-icon><Money /></el-icon>
            <span>工资管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主内容区 -->
      <el-main class="layout-main">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Money, SwitchButton } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

const username = ref('')
const activeMenu = computed(() => route.path)

onMounted(() => {
  username.value = localStorage.getItem('username') || '用户'
})

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch {
    // 用户取消
  }
}
</script>

<style scoped>
.layout-container {
  min-height: 100vh;
}

.layout-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.header-title {
  font-size: 22px;
  font-weight: bold;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.username {
  font-size: 16px;
  font-weight: 500;
}

.layout-aside {
  background: #fff;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
}

.sidebar-menu {
  border-right: none;
  padding-top: 20px;
}

.sidebar-menu .el-menu-item {
  margin: 5px 10px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.sidebar-menu .el-menu-item:hover {
  background: #ecf5ff;
}

.sidebar-menu .el-menu-item.is-active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.layout-main {
  background: #f5f7fa;
  padding: 25px;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>
