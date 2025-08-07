<template>
  <div class="analysis-container">
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
          <router-link to="/analysis" class="nav-item active">数据分析</router-link>
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
          <h1 class="page-title">数据分析报告</h1>
          <p class="page-subtitle">ESG评分深度分析与可视化展示</p>
        </div>

        <!-- 分析概览 -->
        <div class="analysis-overview slide-up" v-if="hasResults">
          <div class="overview-cards">
            <div class="overview-card glass-card hover-lift">
              <div class="card-icon">
                <el-icon><TrendCharts /></el-icon>
              </div>
              <div class="card-content">
                <div class="card-title">综合评分</div>
                <div class="card-value">{{ scoringResults?.total_score?.toFixed(1) || 0 }}</div>
                <div class="card-trend positive">+2.3 较上期</div>
              </div>
            </div>
            
            <div class="overview-card glass-card hover-lift">
              <div class="card-icon e-icon">
                <el-icon><Sunny /></el-icon>
              </div>
              <div class="card-content">
                <div class="card-title">环境评分</div>
                <div class="card-value">{{ scoringResults?.e_score?.toFixed(1) || 0 }}</div>
                <div class="card-trend positive">+1.8 较上期</div>
              </div>
            </div>
            
            <div class="overview-card glass-card hover-lift">
              <div class="card-icon s-icon">
                <el-icon><User /></el-icon>
              </div>
              <div class="card-content">
                <div class="card-title">社会评分</div>
                <div class="card-value">{{ scoringResults?.s_score?.toFixed(1) || 0 }}</div>
                <div class="card-trend negative">-0.5 较上期</div>
              </div>
            </div>
            
            <div class="overview-card glass-card hover-lift">
              <div class="card-icon g-icon">
                <el-icon><Setting /></el-icon>
              </div>
              <div class="card-content">
                <div class="card-title">治理评分</div>
                <div class="card-value">{{ scoringResults?.g_score?.toFixed(1) || 0 }}</div>
                <div class="card-trend positive">+3.2 较上期</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 图表分析 -->
        <div class="charts-section slide-up" v-if="hasResults">
          <div class="charts-grid">
            <!-- 雷达图 -->
            <div class="chart-card glass-card">
              <div class="chart-header">
                <h3 class="chart-title">
                  <el-icon><Radar /></el-icon>
                  ESG维度雷达图
                </h3>
                <div class="chart-actions">
                  <el-button size="small" @click="exportChart('radar')">
                    <el-icon><Download /></el-icon>
                  </el-button>
                </div>
              </div>
              <div class="chart-content">
                <v-chart :option="radarOption" style="height: 300px" />
              </div>
            </div>
            
            <!-- 柱状图 -->
            <div class="chart-card glass-card">
              <div class="chart-header">
                <h3 class="chart-title">
                  <el-icon><BarChart /></el-icon>
                  指标得分分布
                </h3>
                <div class="chart-actions">
                  <el-button size="small" @click="exportChart('bar')">
                    <el-icon><Download /></el-icon>
                  </el-button>
                </div>
              </div>
              <div class="chart-content">
                <v-chart :option="barOption" style="height: 300px" />
              </div>
            </div>
            
            <!-- 趋势图 -->
            <div class="chart-card glass-card">
              <div class="chart-header">
                <h3 class="chart-title">
                  <el-icon><LineChart /></el-icon>
                  历史趋势分析
                </h3>
                <div class="chart-actions">
                  <el-button size="small" @click="exportChart('line')">
                    <el-icon><Download /></el-icon>
                  </el-button>
                </div>
              </div>
              <div class="chart-content">
                <v-chart :option="lineOption" style="height: 300px" />
              </div>
            </div>
            
            <!-- 饼图 -->
            <div class="chart-card glass-card">
              <div class="chart-header">
                <h3 class="chart-title">
                  <el-icon><PieChart /></el-icon>
                  权重分布
                </h3>
                <div class="chart-actions">
                  <el-button size="small" @click="exportChart('pie')">
                    <el-icon><Download /></el-icon>
                  </el-button>
                </div>
              </div>
              <div class="chart-content">
                <v-chart :option="pieOption" style="height: 300px" />
              </div>
            </div>
          </div>
        </div>

        <!-- 详细分析 -->
        <div class="detailed-analysis slide-up" v-if="hasResults">
          <div class="analysis-tabs glass-card">
            <el-tabs v-model="activeAnalysisTab">
              <!-- 指标分析 -->
              <el-tab-pane label="指标分析" name="indicators">
                <div class="indicators-analysis">
                  <div class="dimension-analysis" v-for="dimension in ['E', 'S', 'G']" :key="dimension">
                    <h4 class="dimension-title">
                      <el-icon>
                        <Sunny v-if="dimension === 'E'" />
                        <User v-if="dimension === 'S'" />
                        <Setting v-if="dimension === 'G'" />
                      </el-icon>
                      {{ getDimensionName(dimension) }}指标详情
                    </h4>
                    
                    <el-table
                      :data="getIndicatorTableData(dimension)"
                      stripe
                      style="width: 100%"
                    >
                      <el-table-column prop="indicator" label="指标名称" width="300" />
                      <el-table-column prop="value" label="指标值" width="120">
                        <template #default="scope">
                          <span>{{ scope.row.value?.toFixed(2) || 0 }}</span>
                        </template>
                      </el-table-column>
                      <el-table-column prop="score" label="标准化得分" width="120">
                        <template #default="scope">
                          <el-tag
                            :type="getScoreType(scope.row.score)"
                            effect="light"
                          >
                            {{ scope.row.score?.toFixed(1) || 0 }}
                          </el-tag>
                        </template>
                      </el-table-column>
                      <el-table-column prop="weight" label="权重" width="100">
                        <template #default="scope">
                          <span>{{ (scope.row.weight * 100).toFixed(1) }}%</span>
                        </template>
                      </el-table-column>
                      <el-table-column prop="contribution" label="贡献度" width="120">
                        <template #default="scope">
                          <div class="contribution-bar">
                            <div
                              class="contribution-fill"
                              :style="{ width: scope.row.contribution + '%' }"
                            ></div>
                            <span class="contribution-text">{{ scope.row.contribution?.toFixed(1) || 0 }}%</span>
                          </div>
                        </template>
                      </el-table-column>
                    </el-table>
                  </div>
                </div>
              </el-tab-pane>
              
              <!-- 交叉项分析 -->
              <el-tab-pane label="交叉项分析" name="cross">
                <div class="cross-analysis">
                  <div class="cross-matrix">
                    <h4 class="section-title">维度交叉效应矩阵</h4>
                    <div class="matrix-grid">
                      <div class="matrix-item">
                        <div class="matrix-label">E × S</div>
                        <div class="matrix-value">{{ getCrossTermValue('E', 'S') }}</div>
                        <div class="matrix-desc">环境与社会协同效应</div>
                      </div>
                      <div class="matrix-item">
                        <div class="matrix-label">E × G</div>
                        <div class="matrix-value">{{ getCrossTermValue('E', 'G') }}</div>
                        <div class="matrix-desc">环境与治理协同效应</div>
                      </div>
                      <div class="matrix-item">
                        <div class="matrix-label">S × G</div>
                        <div class="matrix-value">{{ getCrossTermValue('S', 'G') }}</div>
                        <div class="matrix-desc">社会与治理协同效应</div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="cross-insights">
                    <h4 class="section-title">交叉项洞察</h4>
                    <div class="insights-list">
                      <div class="insight-item">
                        <el-icon class="insight-icon"><InfoFilled /></el-icon>
                        <div class="insight-content">
                          <div class="insight-title">环境-社会协同</div>
                          <div class="insight-desc">环境保护措施与社会责任表现呈现正相关，建议加强绿色供应链管理</div>
                        </div>
                      </div>
                      <div class="insight-item">
                        <el-icon class="insight-icon"><InfoFilled /></el-icon>
                        <div class="insight-content">
                          <div class="insight-title">治理-环境联动</div>
                          <div class="insight-desc">公司治理结构完善度直接影响环境管理效果，建议优化ESG治理架构</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </el-tab-pane>
              
              <!-- 事件影响 -->
              <el-tab-pane label="事件影响" name="events">
                <div class="events-analysis">
                  <div class="events-summary">
                    <h4 class="section-title">重大事件影响分析</h4>
                    <div class="events-stats">
                      <div class="stat-item">
                        <div class="stat-label">事件总数</div>
                        <div class="stat-value">{{ events.length }}</div>
                      </div>
                      <div class="stat-item">
                        <div class="stat-label">总体影响</div>
                        <div class="stat-value negative">-{{ getTotalEventImpact() }}</div>
                      </div>
                      <div class="stat-item">
                        <div class="stat-label">最大单项影响</div>
                        <div class="stat-value">-{{ getMaxEventImpact() }}</div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="events-list" v-if="events.length > 0">
                    <div
                      v-for="(event, index) in events"
                      :key="index"
                      class="event-analysis-item"
                    >
                      <div class="event-header">
                        <div class="event-type">{{ event.type }}</div>
                        <div class="event-severity">
                          <el-tag :type="getSeverityType(event.severity)">
                            严重度: {{ event.severity }}/10
                          </el-tag>
                        </div>
                      </div>
                      <div class="event-impact">
                        <div class="impact-label">评分影响:</div>
                        <div class="impact-value">-{{ calculateEventImpact(event) }}</div>
                      </div>
                      <div class="event-desc">{{ event.description || '暂无描述' }}</div>
                    </div>
                  </div>
                  
                  <div v-else class="no-events">
                    <el-empty description="暂无重大事件记录" />
                  </div>
                </div>
              </el-tab-pane>
              
              <!-- 改进建议 -->
              <el-tab-pane label="改进建议" name="suggestions">
                <div class="suggestions-analysis">
                  <div class="suggestions-grid">
                    <div class="suggestion-card" v-for="suggestion in suggestions" :key="suggestion.id">
                      <div class="suggestion-header">
                        <div class="suggestion-priority" :class="suggestion.priority">
                          {{ getPriorityText(suggestion.priority) }}
                        </div>
                        <div class="suggestion-dimension">{{ suggestion.dimension }}</div>
                      </div>
                      <div class="suggestion-title">{{ suggestion.title }}</div>
                      <div class="suggestion-desc">{{ suggestion.description }}</div>
                      <div class="suggestion-impact">
                        <span class="impact-label">预期提升:</span>
                        <span class="impact-value">+{{ suggestion.expectedImprovement }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>
        </div>

        <!-- 无数据状态 -->
        <div v-else class="no-data-state slide-up">
          <el-empty description="暂无分析数据">
            <el-button type="primary" @click="goToScoring">
              <el-icon><Operation /></el-icon>
              开始评分
            </el-button>
          </el-empty>
        </div>

        <!-- 操作按钮 -->
        <div class="analysis-actions glass-card" v-if="hasResults">
          <el-button type="primary" @click="exportAnalysis">
            <el-icon><Download /></el-icon>
            导出分析报告
          </el-button>
          <el-button @click="generateReport">
            <el-icon><Document /></el-icon>
            生成详细报告
          </el-button>
          <el-button @click="shareAnalysis">
            <el-icon><Share /></el-icon>
            分享分析
          </el-button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useESGStore } from '@/stores/esg'
