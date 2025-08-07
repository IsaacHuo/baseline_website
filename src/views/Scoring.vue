<template>
  <div class="scoring-container">
    <!-- 导航栏 -->
    <nav class="navbar glass-card">
      <div class="nav-content">
        <div class="logo">
          <el-icon class="logo-icon"><TrendCharts /></el-icon>
          <span class="logo-text gradient-text">ESG评分系统</span>
        </div>
        <div class="nav-menu">
          <router-link to="/" class="nav-item">首页</router-link>
          <router-link to="/scoring" class="nav-item active">评分计算</router-link>
          <router-link to="/analysis" class="nav-item">数据分析</router-link>
          <router-link to="/reports" class="nav-item">报告管理</router-link>
          <router-link to="/settings" class="nav-item">系统设置</router-link>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <main class="main-content">
      <div class="content-wrapper">
        <!-- 页面标题 -->
        <div class="page-header fade-in">
          <h1 class="page-title">ESG评分计算</h1>
          <p class="page-subtitle">基于甲模型的企业ESG综合评分</p>
        </div>

        <!-- 评分步骤 -->
        <div class="scoring-steps slide-up">
          <el-steps :active="currentStep" align-center>
            <el-step title="企业信息" description="输入基本信息" />
            <el-step title="指标数据" description="录入ESG指标" />
            <el-step title="事件调整" description="添加重大事件" />
            <el-step title="参数配置" description="调整模型参数" />
            <el-step title="计算结果" description="查看评分结果" />
          </el-steps>
        </div>

        <!-- 步骤内容 -->
        <div class="step-content glass-card slide-up">
          <!-- 步骤1: 企业信息 -->
          <div v-if="currentStep === 0" class="step-panel">
            <h3 class="panel-title">
              <el-icon><OfficeBuilding /></el-icon>
              企业基本信息
            </h3>
            <el-form :model="companyForm" label-width="120px" class="company-form">
              <el-row :gutter="24">
                <el-col :span="12">
                  <el-form-item label="企业名称" required>
                    <el-input v-model="companyForm.name" placeholder="请输入企业名称" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="所属行业" required>
                    <el-select v-model="companyForm.industry" placeholder="请选择行业">
                      <el-option
                        v-for="industry in industries"
                        :key="industry"
                        :label="industry"
                        :value="industry"
                      />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="企业规模">
                    <el-select v-model="companyForm.scale" placeholder="请选择企业规模">
                      <el-option label="大型企业" value="large" />
                      <el-option label="中型企业" value="medium" />
                      <el-option label="小型企业" value="small" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="评估年度">
                    <el-date-picker
                      v-model="companyForm.year"
                      type="year"
                      placeholder="选择评估年度"
                      style="width: 100%"
                    />
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
          </div>

          <!-- 步骤2: 指标数据 -->
          <div v-if="currentStep === 1" class="step-panel">
            <div class="panel-header">
              <h3 class="panel-title">
                <el-icon><DataAnalysis /></el-icon>
                ESG指标数据录入
              </h3>
              <div class="panel-actions">
                <el-button @click="importData">
                  <el-icon><Upload /></el-icon>
                  导入数据
                </el-button>
                <el-button @click="downloadTemplate">
                  <el-icon><Download /></el-icon>
                  下载模板
                </el-button>
              </div>
            </div>
            
            <el-tabs v-model="activeTab" class="indicator-tabs">
              <!-- 环境指标 -->
              <el-tab-pane label="环境指标 (E)" name="E">
                <div class="indicator-grid">
                  <div
                    v-for="(indicator, index) in indicators.E"
                    :key="indicator"
                    class="indicator-item"
                  >
                    <label class="indicator-label">{{ indicator }}</label>
                    <el-input-number
                      v-model="indicatorData.E[index]"
                      :precision="2"
                      :min="0"
                      :max="100"
                      placeholder="请输入数值"
                      style="width: 100%"
                    />
                  </div>
                </div>
              </el-tab-pane>
              
              <!-- 社会指标 -->
              <el-tab-pane label="社会指标 (S)" name="S">
                <div class="indicator-grid">
                  <div
                    v-for="(indicator, index) in indicators.S"
                    :key="indicator"
                    class="indicator-item"
                  >
                    <label class="indicator-label">{{ indicator }}</label>
                    <el-input-number
                      v-model="indicatorData.S[index]"
                      :precision="2"
                      :min="0"
                      :max="100"
                      placeholder="请输入数值"
                      style="width: 100%"
                    />
                  </div>
                </div>
              </el-tab-pane>
              
              <!-- 治理指标 -->
              <el-tab-pane label="治理指标 (G)" name="G">
                <div class="indicator-grid">
                  <div
                    v-for="(indicator, index) in indicators.G"
                    :key="indicator"
                    class="indicator-item"
                  >
                    <label class="indicator-label">{{ indicator }}</label>
                    <el-input-number
                      v-model="indicatorData.G[index]"
                      :precision="2"
                      :min="0"
                      :max="100"
                      placeholder="请输入数值"
                      style="width: 100%"
                    />
                  </div>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>

          <!-- 步骤3: 事件调整 -->
          <div v-if="currentStep === 2" class="step-panel">
            <div class="panel-header">
              <h3 class="panel-title">
                <el-icon><Warning /></el-icon>
                重大事件调整
              </h3>
              <el-button type="primary" @click="addEvent">
                <el-icon><Plus /></el-icon>
                添加事件
              </el-button>
            </div>
            
            <div v-if="events.length === 0" class="empty-state">
              <el-empty description="暂无重大事件">
                <el-button type="primary" @click="addEvent">添加第一个事件</el-button>
              </el-empty>
            </div>
            
            <div v-else class="events-list">
              <div
                v-for="(event, index) in events"
                :key="index"
                class="event-item glass-card"
              >
                <div class="event-header">
                  <h4 class="event-title">事件 {{ index + 1 }}</h4>
                  <el-button
                    type="danger"
                    size="small"
                    @click="removeEvent(index)"
                    circle
                  >
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
                <el-form :model="event" label-width="100px">
                  <el-row :gutter="16">
                    <el-col :span="8">
                      <el-form-item label="事件类型">
                        <el-select v-model="event.type" placeholder="选择事件类型">
                          <el-option label="数据泄露" value="数据泄露" />
                          <el-option label="环境污染" value="环境污染" />
                          <el-option label="工伤事故" value="工伤事故" />
                          <el-option label="财务舞弊" value="财务舞弊" />
                          <el-option label="劳动纠纷" value="劳动纠纷" />
                          <el-option label="产品召回" value="产品召回" />
                        </el-select>
                      </el-form-item>
                    </el-col>
                    <el-col :span="8">
                      <el-form-item label="严重程度">
                        <el-slider
                          v-model="event.severity"
                          :min="1"
                          :max="10"
                          show-stops
                          show-tooltip
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :span="8">
                      <el-form-item label="影响范围">
                        <el-input-number
                          v-model="event.impact"
                          :min="0"
                          :max="100"
                          placeholder="影响范围"
                          style="width: 100%"
                        />
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <el-form-item label="事件描述">
                    <el-input
                      v-model="event.description"
                      type="textarea"
                      :rows="2"
                      placeholder="请描述事件详情"
                    />
                  </el-form-item>
                </el-form>
              </div>
            </div>
          </div>

          <!-- 步骤4: 参数配置 -->
          <div v-if="currentStep === 3" class="step-panel">
            <h3 class="panel-title">
              <el-icon><Setting /></el-icon>
              模型参数配置
            </h3>
            
            <el-tabs class="param-tabs">
              <el-tab-pane label="权重配置" name="weights">
                <el-form label-width="150px" class="param-form">
                  <el-form-item label="主观权重系数 (α)">
                    <el-slider
                      v-model="modelParams.alpha"
                      :min="0"
                      :max="1"
                      :step="0.1"
                      show-input
                    />
                  </el-form-item>
                  <el-form-item label="环境权重 (E)">
                    <el-slider
                      v-model="modelParams.e_weight"
                      :min="0"
                      :max="1"
                      :step="0.1"
                      show-input
                    />
                  </el-form-item>
                  <el-form-item label="社会权重 (S)">
                    <el-slider
                      v-model="modelParams.s_weight"
                      :min="0"
                      :max="1"
                      :step="0.1"
                      show-input
                    />
                  </el-form-item>
                  <el-form-item label="治理权重 (G)">
                    <el-slider
                      v-model="modelParams.g_weight"
                      :min="0"
                      :max="1"
                      :step="0.1"
                      show-input
                    />
                  </el-form-item>
                </el-form>
              </el-tab-pane>
              
              <el-tab-pane label="交叉项系数" name="cross">
                <el-form label-width="150px" class="param-form">
                  <el-form-item label="E×S系数 (δ)">
                    <el-slider
                      v-model="modelParams.delta_coeff"
                      :min="0"
                      :max="0.5"
                      :step="0.01"
                      show-input
                    />
                  </el-form-item>
                  <el-form-item label="E×G系数 (ε)">
                    <el-slider
                      v-model="modelParams.epsilon_coeff"
                      :min="0"
                      :max="0.5"
                      :step="0.01"
                      show-input
                    />
                  </el-form-item>
                  <el-form-item label="S×G系数 (ζ)">
                    <el-slider
                      v-model="modelParams.zeta_coeff"
                      :min="0"
                      :max="0.5"
                      :step="0.01"
                      show-input
                    />
                  </el-form-item>
                </el-form>
              </el-tab-pane>
              
              <el-tab-pane label="非线性调整" name="nonlinear">
                <el-form label-width="150px" class="param-form">
                  <el-form-item label="严重度因子 (β)">
                    <el-slider
                      v-model="modelParams.severity_factor"
                      :min="0"
                      :max="1"
                      :step="0.1"
                      show-input
                    />
                  </el-form-item>
                  <el-form-item label="最大加分值">
                    <el-slider
                      v-model="modelParams.max_bonus"
                      :min="0"
                      :max="20"
                      :step="1"
                      show-input
                    />
                  </el-form-item>
                  <el-form-item label="奖励曲线陡度">
                    <el-slider
                      v-model="modelParams.bonus_steepness"
                      :min="0.1"
                      :max="2"
                      :step="0.1"
                      show-input
                    />
                  </el-form-item>
                </el-form>
              </el-tab-pane>
            </el-tabs>
          </div>

          <!-- 步骤5: 计算结果 -->
          <div v-if="currentStep === 4" class="step-panel">
            <div class="results-container" v-if="scoringResults">
              <div class="score-overview">
                <div class="main-score">
                  <div class="score-circle">
                    <div class="score-value">{{ scoringResults.total_score?.toFixed(1) || 0 }}</div>
                    <div class="score-label">ESG综合评分</div>
                  </div>
                  <div class="score-grade">
                    <span class="grade-text">{{ getScoreGrade(scoringResults.total_score) }}</span>
                  </div>
                </div>
                
                <div class="dimension-scores">
                  <div class="dimension-item">
                    <div class="dimension-icon e-icon">
                      <el-icon><Sunny /></el-icon>
                    </div>
                    <div class="dimension-info">
                      <div class="dimension-name">环境 (E)</div>
                      <div class="dimension-score">{{ scoringResults.e_score?.toFixed(1) || 0 }}</div>
                    </div>
                  </div>
                  
                  <div class="dimension-item">
                    <div class="dimension-icon s-icon">
                      <el-icon><User /></el-icon>
                    </div>
                    <div class="dimension-info">
                      <div class="dimension-name">社会 (S)</div>
                      <div class="dimension-score">{{ scoringResults.s_score?.toFixed(1) || 0 }}</div>
                    </div>
                  </div>
                  
                  <div class="dimension-item">
                    <div class="dimension-icon g-icon">
                      <el-icon><Setting /></el-icon>
                    </div>
                    <div class="dimension-info">
                      <div class="dimension-name">治理 (G)</div>
                      <div class="dimension-score">{{ scoringResults.g_score?.toFixed(1) || 0 }}</div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="results-actions">
                <el-button type="primary" @click="generateReport">
                  <el-icon><Document /></el-icon>
                  生成报告
                </el-button>
                <el-button @click="exportResults">
                  <el-icon><Download /></el-icon>
                  导出结果
                </el-button>
                <el-button @click="viewAnalysis">
                  <el-icon><DataAnalysis /></el-icon>
                  查看分析
                </el-button>
              </div>
            </div>
            
            <div v-else class="no-results">
              <el-empty description="暂无计算结果">
                <el-button type="primary" @click="calculateScore">开始计算</el-button>
              </el-empty>
            </div>
          </div>
        </div>

        <!-- 步骤导航 -->
        <div class="step-navigation glass-card">
          <el-button
            :disabled="currentStep === 0"
            @click="prevStep"
          >
            <el-icon><ArrowLeft /></el-icon>
            上一步
          </el-button>
          
          <el-button
            v-if="currentStep < 4"
            type="primary"
            @click="nextStep"
            :disabled="!canProceed"
          >
            下一步
            <el-icon><ArrowRight /></el-icon>
          </el-button>
          
          <el-button
            v-if="currentStep === 3"
            type="success"
            @click="calculateScore"
            :loading="loading"
          >
            <el-icon><Operation /></el-icon>
            开始计算
          </el-button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useESGStore } from '@/stores/esg'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  TrendCharts, OfficeBuilding, DataAnalysis, Upload, Download,
  Warning, Plus, Delete, Setting, Sunny, User, Document,
  ArrowLeft, ArrowRight, Operation
} from '@element-plus/icons-vue'

