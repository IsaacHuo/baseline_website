<template>
  <div class="reports-container">
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
          <router-link to="/reports" class="nav-item active">报告管理</router-link>
          <router-link to="/settings" class="nav-item">系统设置</router-link>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <main class="main-content">
      <div class="content-wrapper">
        <!-- 页面标题 -->
        <div class="page-header fade-in">
          <h1 class="page-title">报告管理</h1>
          <p class="page-subtitle">管理和查看历史ESG评分报告</p>
        </div>

        <!-- 工具栏 -->
        <div class="toolbar glass-card slide-up">
          <div class="toolbar-left">
            <el-input
              v-model="searchQuery"
              placeholder="搜索报告..."
              prefix-icon="Search"
              style="width: 300px"
              clearable
            />
            <el-select
              v-model="filterStatus"
              placeholder="状态筛选"
              style="width: 150px"
              clearable
            >
              <el-option label="全部" value="" />
              <el-option label="已完成" value="completed" />
              <el-option label="处理中" value="processing" />
              <el-option label="草稿" value="draft" />
            </el-select>
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            />
          </div>
          <div class="toolbar-right">
            <el-button type="primary" @click="createNewReport">
              <el-icon><Plus /></el-icon>
              新建报告
            </el-button>
            <el-button @click="exportReports">
              <el-icon><Download /></el-icon>
              批量导出
            </el-button>
            <el-button @click="refreshReports">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </div>

        <!-- 报告统计 -->
        <div class="reports-stats slide-up">
          <div class="stats-grid">
            <div class="stat-card glass-card hover-lift">
              <div class="stat-icon">
                <el-icon><Document /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ totalReports }}</div>
                <div class="stat-label">总报告数</div>
              </div>
            </div>
            
            <div class="stat-card glass-card hover-lift">
              <div class="stat-icon completed">
                <el-icon><CircleCheck /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ completedReports }}</div>
                <div class="stat-label">已完成</div>
              </div>
            </div>
            
            <div class="stat-card glass-card hover-lift">
              <div class="stat-icon processing">
                <el-icon><Loading /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ processingReports }}</div>
                <div class="stat-label">处理中</div>
              </div>
            </div>
            
            <div class="stat-card glass-card hover-lift">
              <div class="stat-icon draft">
                <el-icon><Edit /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ draftReports }}</div>
                <div class="stat-label">草稿</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 报告列表 -->
        <div class="reports-list slide-up">
          <div class="list-header glass-card">
            <div class="view-controls">
              <el-radio-group v-model="viewMode" size="small">
                <el-radio-button label="grid">
                  <el-icon><Grid /></el-icon>
                  卡片视图
                </el-radio-button>
                <el-radio-button label="table">
                  <el-icon><List /></el-icon>
                  列表视图
                </el-radio-button>
              </el-radio-group>
            </div>
            <div class="sort-controls">
              <el-select v-model="sortBy" size="small" style="width: 120px">
                <el-option label="创建时间" value="created_at" />
                <el-option label="更新时间" value="updated_at" />
                <el-option label="公司名称" value="company" />
                <el-option label="评分" value="score" />
              </el-select>
              <el-button
                size="small"
                @click="toggleSortOrder"
                :icon="sortOrder === 'desc' ? 'ArrowDown' : 'ArrowUp'"
              />
            </div>
          </div>

          <!-- 卡片视图 -->
          <div v-if="viewMode === 'grid'" class="reports-grid">
            <div
              v-for="report in filteredReports"
              :key="report.id"
              class="report-card glass-card hover-lift"
              @click="viewReport(report)"
            >
              <div class="card-header">
                <div class="company-info">
                  <div class="company-name">{{ report.company }}</div>
                  <div class="report-type">{{ report.type }}</div>
                </div>
                <div class="report-status">
                  <el-tag :type="getStatusType(report.status)" size="small">
                    {{ getStatusText(report.status) }}
                  </el-tag>
                </div>
              </div>
              
              <div class="card-content">
                <div class="score-display">
                  <div class="score-circle" :class="getScoreLevel(report.score)">
                    <span class="score-value">{{ report.score }}</span>
                  </div>
                  <div class="score-breakdown">
                    <div class="score-item">
                      <span class="score-label">E</span>
                      <span class="score-val">{{ report.e_score }}</span>
                    </div>
                    <div class="score-item">
                      <span class="score-label">S</span>
                      <span class="score-val">{{ report.s_score }}</span>
                    </div>
                    <div class="score-item">
                      <span class="score-label">G</span>
                      <span class="score-val">{{ report.g_score }}</span>
                    </div>
                  </div>
                </div>
                
                <div class="report-meta">
                  <div class="meta-item">
                    <el-icon><Calendar /></el-icon>
                    <span>{{ formatDate(report.created_at) }}</span>
                  </div>
                  <div class="meta-item">
                    <el-icon><User /></el-icon>
                    <span>{{ report.creator }}</span>
                  </div>
                </div>
              </div>
              
              <div class="card-actions">
                <el-button size="small" type="primary" @click.stop="viewReport(report)">
                  <el-icon><View /></el-icon>
                  查看
                </el-button>
                <el-button size="small" @click.stop="downloadReport(report)">
                  <el-icon><Download /></el-icon>
                  下载
                </el-button>
                <el-dropdown @command="handleAction" trigger="click" @click.stop>
                  <el-button size="small">
                    <el-icon><More /></el-icon>
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item :command="{action: 'edit', report}">
                        <el-icon><Edit /></el-icon>
                        编辑
                      </el-dropdown-item>
                      <el-dropdown-item :command="{action: 'duplicate', report}">
                        <el-icon><CopyDocument /></el-icon>
                        复制
                      </el-dropdown-item>
                      <el-dropdown-item :command="{action: 'share', report}">
                        <el-icon><Share /></el-icon>
                        分享
                      </el-dropdown-item>
                      <el-dropdown-item :command="{action: 'delete', report}" divided>
                        <el-icon><Delete /></el-icon>
                        删除
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
          </div>

          <!-- 表格视图 -->
          <div v-else class="reports-table glass-card">
            <el-table
              :data="filteredReports"
              style="width: 100%"
              @row-click="viewReport"
              row-class-name="table-row"
            >
              <el-table-column prop="company" label="公司名称" width="200">
                <template #default="scope">
                  <div class="company-cell">
                    <div class="company-name">{{ scope.row.company }}</div>
                    <div class="company-industry">{{ scope.row.industry }}</div>
                  </div>
                </template>
              </el-table-column>
              
              <el-table-column prop="type" label="报告类型" width="120" />
              
              <el-table-column prop="score" label="综合评分" width="100" align="center">
                <template #default="scope">
                  <el-tag :type="getScoreTagType(scope.row.score)" effect="light">
                    {{ scope.row.score }}
                  </el-tag>
                </template>
              </el-table-column>
              
              <el-table-column label="ESG评分" width="150" align="center">
                <template #default="scope">
                  <div class="esg-scores">
                    <span class="esg-item e">E: {{ scope.row.e_score }}</span>
                    <span class="esg-item s">S: {{ scope.row.s_score }}</span>
                    <span class="esg-item g">G: {{ scope.row.g_score }}</span>
                  </div>
                </template>
              </el-table-column>
              
              <el-table-column prop="status" label="状态" width="100" align="center">
                <template #default="scope">
                  <el-tag :type="getStatusType(scope.row.status)" size="small">
                    {{ getStatusText(scope.row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              
              <el-table-column prop="created_at" label="创建时间" width="120">
                <template #default="scope">
                  {{ formatDate(scope.row.created_at) }}
                </template>
              </el-table-column>
              
              <el-table-column prop="creator" label="创建者" width="100" />
              
              <el-table-column label="操作" width="200" align="center">
                <template #default="scope">
                  <div class="table-actions">
                    <el-button size="small" type="primary" @click.stop="viewReport(scope.row)">
                      查看
                    </el-button>
                    <el-button size="small" @click.stop="downloadReport(scope.row)">
                      下载
                    </el-button>
                    <el-dropdown @command="handleAction" trigger="click" @click.stop>
                      <el-button size="small">
                        <el-icon><More /></el-icon>
                      </el-button>
                      <template #dropdown>
                        <el-dropdown-menu>
                          <el-dropdown-item :command="{action: 'edit', report: scope.row}">
                            编辑
                          </el-dropdown-item>
                          <el-dropdown-item :command="{action: 'duplicate', report: scope.row}">
                            复制
                          </el-dropdown-item>
                          <el-dropdown-item :command="{action: 'share', report: scope.row}">
                            分享
                          </el-dropdown-item>
                          <el-dropdown-item :command="{action: 'delete', report: scope.row}" divided>
                            删除
                          </el-dropdown-item>
                        </el-dropdown-menu>
                      </template>
                    </el-dropdown>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </div>

          <!-- 分页 -->
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[10, 20, 50, 100]"
              :total="totalReports"
              layout="total, sizes, prev, pager, next, jumper"
              background
            />
          </div>
        </div>

        <!-- 空状态 -->
        <div v-if="filteredReports.length === 0" class="empty-state slide-up">
          <el-empty description="暂无报告数据">
            <el-button type="primary" @click="createNewReport">
              <el-icon><Plus /></el-icon>
              创建第一个报告
            </el-button>
          </el-empty>
        </div>
      </div>
    </main>

    <!-- 报告详情对话框 -->
    <el-dialog
      v-model="reportDialogVisible"
      :title="selectedReport?.company + ' - ESG评分报告'"
      width="80%"
      top="5vh"
    >
      <div v-if="selectedReport" class="report-detail">
        <div class="detail-header">
          <div class="company-info">
            <h3>{{ selectedReport.company }}</h3>
            <p>{{ selectedReport.industry }} | {{ selectedReport.type }}</p>
          </div>
          <div class="score-summary">
            <div class="total-score">
              <div class="score-label">综合评分</div>
              <div class="score-value">{{ selectedReport.score }}</div>
            </div>
            <div class="dimension-scores">
              <div class="dimension-item">
                <div class="dimension-label">环境 (E)</div>
                <div class="dimension-value">{{ selectedReport.e_score }}</div>
              </div>
              <div class="dimension-item">
                <div class="dimension-label">社会 (S)</div>
                <div class="dimension-value">{{ selectedReport.s_score }}</div>
              </div>
              <div class="dimension-item">
                <div class="dimension-label">治理 (G)</div>
                <div class="dimension-value">{{ selectedReport.g_score }}</div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="detail-content">
          <el-tabs>
            <el-tab-pane label="评分详情" name="scores">
              <div class="scores-detail">
                <p>详细的评分分析和指标数据...</p>
              </div>
            </el-tab-pane>
            <el-tab-pane label="分析报告" name="analysis">
              <div class="analysis-detail">
                <p>深度分析和改进建议...</p>
              </div>
            </el-tab-pane>
            <el-tab-pane label="历史对比" name="history">
              <div class="history-detail">
                <p>历史评分趋势和对比分析...</p>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="reportDialogVisible = false">关闭</el-button>
          <el-button type="primary" @click="downloadReport(selectedReport)">
            <el-icon><Download /></el-icon>
            下载报告
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useESGStore } from '@/stores/esg'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  TrendCharts, Plus, Download, Refresh, Document, CircleCheck, Loading, Edit,
  Grid, List, Calendar, User, View, More, CopyDocument, Share, Delete
} from '@element-plus/icons-vue'

const router = useRouter()
const esgStore = useESGStore()

// 响应式数据
const searchQuery = ref('')
const filterStatus = ref('')
const dateRange = ref([])
const viewMode = ref('grid')
const sortBy = ref('created_at')
const sortOrder = ref('desc')
const currentPage = ref(1)
const pageSize = ref(20)
const reportDialogVisible = ref(false)
const selectedReport = ref(null)

// 模拟报告数据
const reports = ref([
  {
    id: 1,
    company: '阿里巴巴集团',
    industry: '互联网科技',
    type: '年度报告',
    score: 85.2,
    e_score: 82.5,
    s_score: 88.0,
    g_score: 85.1,
    status: 'completed',
    created_at: '2024-01-15',
    updated_at: '2024-01-20',
    creator: '张三'
  },
  {
    id: 2,
    company: '腾讯控股',
    industry: '互联网科技',
    type: '季度报告',
    score: 78.9,
    e_score: 75.2,
    s_score: 82.1,
    g_score: 79.4,
    status: 'processing',
    created_at: '2024-01-10',
    updated_at: '2024-01-18',
    creator: '李四'
  },
  {
    id: 3,
    company: '中国平安',
    industry: '金融保险',
    type: '专项报告',
    score: 91.3,
    e_score: 89.7,
    s_score: 93.2,
    g_score: 91.0,
    status: 'completed',
    created_at: '2024-01-05',
    updated_at: '2024-01-12',
    creator: '王五'
  },
  {
    id: 4,
    company: '比亚迪股份',
    industry: '新能源汽车',
    type: '年度报告',
    score: 88.7,
    e_score: 95.3,
    s_score: 84.1,
    g_score: 86.7,
    status: 'draft',
    created_at: '2024-01-01',
    updated_at: '2024-01-08',
    creator: '赵六'
  }
])

// 计算属性
const totalReports = computed(() => reports.value.length)
const completedReports = computed(() => reports.value.filter(r => r.status === 'completed').length)
const processingReports = computed(() => reports.value.filter(r => r.status === 'processing').length)
const draftReports = computed(() => reports.value.filter(r => r.status === 'draft').length)

const filteredReports = computed(() => {
  let filtered = reports.value
  
  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(report => 
      report.company.toLowerCase().includes(query) ||
      report.industry.toLowerCase().includes(query) ||
      report.type.toLowerCase().includes(query)
    )
  }
  
  // 状态过滤
  if (filterStatus.value) {
    filtered = filtered.filter(report => report.status === filterStatus.value)
  }
  
  // 日期范围过滤
  if (dateRange.value && dateRange.value.length === 2) {
    const [startDate, endDate] = dateRange.value
    filtered = filtered.filter(report => {
      const reportDate = new Date(report.created_at)
      return reportDate >= new Date(startDate) && reportDate <= new Date(endDate)
    })
  }
  
  // 排序
  filtered.sort((a, b) => {
    const aVal = a[sortBy.value]
    const bVal = b[sortBy.value]
    const order = sortOrder.value === 'desc' ? -1 : 1
    
    if (typeof aVal === 'string') {
      return aVal.localeCompare(bVal) * order
    }
    return (aVal - bVal) * order
  })
  
  return filtered
})