import { ElMessage } from 'element-plus'
import VChart from 'vue-echarts'
import {
  TrendCharts, Sunny, User, Setting, Radar, BarChart, LineChart, PieChart,
  Download, InfoFilled, Operation, Document, Share
} from '@element-plus/icons-vue'

const router = useRouter()
const esgStore = useESGStore()

// 响应式数据
const activeAnalysisTab = ref('indicators')
const scoringResults = computed(() => esgStore.scoringResults)
const hasResults = computed(() => esgStore.hasResults)
const indicators = computed(() => esgStore.indicators)

// 模拟事件数据
const events = ref([
  {
    type: '数据泄露',
    severity: 7,
    impact: 15,
    description: '客户数据安全事件'
  },
  {
    type: '环境污染',
    severity: 5,
    impact: 10,
    description: '废水排放超标'
  }
])

// 改进建议数据
const suggestions = ref([
  {
    id: 1,
    dimension: '环境 (E)',
    priority: 'high',
    title: '提升可再生能源使用比例',
    description: '建议将可再生能源占比从当前30%提升至50%，可显著改善环境评分',
    expectedImprovement: '5.2'
  },
  {
    id: 2,
    dimension: '社会 (S)',
    priority: 'medium',
    title: '加强员工培训体系',
    description: '完善员工技能培训和职业发展规划，提升员工满意度和留存率',
    expectedImprovement: '3.8'
  },
  {
    id: 3,
    dimension: '治理 (G)',
    priority: 'high',
    title: '优化董事会结构',
    description: '增加独立董事比例，建立更完善的风险管控机制',
    expectedImprovement: '4.5'
  }
])

