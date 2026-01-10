<template>
  <span class="inline-block px-2 py-1 text-xs rounded-full" :class="getStatusClass(status)">
    {{ getStatusText(status) }}
  </span>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  status: {
    type: String,
    required: true,
    validator: (value) => {
      return ['untranslated', 'edited', 'confirmed', 'locked'].includes(value);
    }
  }
});

// 获取状态对应的文本
const getStatusText = (status) => {
  switch (status) {
    case 'untranslated':
      return '未翻译';
    case 'edited':
      return '已编辑';
    case 'confirmed':
      return '已确认';
    case 'locked':
      return '已锁定';
    default:
      return '未翻译';
  }
};

// 获取状态对应的样式类
const getStatusClass = (status) => {
  switch (status) {
    case 'untranslated':
      return 'bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-200';
    case 'edited':
      return 'bg-blue-200 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
    case 'confirmed':
      return 'bg-green-200 text-green-800 dark:bg-green-900 dark:text-green-200';
    case 'locked':
      return 'bg-purple-200 text-purple-800 dark:bg-purple-900 dark:text-purple-200';
    default:
      return 'bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-200';
  }
};
</script>

<style scoped>
/* 可以添加组件特定的样式 */
</style>