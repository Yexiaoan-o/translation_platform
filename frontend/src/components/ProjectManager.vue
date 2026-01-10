<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <!-- Header -->
    <header class="bg-white dark:bg-gray-800 shadow-md p-4">
      <div class="flex justify-between items-center">
        <h1 class="text-xl font-bold text-gray-900 dark:text-white">翻译平台</h1>
        <nav class="flex space-x-6">
          <a href="/" class="text-blue-600 dark:text-blue-400 hover:underline">项目管理</a>
          <a href="/workbench" class="text-gray-600 dark:text-gray-300 hover:underline">翻译工作台</a>
          <a href="/terminology" class="text-gray-600 dark:text-gray-300 hover:underline">术语库</a>
        </nav>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto p-6">
      <!-- Create Project Form -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <h2 class="text-lg font-semibold mb-4 text-gray-900 dark:text-white">创建新项目</h2>
        <form @submit.prevent="createProject" enctype="multipart/form-data">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label for="projectName" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">项目名称</label>
              <input 
                type="text" 
                id="projectName" 
                v-model="projectForm.name" 
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-900 dark:text-white"
                required
              >
            </div>
            <div>
              <label for="sourceLanguage" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">源语言</label>
              <select 
                id="sourceLanguage" 
                v-model="projectForm.source_language" 
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-900 dark:text-white"
                required
              >
                <option value="en">英语 (EN)</option>
                <option value="zh">中文 (ZH)</option>
                <option value="ja">日语 (JA)</option>
                <option value="ko">韩语 (KO)</option>
                <option value="fr">法语 (FR)</option>
                <option value="de">德语 (DE)</option>
              </select>
            </div>
          </div>
          
          <div class="mb-4">
            <label for="targetLanguage" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">目标语言</label>
            <select 
              id="targetLanguage" 
              v-model="projectForm.target_language" 
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-900 dark:text-white"
              required
            >
              <option value="zh">中文 (ZH)</option>
              <option value="en">英语 (EN)</option>
              <option value="ja">日语 (JA)</option>
              <option value="ko">韩语 (KO)</option>
              <option value="fr">法语 (FR)</option>
              <option value="de">德语 (DE)</option>
            </select>
          </div>
          
          <div class="mb-4">
            <label for="files" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">上传文件</label>
            <input 
              type="file" 
              id="files" 
              multiple 
              accept=".md,.docx,.pdf,.txt" 
              @change="handleFileUpload" 
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-900 dark:text-white"
              required
            >
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">支持的格式：Markdown (.md), Word (.docx), PDF (.pdf), 文本 (.txt)</p>
          </div>
          
          <div v-if="selectedFiles.length > 0" class="mb-4">
            <h3 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">已选择的文件：</h3>
            <ul class="list-disc list-inside text-sm text-gray-600 dark:text-gray-300">
              <li v-for="(file, index) in selectedFiles" :key="index">{{ file.name }}</li>
            </ul>
          </div>
          
          <button 
                  type="submit" 
                  class="px-4 py-2 border-2 border-blue-600 text-blue-600 rounded-md hover:bg-blue-50 transition-colors font-semibold text-base"
                  :disabled="isSubmitting"
                >
                  {{ isSubmitting ? '创建中...' : '创建项目' }}
                </button>
        </form>
      </div>

      <!-- Project List -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 class="text-lg font-semibold mb-4 text-gray-900 dark:text-white">项目列表</h2>
        <div v-if="projects.length === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
          暂无项目，请创建新项目
        </div>
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-900">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">项目名称</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">源语言</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">目标语言</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">创建时间</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">操作</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-for="project in projects" :key="project.id">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ project.name }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">{{ project.source_language }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">{{ project.target_language }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">{{ formatDate(project.created_at) }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button 
                    @click="openWorkbench(project.id)" 
                    class="text-blue-600 hover:text-blue-800 mr-4 transition-colors font-medium"
                  >
                    翻译
                  </button>
                  <button 
                    @click="deleteProject(project.id)" 
                    class="text-red-600 hover:text-red-800 transition-colors font-medium"
                  >
                    删除
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { projectAPI } from '../api';

// 项目表单数据
const projectForm = ref({
  name: '',
  source_language: 'en',
  target_language: 'zh'
});

// 选中的文件
const selectedFiles = ref([]);

// 提交状态
const isSubmitting = ref(false);

// 项目列表
const projects = ref([]);

// 处理文件上传
const handleFileUpload = (event) => {
  selectedFiles.value = Array.from(event.target.files);
};

// 创建项目
const createProject = async () => {
  isSubmitting.value = true;
  try {
    // 创建 FormData 对象
    const formData = new FormData();
    formData.append('name', projectForm.value.name);
    formData.append('source_language', projectForm.value.source_language);
    formData.append('target_language', projectForm.value.target_language);
    
    // 添加文件
    selectedFiles.value.forEach(file => {
      formData.append('files', file);
    });
    
    // 调用API创建项目
    const newProject = await projectAPI.createProject(formData);
    
    // 添加到项目列表
    projects.value.unshift(newProject);
    
    // 重置表单
    projectForm.value = {
      name: '',
      source_language: 'en',
      target_language: 'zh'
    };
    selectedFiles.value = [];
    
    // 显示成功消息
    alert('项目创建成功！');
  } catch (error) {
    console.error('Error creating project:', error);
    alert('创建项目失败，请重试');
  } finally {
    isSubmitting.value = false;
  }
};

// 获取项目列表
const fetchProjects = async () => {
  try {
    // 调用API获取项目列表
    projects.value = await projectAPI.getProjects();
  } catch (error) {
    console.error('Error fetching projects:', error);
    alert('获取项目列表失败，请刷新页面重试');
  }
};

// 打开翻译工作台
const openWorkbench = (projectId) => {
  // 导航到翻译工作台页面，并传递项目 ID
  window.location.href = `/workbench?projectId=${projectId}`;
};

// 删除项目
const deleteProject = async (projectId) => {
  if (confirm('确定要删除这个项目吗？')) {
    try {
      // 调用API删除项目
      await projectAPI.deleteProject(projectId);
      
      // 从列表中移除项目
      projects.value = projects.value.filter(project => project.id !== projectId);
      
      // 显示成功消息
      alert('项目删除成功！');
    } catch (error) {
      console.error('Error deleting project:', error);
      alert('删除项目失败，请重试');
    }
  }
};

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString();
};

// 页面加载时获取项目列表
onMounted(() => {
  fetchProjects();
});
</script>

<style scoped>
/* 可以添加组件特定的样式 */
</style>