const router = useRouter()
const esgStore = useESGStore()

// 响应式数据
const currentStep = ref(0)
const activeTab = ref('E')
const loading = computed(() => esgStore.loading)
const indicators = computed(() => esgStore.indicators)
const industries = computed(() => esgStore.industries)
const scoringResults = computed(() => esgStore.scoringResults)

// 表单数据
const companyForm = reactive({
  name: '',
  industry: '',
  scale: '',
  year: new Date()
})

// 指标数据
const indicatorData = reactive({
  E: new Array(indicators.value.E.length).fill(0),
  S: new Array(indicators.value.S.length).fill(0),
  G: new Array(indicators.value.G.length).fill(0)
})

// 事件数据
const events = ref([])

// 模型参数
const modelParams = reactive({ ...esgStore.modelParams })

// 计算属性
const canProceed = computed(() => {
  switch (currentStep.value) {
    case 0:
      return companyForm.name && companyForm.industry
    case 1:
      return true // 指标数据可以为空
    case 2:
      return true // 事件可以为空
    case 3:
      return true
    default:
      return false
  }
})

// 方法
const nextStep = () => {
  if (currentStep.value < 4) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const addEvent = () => {
  events.value.push({
    type: '',
    severity: 5,
    impact: 0,
    description: ''
  })
}

const removeEvent = (index) => {
  events.value.splice(index, 1)
}

const importData = () => {
  // 实现数据导入逻辑
  ElMessage.info('数据导入功能开发中')
}

const downloadTemplate = () => {
  // 实现模板下载逻辑
  ElMessage.info('模板下载功能开发中')
}

const calculateScore = async () => {
  try {
    // 准备计算数据
    const companyData = {
      company_name: companyForm.name,
      industry: companyForm.industry,
      indicators: indicatorData
    }
    
    // 调用评分计算
    await esgStore.calculateESGScore(companyData, events.value)
    
    // 跳转到结果页面
    currentStep.value = 4
    
    ElMessage.success('ESG评分计算完成')
  } catch (error) {
    ElMessage.error('计算失败: ' + error.message)
  }
}

const getScoreGrade = (score) => {
  if (score >= 90) return 'AAA'
  if (score >= 80) return 'AA'
  if (score >= 70) return 'A'
  if (score >= 60) return 'BBB'
  if (score >= 50) return 'BB'
  if (score >= 40) return 'B'
  return 'C'
}

const generateReport = () => {
  router.push('/reports')
}

const exportResults = () => {
  ElMessage.info('结果导出功能开发中')
}

const viewAnalysis = () => {
  router.push('/analysis')
}
</script>

<style lang="scss" scoped>
.scoring-container {
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
  max-width: 1200px;
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

.scoring-steps {
  margin-bottom: 40px;
  
  :deep(.el-steps) {
    .el-step__title {
      color: var(--text-secondary);
      
      &.is-process {
        color: var(--text-primary);
        font-weight: 600;
      }
    }
    
    .el-step__description {
      color: var(--text-tertiary);
    }
    
    .el-step__icon {
      border-color: var(--border-color);
      color: var(--text-tertiary);
      
      &.is-process {
        border-color: var(--primary-color);
        color: #ffffff;
        background: var(--primary-color);
      }
    }
    
    .el-step__line {
      background: var(--border-color);
    }
  }
}

.step-content {
  padding: 40px;
  margin-bottom: 24px;
  min-height: 500px;
}

.step-panel {
  .panel-title {
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--text-primary);
  }
  
  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    
    .panel-actions {
      display: flex;
      gap: 12px;
    }
  }
}

