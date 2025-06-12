"use client";

import React from 'react';
import { 
  CpuChipIcon,
  DocumentTextIcon,
  BookOpenIcon
} from '@heroicons/react/24/outline';

interface QuickActionsProps {
  onAction: (action: string, data?: string) => void;
  onDictionary: () => void;
  onHelp: () => void;
}

export function QuickActions({ onAction, onDictionary, onHelp }: QuickActionsProps) {
  const actions = [
    {
      id: 'smart-coding',
      label: '智能编码',
      icon: CpuChipIcon,
      description: '生成或解析ReadingType编码',
      action: 'quick-generate',
      data: '我想使用ReadingType编码功能，请告诉我可以帮助我生成新编码或解析现有编码。'
    },
    {
      id: 'dictionary',
      label: '编码字典',
      icon: BookOpenIcon,
      description: '查看编码字典和规范',
      onClick: onDictionary
    },
    {
      id: 'help',
      label: '使用帮助',
      icon: DocumentTextIcon,
      description: '查看详细使用指南',
      onClick: onHelp
    }
  ];

  const handleAction = (action: any) => {
    if (action.onClick) {
      action.onClick();
    } else if (action.action) {
      onAction(action.action, action.data);
    } else {
      onAction(action.id);
    }
  };

  return (
    <div>
      <h3 className="text-sm font-medium mb-3" style={{ color: 'var(--foreground)' }}>
        功能菜单
      </h3>
      
      <div className="space-y-2">
        {actions.map((action) => (
          <button
            key={action.id}
            onClick={() => handleAction(action)}
            className="w-full p-3 rounded text-left transition-colors"
            style={{
              background: 'var(--surface-secondary)',
              border: '1px solid var(--border)'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = 'var(--foreground-muted)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = 'var(--border)';
            }}
          >
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded flex items-center justify-center"
                style={{ background: 'var(--primary)' }}>
                <action.icon className="w-4 h-4" style={{ color: 'var(--background)' }} />
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-sm" style={{ color: 'var(--foreground)' }}>
                  {action.label}
                </p>
                <p className="text-xs mt-1" style={{ color: 'var(--foreground-secondary)' }}>
                  {action.description}
                </p>
              </div>
            </div>
          </button>
        ))}
      </div>

      {/* AI对话专用提示 */}
      <div className="mt-6 p-3 rounded border" 
        style={{ 
          background: 'var(--surface)',
          borderColor: 'var(--border)'
        }}>
        <p className="text-xs font-medium mb-2" style={{ color: 'var(--foreground)' }}>
          AI智能编码助手
        </p>
        <div className="space-y-1 text-xs" style={{ color: 'var(--foreground-secondary)' }}>
          <p>• <strong>生成编码：</strong>描述测量需求，如"三相有功电能，15分钟间隔"</p>
          <p>• <strong>解析编码：</strong>提供编码，如"解析编码：0.0.2.1.1.1.12.0.0.0.0.0.0.0.72.0"</p>
        </div>
      </div>
    </div>
  );
} 