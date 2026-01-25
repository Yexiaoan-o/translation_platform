import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

// 1. 定义严格的接口类型
interface Segment {
  id: number;
  source: string;
  target: string;
}

export default function Workspace() {
  // 获取路由中的 projectId 参数
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();

  // 2. 正确初始化状态，避免 'never' 类型报错
  const [segments, setSegments] = useState<Segment[]>([]);
  const [translations, setTranslations] = useState<Record<number, string>>({});
  const [isExporting, setIsExporting] = useState(false);
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'saved'>('idle');

  // 3. 初始数据加载
  useEffect(() => {
    const loadProject = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/v1/project/${projectId}`);
        if (!res.ok) throw new Error("项目加载失败");
        const data = await res.json();
        
        const fetchedSegments: Segment[] = data.segments || [];
        setSegments(fetchedSegments);

        // 将已有译文同步到 state
        const initialTrans: Record<number, string> = {};
        fetchedSegments.forEach(s => {
          if (s.target) initialTrans[s.id] = s.target;
        });
        setTranslations(initialTrans);
      } catch (err) {
        console.error(err);
        alert("无法获取项目数据，请检查后端和数据库。");
      }
    };

    if (projectId) loadProject();
  }, [projectId]);

  // 4. 实时保存逻辑 (当输入框失去焦点时触发)
  const handleSaveProgress = async (segId: number, text: string) => {
    setSaveStatus('saving');
    try {
      const response = await fetch(`http://localhost:8000/api/v1/project/${projectId}/save`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // 后端 API 接收 target 和 seg_id
        body: JSON.stringify({ target: text, seg_id: segId })
      });
      if (response.ok) {
        setSaveStatus('saved');
        setTimeout(() => setSaveStatus('idle'), 2000);
      }
    } catch (err) {
      console.error("保存失败:", err);
      setSaveStatus('idle');
    }
  };

  // 5. 导出文件逻辑
  const handleExport = async () => {
    setIsExporting(true);
    try {
      const res = await fetch(`http://localhost:8000/api/v1/export/${projectId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(translations)
      });
      const data = await res.json();
      
      const blob = new Blob([data.markdown], { type: 'text/markdown' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `translated_${projectId?.slice(0, 5)}.md`;
      a.click();
    } catch (err) {
      alert("导出失败");
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-50">
      {/* 顶部导航栏 */}
      <header className="bg-white border-b px-6 py-3 flex justify-between items-center shadow-sm">
        <div className="flex items-center gap-4">
          <button 
            onClick={() => navigate('/')}
            className="text-slate-500 hover:text-blue-600 transition-colors"
          >
            ← 返回列表
          </button>
          <div className="h-6 w-px bg-slate-200"></div>
          <h2 className="font-semibold text-slate-700">
            项目 ID: <span className="font-mono text-sm bg-slate-100 px-2 py-1 rounded">{projectId?.slice(0, 8)}...</span>
          </h2>
          {saveStatus === 'saving' && <span className="text-xs text-blue-500 animate-pulse">正在保存...</span>}
          {saveStatus === 'saved' && <span className="text-xs text-green-500">已保存</span>}
        </div>
        
        <button 
          onClick={handleExport}
          disabled={isExporting}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 text-white px-6 py-2 rounded-lg font-medium transition-all shadow-sm"
        >
          {isExporting ? '生成中...' : '导出译文'}
        </button>
      </header>

      {/* 翻译主体区 */}
      <main className="flex-1 overflow-y-auto p-6">
        <div className="max-w-6xl mx-auto bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
          {/* 表头 */}
          <div className="grid grid-cols-2 bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-500 uppercase tracking-wider">
            <div className="p-4 border-r border-slate-200">原文 (Source)</div>
            <div className="p-4">译文 (Target)</div>
          </div>

          {/* 句段列表 */}
          <div className="divide-y divide-slate-100">
            {segments.map((seg) => (
              <div key={seg.id} className="grid grid-cols-2 group hover:bg-blue-50/20 transition-colors">
                {/* 原文列 */}
                <div className="p-5 text-slate-700 leading-relaxed border-r border-slate-100 whitespace-pre-wrap">
                  {seg.source}
                </div>
                
                {/* 译文列 */}
                <div className="p-0 bg-transparent">
                  <textarea 
                    className="w-full h-full min-h-[120px] p-5 bg-transparent outline-none focus:bg-white focus:ring-1 focus:ring-blue-200 transition-all resize-none text-slate-800"
                    placeholder="点击此处开始翻译..."
                    value={translations[seg.id] || ""}
                    onChange={(e) => setTranslations({
                      ...translations, 
                      [seg.id]: e.target.value
                    })}
                    // 失去焦点时自动保存到 DolphinDB
                    onBlur={(e) => handleSaveProgress(seg.id, e.target.value)}
                  />
                </div>
              </div>
            ))}
          </div>

          {segments.length === 0 && (
            <div className="p-20 text-center text-slate-400">
              数据加载中或项目为空...
            </div>
          )}
        </div>
      </main>
    </div>
  );
}