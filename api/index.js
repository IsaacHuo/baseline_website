// Vercel Serverless Function for ESG Scoring System
// This file handles all backend API requests for the ESG scoring system

import { ESGModel } from '../esg_model.js'
import { ESGDataProcessor } from '../esg_data_utils.js'

// CORS headers for cross-origin requests
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
}

// Initialize ESG model and data processor
const esgModel = new ESGModel()
const dataProcessor = new ESGDataProcessor()

// Main handler function
export default async function handler(req, res) {
  // Handle CORS preflight requests
  if (req.method === 'OPTIONS') {
    return res.status(200).json({ message: 'OK' })
  }

  // Set CORS headers
  Object.entries(corsHeaders).forEach(([key, value]) => {
    res.setHeader(key, value)
  })

  try {
    const { method, url } = req
    const urlPath = new URL(url, `http://${req.headers.host}`).pathname

    // Route handling
    switch (method) {
      case 'GET':
        return await handleGet(req, res, urlPath)
      case 'POST':
        return await handlePost(req, res, urlPath)
      case 'PUT':
        return await handlePut(req, res, urlPath)
      case 'DELETE':
        return await handleDelete(req, res, urlPath)
      default:
        return res.status(405).json({ error: 'Method not allowed' })
    }
  } catch (error) {
    console.error('API Error:', error)
    return res.status(500).json({ 
      error: 'Internal server error',
      message: error.message 
    })
  }
}

// Handle GET requests
async function handleGet(req, res, path) {
  switch (path) {
    case '/api/health':
      return res.status(200).json({ 
        status: 'healthy',
        timestamp: new Date().toISOString(),
        version: '1.0.0'
      })

    case '/api/indicators':
      return res.status(200).json({
        success: true,
        data: dataProcessor.getIndicators()
      })

    case '/api/industries':
      return res.status(200).json({
        success: true,
        data: esgModel.getIndustryTypes()
      })

    case '/api/model-params':
      return res.status(200).json({
        success: true,
        data: esgModel.getModelParameters()
      })

    case '/api/reports':
      // Mock reports data - in production, this would come from a database
      return res.status(200).json({
        success: true,
        data: getMockReports()
      })

    default:
      return res.status(404).json({ error: 'Endpoint not found' })
  }
}

// Handle POST requests
async function handlePost(req, res, path) {
  const body = req.body

  switch (path) {
    case '/api/calculate-score':
      return await calculateESGScore(req, res, body)

    case '/api/generate-analysis':
      return await generateAnalysis(req, res, body)

    case '/api/export-report':
      return await exportReport(req, res, body)

    case '/api/upload-data':
      return await uploadData(req, res, body)

    case '/api/save-report':
      return await saveReport(req, res, body)

    default:
      return res.status(404).json({ error: 'Endpoint not found' })
  }
}

// Handle PUT requests
async function handlePut(req, res, path) {
  const body = req.body

  switch (path) {
    case '/api/model-params':
      return await updateModelParameters(req, res, body)

    case '/api/indicators':
      return await updateIndicators(req, res, body)

    default:
      return res.status(404).json({ error: 'Endpoint not found' })
  }
}

// Handle DELETE requests
async function handleDelete(req, res, path) {
  const reportId = path.split('/').pop()

  switch (true) {
    case path.startsWith('/api/reports/'):
      return await deleteReport(req, res, reportId)

    default:
      return res.status(404).json({ error: 'Endpoint not found' })
  }
}

// ESG Score calculation
async function calculateESGScore(req, res, body) {
  try {
    const { companyData, indicatorData, events = [], modelParams } = body

    // Validate required data
    if (!companyData || !indicatorData) {
      return res.status(400).json({
        error: 'Missing required data',
        message: 'Company data and indicator data are required'
      })
    }

    // Update model parameters if provided
    if (modelParams) {
      esgModel.updateParameters(modelParams)
    }

    // Process and validate indicator data
    const processedData = dataProcessor.processData(indicatorData)
    
    // Calculate ESG scores
    const scores = esgModel.calculateScore(
      processedData,
      companyData.industry || 'default',
      events
    )

    // Generate detailed breakdown
    const breakdown = esgModel.getScoreBreakdown(processedData)
    
    // Calculate cross-term effects
    const crossTerms = esgModel.calculateCrossTerms(scores)

    return res.status(200).json({
      success: true,
      data: {
        scores,
        breakdown,
        crossTerms,
        metadata: {
          calculatedAt: new Date().toISOString(),
          modelVersion: esgModel.getVersion(),
          company: companyData.name,
          industry: companyData.industry
        }
      }
    })
  } catch (error) {
    console.error('Score calculation error:', error)
    return res.status(500).json({
      error: 'Score calculation failed',
      message: error.message
    })
  }
}

