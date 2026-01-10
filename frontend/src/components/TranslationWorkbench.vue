<template>
  <div class="flex flex-col h-screen bg-gray-100 dark:bg-gray-900">
    <!-- Header -->
    <header class="bg-white dark:bg-gray-800 shadow-md p-4">
      <div class="flex justify-between items-center">
          <h1 class="text-xl font-bold text-gray-900 dark:text-white">翻译工作台</h1>
          <div class="flex space-x-4">
            <button class="px-4 py-2 border-2 border-blue-600 text-blue-600 rounded-md hover:bg-blue-50 transition-colors font-semibold">
              保存
            </button>
            <button class="px-4 py-2 border-2 border-green-600 text-green-600 rounded-md hover:bg-green-50 transition-colors font-semibold">
              导出
            </button>
          </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 overflow-hidden">
      <div class="h-full overflow-y-auto">
        <!-- Segment List -->
        <div class="space-y-4 p-4">
          <!-- Segment Item -->
          <div 
            v-for="(segment, index) in segments" 
            :key="index"
            class="flex flex-col md:flex-row gap-4"
          >
            <!-- Source Text (Left) -->
            <div class="flex-1 bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4 border-l-4"
                 :class="getStatusBorderClass(segment.status)">
              <div class="flex justify-between items-start">
                <span class="text-sm text-gray-500 dark:text-gray-400">#{{ index + 1 }}</span>
                <StatusIndicator :status="segment.status" />
              </div>
              <p class="mt-2 text-gray-900 dark:text-white">{{ segment.source_text }}</p>
            </div>

            <!-- Target Text (Right) -->
            <div class="flex-1 bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4">
              <textarea
                v-model="segment.target_text"
                @keyup.ctrl.enter="nextSegment(index)"
                class="w-full p-2 border border-gray-300 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-900 dark:text-white"
                rows="4"
                placeholder="请输入译文..."
                @input="updateStatus(index, 'edited')"
              ></textarea>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import StatusIndicator from './StatusIndicator.vue';
import { translationAPI } from '../api';

// 段落数据
const segments = ref([]);

// 获取URL参数中的项目ID
const getProjectId = () => {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('projectId');
};

// 获取翻译段落
const fetchSegments = async () => {
  try {
    const projectId = getProjectId();
    if (!projectId) {
      alert('请先选择一个项目');
      return;
    }
    
    // 调用API获取段落
    segments.value = await translationAPI.getSegments(projectId);
  } catch (error) {
    console.error('Error fetching segments:', error);
    alert('获取翻译段落失败，请重试');
  }
};

// 获取状态对应的边框颜色
const getStatusBorderClass = (status) => {
  switch (status) {
    case 'untranslated':
      return 'border-gray-300 dark:border-gray-700';
    case 'edited':
      return 'border-blue-500';
    case 'confirmed':
      return 'border-green-500';
    case 'locked':
      return 'border-purple-500';
    default:
      return 'border-gray-300 dark:border-gray-700';
  }
};

// 更新段落状态
const updateStatus = (index, status) => {
  segments.value[index].status = status;
};

// 跳转到下一个段落
const nextSegment = (currentIndex) => {
  if (currentIndex < segments.value.length - 1) {
    segments.value[currentIndex].status = 'confirmed';
    // 这里可以添加自动滚动到下一个段落的逻辑
  }
};

// 页面加载时获取段落
onMounted(() => {
  fetchSegments();
});
</script>

<style scoped>
/* 可以添加组件特定的样式 */
</style>