// 图表配置
const radarOption = computed(() => ({
  title: {
    text: 'ESG维度评分',
    left: 'center',
    textStyle: {
      fontSize: 14,
      color: '#666'
    }
  },
  radar: {
    indicator: [
      { name: '环境保护', max: 100 },
      { name: '社会责任', max: 100 },
      { name: '公司治理', max: 100 },
      { name: '创新发展', max: 100 },
      { name: '风险管控', max: 100 },
      { name: '透明度', max: 100 }
    ],
    radius: '60%'
  },
  series: [{
    type: 'radar',
    data: [{
      value: [
        scoringResults.value?.e_score || 0,
        scoringResults.value?.s_score || 0,
        scoringResults.value?.g_score || 0,
        85, 78, 82
      ],
      name: '当前评分',
      areaStyle: {
        color: 'rgba(102, 126, 234, 0.3)'
      },
      lineStyle: {
        color: '#667eea'
      }
    }]
  }]
}))

const barOption = computed(() => ({
  title: {
    text: '各维度得分对比',
    left: 'center',
    textStyle: {
      fontSize: 14,
      color: '#666'
    }
  },
  xAxis: {
    type: 'category',
    data: ['环境 (E)', '社会 (S)', '治理 (G)']
  },
  yAxis: {
    type: 'value',
    max: 100
  },
  series: [{
    type: 'bar',
    data: [
      {
        value: scoringResults.value?.e_score || 0,
        itemStyle: { color: '#52c41a' }
      },
      {
        value: scoringResults.value?.s_score || 0,
        itemStyle: { color: '#1890ff' }
      },
      {
        value: scoringResults.value?.g_score || 0,
        itemStyle: { color: '#722ed1' }
      }
    ],
    barWidth: '50%'
  }]
}))

