<template>
  <div class="settings-container">
    <!-- 导航栏 -->
    <nav class="navbar glass-card">
      <div class="nav-content">
        <div class="logo">
          <el-icon class="logo-icon"><TrendCharts /></el-icon>
          <span class="logo-text gradient-text">ESG评分系统</span>
        </div>
        <div class="nav-menu">
          <router-link to="/" class="nav-item">首页</router-link>
          <router-link to="/scoring" class="nav-item">评分计算</router-link>
          <router-link to="/analysis" class="nav-item">数据分析</router-link>
          <router-link to="/reports" class="nav-item">报告管理</router-link>
          <router-link to="/settings" class="nav-item active">系统设置</router-link>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <main class="main-content">
      <div class="content-wrapper">
        <!-- 页面标题 -->
        <div class="page-header fade-in">
          <h1 class="page-title">系统设置</h1>
          <p class="page-subtitle">配置ESG评分系统参数和选项</p>
        </div>

        <!-- 设置内容 -->
        <div class="settings-content slide-up">
          <div class="settings-layout">
            <!-- 侧边栏导航 -->
            <div class="settings-sidebar glass-card">
              <div class="sidebar-menu">
                <div
                  v-for="item in menuItems"
                  :key="item.key"
                  class="menu-item"
                  :class="{ active: activeTab === item.key }"
                  @click="activeTab = item.key"
                >
                  <el-icon class="menu-icon">
                    <component :is="item.icon" />
                  </el-icon>
                  <span class="menu-label">{{ item.label }}</span>
                </div>
              </div>
            </div>

            <!-- 设置面板 -->
            <div class="settings-panel glass-card">
              <!-- 模型参数设置 -->
              <div v-if="activeTab === 'model'" class="setting-section">
                <div class="section-header">
                  <h3 class="section-title">
                    <el-icon><Setting /></el-icon>
                    模型参数配置
                  </h3>
                  <p class="section-desc">调整ESG评分模型的核心参数</p>
                </div>
                
                <div class="setting-groups">
                  <!-- 维度权重 -->
                  <div class="setting-group">
                    <h4 class="group-title">维度权重配置</h4>
                    <div class="weight-controls">
                      <div class="weight-item">
                        <label class="weight-label">
                          <el-icon class="dimension-icon e"><Sunny /></el-icon>
                          环境 (E)
                        </label>
                        <div class="weight-control">
                          <el-slider
                            v-model="modelParams.weights.E"
                            :min="0"
                            :max="100"
                            :step="1"
                            show-input
                            @change="updateWeights"
                          />
                          <span class="weight-value">{{ modelParams.weights.E }}%</span>
                        </div>
                      </div>
                      
                      <div class="weight-item">
                        <label class="weight-label">
                          <el-icon class="dimension-icon s"><User /></el-icon>
                          社会 (S)
                        </label>
                        <div class="weight-control">
                          <el-slider
                            v-model="modelParams.weights.S"
                            :min="0"
                            :max="100"
                            :step="1"
                            show-input
                            @change="updateWeights"
                          />
                          <span class="weight-value">{{ modelParams.weights.S }}%</span>
                        </div>
                      </div>
                      
                      <div class="weight-item">
                        <label class="weight-label">
                          <el-icon class="dimension-icon g"><Management /></el-icon>
                          治理 (G)
                        </label>
                        <div class="weight-control">
                          <el-slider
                            v-model="modelParams.weights.G"
                            :min="0"
                            :max="100"
                            :step="1"
                            show-input
                            @change="updateWeights"
                          />
                          <span class="weight-value">{{ modelParams.weights.G }}%</span>
                        </div>
                      </div>
                      
                      <div class="weight-total">
                        <span class="total-label">权重总和:</span>
                        <span class="total-value" :class="{ error: totalWeight !== 100 }">
                          {{ totalWeight }}%
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 交叉项系数 -->
                  <div class="setting-group">
                    <h4 class="group-title">交叉项系数</h4>
                    <div class="cross-terms">
                      <div class="cross-item">
                        <label>E × S 系数</label>
                        <el-input-number
                          v-model="modelParams.crossTerms.ES"
                          :min="0"
                          :max="1"
                          :step="0.01"
                          :precision="2"
                        />
                      </div>
                      <div class="cross-item">
                        <label>E × G 系数</label>
                        <el-input-number
                          v-model="modelParams.crossTerms.EG"
                          :min="0"
                          :max="1"
                          :step="0.01"
                          :precision="2"
                        />
                      </div>
                      <div class="cross-item">
                        <label>S × G 系数</label>
                        <el-input-number
                          v-model="modelParams.crossTerms.SG"
                          :min="0"
                          :max="1"
                          :step="0.01"
                          :precision="2"
                        />
                      </div>
                    </div>
                  </div>
                  
                  <!-- 非线性调整 -->
                  <div class="setting-group">
                    <h4 class="group-title">非线性调整参数</h4>
                    <div class="nonlinear-params">
                      <div class="param-item">
                        <label>调整强度</label>
                        <el-slider
                          v-model="modelParams.nonlinear.intensity"
                          :min="0"
                          :max="2"
                          :step="0.1"
                          show-input
                        />
                      </div>
                      <div class="param-item">
                        <label>阈值参数</label>
                        <el-input-number
                          v-model="modelParams.nonlinear.threshold"
                          :min="0"
                          :max="100"
                          :step="1"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 行业配置 -->
              <div v-if="activeTab === 'industry'" class="setting-section">
                <div class="section-header">
                  <h3 class="section-title">
                    <el-icon><OfficeBuilding /></el-icon>
                    行业配置管理
                  </h3>
                  <p class="section-desc">管理支持的行业类型和特定权重</p>
                </div>
                
                <div class="industry-management">
                  <div class="industry-toolbar">
                    <el-button type="primary" @click="addIndustry">
                      <el-icon><Plus /></el-icon>
                      添加行业
                    </el-button>
                    <el-button @click="importIndustries">
                      <el-icon><Upload /></el-icon>
                      导入配置
                    </el-button>
                    <el-button @click="exportIndustries">
                      <el-icon><Download /></el-icon>
                      导出配置
                    </el-button>
                  </div>
                  
                  <div class="industry-list">
                    <div
                      v-for="(industry, index) in industries"
                      :key="index"
                      class="industry-item"
                    >
                      <div class="industry-header">
                        <div class="industry-info">
                          <el-input
                            v-model="industry.name"
                            placeholder="行业名称"
                            class="industry-name"
                          />
                          <el-input
                            v-model="industry.description"
                            placeholder="行业描述"
                            class="industry-desc"
                          />
                        </div>
                        <div class="industry-actions">
                          <el-button size="small" @click="duplicateIndustry(index)">
                            <el-icon><CopyDocument /></el-icon>
                          </el-button>
                          <el-button size="small" type="danger" @click="removeIndustry(index)">
                            <el-icon><Delete /></el-icon>
                          </el-button>
                        </div>
                      </div>
                      
                      <div class="industry-weights">
                        <div class="weight-row">
                          <span class="weight-label">环境权重:</span>
                          <el-slider
                            v-model="industry.weights.E"
                            :min="0"
                            :max="100"
                            show-input
                            style="flex: 1; margin: 0 16px;"
                          />
                        </div>
                        <div class="weight-row">
                          <span class="weight-label">社会权重:</span>
                          <el-slider
                            v-model="industry.weights.S"
                            :min="0"
                            :max="100"
                            show-input
                            style="flex: 1; margin: 0 16px;"
                          />
                        </div>
                        <div class="weight-row">
                          <span class="weight-label">治理权重:</span>
                          <el-slider
                            v-model="industry.weights.G"
                            :min="0"
                            :max="100"
                            show-input
                            style="flex: 1; margin: 0 16px;"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 指标管理 -->
              <div v-if="activeTab === 'indicators'" class="setting-section">
                <div class="section-header">
                  <h3 class="section-title">
                    <el-icon><DataAnalysis /></el-icon>
                    指标管理
                  </h3>
                  <p class="section-desc">配置ESG评分指标体系</p>
                </div>
                
                <div class="indicators-management">
                  <el-tabs v-model="activeIndicatorTab">
                    <el-tab-pane label="环境指标" name="E">
                      <indicator-config
                        v-model="indicators.E"
                        dimension="E"
                        @add="addIndicator"
                        @remove="removeIndicator"
                      />
                    </el-tab-pane>
                    <el-tab-pane label="社会指标" name="S">
                      <indicator-config
                        v-model="indicators.S"
                        dimension="S"
                        @add="addIndicator"
                        @remove="removeIndicator"
                      />
                    </el-tab-pane>
                    <el-tab-pane label="治理指标" name="G">
                      <indicator-config
                        v-model="indicators.G"
                        dimension="G"
                        @add="addIndicator"
                        @remove="removeIndicator"
                      />
                    </el-tab-pane>
                  </el-tabs>
                </div>
              </div>

              <!-- 系统配置 -->
              <div v-if="activeTab === 'system'" class="setting-section">
                <div class="section-header">
                  <h3 class="section-title">
                    <el-icon><Tools /></el-icon>
                    系统配置
                  </h3>
                  <p class="section-desc">系统运行参数和界面设置</p>
                </div>
                
                <div class="system-settings">
                  <div class="setting-group">
                    <h4 class="group-title">界面设置</h4>
                    <div class="setting-items">
                      <div class="setting-item">
                        <div class="setting-label">
                          <span>主题模式</span>
                          <span class="setting-desc">选择界面主题</span>
                        </div>
                        <el-select v-model="systemConfig.theme" style="width: 120px">
                          <el-option label="自动" value="auto" />
                          <el-option label="浅色" value="light" />
                          <el-option label="深色" value="dark" />
                        </el-select>
                      </div>
                      
                      <div class="setting-item">
                        <div class="setting-label">
                          <span>语言设置</span>
                          <span class="setting-desc">界面显示语言</span>
                        </div>
                        <el-select v-model="systemConfig.language" style="width: 120px">
                          <el-option label="中文" value="zh-CN" />
                          <el-option label="English" value="en-US" />
                        </el-select>
                      </div>
                      
                      <div class="setting-item">
                        <div class="setting-label">
                          <span>动画效果</span>
                          <span class="setting-desc">启用界面动画</span>
                        </div>
                        <el-switch v-model="systemConfig.animations" />
                      </div>
                    </div>
                  </div>
                  
                  <div class="setting-group">
                    <h4 class="group-title">数据设置</h4>
                    <div class="setting-items">
                      <div class="setting-item">
                        <div class="setting-label">
                          <span>自动保存</span>
                          <span class="setting-desc">自动保存评分数据</span>
                        </div>
                        <el-switch v-model="systemConfig.autoSave" />
                      </div>
                      
                      <div class="setting-item">
                        <div class="setting-label">
                          <span>保存间隔</span>
                          <span class="setting-desc">自动保存时间间隔（分钟）</span>
                        </div>
                        <el-input-number
                          v-model="systemConfig.saveInterval"
                          :min="1"
                          :max="60"
                          :disabled="!systemConfig.autoSave"
                        />
                      </div>
                      
                      <div class="setting-item">
                        <div class="setting-label">
                          <span>数据验证</span>
                          <span class="setting-desc">启用严格数据验证</span>
                        </div>
                        <el-switch v-model="systemConfig.strictValidation" />
                      </div>
                    </div>
                  </div>
                  
                  <div class="setting-group">
                    <h4 class="group-title">导出设置</h4>
                    <div class="setting-items">
                      <div class="setting-item">
                        <div class="setting-label">
                          <span>默认格式</span>
                          <span class="setting-desc">报告导出默认格式</span>
                        </div>
                        <el-select v-model="systemConfig.exportFormat" style="width: 120px">
                          <el-option label="PDF" value="pdf" />
                          <el-option label="Excel" value="xlsx" />
                          <el-option label="Word" value="docx" />
                        </el-select>
                      </div>
                      
                      <div class="setting-item">
                        <div class="setting-label">
                          <span>包含图表</span>
                          <span class="setting-desc">导出时包含可视化图表</span>
                        </div>
                        <el-switch v-model="systemConfig.includeCharts" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 用户管理 -->
              <div v-if="activeTab === 'users'" class="setting-section">
                <div class="section-header">
                  <h3 class="section-title">
                    <el-icon><UserFilled /></el-icon>
                    用户管理
                  </h3>
                  <p class="section-desc">管理系统用户和权限</p>
                </div>
                
                <div class="user-management">
                  <div class="user-toolbar">
                    <el-button type="primary" @click="addUser">
                      <el-icon><Plus /></el-icon>
                      添加用户
                    </el-button>
                    <el-input
                      v-model="userSearchQuery"
                      placeholder="搜索用户..."
                      prefix-icon="Search"
                      style="width: 300px"
                    />
                  </div>
                  
                  <el-table :data="filteredUsers" style="width: 100%">
                    <el-table-column prop="name" label="姓名" width="120" />
                    <el-table-column prop="email" label="邮箱" width="200" />
                    <el-table-column prop="role" label="角色" width="120">
                      <template #default="scope">
                        <el-tag :type="getRoleType(scope.row.role)">
                          {{ getRoleText(scope.row.role) }}
                        </el-tag>
                      </template>
                    </el-table-column>
                    <el-table-column prop="status" label="状态" width="100">
                      <template #default="scope">
                        <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
                          {{ scope.row.status === 'active' ? '活跃' : '禁用' }}
                        </el-tag>
                      </template>
                    </el-table-column>
                    <el-table-column prop="lastLogin" label="最后登录" width="150" />
                    <el-table-column label="操作" width="200">
                      <template #default="scope">
                        <el-button size="small" @click="editUser(scope.row)">
                          编辑
                        </el-button>
                        <el-button
                          size="small"
                          :type="scope.row.status === 'active' ? 'warning' : 'success'"
                          @click="toggleUserStatus(scope.row)"
                        >
                          {{ scope.row.status === 'active' ? '禁用' : '启用' }}
                        </el-button>
                        <el-button
                          size="small"
                          type="danger"
                          @click="deleteUser(scope.row)"
                        >
                          删除
                        </el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="settings-actions glass-card">
          <div class="actions-left">
            <el-button @click="resetToDefaults">
              <el-icon><RefreshLeft /></el-icon>
              恢复默认
            </el-button>
            <el-button @click="importSettings">
              <el-icon><Upload /></el-icon>
              导入配置
            </el-button>
            <el-button @click="exportSettings">
              <el-icon><Download /></el-icon>
              导出配置
            </el-button>
          </div>
          <div class="actions-right">
            <el-button @click="cancelChanges">取消</el-button>
            <el-button type="primary" @click="saveSettings">
              <el-icon><Check /></el-icon>
              保存设置
            </el-button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useESGStore } from '@/stores/esg'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  TrendCharts, Setting, Sunny, User, Management, OfficeBuilding, DataAnalysis,
  Tools, UserFilled, Plus, Upload, Download, CopyDocument, Delete, RefreshLeft,
  Check
} from '@element-plus/icons-vue'

