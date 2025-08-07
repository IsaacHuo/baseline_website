import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api'

export const useESGStore = defineStore('esg', () => {
  // 状态
  const loading = ref(false)
  const currentCompany = ref(null)
  const scoringResults = ref(null)
  const analysisData = ref(null)
  const reports = ref([])
  
  // ESG指标数据
  const indicators = ref({
    E: [
      '碳排放总量', '范围1直接排放', '范围2间接排放', '范围3价值链排放',
      '单位营收能耗', '可再生能源占比', '水资源循环利用率', '危险废物处置合规率',
      '温室气体减排量', '碳排放权交易履约率', '环保行政处罚次数'
    ],
    S: [
      '员工流失率（核心岗位）', '残疾人就业比例', '客户隐私保护认证情况',
      '突发公共卫生事件应急响应效率', '员工培训覆盖率', '职业健康安全事故率',
      '供应链ESG审核比例', '中小企业账款逾期率', '乡村振兴投入金额', '公益捐赠占净利润比例'
    ],
    G: [
      '产品质量投诉处理时效', '数据安全事件发生次数', '供应链本地化率',
      '行业协会ESG评级', '供应链ESG风险应急预案完备性', '气候风险压力测试覆盖率'
    ]
  })
  
  // 行业类型
  const industries = ref([
    '能源', '金融', '科技', '制造', '制造业', '消费', '默认'
  ])
  
  // 模型参数
  const modelParams = ref({
    alpha: 0.5,
    e_weight: 0.4,
    s_weight: 0.3,
    g_weight: 0.3,
    delta_coeff: 0.1,
    epsilon_coeff: 0.15,
    zeta_coeff: 0.12,
    severity_factor: 0.4,
    max_bonus: 10,
    bonus_steepness: 0.8,
    threshold_multiplier: 1.0,
    use_cross_terms: true
  })
  
  // 计算属性
  const totalIndicators = computed(() => {
    return indicators.value.E.length + indicators.value.S.length + indicators.value.G.length
  })
  
  const hasResults = computed(() => {
    return scoringResults.value !== null
  })
  
  // Actions
  const setLoading = (value) => {
    loading.value = value
  }
  
  const setCurrentCompany = (company) => {
    currentCompany.value = company
  }
  
  const updateModelParams = (params) => {
    modelParams.value = { ...modelParams.value, ...params }
  }
  
  // ESG评分计算
  const calculateESGScore = async (companyData, events = []) => {
    try {
      setLoading(true)
      const response = await api.calculateScore({
        company_data: companyData,
        events: events,
        model_params: modelParams.value
      })
      
      scoringResults.value = response.data
      return response.data
    } catch (error) {
      console.error('ESG评分计算失败:', error)
      throw error
    } finally {
      setLoading(false)
    }
  }
  
  // 生成分析报告
  const generateAnalysis = async (resultsData) => {
    try {
      setLoading(true)
      const response = await api.generateAnalysis(resultsData)
      analysisData.value = response.data
      return response.data
    } catch (error) {
      console.error('分析报告生成失败:', error)
      throw error
    } finally {
      setLoading(false)
    }
  }
  
  // 导出报告
  const exportReport = async (reportType, data) => {
    try {
      setLoading(true)
      const response = await api.exportReport({
        type: reportType,
        data: data
      })
      return response.data
    } catch (error) {
      console.error('报告导出失败:', error)
      throw error
    } finally {
      setLoading(false)
    }
  }
  
  // 保存报告
  const saveReport = (report) => {
    const newReport = {
      id: Date.now(),
      ...report,
      createdAt: new Date().toISOString()
    }
    reports.value.unshift(newReport)
    return newReport
  }
  
  // 删除报告
  const deleteReport = (reportId) => {
    const index = reports.value.findIndex(r => r.id === reportId)
    if (index > -1) {
      reports.value.splice(index, 1)
    }
  }
  
  // 清空结果
  const clearResults = () => {
    scoringResults.value = null
    analysisData.value = null
    currentCompany.value = null
  }
  
  return {
    // 状态
    loading,
    currentCompany,
    scoringResults,
    analysisData,
    reports,
    indicators,
    industries,
    modelParams,
    
    // 计算属性
    totalIndicators,
    hasResults,
    
    // 方法
    setLoading,
    setCurrentCompany,
    updateModelParams,
    calculateESGScore,
    generateAnalysis,
    exportReport,
    saveReport,
    deleteReport,
    clearResults
  }
})