const lineOption = computed(() => ({
  title: {
    text: 'ESG评分趋势',
    left: 'center',
    textStyle: {
      fontSize: 14,
      color: '#666'
    }
  },
  xAxis: {
    type: 'category',
    data: ['2020', '2021', '2022', '2023', '2024']
  },
  yAxis: {
    type: 'value',
    max: 100
  },
  series: [
    {
      name: '环境',
      type: 'line',
      data: [65, 70, 75, 78, scoringResults.value?.e_score || 80],
      smooth: true,
      lineStyle: { color: '#52c41a' }
    },
    {
      name: '社会',
      type: 'line',
      data: [72, 74, 76, 75, scoringResults.value?.s_score || 77],
      smooth: true,
      lineStyle: { color: '#1890ff' }
    },
    {
      name: '治理',
      type: 'line',
      data: [68, 72, 75, 80, scoringResults.value?.g_score || 82],
      smooth: true,
      lineStyle: { color: '#722ed1' }
    }
  ],
  legend: {
    bottom: 0
  }
}))

const pieOption = computed(() => ({
  title: {
    text: '权重分布',
    left: 'center',
    textStyle: {
      fontSize: 14,
      color: '#666'
    }
  },
  series: [{
    type: 'pie',
    radius: '60%',
    data: [
      { value: 40, name: '环境 (E)', itemStyle: { color: '#52c41a' } },
      { value: 30, name: '社会 (S)', itemStyle: { color: '#1890ff' } },
      { value: 30, name: '治理 (G)', itemStyle: { color: '#722ed1' } }
    ],
    emphasis: {
      itemStyle: {
        shadowBlur: 10,
        shadowOffsetX: 0,
        shadowColor: 'rgba(0, 0, 0, 0.5)'
      }
    }
  }]
}))

// 方法
const getDimensionName = (dimension) => {
  const names = {
    E: '环境',
    S: '社会',
    G: '治理'
  }
  return names[dimension]
}

const getIndicatorTableData = (dimension) => {
  const indicatorList = indicators.value[dimension]
  return indicatorList.map((indicator, index) => ({
    indicator,
    value: Math.random() * 100, // 模拟数据
    score: Math.random() * 100,
    weight: 1 / indicatorList.length,
    contribution: Math.random() * 20
  }))
}

