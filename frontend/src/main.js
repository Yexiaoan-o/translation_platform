import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'
import ProjectManager from './components/ProjectManager.vue'
import TranslationWorkbench from './components/TranslationWorkbench.vue'

// 创建路由
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'ProjectManager',
      component: ProjectManager
    },
    {
      path: '/workbench',
      name: 'TranslationWorkbench',
      component: TranslationWorkbench
    },
    {
      path: '/terminology',
      name: 'Terminology',
      component: () => import('./components/TerminologyManager.vue')
    }
  ]
});

// 创建应用并使用路由
const app = createApp(App)
app.use(router)
app.mount('#app')
