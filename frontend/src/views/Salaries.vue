<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">工资管理</h2>
      <el-button type="primary" :icon="Plus" @click="handleAdd">
        新增工资记录
      </el-button>
    </div>

    <!-- 工资列表 -->
    <el-card class="table-card">
      <el-table
        :data="salaries"
        v-loading="loading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="员工姓名" width="120">
          <template #default="{ row }">
            {{ row.employee?.name || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="month" label="月份" width="120" />
        <el-table-column label="基本工资" width="120">
          <template #default="{ row }">
            ¥{{ row.base_salary.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column label="奖金" width="120">
          <template #default="{ row }">
            ¥{{ row.bonus.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column label="扣款" width="120">
          <template #default="{ row }">
            ¥{{ row.deduction.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column label="实发工资" width="140">
          <template #default="{ row }">
            <span class="total-salary">¥{{ row.total.toFixed(2) }}</span>
          </template>
        </el-table-column>
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
        label-width="100px"
      >
        <el-form-item label="选择员工" prop="employee_id">
          <el-select
            v-model="form.employee_id"
            placeholder="请选择员工"
            style="width: 100%"
          >
            <el-option
              v-for="emp in employees"
              :key="emp.id"
              :label="emp.name"
              :value="emp.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="月份" prop="month">
          <el-date-picker
            v-model="monthPicker"
            type="month"
            placeholder="请选择月份"
            format="YYYY-MM"
            value-format="YYYY-MM"
            style="width: 100%"
            @change="handleMonthChange"
          />
        </el-form-item>
        <el-form-item label="基本工资" prop="base_salary">
          <el-input-number
            v-model="form.base_salary"
            :min="0"
            :precision="2"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="奖金" prop="bonus">
          <el-input-number
            v-model="form.bonus"
            :min="0"
            :precision="2"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="扣款" prop="deduction">
          <el-input-number
            v-model="form.deduction"
            :min="0"
            :precision="2"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="实发工资">
          <el-input
            :value="`¥${totalSalary.toFixed(2)}`"
            disabled
          />
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
        <p class="confirm-text">确定要删除该工资记录吗？</p>
        <p class="confirm-tip">删除后将无法恢复！</p>
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
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Edit, Delete, WarningFilled } from '@element-plus/icons-vue'
import api from '../utils/api'

const loading = ref(false)
const salaries = ref([])
const employees = ref([])
const dialogVisible = ref(false)
const deleteDialogVisible = ref(false)
const submitting = ref(false)
const deleting = ref(false)
const formRef = ref(null)
const currentSalary = ref(null)
const isEdit = ref(false)
const monthPicker = ref('')

const form = reactive({
  employee_id: null,
  month: '',
  base_salary: 0,
  bonus: 0,
  deduction: 0
})

const rules = {
  employee_id: [{ required: true, message: '请选择员工', trigger: 'change' }],
  month: [{ required: true, message: '请选择月份', trigger: 'blur' }],
  base_salary: [{ required: true, message: '请输入基本工资', trigger: 'blur' }]
}

const dialogTitle = ref('新增工资记录')

// 计算实发工资
const totalSalary = computed(() => {
  return form.base_salary + form.bonus - form.deduction
})

// 月份选择器变化
const handleMonthChange = (value) => {
  form.month = value
}

// 获取工资列表
const fetchSalaries = async () => {
  loading.value = true
  try {
    const res = await api.get('/salaries')
    salaries.value = res.data || []
  } catch (error) {
    console.error('Failed to fetch salaries:', error)
  } finally {
    loading.value = false
  }
}

// 获取员工列表
const fetchEmployees = async () => {
  try {
    const res = await api.get('/employees')
    employees.value = res.data || []
  } catch (error) {
    console.error('Failed to fetch employees:', error)
  }
}

// 新增工资记录
const handleAdd = () => {
  isEdit.value = false
  dialogTitle.value = '新增工资记录'
  dialogVisible.value = true
}

// 编辑工资记录
const handleEdit = (row) => {
  isEdit.value = true
  dialogTitle.value = '编辑工资记录'
  currentSalary.value = row
  Object.assign(form, {
    employee_id: row.employee_id,
    month: row.month,
    base_salary: row.base_salary,
    bonus: row.bonus,
    deduction: row.deduction
  })
  monthPicker.value = row.month
  dialogVisible.value = true
}

// 删除工资记录
const handleDelete = (row) => {
  currentSalary.value = row
  deleteDialogVisible.value = true
}

// 确认删除
const confirmDelete = async () => {
  deleting.value = true
  try {
    await api.delete(`/salaries/${currentSalary.value.id}`)
    ElMessage.success('删除成功')
    deleteDialogVisible.value = false
    fetchSalaries()
  } catch (error) {
    console.error('Failed to delete salary:', error)
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
        await api.put(`/salaries/${currentSalary.value.id}`, form)
        ElMessage.success('更新成功')
      } else {
        await api.post('/salaries', form)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      fetchSalaries()
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
    employee_id: null,
    month: '',
    base_salary: 0,
    bonus: 0,
    deduction: 0
  })
  monthPicker.value = ''
}

onMounted(() => {
  fetchSalaries()
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

.total-salary {
  font-weight: bold;
  color: #67c23a;
  font-size: 15px;
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
