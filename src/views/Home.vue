<template>
  <div class="home-container">
    <!-- 导航栏 -->
    <nav class="navbar glass-card">
      <div class="nav-content">
        <div class="logo">
          <el-icon class="logo-icon"><TrendCharts /></el-icon>
          <span class="logo-text gradient-text">ESG评分系统</span>
        </div>
        <div class="nav-menu">
          <router-link to="/" class="nav-item active">首页</router-link>
          <router-link to="/scoring" class="nav-item">评分计算</router-link>
          <router-link to="/analysis" class="nav-item">数据分析</router-link>
          <router-link to="/reports" class="nav-item">报告管理</router-link>
          <router-link to="/settings" class="nav-item">系统设置</router-link>
        </div>
      </div>
    </nav>

    <!-- 主要内容 -->
    <main class="main-content">
      <!-- 英雄区域 -->
      <section class="hero-section fade-in">
        <div class="hero-content">
          <h1 class="hero-title">
            基于甲模型的企业
            <span class="gradient-text">ESG综合评分平台</span>
          </h1>
          <p class="hero-subtitle">
            科学、透明、可操作的ESG投资决策支持系统
          </p>
          <div class="hero-stats">
            <div class="stat-item">
              <div class="stat-number">{{ totalIndicators }}</div>
              <div class="stat-label">评估指标</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">7</div>
              <div class="stat-label">支持行业</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">4</div>
              <div class="stat-label">报告类型</div>
            </div>
          </div>
          <div class="hero-actions">
            <el-button type="primary" size="large" @click="startScoring" class="action-btn">
              <el-icon><Operation /></el-icon>
              开始评分
            </el-button>
            <el-button size="large" @click="viewDemo" class="action-btn demo-btn">
              <el-icon><View /></el-icon>
              查看演示
            </el-button>
          </div>
        </div>
        <div class="hero-visual">
          <div class="floating-card card-1 hover-lift">
            <el-icon class="card-icon"><Sunny /></el-icon>
            <div class="card-title">环境 (E)</div>
            <div class="card-desc">{{ indicators.E.length }}项指标</div>
          </div>
          <div class="floating-card card-2 hover-lift">
            <el-icon class="card-icon"><User /></el-icon>
            <div class="card-title">社会 (S)</div>
            <div class="card-desc">{{ indicators.S.length }}项指标</div>
          </div>
          <div class="floating-card card-3 hover-lift">
            <el-icon class="card-icon"><Setting /></el-icon>
            <div class="card-title">治理 (G)</div>
            <div class="card-desc">{{ indicators.G.length }}项指标</div>
          </div>
        </div>
      </section>

      <!-- 特色功能 -->
      <section class="features-section slide-up">
        <div class="section-header">
          <h2 class="section-title">系统特色</h2>
          <p class="section-subtitle">基于甲模型量化评估框架的专业ESG评分系统</p>
        </div>
        <div class="features-grid">
          <div class="feature-card glass-card hover-lift" v-for="feature in features" :key="feature.id">
            <div class="feature-icon">
              <el-icon><component :is="feature.icon" /></el-icon>
            </div>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-desc">{{ feature.description }}</p>
          </div>
        </div>
      </section>

      <!-- 模型介绍 -->
      <section class="model-section slide-up">
        <div class="model-content glass-card">
          <div class="model-text">
            <h2 class="model-title">甲模型核心算法</h2>
            <p class="model-desc">
              采用多维度交叉项效应建模，实现E、S、G三个维度的协同评估
            </p>
            <div class="model-formula">
              <code>
                ESG Score = αW₁E + αW₂S + αW₃G + δ(E×S) + ε(E×G) + ζ(S×G) + Events_Adjustment
              </code>
            </div>
            <ul class="model-features">
              <li><el-icon><Check /></el-icon>组合赋权机制：主观权重+客观权重动态平衡</li>
              <li><el-icon><Check /></el-icon>交叉项建模：量化E×S、E×G、S×G维度协同效应</li>
              <li><el-icon><Check /></el-icon>非线性调整：事件分级惩罚与饱和函数奖励</li>
              <li><el-icon><Check /></el-icon>动态适应：支持行业特色权重配置</li>
            </ul>
          </div>
          <div class="model-visual">
            <div class="formula-visual">
              <div class="dimension-node e-node">E</div>
              <div class="dimension-node s-node">S</div>
              <div class="dimension-node g-node">G</div>
              <div class="cross-line line-1"></div>
              <div class="cross-line line-2"></div>
              <div class="cross-line line-3"></div>
              <div class="result-node">ESG</div>
            </div>
          </div>
        </div>
      </section>

      <!-- 快速开始 -->
      <section class="quickstart-section slide-up">
        <div class="section-header">
          <h2 class="section-title">快速开始</h2>
          <p class="section-subtitle">三步完成企业ESG评分</p>
        </div>
        <div class="steps-container">
          <div class="step-item" v-for="(step, index) in steps" :key="step.id">
            <div class="step-number">{{ index + 1 }}</div>
            <div class="step-content">
              <h3 class="step-title">{{ step.title }}</h3>
              <p class="step-desc">{{ step.description }}</p>
            </div>
            <div class="step-icon">
              <el-icon><component :is="step.icon" /></el-icon>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-text">
          <p>&copy; 2024 ESG评分系统. 基于甲模型量化评估框架</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useESGStore } from '@/stores/esg'