// Generate analysis report
async function generateAnalysis(req, res, body) {
  try {
    const { scores, companyData, indicatorData } = body

    if (!scores || !companyData) {
      return res.status(400).json({
        error: 'Missing required data for analysis'
      })
    }

    // Generate insights and recommendations
    const insights = generateInsights(scores, indicatorData)
    const recommendations = generateRecommendations(scores)
    const benchmarks = getBenchmarkData(companyData.industry)
    
    // Create analysis report
    const analysis = {
      summary: {
        overallScore: scores.total_score,
        dimensionScores: {
          environmental: scores.e_score,
          social: scores.s_score,
          governance: scores.g_score
        },
        performanceLevel: getPerformanceLevel(scores.total_score),
        industryRanking: calculateIndustryRanking(scores, companyData.industry)
      },
      insights,
      recommendations,
      benchmarks,
      trends: generateTrendAnalysis(scores),
      generatedAt: new Date().toISOString()
    }

    return res.status(200).json({
      success: true,
      data: analysis
    })
  } catch (error) {
    console.error('Analysis generation error:', error)
    return res.status(500).json({
      error: 'Analysis generation failed',
      message: error.message
    })
  }
}

// Export report
async function exportReport(req, res, body) {
  try {
    const { reportData, format = 'pdf' } = body

    if (!reportData) {
      return res.status(400).json({
        error: 'Missing report data'
      })
    }

    // Generate export data based on format
    let exportData
    switch (format.toLowerCase()) {
      case 'pdf':
        exportData = await generatePDFReport(reportData)
        break
      case 'xlsx':
        exportData = await generateExcelReport(reportData)
        break
      case 'json':
        exportData = JSON.stringify(reportData, null, 2)
        break
      default:
        return res.status(400).json({
          error: 'Unsupported export format'
        })
    }

    return res.status(200).json({
      success: true,
      data: {
        format,
        content: exportData,
        filename: `esg-report-${Date.now()}.${format}`,
        generatedAt: new Date().toISOString()
      }
    })
  } catch (error) {
    console.error('Export error:', error)
    return res.status(500).json({
      error: 'Export failed',
      message: error.message
    })
  }
}

// Upload and process data
async function uploadData(req, res, body) {
  try {
    const { fileData, fileType } = body

    if (!fileData) {
      return res.status(400).json({
        error: 'No file data provided'
      })
    }

    // Process uploaded data based on file type
    let processedData
    switch (fileType) {
      case 'csv':
        processedData = dataProcessor.processCSV(fileData)
        break
      case 'xlsx':
        processedData = dataProcessor.processExcel(fileData)
        break
      case 'json':
        processedData = dataProcessor.processJSON(fileData)
        break
      default:
        return res.status(400).json({
          error: 'Unsupported file type'
        })
    }

    // Validate processed data
    const validation = dataProcessor.validateData(processedData)
    
    return res.status(200).json({
      success: true,
      data: {
        processedData,
        validation,
        recordCount: processedData.length,
        processedAt: new Date().toISOString()
      }
    })
  } catch (error) {
    console.error('Upload processing error:', error)
    return res.status(500).json({
      error: 'Data processing failed',
      message: error.message
    })
  }
}

