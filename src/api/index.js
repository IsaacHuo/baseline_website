import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加token等认证信息
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    const message = error.response?.data?.message || error.message || '请求失败'
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

// API接口定义
export default {
  // ESG评分计算
  calculateScore(data) {
    return api.post('/calculate-score', data)
  },
  
  // 生成分析报告
  generateAnalysis(data) {
    return api.post('/generate-analysis', data)
  },
  
  // 导出报告
  exportReport(data) {
    return api.post('/export-report', data, {
      responseType: 'blob'
    })
  },
  
  // 上传数据文件
  uploadFile(file) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/upload-file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  
  // 获取指标配置
  getIndicators() {
    return api.get('/indicators')
  },
  
  // 获取行业配置
  getIndustries() {
    return api.get('/industries')
  },
  
  // 验证数据
  validateData(data) {
    return api.post('/validate-data', data)
  },
  
  // 获取模型参数
  getModelParams() {
    return api.get('/model-params')
  },
  
  // 更新模型参数
  updateModelParams(params) {
    return api.post('/model-params', params)
  }
}

export { api }