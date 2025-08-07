# ESG评分系统 - Vue前端版本

基于甲模型量化评估框架的企业ESG（环境、社会、治理）综合评分系统，采用Vue 3 + Vite构建现代化前端界面，支持自动部署到Vercel。

## 🌟 系统特色

### 原有Python后端特色
- **🔄 智能数据处理**: 多源数据融合与标准化清洗
- **⚖️ 组合赋权机制**: 主观权重+客观权重动态平衡  
- **📈 交叉项建模**: E×S、E×G、S×G维度协同效应量化
- **🎯 非线性调整**: 事件分级惩罚与饱和函数奖励
- **📊 多维度分析**: 单企业深度画像与可视化展示
- **📋 专业报告**: 标准/简化/技术/投资四类报告模板

### 新增Vue前端特色
- **专业美观的界面设计** - 采用现代化设计语言，体现专业和高级感
- **完整的ESG评分流程** - 从数据输入到报告生成的全流程支持
- **可视化图表展示** - 基于ECharts的丰富图表类型
- **报告管理系统** - 完整的报告生成、保存、导出功能
- **响应式设计** - 支持桌面端和移动端访问
- **自动化部署** - 通过GitHub Actions自动部署到Vercel

## 🚀 技术栈

### 前端技术
- **Vue 3** - 渐进式JavaScript框架
- **Vite** - 下一代前端构建工具
- **Vue Router** - 官方路由管理器
- **Pinia** - Vue状态管理库
- **Element Plus** - Vue 3组件库
- **ECharts** - 数据可视化图表库
- **Axios** - HTTP客户端
- **SCSS** - CSS预处理器

### 后端技术
- **Python 3.8+** - 原有ESG评分模型
- **Vercel Serverless Functions** - 无服务器后端API
- **Node.js** - JavaScript运行时

## 🛠️ 本地开发

### 环境要求
- Node.js >= 18.0.0
- npm >= 8.0.0
- Python 3.8+ (用于ESG模型)
- uv包管理器 (Python依赖管理)

### Vue前端开发
```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

### Python后端开发（原有功能）
```bash
# 安装依赖
uv sync

# 启动系统  
uv run main.py

# 访问地址
http://localhost:7860
```

## 🚀 部署到Vercel

### 通过GitHub Actions自动部署（推荐）

1. **配置GitHub Secrets**
   在GitHub仓库设置中添加：
   ```
   VERCEL_TOKEN=your_vercel_api_token
   VERCEL_ORG_ID=your_team_id_or_username
   VERCEL_PROJECT_ID=your_project_id
   ```

2. **推送代码触发部署**
   ```bash
   git add .
   git commit -m "Deploy ESG scoring system"
   git push origin main
   ```

### 手动部署
```bash
# 安装Vercel CLI
npm install -g vercel

# 登录并部署
vercel login
vercel --prod
```

## 📊 功能模块

### 1. 首页 (Home)
- 系统概览和统计数据
- 快速导航到各功能模块
- ESG评分模型介绍

### 2. ESG评分 (Scoring)
- 企业基本信息录入
- ESG指标数据输入
- 事件调整配置
- 实时评分计算

### 3. 数据分析 (Analysis)
- 评分结果详细分析
- 多维度图表展示
- 行业对比分析

### 4. 报告管理 (Reports)
- 历史报告查看
- 报告导出功能
- 报告分享和管理

### 5. 系统设置 (Settings)
- 模型参数配置
- 行业权重设置
- 指标管理

## 核心模型

甲模型采用多维度交叉项效应建模：

```
ESG Score = αW₁E + αW₂S + αW₃G + δ(E×S) + ε(E×G) + ζ(S×G) + Events_Adjustment
```

其中：
- `α`: 主观权重系数
- `W₁,W₂,W₃`: E、S、G维度权重  
- `δ,ε,ζ`: 交叉项联动系数
- `Events_Adjustment`: 非线性事件调整机制

## 📁 项目结构

```
esg-scoring-system/
├── .github/workflows/     # GitHub Actions配置
├── api/                   # Vercel Serverless API
├── src/                   # Vue前端源码
│   ├── api/              # 前端API接口
│   ├── components/       # Vue组件
│   ├── router/           # 路由配置
│   ├── stores/           # Pinia状态管理
│   ├── styles/           # 样式文件
│   └── views/            # 页面组件
├── baseline/             # 原Python版本
│   ├── main.py              # 应用入口
│   ├── esg_model.py         # 甲模型核心算法
│   ├── esg_data_utils.py    # 数据处理工具
│   ├── gradio_app.py        # Web界面实现
│   ├── pyproject.toml       # 项目配置
│   └── knowledge/           # 知识库文档
│       ├── 甲模型.txt        # 模型设计理念
│       ├── 投资意见.txt      # 投资策略指导
│       └── 政策.txt          # 政策响应机制
├── package.json          # 前端依赖配置
├── vite.config.js        # Vite构建配置
├── vercel.json           # Vercel部署配置
└── README.md             # 项目说明文档
```

## 使用流程

1. **数据输入**: 手动录入或上传CSV/Excel文件
2. **模型配置**: 调整权重参数与交叉项系数  
3. **评分计算**: 生成ESG综合得分与评级
4. **结果分析**: 查看可视化图表与维度分解
5. **报告生成**: 导出专业分析报告（txt/word/pdf）

## 📋 原有技术栈（Python版本）

- **后端**: Python + Pandas + NumPy + SciPy
- **前端**: Gradio + Plotly + HTML/CSS
- **文档**: python-docx + reportlab
- **数据**: Excel/CSV文件处理

---

**QureLab团队** | ESG量化投资解决方案