import {
  TrendCharts, Operation, View, Sunny, User, Setting,
  Check, Upload, DataAnalysis, Document
} from '@element-plus/icons-vue'

const router = useRouter()
const esgStore = useESGStore()

// 计算属性
const totalIndicators = computed(() => esgStore.totalIndicators)
const indicators = computed(() => esgStore.indicators)

// 系统特色
const features = [
  {
    id: 1,
    icon: 'DataAnalysis',
    title: '智能数据处理',
    description: '多源数据融合与标准化清洗，支持Excel、CSV等多种格式'
  },
  {
    id: 2,
    icon: 'Setting',
    title: '组合赋权机制',
    description: '主观权重+客观权重动态平衡，确保评分科学性'
  },
  {
    id: 3,
    icon: 'TrendCharts',
    title: '交叉项建模',
    description: 'E×S、E×G、S×G维度协同效应量化分析'
  },
  {
    id: 4,
    icon: 'Document',
    title: '专业报告',
    description: '标准/简化/技术/投资四类报告模板，支持多格式导出'
  }
]

// 快速开始步骤
const steps = [
  {
    id: 1,
    icon: 'Upload',
    title: '数据输入',
    description: '上传企业ESG数据或手动输入指标值'
  },
  {
    id: 2,
    icon: 'Operation',
    title: '评分计算',
    description: '基于甲模型算法自动计算ESG综合评分'
  },
  {
    id: 3,
    icon: 'Document',
    title: '报告生成',
    description: '生成专业分析报告并支持多格式导出'
  }
]

// 方法
const startScoring = () => {
  router.push('/scoring')
}

const viewDemo = () => {
  // 这里可以添加演示逻辑
  router.push('/scoring?demo=true')
}
</script>

<style lang="scss" scoped>
.home-container {
  min-height: 100vh;
  background: var(--bg-color);
}