// Save report
async function saveReport(req, res, body) {
  try {
    const { reportData, metadata } = body

    if (!reportData) {
      return res.status(400).json({
        error: 'No report data provided'
      })
    }

    // In production, this would save to a database
    // For now, we'll simulate saving and return a mock ID
    const reportId = `report_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    
    const savedReport = {
      id: reportId,
      ...reportData,
      metadata: {
        ...metadata,
        savedAt: new Date().toISOString(),
        version: '1.0'
      }
    }

    return res.status(201).json({
      success: true,
      data: savedReport
    })
  } catch (error) {
    console.error('Save report error:', error)
    return res.status(500).json({
      error: 'Failed to save report',
      message: error.message
    })
  }
}

// Update model parameters
async function updateModelParameters(req, res, body) {
  try {
    const { parameters } = body

    if (!parameters) {
      return res.status(400).json({
        error: 'No parameters provided'
      })
    }

    // Validate parameters
    const validation = esgModel.validateParameters(parameters)
    if (!validation.isValid) {
      return res.status(400).json({
        error: 'Invalid parameters',
        details: validation.errors
      })
    }

    // Update model parameters
    esgModel.updateParameters(parameters)

    return res.status(200).json({
      success: true,
      data: {
        updatedParameters: esgModel.getModelParameters(),
        updatedAt: new Date().toISOString()
      }
    })
  } catch (error) {
    console.error('Parameter update error:', error)
    return res.status(500).json({
      error: 'Failed to update parameters',
      message: error.message
    })
  }
}

// Update indicators
async function updateIndicators(req, res, body) {
  try {
    const { indicators } = body

    if (!indicators) {
      return res.status(400).json({
        error: 'No indicators provided'
      })
    }

    // Update indicators
    dataProcessor.updateIndicators(indicators)

    return res.status(200).json({
      success: true,
      data: {
        updatedIndicators: dataProcessor.getIndicators(),
        updatedAt: new Date().toISOString()
      }
    })
  } catch (error) {
    console.error('Indicators update error:', error)
    return res.status(500).json({
      error: 'Failed to update indicators',
      message: error.message
    })
  }
}

// Delete report
async function deleteReport(req, res, reportId) {
  try {
    if (!reportId) {
      return res.status(400).json({
        error: 'Report ID is required'
      })
    }

    // In production, this would delete from database
    // For now, we'll simulate deletion
    
    return res.status(200).json({
      success: true,
      data: {
        deletedReportId: reportId,
        deletedAt: new Date().toISOString()
      }
    })
  } catch (error) {
    console.error('Delete report error:', error)
    return res.status(500).json({
      error: 'Failed to delete report',
      message: error.message
    })
  }
}

// Helper functions
function generateInsights(scores, indicatorData) {
  const insights = []
  
  // Environmental insights
  if (scores.e_score < 70) {
    insights.push({
      type: 'warning',
      dimension: 'Environmental',
      message: '环境评分偏低，建议加强环境保护措施',
      priority: 'high'
    })
  }
  
  // Social insights
  if (scores.s_score > 85) {
    insights.push({
      type: 'success',
      dimension: 'Social',
      message: '社会责任表现优秀，继续保持',
      priority: 'medium'
    })
  }
  
  // Governance insights
  if (scores.g_score < 75) {
    insights.push({
      type: 'info',
      dimension: 'Governance',
      message: '治理结构有改进空间，建议优化董事会结构',
      priority: 'medium'
    })
  }
  
  return insights
}

function generateRecommendations(scores) {
  const recommendations = []
  
  // Generate recommendations based on scores
  if (scores.e_score < scores.s_score && scores.e_score < scores.g_score) {
    recommendations.push({
      dimension: 'Environmental',
      title: '提升环境管理水平',
      description: '建议制定更严格的环境保护政策，增加可再生能源使用比例',
      expectedImprovement: 5.2,
      priority: 'high'
    })
  }
  
  if (scores.total_score < 80) {
    recommendations.push({
      dimension: 'Overall',
      title: '全面提升ESG表现',
      description: '建议建立专门的ESG管理团队，制定系统性改进计划',
      expectedImprovement: 8.5,
      priority: 'high'
    })
  }
  
  return recommendations
}

function getBenchmarkData(industry) {
  // Mock benchmark data - in production, this would come from a database
  const benchmarks = {
    'technology': { average: 78.5, top10: 92.3, median: 76.8 },
    'finance': { average: 82.1, top10: 94.7, median: 81.2 },
    'manufacturing': { average: 71.3, top10: 88.9, median: 70.1 },
    'default': { average: 75.0, top10: 90.0, median: 74.5 }
  }
  
  return benchmarks[industry] || benchmarks.default
}

function getPerformanceLevel(score) {
  if (score >= 90) return 'Excellent'
  if (score >= 80) return 'Good'
  if (score >= 70) return 'Average'
  if (score >= 60) return 'Below Average'
  return 'Poor'
}

function calculateIndustryRanking(scores, industry) {
  // Mock ranking calculation
  const totalScore = scores.total_score
  const percentile = Math.min(95, Math.max(5, totalScore + Math.random() * 10 - 5))
  
  return {
    percentile: Math.round(percentile),
    rank: Math.ceil((100 - percentile) / 100 * 1000),
    totalCompanies: 1000
  }
}

function generateTrendAnalysis(scores) {
  // Mock trend data
  return {
    direction: scores.total_score > 75 ? 'improving' : 'stable',
    changeRate: Math.random() * 5 - 2.5,
    forecast: {
      nextQuarter: scores.total_score + Math.random() * 3 - 1.5,
      nextYear: scores.total_score + Math.random() * 8 - 4
    }
  }
}

function getMockReports() {
  return [
    {
      id: 'report_001',
      company: '阿里巴巴集团',
      industry: 'technology',
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
      id: 'report_002',
      company: '腾讯控股',
      industry: 'technology',
      type: '季度报告',
      score: 78.9,
      e_score: 75.2,
      s_score: 82.1,
      g_score: 79.4,
      status: 'processing',
      created_at: '2024-01-10',
      updated_at: '2024-01-18',
      creator: '李四'
    }
  ]
}

async function generatePDFReport(reportData) {
  // Mock PDF generation - in production, use a PDF library
  return `PDF Report for ${reportData.company} - Generated at ${new Date().toISOString()}`
}

async function generateExcelReport(reportData) {
  // Mock Excel generation - in production, use an Excel library
  return `Excel Report for ${reportData.company} - Generated at ${new Date().toISOString()}`
}