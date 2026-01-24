import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

interface Segment { id: number; source: string; target: string; }

export default function Workspace() {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const [segments, setSegments] = useState<Segment[]>([]);
  const [translations, setTranslations] = useState<Record<number, string>>({});

  useEffect(() => {
    fetch(`http://localhost:8000/api/v1/project/${projectId}`)
      .then(res => res.json())
      .then(data => {
        setSegments(data.segments);
        const t: any = {};
        data.segments.forEach((s: any) => t[s.id] = s.target);
        setTranslations(t);
      });
  }, [projectId]);

  const saveSeg = (id: number, val: string) => {
    fetch(`http://localhost:8000/api/v1/project/${projectId}/save`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ seg_id: id, target: val })
    });
  };

  const handleExport = async () => {
    const res = await fetch(`http://localhost:8000/api/v1/export/${projectId}`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(translations)
    });
    const data = await res.json();
    const blob = new Blob([data.markdown], { type: 'text/markdown' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = "export.md";
    a.click();
  };

  return (
    <div className="h-screen flex flex-col">
      <header className="p-4 border-b flex justify-between bg-white">
        <button onClick={() => navigate('/')}>← 返回</button>
        <button onClick={handleExport} className="bg-green-600 text-white px-4 py-1 rounded">导出</button>
      </header>
      <main className="flex-1 overflow-auto p-6 bg-gray-50">
        <div className="max-w-5xl mx-auto bg-white border">
          {segments.map(s => (
            <div key={s.id} className="grid grid-cols-2 border-b">
              <div className="p-4 bg-gray-50 border-r">{s.source}</div>
              <textarea 
                className="p-4 outline-none focus:bg-blue-50"
                value={translations[s.id] || ""}
                onChange={e => setTranslations({...translations, [s.id]: e.target.value})}
                onBlur={e => saveSeg(s.id, e.target.value)}
              />
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}