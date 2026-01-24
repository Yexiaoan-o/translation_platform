import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

interface Segment {
  id: number;
  source: string;
  target: string;
}

export default function Workspace() {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const [segments, setSegments] = useState<Segment[]>([]);
  const [translations, setTranslations] = useState<Record<number, string>>({});
  const [isSaving, setIsSaving] = useState(false);

  // 1. 初始化：从后端获取数据并同步到本地编辑状态
// 在 Workspace.tsx 里的加载部分
useEffect(() => {
  const loadData = async () => {
    const res = await fetch(`http://localhost:8000/api/v1/project/${projectId}`);
    const data = await res.json();
    
    setSegments(data.segments);
    
    // 【关键】同步 AI 预翻译的内容到本地 translations 状态
    const syncTrans: Record<number, string> = {};
    data.segments.forEach((s: any) => {
        // 如果 target 有值，就放入映射表，否则导出时后端找不到对应的 ID 就会出原文
        syncTrans[s.id] = s.target || "";
    });
    setTranslations(syncTrans);
  };
  loadData();
}, [projectId]);

  // 2. 实时保存句段到 DolphinDB
  const handleSaveSegment = async (id: number, text: string) => {
    setIsSaving(true);
    try {
      const res = await fetch(`http://localhost:8000/api/v1/project/${projectId}/save`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ seg_id: id, target: text })
      });
      if (!res.ok) throw new Error("保存失败");
    } catch (err) {
      console.error("保存错误:", err);
    } finally {
      // 延迟关闭提示，增加用户体感
      setTimeout(() => setIsSaving(false), 500);
    }
  };

  // 3. 导出最终 Markdown 文件
  const handleExport = async () => {
    try {
      // 发送当前的 translations 对象，确保所有手动修改和 AI 译文都被包含
      const res = await fetch(`http://localhost:8000/api/v1/export/${projectId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(translations)
      });
      
      if (!res.ok) throw new Error("导出失败");
      
      const data = await res.json();
      const blob = new Blob([data.markdown], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `translated_project.md`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      alert("导出失败，请检查后端服务");
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-50 font-sans">
      {/* 顶部导航栏 */}
      <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8 shadow-sm shrink-0">
        <div className="flex items-center gap-6">
          <button 
            onClick={() => navigate('/')}
            className="flex items-center gap-2 text-slate-500 hover:text-blue-600 transition-colors font-medium"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            项目列表
          </button>
          <div className="h-6 w-px bg-slate-200" />
          <div className="flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${isSaving ? 'bg-amber-400 animate-pulse' : 'bg-emerald-400'}`} />
            <span className="text-sm text-slate-500 font-medium">
              {isSaving ? "正在保存到数据库..." : "所有更改已保存"}
            </span>
          </div>
        </div>

        <button 
          onClick={handleExport}
          className="bg-slate-900 hover:bg-slate-800 text-white px-5 py-2 rounded-lg font-bold transition-all flex items-center gap-2 shadow-lg shadow-slate-200"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a2 2 0 002 2h12a2 2 0 002-2v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          导出译文
        </button>
      </header>

      {/* 翻译主体区 */}
      <main className="flex-1 overflow-hidden p-6">
        <div className="h-full max-w-7xl mx-auto bg-white rounded-2xl border border-slate-200 shadow-xl shadow-slate-200/50 flex flex-col">
          {/* 表头 */}
          <div className="grid grid-cols-2 bg-slate-50/50 border-b border-slate-200 shrink-0 text-slate-400 font-bold text-xs uppercase tracking-wider">
            <div className="px-8 py-4 border-r border-slate-200">原文内容 (Source)</div>
            <div className="px-8 py-4">译文编辑 (Translation)</div>
          </div>

          {/* 句段滚动列表 */}
          <div className="flex-1 overflow-y-auto divide-y divide-slate-100">
            {segments.map((s) => (
              <div key={s.id} className="grid grid-cols-2 group hover:bg-slate-50/80 transition-all">
                {/* 原文显示 */}
                <div className="px-8 py-6 text-slate-700 text-[15px] leading-relaxed border-r border-slate-100 font-mono break-words whitespace-pre-wrap">
                  {s.source}
                </div>
                
                {/* 译文编辑 */}
                <textarea
                  className="px-8 py-6 bg-transparent text-[15px] leading-relaxed text-slate-900 outline-none focus:bg-white focus:ring-4 focus:ring-blue-50 transition-all resize-none min-h-[120px]"
                  placeholder="请输入翻译内容..."
                  value={translations[s.id] || ""}
                  onChange={(e) => {
                    setTranslations({ ...translations, [s.id]: e.target.value });
                  }}
                  onBlur={(e) => handleSaveSegment(s.id, e.target.value)}
                />
              </div>
            ))}
            
            {segments.length === 0 && (
              <div className="flex flex-col items-center justify-center py-40 text-slate-400">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mb-4 opacity-20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <p className="italic">未解析出可翻译内容</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}