const esgStore = useESGStore()

// 响应式数据
const activeTab = ref('model')
const activeIndicatorTab = ref('E')
const userSearchQuery = ref('')

// 菜单项
const menuItems = ref([
  { key: 'model', label: '模型参数', icon: 'Setting' },
  { key: 'industry', label: '行业配置', icon: 'OfficeBuilding' },
  { key: 'indicators', label: '指标管理', icon: 'DataAnalysis' },
  { key: 'system', label: '系统配置', icon: 'Tools' },
  { key: 'users', label: '用户管理', icon: 'UserFilled' }
])

// 模型参数
const modelParams = ref({
  weights: {
    E: 40,
    S: 30,
    G: 30
  },
  crossTerms: {
    ES: 0.1,
    EG: 0.08,
    SG: 0.12
  },
  nonlinear: {
    intensity: 1.2,
    threshold: 75
  }
})

// 行业配置
const industries = ref([
  {
    name: '互联网科技',
    description: '互联网、软件、科技服务等行业',
    weights: { E: 35, S: 35, G: 30 }
  },
  {
    name: '金融保险',
    description: '银行、保险、证券等金融服务业',
    weights: { E: 25, S: 40, G: 35 }
  },
  {
    name: '制造业',
    description: '传统制造、重工业等',
    weights: { E: 50, S: 25, G: 25 }
  }
])

