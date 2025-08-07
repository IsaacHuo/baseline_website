# ESG评分系统部署指南

本指南将帮助您将ESG评分系统部署到Vercel，并设置GitHub Actions自动部署流水线。

## 🚀 快速部署步骤

### 1. 准备工作

确保您已经：
- 拥有GitHub账户
- 拥有Vercel账户（可以用GitHub账户登录）
- 项目代码已推送到GitHub仓库

### 2. 在Vercel中创建项目

1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 "New Project" 按钮
3. 选择 "Import Git Repository"
4. 选择您的GitHub仓库
5. 配置项目设置：
   - **Framework Preset**: Vite
   - **Root Directory**: `./` (保持默认)
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

6. 点击 "Deploy" 开始首次部署

### 3. 获取Vercel配置信息

部署完成后，您需要获取以下信息用于GitHub Actions：

#### 3.1 获取Project ID
1. 在Vercel项目页面，点击 "Settings"
2. 在 "General" 标签页中找到 "Project ID"
3. 复制这个ID

#### 3.2 获取Team ID (Organization ID)
1. 在Vercel Dashboard中，点击右上角的团队名称
2. 选择 "Team Settings"
3. 在 "General" 标签页中找到 "Team ID"
4. 如果是个人账户，则使用您的用户名

#### 3.3 创建API Token
1. 访问 [Vercel Tokens页面](https://vercel.com/account/tokens)
2. 点击 "Create Token"
3. 输入Token名称（如："ESG-System-Deploy"）
4. 选择适当的权限范围
5. 点击 "Create" 并复制生成的Token

### 4. 配置GitHub Secrets

1. 在GitHub仓库页面，点击 "Settings"
2. 在左侧菜单中选择 "Secrets and variables" > "Actions"
3. 点击 "New repository secret" 添加以下三个密钥：

```
VERCEL_TOKEN=your_vercel_api_token
VERCEL_ORG_ID=your_team_id_or_username
VERCEL_PROJECT_ID=your_project_id
```

**重要提示**：
- `VERCEL_TOKEN`: 步骤3.3中创建的API Token
- `VERCEL_ORG_ID`: 步骤3.2中获取的Team ID或用户名
- `VERCEL_PROJECT_ID`: 步骤3.1中获取的Project ID

### 5. 触发自动部署

配置完成后，每次推送代码到main分支都会自动触发部署：

```bash
git add .
git commit -m "Setup automatic deployment"
git push origin main
```

### 6. 验证部署

1. 在GitHub仓库的 "Actions" 标签页中查看工作流运行状态
2. 部署成功后，访问Vercel提供的域名查看网站
3. 检查所有功能是否正常工作

## 🔧 高级配置

### 自定义域名

1. 在Vercel项目设置中，选择 "Domains"
2. 添加您的自定义域名
3. 按照提示配置DNS记录

### 环境变量

如果需要添加环境变量：

1. 在Vercel项目设置中，选择 "Environment Variables"
2. 添加所需的环境变量
3. 重新部署项目

### 分支部署

- **生产环境**: main/master分支自动部署到生产环境
- **预览环境**: 其他分支和Pull Request自动创建预览部署

## 🐛 常见问题

### 问题1：部署失败 - "Build failed"

**解决方案**：
1. 检查 `package.json` 中的构建脚本
2. 确保所有依赖都已正确安装
3. 查看构建日志中的具体错误信息

### 问题2：API请求失败

**解决方案**：
1. 检查 `vercel.json` 配置是否正确
2. 确保API路由配置正确
3. 检查CORS设置

### 问题3：静态资源加载失败

**解决方案**：
1. 检查 `vite.config.js` 中的base配置
2. 确保资源路径使用相对路径
3. 检查构建输出目录设置

### 问题4：GitHub Actions权限错误

**解决方案**：
1. 确认所有Secrets都已正确设置
2. 检查Vercel Token权限
3. 验证Project ID和Organization ID是否正确

## 📊 监控和维护

### 性能监控

- Vercel自动提供性能分析
- 查看 "Analytics" 标签页了解网站性能
- 使用Lighthouse CI进行持续性能监控

### 日志查看

- 在Vercel项目页面查看函数日志
- 在GitHub Actions中查看部署日志
- 使用浏览器开发者工具调试前端问题

### 更新和维护

1. **依赖更新**：定期更新npm依赖
2. **安全扫描**：GitHub Actions包含安全审计
3. **备份**：Vercel自动保存部署历史

## 🔗 有用链接

- [Vercel文档](https://vercel.com/docs)
- [GitHub Actions文档](https://docs.github.com/en/actions)
- [Vue.js文档](https://vuejs.org/)
- [Vite文档](https://vitejs.dev/)

## 💡 最佳实践

1. **分支策略**：使用feature分支开发，通过PR合并到main
2. **代码审查**：设置PR审查规则
3. **测试**：在合并前运行测试
4. **监控**：设置错误监控和性能监控
5. **备份**：定期备份重要数据

---

如果遇到问题，请查看GitHub仓库的Issues页面或创建新的Issue。