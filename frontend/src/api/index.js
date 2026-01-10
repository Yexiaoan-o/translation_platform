// API配置
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// 通用请求函数
async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  // 默认选项
  const defaultOptions = {};
  
  // 如果没有设置headers且不是FormData，则设置默认的Content-Type
  if (!options.headers && !(options.body instanceof FormData)) {
    defaultOptions.headers = {
      'Content-Type': 'application/json',
    };
  }
  
  // 合并选项
  const mergedOptions = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  };
  
  try {
    const response = await fetch(url, mergedOptions);
    
    // 检查响应状态
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`HTTP error! status: ${response.status}, detail: ${JSON.stringify(errorData)}`);
    }
    
    // 解析响应数据
    return await response.json();
  } catch (error) {
    console.error('API request error:', error);
    throw error;
  }
}

// 项目相关API
export const projectAPI = {
  // 获取项目列表
  getProjects: () => request('/projects'),
  
  // 创建项目
  createProject: (formData) => request('/projects', {
    method: 'POST',
    headers: {}, // 不设置Content-Type，让浏览器自动设置
    body: formData,
  }),
  
  // 删除项目
  deleteProject: (id) => request(`/projects/${id}`, {
    method: 'DELETE',
  }),
};

// 术语相关API
export const terminologyAPI = {
  // 获取术语列表
  getTerms: () => request('/terminology'),
  
  // 创建术语
  createTerm: (termData) => request('/terminology', {
    method: 'POST',
    body: JSON.stringify(termData),
  }),
  
  // 删除术语
  deleteTerm: (id) => request(`/terminology/${id}`, {
    method: 'DELETE',
  }),
};

// 翻译相关API
export const translationAPI = {
  // 获取翻译段落
  getSegments: (projectId) => request(`/translation/segments/${projectId}`),
  
  // 保存翻译
  saveTranslation: (segmentId, translation) => request(`/translation/segments/${segmentId}`, {
    method: 'PUT',
    body: JSON.stringify({ target: translation }),
  }),
};