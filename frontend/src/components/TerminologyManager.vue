<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <!-- Header -->
    <header class="bg-white dark:bg-gray-800 shadow-md p-4">
      <div class="flex justify-between items-center">
        <h1 class="text-xl font-bold text-gray-900 dark:text-white">翻译平台</h1>
        <nav class="flex space-x-6">
          <a href="/" class="text-gray-600 dark:text-gray-300 hover:underline">项目管理</a>
          <a href="/workbench" class="text-gray-600 dark:text-gray-300 hover:underline">翻译工作台</a>
          <a href="/terminology" class="text-blue-600 dark:text-blue-400 hover:underline">术语库</a>
        </nav>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto p-6">
      <!-- Create Term Form -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-8">
        <h2 class="text-lg font-semibold mb-4 text-gray-900 dark:text-white">添加新术语</h2>
        <form @submit.prevent="createTerm">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label for="sourceTerm" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">源术语</label>
              <input 
                type="text" 
                id="sourceTerm" 
                v-model="termForm.source_term" 
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-900 dark:text-white"
                required
              >
            </div>
            <div>
              <label for="targetTerm" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">目标术语</label>
              <input 
                type="text" 
                id="targetTerm" 
                v-model="termForm.target_term" 
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-900 dark:text-white"
                required
              >
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label for="sourceLanguage" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">源语言</label>
              <select 
                id="sourceLanguage" 
                v-model="termForm.source_language" 
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
            <div>
              <label for="targetLanguage" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">目标语言</label>
              <select 
                id="targetLanguage" 
                v-model="termForm.target_language" 
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
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label for="domain" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">领域</label>
              <input 
                type="text" 
                id="domain" 
                v-model="termForm.domain" 
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-900 dark:text-white"
                placeholder="例如：计算机科学"
              >
            </div>
          </div>
          
          <div class="mb-4">
            <label for="definition" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">定义</label>
            <textarea 
              id="definition" 
              v-model="termForm.definition" 
              rows="3" 
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-900 dark:text-white"
              placeholder="请输入术语定义..."
            ></textarea>
          </div>
          
          <button 
            type="submit" 
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors shadow-sm font-medium"
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? '添加中...' : '添加术语' }}
          </button>
        </form>
      </div>

      <!-- Term List -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
        <h2 class="text-lg font-semibold mb-4 text-gray-900 dark:text-white">术语列表</h2>
        <div class="mb-4">
          <div class="flex space-x-4">
            <select 
              v-model="filter.source_language" 
              class="px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-900 dark:text-white"
            >
              <option value="">所有源语言</option>
              <option value="en">英语 (EN)</option>
              <option value="zh">中文 (ZH)</option>
              <option value="ja">日语 (JA)</option>
              <option value="ko">韩语 (KO)</option>
              <option value="fr">法语 (FR)</option>
              <option value="de">德语 (DE)</option>
            </select>
            <select 
              v-model="filter.target_language" 
              class="px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-900 dark:text-white"
            >
              <option value="">所有目标语言</option>
              <option value="zh">中文 (ZH)</option>
              <option value="en">英语 (EN)</option>
              <option value="ja">日语 (JA)</option>
              <option value="ko">韩语 (KO)</option>
              <option value="fr">法语 (FR)</option>
              <option value="de">德语 (DE)</option>
            </select>
            <input 
              type="text" 
              v-model="filter.domain" 
              placeholder="按领域筛选..." 
              class="px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-900 dark:text-white"
            >
            <button 
              @click="applyFilters" 
              class="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors"
            >
              筛选
            </button>
          </div>
        </div>
        
        <div v-if="terms.length === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
          暂无术语，请添加新术语
        </div>
        <div v-else class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-900">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">源术语</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">目标术语</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">源语言</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">目标语言</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">领域</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">操作</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-for="term in terms" :key="term.id">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ term.source_term }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">{{ term.target_term }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">{{ term.source_language }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">{{ term.target_language }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">{{ term.domain || '-' }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button 
                    @click="editTerm(term)" 
                    class="text-blue-600 hover:text-blue-800 mr-4 transition-colors font-medium"
                  >
                    编辑
                  </button>
                  <button 
                    @click="deleteTerm(term.id)" 
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
import { terminologyAPI } from '../api';

// 术语表单数据
const termForm = ref({
  source_term: '',
  target_term: '',
  source_language: 'en',
  target_language: 'zh',
  domain: '',
  definition: ''
});

// 提交状态
const isSubmitting = ref(false);

// 术语列表
const terms = ref([]);

// 筛选条件
const filter = ref({
  source_language: '',
  target_language: '',
  domain: ''
});

// 创建术语
const createTerm = async () => {
  isSubmitting.value = true;
  try {
    // 调用API创建术语
    const newTerm = await terminologyAPI.createTerm(termForm.value);
    
    // 添加到术语列表
    terms.value.unshift(newTerm);
    
    // 重置表单
    termForm.value = {
      source_term: '',
      target_term: '',
      source_language: 'en',
      target_language: 'zh',
      domain: '',
      definition: ''
    };
    
    // 显示成功消息
    alert('术语添加成功！');
  } catch (error) {
    console.error('Error creating term:', error);
    alert('添加术语失败，请重试');
  } finally {
    isSubmitting.value = false;
  }
};

// 获取术语列表
const fetchTerms = async () => {
  try {
    // 调用API获取术语列表
    terms.value = await terminologyAPI.getTerms();
  } catch (error) {
    console.error('Error fetching terms:', error);
    alert('获取术语列表失败，请刷新页面重试');
  }
};

// 编辑术语
const editTerm = (term) => {
  // 实际项目中应该打开编辑对话框
  console.log('Editing term:', term);
  alert('编辑功能开发中...');
};

// 删除术语
const deleteTerm = async (termId) => {
  if (confirm('确定要删除这个术语吗？')) {
    try {
      // 调用API删除术语
      await terminologyAPI.deleteTerm(termId);
      
      // 从列表中移除术语
      terms.value = terms.value.filter(term => term.id !== termId);
      
      // 显示成功消息
      alert('术语删除成功！');
    } catch (error) {
      console.error('Error deleting term:', error);
      alert('删除术语失败，请重试');
    }
  }
};

// 应用筛选
const applyFilters = async () => {
  try {
    // 模拟 API 调用
    // 实际项目中应该使用 axios 等库调用后端 API
    console.log('Applying filters:', filter.value);
    
    // 模拟筛选结果
    // 实际项目中应该根据筛选条件从后端获取数据
    alert('筛选功能开发中...');
  } catch (error) {
    console.error('Error applying filters:', error);
  }
};

// 页面加载时获取术语列表
onMounted(() => {
  fetchTerms();
});
</script>

<style scoped>
/* 可以添加组件特定的样式 */
</style>