// 指标配置
const indicators = ref({
  E: ['碳排放强度', '能源消耗', '水资源利用', '废物管理', '生物多样性'],
  S: ['员工权益', '社区发展', '产品责任', '供应链管理', '客户隐私'],
  G: ['董事会结构', '透明度', '风险管理', '商业道德', '股东权益']
})

// 系统配置
const systemConfig = ref({
  theme: 'auto',
  language: 'zh-CN',
  animations: true,
  autoSave: true,
  saveInterval: 5,
  strictValidation: true,
  exportFormat: 'pdf',
  includeCharts: true
})

// 用户数据
const users = ref([
  {
    id: 1,
    name: '张三',
    email: 'zhangsan@example.com',
    role: 'admin',
    status: 'active',
    lastLogin: '2024-01-20'
  },
  {
    id: 2,
    name: '李四',
    email: 'lisi@example.com',
    role: 'analyst',
    status: 'active',
    lastLogin: '2024-01-19'
  },
  {
    id: 3,
    name: '王五',
    email: 'wangwu@example.com',
    role: 'viewer',
    status: 'inactive',
    lastLogin: '2024-01-15'
  }
])

// 计算属性
const totalWeight = computed(() => {
  return modelParams.value.weights.E + modelParams.value.weights.S + modelParams.value.weights.G
})