// 导航栏 - 黑白专业风格
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  backdrop-filter: blur(10px);
  
  .nav-content {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
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

// 主要内容
.main-content {
  padding-top: 100px;
}

// 英雄区域 - 黑白专业风格
.hero-section {
  padding: 80px 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  gap: 80px;
  
  .hero-content {
    flex: 1;
    
    .hero-title {
      font-size: 48px;
      font-weight: 700;
      line-height: 1.2;
      color: var(--text-primary);
      margin-bottom: 24px;
    }
    
    .hero-subtitle {
      font-size: 20px;
      color: var(--text-secondary);
      margin-bottom: 40px;
      line-height: 1.6;
    }
    
    .hero-stats {
      display: flex;
      gap: 40px;
      margin-bottom: 40px;
      
      .stat-item {
        text-align: center;
        padding: 20px;
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-sm);
        
        .stat-number {
          font-size: 36px;
          font-weight: 700;
          color: var(--text-primary);
          line-height: 1;
        }
        
        .stat-label {
          font-size: 14px;
          color: var(--text-muted);
          margin-top: 8px;
        }
      }
    }
    
    .hero-actions {
      display: flex;
      gap: 16px;
      
      .action-btn {
        height: 48px;
        padding: 0 32px;
        font-size: 16px;
        border-radius: 24px;
        
        &.demo-btn {
          background: rgba(255, 255, 255, 0.2);
          border: 1px solid rgba(255, 255, 255, 0.3);
          color: white;
          
          &:hover {
            background: rgba(255, 255, 255, 0.3);
          }
        }
      }
    }
  }
  
  .hero-visual {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 32px;
    height: 400px;
    
    @media (max-width: 1200px) {
      flex-direction: column;
      height: auto;
      gap: 20px;
    }
    
    .floating-card {
      padding: 24px;
      border-radius: 16px;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(20px);
      text-align: center;
      min-width: 200px;
      flex: 1;
      max-width: 280px;
      
      .card-icon {
        font-size: 32px;
        margin-bottom: 12px;
      }
      
      .card-title {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 8px;
      }
      
      .card-desc {
        font-size: 14px;
        color: var(--text-secondary);
      }
      
      &.card-1 {
        .card-icon {
          color: #52c41a;
        }
      }
      
      &.card-2 {
        .card-icon {
          color: #1890ff;
        }
      }
      
      &.card-3 {
        .card-icon {
          color: #722ed1;
        }
      }
    }
  }
}

// 特色功能 - 黑白专业风格
.features-section {
  padding: 80px 40px;
  max-width: 1200px;
  margin: 0 auto;
  background: var(--bg-secondary);
  border-radius: var(--radius-xl);
  margin-top: 40px;
  
  .section-header {
    text-align: center;
    margin-bottom: 60px;
    
    .section-title {
      font-size: 36px;
      font-weight: 700;
      color: var(--text-primary);
      margin-bottom: 16px;
    }
    
    .section-subtitle {
      font-size: 18px;
      color: var(--text-secondary);
    }
  }
  
  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 32px;
    
    .feature-card {
      padding: 32px;
      text-align: center;
      background: var(--bg-primary);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-sm);
      transition: all 0.3s ease;
      
      &:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-color: var(--border-dark);
      }
      
      .feature-icon {
        width: 64px;
        height: 64px;
        border-radius: 50%;
        background: var(--primary-color);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 24px;
        
        .el-icon {
          font-size: 28px;
          color: #ffffff;
        }
      }
      
      .feature-title {
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 16px;
        color: var(--text-primary);
      }
      
      .feature-desc {
        color: var(--text-secondary);
        line-height: 1.6;
      }
    }
  }
}

// 模型介绍
.model-section {
  padding: 80px 40px;
  max-width: 1200px;
  margin: 0 auto;
  
  .model-content {
    padding: 48px;
    display: flex;
    align-items: center;
    gap: 60px;
    
    .model-text {
      flex: 1;
      
      .model-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 16px;
        color: var(--text-primary);
      }
      
      .model-desc {
        font-size: 18px;
        color: var(--text-secondary);
        margin-bottom: 24px;
        line-height: 1.6;
      }
      
      .model-formula {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 24px;
        
        code {
          font-family: 'Monaco', 'Menlo', monospace;
          font-size: 14px;
          color: var(--primary-color);
          font-weight: 500;
        }
      }
      
      .model-features {
        list-style: none;
        
        li {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 12px;
          color: var(--text-secondary);
          
          .el-icon {
            color: #52c41a;
            font-size: 16px;
          }
        }
      }
    }
    
    .model-visual {
      flex: 1;
      
      .formula-visual {
        position: relative;
        height: 300px;
        
        .dimension-node {
          position: absolute;
          width: 60px;
          height: 60px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 20px;
          font-weight: 600;
          color: white;
          
          &.e-node {
            top: 20px;
            left: 20px;
            background: #52c41a;
          }
          
          &.s-node {
            top: 20px;
            right: 20px;
            background: #1890ff;
          }
          
          &.g-node {
            bottom: 120px;
            left: 50%;
            transform: translateX(-50%);
            background: #722ed1;
          }
        }
        
        .result-node {
          position: absolute;
          bottom: 20px;
          left: 50%;
          transform: translateX(-50%);
          width: 80px;
          height: 80px;
          border-radius: 50%;
          background: var(--gradient-primary);
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 18px;
          font-weight: 600;
          color: white;
        }
        
        .cross-line {
          position: absolute;
          height: 2px;
          background: var(--primary-color);
          opacity: 0.6;
          
          &.line-1 {
            top: 50px;
            left: 80px;
            width: 120px;
          }
          
          &.line-2 {
            top: 80px;
            left: 50px;
            width: 100px;
            transform: rotate(45deg);
          }
          
          &.line-3 {
            top: 80px;
            right: 50px;
            width: 100px;
            transform: rotate(-45deg);
          }
        }
      }
    }
  }
}