.company-form {
  .el-form-item {
    margin-bottom: 24px;
  }
}

.indicator-tabs {
  :deep(.el-tabs__header) {
    margin-bottom: 24px;
  }
  
  :deep(.el-tabs__item) {
    font-size: 16px;
    font-weight: 500;
  }
}

.indicator-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  
  .indicator-item {
    .indicator-label {
      display: block;
      margin-bottom: 8px;
      font-weight: 500;
      color: var(--text-primary);
    }
  }
}

.empty-state {
  text-align: center;
  padding: 60px 0;
}

.events-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  
  .event-item {
    padding: 24px;
    
    .event-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      
      .event-title {
        font-size: 18px;
        font-weight: 600;
        color: var(--text-primary);
      }
    }
  }
}

.param-tabs {
  .param-form {
    max-width: 600px;
    
    .el-form-item {
      margin-bottom: 32px;
    }
  }
}

.results-container {
  .score-overview {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 40px;
    
    .main-score {
      text-align: center;
      
      .score-circle {
          width: 200px;
          height: 200px;
          border-radius: 50%;
          background: var(--primary-color);
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          margin-bottom: 16px;
          border: 4px solid var(--border-color);
          
          .score-value {
            font-size: 48px;
            font-weight: 700;
            color: #ffffff;
            line-height: 1;
          }
          
          .score-label {
            font-size: 14px;
            color: rgba(255, 255, 255, 0.9);
            margin-top: 8px;
          }
        }
      
      .score-grade {
        .grade-text {
          font-size: 24px;
          font-weight: 600;
          color: var(--primary-color);
        }
      }
    }
    
    .dimension-scores {
      display: flex;
      flex-direction: column;
      gap: 24px;
      
      .dimension-item {
        display: flex;
        align-items: center;
        gap: 16px;
        
        .dimension-icon {
          width: 48px;
          height: 48px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          
          .el-icon {
            font-size: 24px;
            color: white;
          }
          
          &.e-icon {
            background: #52c41a;
          }
          
          &.s-icon {
            background: #1890ff;
          }
          
          &.g-icon {
            background: #722ed1;
          }
        }
        
        .dimension-info {
          .dimension-name {
            font-size: 16px;
            color: var(--text-secondary);
            margin-bottom: 4px;
          }
          
          .dimension-score {
            font-size: 24px;
            font-weight: 600;
            color: var(--text-primary);
          }
        }
      }
    }
  }
  
  .results-actions {
    display: flex;
    justify-content: center;
    gap: 16px;
  }
}

.no-results {
  text-align: center;
  padding: 60px 0;
}

.step-navigation {
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

// 响应式设计
@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 20px;
  }
  
  .step-content {
    padding: 24px;
  }
  
  .indicator-grid {
    grid-template-columns: 1fr;
  }
  
  .score-overview {
    flex-direction: column;
    gap: 40px;
    
    .dimension-scores {
      flex-direction: row;
      justify-content: space-around;
    }
  }
  
  .step-navigation {
    flex-direction: column;
    gap: 16px;
  }
}
</style>