const filteredUsers = computed(() => {
  if (!userSearchQuery.value) return users.value
  const query = userSearchQuery.value.toLowerCase()
  return users.value.filter(user => 
    user.name.toLowerCase().includes(query) ||
    user.email.toLowerCase().includes(query)
  )
})

// 方法
const updateWeights = () => {
  // 权重更新逻辑
  if (totalWeight.value !== 100) {
    ElMessage.warning('权重总和应为100%')
  }
}

const addIndustry = () => {
  industries.value.push({
    name: '新行业',
    description: '请输入行业描述',
    weights: { E: 33, S: 33, G: 34 }
  })
}

const removeIndustry = (index) => {
  industries.value.splice(index, 1)
}

const duplicateIndustry = (index) => {
  const industry = { ...industries.value[index] }
  industry.name += ' (副本)'
  industries.value.push(industry)
}

const importIndustries = () => {
  ElMessage.info('导入行业配置功能开发中')
}

const exportIndustries = () => {
  ElMessage.info('导出行业配置功能开发中')
}

const addIndicator = (dimension) => {
  const newIndicator = prompt('请输入新指标名称:')
  if (newIndicator) {
    indicators.value[dimension].push(newIndicator)
  }
}

const removeIndicator = (dimension, index) => {
  indicators.value[dimension].splice(index, 1)
}