// 快速开始 - 黑白专业风格
.quickstart-section {
  padding: 80px 40px;
  max-width: 1200px;
  margin: 0 auto;
  background: var(--bg-secondary);
  border-radius: var(--radius-xl);
  margin-top: 40px;
  
  .section-header {
    text-align: center;
    margin-bottom: 60px;
    
    .section-title {
      font-size: 36px;
      font-weight: 700;
      color: var(--text-primary);
      margin-bottom: 16px;
    }
    
    .section-subtitle {
      font-size: 18px;
      color: var(--text-secondary);
    }
  }
  
  .steps-container {
    display: flex;
    gap: 40px;
    justify-content: center;
    
    .step-item {
      background: var(--bg-primary);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 32px;
      text-align: center;
      position: relative;
      flex: 1;
      max-width: 300px;
      box-shadow: var(--shadow-sm);
      transition: all 0.3s ease;
      
      &:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-color: var(--border-dark);
      }
      
      .step-number {
        position: absolute;
        top: -20px;
        left: 50%;
        transform: translateX(-50%);
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: var(--primary-color);
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: 600;
        box-shadow: var(--shadow-md);
      }
      
      .step-content {
        margin-bottom: 24px;
        
        .step-title {
          font-size: 20px;
          font-weight: 600;
          margin-bottom: 12px;
          color: var(--text-primary);
        }
        
        .step-desc {
          color: var(--text-secondary);
          line-height: 1.6;
        }
      }
      
      .step-icon {
        .el-icon {
          font-size: 48px;
          color: var(--primary-color);
        }
      }
    }
  }
}

// 页脚 - 黑白专业风格
.footer {
  padding: 40px;
  text-align: center;
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-color);
  margin-top: 40px;
  
  .footer-content {
    max-width: 1200px;
    margin: 0 auto;
    
    .footer-text {
      color: var(--text-muted);
      font-size: 14px;
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .navbar {
    .nav-content {
      min-width: auto;
      width: 90vw;
    }
    
    .nav-menu {
      gap: 16px;
      
      .nav-item {
        font-size: 14px;
      }
    }
  }
  
  .hero-section {
    flex-direction: column;
    gap: 40px;
    padding: 40px 20px;
    
    .hero-content {
      text-align: center;
      
      .hero-title {
        font-size: 32px;
      }
      
      .hero-stats {
        justify-content: center;
        gap: 24px;
      }
      
      .hero-actions {
        justify-content: center;
      }
    }
    
    .hero-visual {
      height: 300px;
      
      .floating-card {
        position: relative;
        margin: 16px;
        
        &.card-1,
        &.card-2,
        &.card-3 {
          position: relative;
          top: auto;
          left: auto;
          right: auto;
          bottom: auto;
        }
      }
    }
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .model-content {
    flex-direction: column;
    gap: 40px;
    padding: 32px 20px;
  }
  
  .steps-container {
    flex-direction: column;
    align-items: center;
  }
}
</style>