const getScoreType = (score) => {
  if (score >= 80) return 'success'
  if (score >= 60) return 'warning'
  return 'danger'
}

const getCrossTermValue = (dim1, dim2) => {
  const score1 = scoringResults.value?.[`${dim1.toLowerCase()}_score`] || 0
  const score2 = scoringResults.value?.[`${dim2.toLowerCase()}_score`] || 0
  return ((score1 * score2) / 10000 * 0.1).toFixed(2)
}

const getTotalEventImpact = () => {
  return events.value.reduce((total, event) => total + calculateEventImpact(event), 0).toFixed(1)
}

const getMaxEventImpact = () => {
  if (events.value.length === 0) return '0'
  return Math.max(...events.value.map(event => calculateEventImpact(event))).toFixed(1)
}

const calculateEventImpact = (event) => {
  return (event.severity * event.impact / 100 * 2).toFixed(1)
}

const getSeverityType = (severity) => {
  if (severity >= 8) return 'danger'
  if (severity >= 5) return 'warning'
  return 'info'
}

const getPriorityText = (priority) => {
  const texts = {
    high: '高优先级',
    medium: '中优先级',
    low: '低优先级'
  }
  return texts[priority]
}

const exportChart = (type) => {
  ElMessage.info(`导出${type}图表功能开发中`)
}

const goToScoring = () => {
  router.push('/scoring')
}

const exportAnalysis = () => {
  ElMessage.info('导出分析报告功能开发中')
}

const generateReport = () => {
  router.push('/reports')
}

const shareAnalysis = () => {
  ElMessage.info('分享分析功能开发中')
}

onMounted(() => {
  // 页面加载时的初始化逻辑
})
</script>

<style lang="scss" scoped>
.analysis-container {
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

// 分析概览
.analysis-overview {
  margin-bottom: 40px;
  
  .overview-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 24px;
    
    .overview-card {
      padding: 24px;
      display: flex;
      align-items: center;
      gap: 16px;
      
      .card-icon {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        background: var(--gradient-primary);
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
      
      .card-content {
        flex: 1;
        
        .card-title {
          font-size: 14px;
          color: var(--text-secondary);
          margin-bottom: 4px;
        }
        
        .card-value {
          font-size: 28px;
          font-weight: 700;
          color: var(--text-primary);
          margin-bottom: 4px;
        }
        
        .card-trend {
          font-size: 12px;
          
          &.positive {
            color: #52c41a;
          }
          
          &.negative {
            color: #ff4d4f;
          }
        }
      }
    }
  }
}

// 图表区域
.charts-section {
  margin-bottom: 40px;
  
  .charts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 24px;
    
    .chart-card {
      padding: 24px;
      
      .chart-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        
        .chart-title {
          font-size: 18px;
          font-weight: 600;
          color: var(--text-primary);
          display: flex;
          align-items: center;
          gap: 8px;
        }
      }
      
      .chart-content {
        width: 100%;
      }
    }
  }
}

// 详细分析
.detailed-analysis {
  margin-bottom: 40px;
  
  .analysis-tabs {
    padding: 24px;
    
    :deep(.el-tabs__header) {
      margin-bottom: 24px;
    }
    
    :deep(.el-tabs__item) {
      font-size: 16px;
      font-weight: 500;
    }
  }
}

// 指标分析
.indicators-analysis {
  .dimension-analysis {
    margin-bottom: 40px;
    
    .dimension-title {
      font-size: 20px;
      font-weight: 600;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--text-primary);
    }
    
    .contribution-bar {
      position: relative;
      width: 100px;
      height: 20px;
      background: #f0f0f0;
      border-radius: 10px;
      overflow: hidden;
      
      .contribution-fill {
        height: 100%;
        background: var(--gradient-primary);
        transition: width 0.3s ease;
      }
      
      .contribution-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 12px;
        color: var(--text-primary);
        font-weight: 500;
      }
    }
  }
}

