<template>
  <div id="app" class="app-container">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(() => {
  // 移除加载动画
  const loading = document.querySelector('.loading')
  if (loading) {
    setTimeout(() => {
      loading.style.opacity = '0'
      setTimeout(() => {
        loading.remove()
      }, 300)
    }, 1000)
  }
})
</script>

<style lang="scss">
/* 全局字体设置 */
@font-face {
  font-family: 'Goudy Old Style';
  src: url('/static/Goudy Old Style Regular.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'EduKai';
  src: url('/static/edukai-4.0.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

* {
  font-family: 'EduKai', 'Goudy Old Style', serif;
}

.app-container {
  min-height: 100vh;
  background: var(--bg-color);
}

// 全局滚动条样式 - 黑白风格
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--bg-secondary);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: var(--border-dark);
  border-radius: 4px;
  
  &:hover {
    background: var(--accent-color);
  }
}

// Element Plus 主题定制 - 黑白专业风格
.el-card {
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  
  &:hover {
    box-shadow: var(--shadow-md);
    border-color: var(--border-dark);
  }
}

.el-button {
  border-radius: var(--radius-md);
  font-weight: 500;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
  }
}

.el-input__wrapper {
  border-radius: var(--radius-md);
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  
  &:hover {
    border-color: var(--border-dark);
  }
}

.el-table {
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
}
</style>