const addUser = () => {
  ElMessage.info('添加用户功能开发中')
}

const editUser = (user) => {
  ElMessage.info(`编辑用户: ${user.name}`)
}

const toggleUserStatus = (user) => {
  user.status = user.status === 'active' ? 'inactive' : 'active'
  ElMessage.success(`用户状态已${user.status === 'active' ? '启用' : '禁用'}`)
}

const deleteUser = (user) => {
  ElMessageBox.confirm(
    `确定要删除用户 ${user.name} 吗？`,
    '确认删除',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    const index = users.value.findIndex(u => u.id === user.id)
    if (index > -1) {
      users.value.splice(index, 1)
      ElMessage.success('用户已删除')
    }
  })
}

const getRoleType = (role) => {
  const types = {
    admin: 'danger',
    analyst: 'warning',
    viewer: 'info'
  }
  return types[role] || 'info'
}

const getRoleText = (role) => {
  const texts = {
    admin: '管理员',
    analyst: '分析师',
    viewer: '查看者'
  }
  return texts[role] || '未知'
}

const resetToDefaults = () => {
  ElMessageBox.confirm(
    '确定要恢复所有设置到默认值吗？此操作不可撤销。',
    '确认重置',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // 重置逻辑
    ElMessage.success('设置已恢复默认')
  })
}

