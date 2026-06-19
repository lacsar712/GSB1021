<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">员工管理</h2>
      <el-button type="primary" :icon="Plus" @click="handleAdd">
        新增员工
      </el-button>
    </div>

    <!-- 员工列表 -->
    <el-card class="table-card">
      <el-table
        :data="employees"
        v-loading="loading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="department" label="部门" width="150" />
        <el-table-column prop="position" label="职位" width="150" />
        <el-table-column prop="phone" label="电话" width="150" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              :icon="Edit"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              type="danger"
              size="small"
              :icon="Delete"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="resetForm"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-input v-model="form.department" placeholder="请输入部门" />
        </el-form-item>
        <el-form-item label="职位" prop="position">
          <el-input v-model="form.position" placeholder="请输入职位" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入电话" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 删除确认对话框 -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="确认删除"
      width="400px"
    >
      <div class="delete-confirm">
        <el-icon :size="50" color="#f56c6c">
          <WarningFilled />
        </el-icon>
        <p class="confirm-text">确定要删除员工 <strong>{{ currentEmployee?.name }}</strong> 吗？</p>
        <p class="confirm-tip">删除后将无法恢复，该员工的工资记录也会被删除！</p>
      </div>
      <template #footer>
        <el-button @click="deleteDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="confirmDelete" :loading="deleting">
          确认删除
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Edit, Delete, WarningFilled } from '@element-plus/icons-vue'
import api from '../utils/api'

const loading = ref(false)
const employees = ref([])
const dialogVisible = ref(false)
const deleteDialogVisible = ref(false)
const submitting = ref(false)
const deleting = ref(false)
const formRef = ref(null)
const currentEmployee = ref(null)
const isEdit = ref(false)

const form = reactive({
  name: '',
  department: '',
  position: '',
  phone: '',
  email: ''
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  department: [{ required: true, message: '请输入部门', trigger: 'blur' }],
  position: [{ required: true, message: '请输入职位', trigger: 'blur' }]
}

const dialogTitle = ref('新增员工')

// 获取员工列表
const fetchEmployees = async () => {
  loading.value = true
  try {
    const res = await api.get('/employees')
    employees.value = res.data || []
  } catch (error) {
    console.error('Failed to fetch employees:', error)
  } finally {
    loading.value = false
  }
}

// 新增员工
const handleAdd = () => {
  isEdit.value = false
  dialogTitle.value = '新增员工'
  dialogVisible.value = true
}

// 编辑员工
const handleEdit = (row) => {
  isEdit.value = true
  dialogTitle.value = '编辑员工'
  currentEmployee.value = row
  Object.assign(form, {
    name: row.name,
    department: row.department,
    position: row.position,
    phone: row.phone || '',
    email: row.email || ''
  })
  dialogVisible.value = true
}

// 删除员工
const handleDelete = (row) => {
  currentEmployee.value = row
  deleteDialogVisible.value = true
}

// 确认删除
const confirmDelete = async () => {
  deleting.value = true
  try {
    await api.delete(`/employees/${currentEmployee.value.id}`)
    ElMessage.success('删除成功')
    deleteDialogVisible.value = false
    fetchEmployees()
  } catch (error) {
    console.error('Failed to delete employee:', error)
  } finally {
    deleting.value = false
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    
    submitting.value = true
    try {
      if (isEdit.value) {
        await api.put(`/employees/${currentEmployee.value.id}`, form)
        ElMessage.success('更新成功')
      } else {
        await api.post('/employees', form)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      fetchEmployees()
    } catch (error) {
      console.error('Failed to submit:', error)
    } finally {
      submitting.value = false
    }
  })
}

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  Object.assign(form, {
    name: '',
    department: '',
    position: '',
    phone: '',
    email: ''
  })
}

onMounted(() => {
  fetchEmployees()
})
</script>

<style scoped>
.page-container {
  width: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.table-card {
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.delete-confirm {
  text-align: center;
  padding: 20px;
}

.confirm-text {
  font-size: 16px;
  margin: 20px 0 10px;
  color: #303133;
}

.confirm-tip {
  font-size: 14px;
  color: #909399;
}

:deep(.el-table) {
  font-size: 14px;
}

:deep(.el-table th) {
  background: #f5f7fa;
  color: #606266;
  font-weight: 600;
}

:deep(.el-dialog) {
  border-radius: 12px;
}

:deep(.el-button) {
  border-radius: 6px;
  transition: all 0.3s ease;
}

:deep(.el-button:hover) {
  transform: translateY(-2px);
}
</style>