// 方法
const getStatusType = (status) => {
  const types = {
    completed: 'success',
    processing: 'warning',
    draft: 'info'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    completed: '已完成',
    processing: '处理中',
    draft: '草稿'
  }
  return texts[status] || '未知'
}

const getScoreLevel = (score) => {
  if (score >= 90) return 'excellent'
  if (score >= 80) return 'good'
  if (score >= 70) return 'average'
  return 'poor'
}

const getScoreTagType = (score) => {
  if (score >= 90) return 'success'
  if (score >= 80) return ''
  if (score >= 70) return 'warning'
  return 'danger'
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

const toggleSortOrder = () => {
  sortOrder.value = sortOrder.value === 'desc' ? 'asc' : 'desc'
}

const createNewReport = () => {
  router.push('/scoring')
}

const exportReports = () => {
  ElMessage.info('批量导出功能开发中')
}

const refreshReports = () => {
  ElMessage.success('报告列表已刷新')
}

const viewReport = (report) => {
  selectedReport.value = report
  reportDialogVisible.value = true
}

const downloadReport = (report) => {
  ElMessage.info(`下载报告: ${report.company}`)
}

const handleAction = ({ action, report }) => {
  switch (action) {
    case 'edit':
      ElMessage.info(`编辑报告: ${report.company}`)
      break
    case 'duplicate':
      ElMessage.info(`复制报告: ${report.company}`)
      break
    case 'share':
      ElMessage.info(`分享报告: ${report.company}`)
      break
    case 'delete':
      ElMessageBox.confirm(
        `确定要删除 ${report.company} 的报告吗？`,
        '确认删除',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        const index = reports.value.findIndex(r => r.id === report.id)
        if (index > -1) {
          reports.value.splice(index, 1)
          ElMessage.success('报告已删除')
        }
      }).catch(() => {
        ElMessage.info('已取消删除')
      })
      break
  }
}

