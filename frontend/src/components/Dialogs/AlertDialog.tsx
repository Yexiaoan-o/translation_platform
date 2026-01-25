//import React from 'react';

interface AlertDialogProps {
  isOpen: boolean;
  title: string;
  message: string;
  type?: 'error' | 'success' | 'info';
  onClose: () => void;
}

export default function AlertDialog({ 
  isOpen, 
  title, 
  message, 
  type = 'info',
  onClose 
}: AlertDialogProps) {
  if (!isOpen) return null;

  // 根据类型确定图标和颜色
  const getIcon = () => {
    switch (type) {
      case 'error':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10" />
            <line x1="15" y1="9" x2="9" y2="15" />
            <line x1="9" y1="9" x2="15" y2="15" />
          </svg>
        );
      case 'success':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10" />
            <path d="m9 12 2 2 4-4" />
          </svg>
        );
      default:
        return (
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10" />
            <path d="M12 16v-4" />
            <path d="M12 8h.01" />
          </svg>
        );
    }
  };

  const getColor = () => {
    switch (type) {
      case 'error':
        return 'text-red-500';
      case 'success':
        return 'text-green-500';
      default:
        return 'text-blue-500';
    }
  };

  return (
    <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-md z-50 flex items-center justify-center">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md p-8">
        {/* 图标 */}
        <div className={`flex justify-center mb-6 ${getColor()}`}>
          {getIcon()}
        </div>
        
        {/* 标题 */}
        <h3 className="text-xl font-bold text-slate-800 mb-4 text-center">{title}</h3>
        
        {/* 消息 */}
        <p className="text-slate-600 mb-8 text-center">{message}</p>
        
        {/* 按钮 */}
        <div className="flex justify-center">
          <button
            onClick={onClose}
            className="px-8 py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition-colors shadow-md shadow-blue-200"
          >
            确定
          </button>
        </div>
      </div>
    </div>
  );
}