// 交叉项分析
.cross-analysis {
  .cross-matrix {
    margin-bottom: 40px;
    
    .section-title {
      font-size: 18px;
      font-weight: 600;
      margin-bottom: 20px;
      color: var(--text-primary);
    }
    
    .matrix-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px;
      
      .matrix-item {
        text-align: center;
        padding: 20px;
        background: #f8f9fa;
        border-radius: 8px;
        
        .matrix-label {
          font-size: 16px;
          font-weight: 600;
          color: var(--primary-color);
          margin-bottom: 8px;
        }
        
        .matrix-value {
          font-size: 24px;
          font-weight: 700;
          color: var(--text-primary);
          margin-bottom: 8px;
        }
        
        .matrix-desc {
          font-size: 12px;
          color: var(--text-secondary);
        }
      }
    }
  }
  
  .cross-insights {
    .insights-list {
      display: flex;
      flex-direction: column;
      gap: 16px;
      
      .insight-item {
        display: flex;
        gap: 12px;
        padding: 16px;
        background: #f8f9fa;
        border-radius: 8px;
        
        .insight-icon {
          color: var(--primary-color);
          font-size: 20px;
          margin-top: 2px;
        }
        
        .insight-content {
          flex: 1;
          
          .insight-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 4px;
            color: var(--text-primary);
          }
          
          .insight-desc {
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.5;
          }
        }
      }
    }
  }
}

// 事件分析
.events-analysis {
  .events-summary {
    margin-bottom: 24px;
    
    .section-title {
      font-size: 18px;
      font-weight: 600;
      margin-bottom: 16px;
      color: var(--text-primary);
    }
    
    .events-stats {
      display: flex;
      gap: 40px;
      
      .stat-item {
        text-align: center;
        
        .stat-label {
          font-size: 14px;
          color: var(--text-secondary);
          margin-bottom: 4px;
        }
        
        .stat-value {
          font-size: 24px;
          font-weight: 600;
          color: var(--text-primary);
          
          &.negative {
            color: #ff4d4f;
          }
        }
      }
    }
  }
  
  .events-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
    
    .event-analysis-item {
      padding: 20px;
      background: #f8f9fa;
      border-radius: 8px;
      
      .event-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        
        .event-type {
          font-size: 16px;
          font-weight: 600;
          color: var(--text-primary);
        }
      }
      
      .event-impact {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
        
        .impact-label {
          font-size: 14px;
          color: var(--text-secondary);
        }
        
        .impact-value {
          font-size: 16px;
          font-weight: 600;
          color: #ff4d4f;
        }
      }
      
      .event-desc {
        font-size: 14px;
        color: var(--text-secondary);
        line-height: 1.5;
      }
    }
  }
}

// 改进建议
.suggestions-analysis {
  .suggestions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    
    .suggestion-card {
      padding: 20px;
      background: #f8f9fa;
      border-radius: 8px;
      border-left: 4px solid var(--primary-color);
      
      .suggestion-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        
        .suggestion-priority {
          padding: 4px 8px;
          border-radius: 4px;
          font-size: 12px;
          font-weight: 500;
          
          &.high {
            background: #fff2e8;
            color: #fa541c;
          }
          
          &.medium {
            background: #fff7e6;
            color: #fa8c16;
          }
          
          &.low {
            background: #f6ffed;
            color: #52c41a;
          }
        }
        
        .suggestion-dimension {
          font-size: 12px;
          color: var(--text-secondary);
        }
      }
      
      .suggestion-title {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 8px;
        color: var(--text-primary);
      }
      
      .suggestion-desc {
        font-size: 14px;
        color: var(--text-secondary);
        line-height: 1.5;
        margin-bottom: 12px;
      }
      
      .suggestion-impact {
        display: flex;
        align-items: center;
        gap: 8px;
        
        .impact-label {
          font-size: 12px;
          color: var(--text-secondary);
        }
        
        .impact-value {
          font-size: 14px;
          font-weight: 600;
          color: #52c41a;
        }
      }
    }
  }
}

// 无数据状态
.no-data-state {
  text-align: center;
  padding: 80px 0;
}

// 操作按钮
.analysis-actions {
  padding: 20px;
  display: flex;
  justify-content: center;
  gap: 16px;
}

// 响应式设计
@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 20px;
  }
  
  .overview-cards {
    grid-template-columns: 1fr;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .suggestions-grid {
    grid-template-columns: 1fr;
  }
  
  .events-stats {
    flex-direction: column;
    gap: 16px;
  }
  
  .analysis-actions {
    flex-direction: column;
    align-items: center;
  }
}
</style>