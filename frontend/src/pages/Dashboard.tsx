import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface Project {
  id: string;
  name: string;
  status: string;
  created_at: string;
}

export default function Dashboard() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [useMT, setUseMT] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // 1. 获取项目列表
  const fetchProjects = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/projects');
      if (!res.ok) throw new Error("无法获取项目");
      const data = await res.json();
      setProjects(data);
    } catch (e) {
      console.error("Fetch projects error:", e);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  // 2. 处理文件上传
  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setLoading(true);
    const fd = new FormData();
    fd.append('file', file);
    
    try {
      // 将 useMT 状态作为查询参数传递给后端
      const res = await fetch(`http://localhost:8000/api/v1/parse?use_mt=${useMT}`, { 
        method: 'POST', 
        body: fd 
      });
      const data = await res.json();
      
      if (data.project_id) {
        navigate(`/workspace/${data.project_id}`);
      }
    } catch (err) {
      alert("上传并解析失败，请检查后端服务。");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // 3. 处理删除项目
  const handleDelete = async (e: React.MouseEvent, id: string, name: string) => {
    e.stopPropagation(); // 防止触发进入项目的导航
    if (!window.confirm(`确定要彻底删除项目 "${name}" 吗？此操作不可撤销。`)) return;

    try {
      const res = await fetch(`http://localhost:8000/api/v1/project/${id}`, {
        method: 'DELETE',
      });
      if (res.ok) {
        setProjects(prev => prev.filter(p => p.id !== id));
      } else {
        alert("删除失败");
      }
    } catch (err) {
      console.error("Delete error:", err);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 p-6 md:p-12">
      {/* 全屏加载遮罩 */}
      {loading && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-md z-50 flex flex-col items-center justify-center text-white">
          <div className="w-12 h-12 border-4 border-blue-400 border-t-transparent rounded-full animate-spin mb-4"></div>
          <p className="text-lg font-bold">AI 正在解析并预翻译文档...</p>
        </div>
      )}

      <div className="max-w-5xl mx-auto">
        {/* 顶部标题与控制区 */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
          <div>
            <h1 className="text-4xl font-black text-slate-900 tracking-tight">DolphinCAT</h1>
            <p className="text-slate-500 mt-2 font-medium">基于 DolphinDB 的高性能翻译协作平台</p>
          </div>

          <div className="flex items-center gap-4 bg-white p-3 rounded-2xl shadow-sm border border-slate-200">
            <label className="flex items-center gap-2 cursor-pointer px-3 py-2 hover:bg-slate-50 rounded-xl transition-colors">
              <input 
                type="checkbox" 
                checked={useMT} 
                onChange={(e) => setUseMT(e.target.checked)}
                className="w-5 h-5 accent-blue-600 rounded"
              />
              <span className="text-sm font-bold text-slate-700">开启 AI 预翻译</span>
            </label>
            <div className="w-px h-8 bg-slate-200"></div>
            <label className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2.5 rounded-xl font-bold cursor-pointer transition-all active:scale-95 shadow-lg shadow-blue-200">
              上传新项目
              <input type="file" className="hidden" onChange={handleUpload} accept=".md" />
            </label>
          </div>
        </div>

        {/* 项目列表 */}
        <div className="grid gap-4">
          <h2 className="text-sm font-bold text-slate-400 uppercase tracking-widest ml-1">项目记录 ({projects.length})</h2>
          
          {projects.map((project) => (
            <div 
              key={project.id} 
              onClick={() => navigate(`/workspace/${project.id}`)}
              className="group bg-white p-6 rounded-2xl border border-slate-200 flex justify-between items-center hover:border-blue-400 hover:shadow-xl hover:shadow-blue-500/5 transition-all cursor-pointer"
            >
              <div className="flex flex-col">
                <span className="text-lg font-bold text-slate-800 group-hover:text-blue-600 transition-colors">
                  {project.name}
                </span>
                <div className="flex items-center gap-4 mt-1">
                  <span className="text-xs font-mono text-slate-400 bg-slate-50 px-2 py-1 rounded">ID: {project.id.slice(0,8)}</span>
                  <span className="text-xs text-slate-400 font-medium">
                    创建于: {new Date(project.created_at).toLocaleString()}
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-3">
                {/* 删除按钮 */}
                <button 
                  onClick={(e) => handleDelete(e, project.id, project.name)}
                  className="p-2.5 text-slate-300 hover:text-red-500 hover:bg-red-50 rounded-xl transition-all"
                  title="删除项目"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M3 6h18m-2 0v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6m3 0V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2M10 11v6M14 11v6" />
                  </svg>
                </button>
                
                <div className="text-blue-600 bg-blue-50 p-2 rounded-xl group-hover:bg-blue-600 group-hover:text-white transition-all">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M5 12h14m-7-7 7 7-7 7" />
                  </svg>
                </div>
              </div>
            </div>
          ))}

          {projects.length === 0 && !loading && (
            <div className="bg-white border-2 border-dashed border-slate-200 rounded-3xl py-20 flex flex-col items-center justify-center text-slate-400">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" className="mb-4 opacity-20">
                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
                <polyline points="14 2 14 8 20 8" />
              </svg>
              <p className="font-medium italic">还没有项目，上传一个文件开始吧！</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}