onMounted(() => {
  // 页面加载时的初始化逻辑
})
</script>

<style lang="scss" scoped>
.reports-container {
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

// 工具栏
.toolbar {
  padding: 20px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  .toolbar-left {
    display: flex;
    gap: 16px;
    align-items: center;
  }
  
  .toolbar-right {
    display: flex;
    gap: 12px;
  }
}

// 统计卡片
.reports-stats {
  margin-bottom: 32px;
  
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    
    .stat-card {
      padding: 20px;
      display: flex;
      align-items: center;
      gap: 16px;
      
      .stat-icon {
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
        
        &.completed {
          background: #52c41a;
        }
        
        &.processing {
          background: #faad14;
        }
        
        &.draft {
          background: #1890ff;
        }
      }
      
      .stat-content {
        .stat-value {
          font-size: 28px;
          font-weight: 700;
          color: var(--text-primary);
          margin-bottom: 4px;
        }
        
        .stat-label {
          font-size: 14px;
          color: var(--text-secondary);
        }
      }
    }
  }
}

// 报告列表
.reports-list {
  .list-header {
    padding: 16px 20px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .sort-controls {
      display: flex;
      gap: 8px;
      align-items: center;
    }
  }
}

// 卡片视图
.reports-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
  
  .report-card {
    padding: 24px;
    cursor: pointer;
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-4px);
      box-shadow: var(--shadow-lg);
    }
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 20px;
      
      .company-info {
        .company-name {
          font-size: 18px;
          font-weight: 600;
          color: var(--text-primary);
          margin-bottom: 4px;
        }
        
        .report-type {
          font-size: 14px;
          color: var(--text-secondary);
        }
      }
    }
    
    .card-content {
      margin-bottom: 20px;
      
      .score-display {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 16px;
        
        .score-circle {
          width: 60px;
          height: 60px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 700;
          color: white;
          
          &.excellent {
            background: #52c41a;
          }
          
          &.good {
            background: #1890ff;
          }
          
          &.average {
            background: #faad14;
          }
          
          &.poor {
            background: #ff4d4f;
          }
          
          .score-value {
            font-size: 16px;
          }
        }
        
        .score-breakdown {
          display: flex;
          flex-direction: column;
          gap: 4px;
          
          .score-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            min-width: 60px;
            
            .score-label {
              font-size: 12px;
              color: var(--text-secondary);
              font-weight: 600;
            }
            
            .score-val {
              font-size: 14px;
              font-weight: 600;
              color: var(--text-primary);
            }
          }
        }
      }
      
      .report-meta {
        display: flex;
        flex-direction: column;
        gap: 8px;
        
        .meta-item {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 14px;
          color: var(--text-secondary);
          
          .el-icon {
            font-size: 16px;
          }
        }
      }
    }
    
    .card-actions {
      display: flex;
      gap: 8px;
      align-items: center;
    }
  }
}