const importSettings = () => {
  ElMessage.info('导入设置功能开发中')
}

const exportSettings = () => {
  ElMessage.info('导出设置功能开发中')
}

const cancelChanges = () => {
  ElMessage.info('已取消更改')
}

const saveSettings = () => {
  if (totalWeight.value !== 100) {
    ElMessage.error('权重总和必须为100%，请调整后再保存')
    return
  }
  
  // 保存设置逻辑
  ElMessage.success('设置已保存')
}

onMounted(() => {
  // 页面加载时的初始化逻辑
})
</script>

<style lang="scss" scoped>
.settings-container {
  min-height: 100vh;
  background: var(--bg-color);
}

// 导航栏样式 - 黑白专业风格
.navbar {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  padding: 16px 32px;
  border-radius: var(--radius-xl);
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-lg);
  
  .nav-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-width: 1000px;
    height: 50px;
  }
  
  .logo {
    display: flex;
    align-items: center;
    gap: 12px;
    
    .logo-icon {
      font-size: 28px;
      color: var(--primary-color);
    }
    
    .logo-text {
      font-size: 20px;
      font-weight: 700;
      color: var(--text-primary);
    }
  }
  
  .nav-menu {
    display: flex;
    gap: 32px;
    
    .nav-item {
      text-decoration: none;
      color: var(--text-secondary);
      font-weight: 500;
      padding: 8px 16px;
      border-radius: var(--radius-md);
      transition: all 0.3s ease;
      
      &:hover {
        color: var(--text-primary);
        background: var(--bg-secondary);
      }
      
      &.active {
        color: #ffffff;
        background: var(--primary-color);
      }
    }
  }
}

.main-content {
  padding-top: 120px;
  min-height: 100vh;
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 40px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
  
  .page-title {
    font-size: 36px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 12px;
  }
  
  .page-subtitle {
    font-size: 18px;
    color: var(--text-secondary);
  }
}

// 设置布局
.settings-content {
  margin-bottom: 32px;
  
  .settings-layout {
    display: grid;
    grid-template-columns: 250px 1fr;
    gap: 24px;
    min-height: 600px;
  }
}

// 侧边栏
.settings-sidebar {
  padding: 0;
  
  .sidebar-menu {
    .menu-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 16px 20px;
      cursor: pointer;
      transition: all 0.3s ease;
      border-bottom: 1px solid rgba(0, 0, 0, 0.05);
      
      &:hover {
        background: rgba(102, 126, 234, 0.1);
      }
      
      &.active {
        background: var(--gradient-primary);
        color: white;
        
        .menu-icon {
          color: white;
        }
      }
      
      .menu-icon {
        font-size: 18px;
        color: var(--primary-color);
      }
      
      .menu-label {
        font-size: 14px;
        font-weight: 500;
      }
    }
  }
}

// 设置面板
.settings-panel {
  padding: 32px;
  
  .setting-section {
    .section-header {
      margin-bottom: 32px;
      
      .section-title {
        font-size: 24px;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
      }
      
      .section-desc {
        font-size: 16px;
        color: var(--text-secondary);
      }
    }
  }
}

// 设置组
.setting-groups {
  display: flex;
  flex-direction: column;
  gap: 32px;
  
  .setting-group {
    .group-title {
      font-size: 18px;
      font-weight: 600;
      color: var(--text-primary);
      margin-bottom: 20px;
    }
  }
}

