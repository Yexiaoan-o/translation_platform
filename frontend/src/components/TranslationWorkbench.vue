<template>
  <div class="flex flex-col h-screen bg-gray-100 dark:bg-gray-900">
    <!-- Header -->
    <header class="bg-white dark:bg-gray-800 shadow-md p-4">
      <div class="flex justify-between items-center">
        <h1 class="text-xl font-bold text-gray-900 dark:text-white">翻译工作台</h1>
        <div class="flex space-x-4">
          <button class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors">
            保存
          </button>
          <button class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors">
            导出
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 flex overflow-hidden">
      <!-- Source Text Column -->
      <div class="w-1/2 border-r border-gray-300 dark:border-gray-700 overflow-y-auto p-4">
        <h2 class="text-lg font-semibold mb-4 text-gray-900 dark:text-white">原文</h2>
        <div class="space-y-4">
          <div 
            v-for="(segment, index) in segments" 
            :key="index"
            class="p-4 rounded-lg bg-white dark:bg-gray-800 shadow-sm border-l-4"
            :class="getStatusBorderClass(segment.status)"
          >
            <div class="flex justify-between items-start">
              <span class="text-sm text-gray-500 dark:text-gray-400">#{{ index + 1 }}</span>
              <StatusIndicator :status="segment.status" />
            </div>
            <p class="mt-2 text-gray-900 dark:text-white">{{ segment.source }}</p>
          </div>
        </div>
      </div>

      <!-- Target Text Column -->
      <div class="w-1/2 overflow-y-auto p-4">
        <h2 class="text-lg font-semibold mb-4 text-gray-900 dark:text-white">译文</h2>
        <div class="space-y-4">
          <div 
            v-for="(segment, index) in segments" 
            :key="index"
            class="p-4 rounded-lg bg-white dark:bg-gray-800 shadow-sm"
          >
            <textarea
              v-model="segment.target"
              @keyup.ctrl.enter="nextSegment(index)"
              class="w-full p-2 border border-gray-300 dark:border-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-900 dark:text-white"
              rows="2"
              placeholder="请输入译文..."
              @input="updateStatus(index, 'edited')"
            ></textarea>
            <div class="flex justify-between items-center mt-2">
              <div class="flex space-x-2">
                <button 
                  class="px-2 py-1 text-xs bg-green-600 text-white rounded hover:bg-green-700 transition-colors"
                  @click="updateStatus(index, 'confirmed')"
                >
                  确认
                </button>
                <button 
                  class="px-2 py-1 text-xs bg-gray-600 text-white rounded hover:bg-gray-700 transition-colors"
                  @click="updateStatus(index, 'locked')"
                >
                  锁定
                </button>
              </div>
              <span class="text-sm text-gray-500 dark:text-gray-400">Ctrl+Enter 下一句</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import StatusIndicator from './StatusIndicator.vue';

// 模拟段落数据
const segments = ref([
  { id: 1, source: 'Hello, how are you?', target: '', status: 'untranslated' },
  { id: 2, source: 'I am fine, thank you.', target: '', status: 'untranslated' },
  { id: 3, source: 'What are you doing today?', target: '', status: 'untranslated' },
  { id: 4, source: 'I am working on a translation project.', target: '', status: 'untranslated' },
  { id: 5, source: 'This is a test paragraph for the translation platform.', target: '', status: 'untranslated' },
]);

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
</script>

<style scoped>
/* 可以添加组件特定的样式 */
</style>