// 表格视图
.reports-table {
  padding: 0;
  margin-bottom: 32px;
  
  :deep(.el-table) {
    background: transparent;
    
    .table-row {
      cursor: pointer;
      
      &:hover {
        background: rgba(102, 126, 234, 0.1);
      }
    }
  }
  
  .company-cell {
    .company-name {
      font-weight: 600;
      color: var(--text-primary);
      margin-bottom: 2px;
    }
    
    .company-industry {
      font-size: 12px;
      color: var(--text-secondary);
    }
  }
  
  .esg-scores {
    display: flex;
    flex-direction: column;
    gap: 2px;
    
    .esg-item {
      font-size: 12px;
      
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
  
  .table-actions {
    display: flex;
    gap: 8px;
    justify-content: center;
  }
}

// 分页
.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 32px;
}

// 空状态
.empty-state {
  text-align: center;
  padding: 80px 0;
}

// 报告详情对话框
.report-detail {
  .detail-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 32px;
    padding-bottom: 20px;
    border-bottom: 1px solid #f0f0f0;
    
    .company-info {
      h3 {
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 8px;
        color: var(--text-primary);
      }
      
      p {
        font-size: 16px;
        color: var(--text-secondary);
      }
    }
    
    .score-summary {
      display: flex;
      gap: 32px;
      align-items: center;
      
      .total-score {
        text-align: center;
        
        .score-label {
          font-size: 14px;
          color: var(--text-secondary);
          margin-bottom: 8px;
        }
        
        .score-value {
          font-size: 36px;
          font-weight: 700;
          color: var(--primary-color);
        }
      }
      
      .dimension-scores {
        display: flex;
        gap: 20px;
        
        .dimension-item {
          text-align: center;
          
          .dimension-label {
            font-size: 12px;
            color: var(--text-secondary);
            margin-bottom: 4px;
          }
          
          .dimension-value {
            font-size: 20px;
            font-weight: 600;
            color: var(--text-primary);
          }
        }
      }
    }
  }
  
  .detail-content {
    .scores-detail,
    .analysis-detail,
    .history-detail {
      padding: 20px 0;
      min-height: 200px;
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

// 响应式设计
@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 20px;
  }
  
  .toolbar {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
    
    .toolbar-left,
    .toolbar-right {
      justify-content: center;
    }
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .reports-grid {
    grid-template-columns: 1fr;
  }
  
  .score-display {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .detail-header {
    flex-direction: column;
    gap: 20px;
    
    .score-summary {
      flex-direction: column;
      gap: 20px;
    }
  }
}
</style>