// 权重控制
.weight-controls {
  .weight-item {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    
    .weight-label {
      min-width: 120px;
      font-size: 16px;
      font-weight: 500;
      display: flex;
      align-items: center;
      gap: 8px;
      
      .dimension-icon {
        font-size: 18px;
        
        &.e {
          color: #52c41a;
        }
        
        &.s {
          color: #1890ff;
        }
        
        &.g {
          color: #722ed1;
        }
      }
    }
    
    .weight-control {
      flex: 1;
      display: flex;
      align-items: center;
      gap: 16px;
      
      .weight-value {
        min-width: 50px;
        font-weight: 600;
        color: var(--primary-color);
      }
    }
  }
  
  .weight-total {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    background: #f8f9fa;
    border-radius: 8px;
    margin-top: 16px;
    
    .total-label {
      font-weight: 600;
      color: var(--text-primary);
    }
    
    .total-value {
      font-size: 18px;
      font-weight: 700;
      color: var(--primary-color);
      
      &.error {
        color: #ff4d4f;
      }
    }
  }
}

// 交叉项
.cross-terms {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  
  .cross-item {
    display: flex;
    flex-direction: column;
    gap: 8px;
    
    label {
      font-size: 14px;
      font-weight: 500;
      color: var(--text-primary);
    }
  }
}

// 非线性参数
.nonlinear-params {
  display: flex;
  flex-direction: column;
  gap: 20px;
  
  .param-item {
    display: flex;
    align-items: center;
    gap: 16px;
    
    label {
      min-width: 100px;
      font-size: 14px;
      font-weight: 500;
      color: var(--text-primary);
    }
  }
}

// 行业管理
.industry-management {
  .industry-toolbar {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
  }
  
  .industry-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
    
    .industry-item {
      padding: 20px;
      background: #f8f9fa;
      border-radius: 8px;
      
      .industry-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 16px;
        
        .industry-info {
          flex: 1;
          display: flex;
          flex-direction: column;
          gap: 8px;
          
          .industry-name {
            font-weight: 600;
          }
        }
        
        .industry-actions {
          display: flex;
          gap: 8px;
        }
      }
      
      .industry-weights {
        display: flex;
        flex-direction: column;
        gap: 12px;
        
        .weight-row {
          display: flex;
          align-items: center;
          
          .weight-label {
            min-width: 80px;
            font-size: 14px;
            color: var(--text-secondary);
          }
        }
      }
    }
  }
}

// 系统设置
.system-settings {
  .setting-items {
    display: flex;
    flex-direction: column;
    gap: 20px;
    
    .setting-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 0;
      border-bottom: 1px solid #f0f0f0;
      
      .setting-label {
        display: flex;
        flex-direction: column;
        gap: 4px;
        
        span:first-child {
          font-size: 16px;
          font-weight: 500;
          color: var(--text-primary);
        }
        
        .setting-desc {
          font-size: 14px;
          color: var(--text-secondary);
        }
      }
    }
  }
}

// 用户管理
.user-management {
  .user-toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
  }
}

// 操作按钮
.settings-actions {
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  .actions-left,
  .actions-right {
    display: flex;
    gap: 12px;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 20px;
  }
  
  .settings-layout {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .settings-sidebar {
    .sidebar-menu {
      display: flex;
      overflow-x: auto;
      
      .menu-item {
        white-space: nowrap;
        border-bottom: none;
        border-right: 1px solid rgba(0, 0, 0, 0.05);
      }
    }
  }
  
  .weight-item {
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
  }
  
  .cross-terms {
    grid-template-columns: 1fr;
  }
  
  .industry-header {
    flex-direction: column;
    gap: 12px;
  }
  
  .setting-item {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  
  .settings-actions {
    flex-direction: column;
    gap: 16px;
    
    .actions-left,
    .actions-right {
      justify-content: center;
    }
  }
}
</style>