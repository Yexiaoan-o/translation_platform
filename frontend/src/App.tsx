import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Workspace from './pages/Workspace';

function App() {
  return (
    // BrowserRouter 监听浏览器地址栏的变化
    <BrowserRouter>
      <div className="min-h-screen bg-slate-50">
        <Routes>
          {/* 首页：展示项目列表和上传入口 */}
          <Route path="/" element={<Dashboard />} />

          {/* 工作台页：:projectId 是一个动态参数，用于获取特定的项目数据 */}
          <Route path="/workspace/:projectId" element={<Workspace />} />

          {/* 404 页面处理（可选） */}
          <Route path="*" element={
            <div className="flex flex-col items-center justify-center h-screen">
              <h1 className="text-4xl font-bold text-slate-800">404</h1>
              <p className="text-slate-600">页面跑丢了</p>
              <a href="/" className="mt-4 text-blue-600 hover:underline">返回首页</a>
            </div>
          } />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;