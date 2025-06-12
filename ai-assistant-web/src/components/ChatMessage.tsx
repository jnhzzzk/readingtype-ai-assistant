"use client";

import React from 'react';
import { Message } from '@/lib/chat-service';
import { UserIcon, CodeBracketIcon, CpuChipIcon } from '@heroicons/react/24/outline';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface ChatMessageProps {
  message: Message;
  isLoading?: boolean;
  useMarkdown?: boolean;
}

export function ChatMessage({ message, isLoading, useMarkdown = false }: ChatMessageProps) {
  const isUser = message.role === 'user';
  const isSystem = message.role === 'system';
  const isFunction = message.role === 'function';

  // 渲染头像
  const Avatar = () => {
    const avatarClass = "w-8 h-8 rounded-full flex items-center justify-center";
    
    if (isUser) {
      return (
        <div className={avatarClass} style={{ background: 'var(--primary)' }}>
          <UserIcon className="w-4 h-4" style={{ color: 'var(--background)' }} />
        </div>
      );
    } else if (isFunction) {
      return (
        <div className={avatarClass} style={{ background: 'var(--warning)' }}>
          <CodeBracketIcon className="w-4 h-4" style={{ color: 'var(--background)' }} />
        </div>
      );
    } else {
      return (
        <div className={avatarClass} style={{ background: 'var(--surface-secondary)' }}>
          <CpuChipIcon className="w-4 h-4" style={{ color: 'var(--foreground)' }} />
        </div>
      );
    }
  };

  // 渲染消息内容
  const renderContent = () => {
    if (isFunction) {
      return (
        <div>
          <p className="font-medium text-sm mb-2" style={{ color: 'var(--warning)' }}>
            {message.name || '函数调用'}
          </p>
          <pre className="whitespace-pre-wrap text-xs p-2 rounded" 
            style={{ 
              background: 'var(--surface-secondary)', 
              color: 'var(--foreground)',
              fontFamily: 'monospace'
            }}>
            {message.content}
          </pre>
        </div>
      );
    } else if (useMarkdown && !isUser) {
      return (
        <div className="markdown-content">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {message.content}
          </ReactMarkdown>
        </div>
      );
    } else {
      return (
        <p className="whitespace-pre-wrap break-words">
          {message.content}
        </p>
      );
    }
  };

  // 如果是系统消息，使用不同的布局
  if (isSystem) {
    return (
      <div className="message-bubble system mx-auto max-w-md">
        <div className="text-center text-xs">
          {renderContent()}
        </div>
      </div>
    );
  }

  return (
    <div className={`flex items-start gap-3 mb-4 ${isUser ? 'flex-row-reverse' : ''}`}>
      <Avatar />
      
      <div className={`message-bubble ${isUser ? 'user' : isFunction ? 'function' : 'assistant'} max-w-[75%]`}>
        {isFunction && (
          <div className="flex items-center gap-2 mb-2 pb-2 border-b" 
            style={{ borderColor: 'var(--border)' }}>
            <CodeBracketIcon className="w-3 h-3" style={{ color: 'var(--warning)' }} />
            <span className="text-xs font-medium" style={{ color: 'var(--warning)' }}>
              函数执行
            </span>
          </div>
        )}
        
        <div className="relative">
          {renderContent()}
          
          {isLoading && (
            <div className="flex items-center gap-1 text-xs mt-2" 
              style={{ color: 'var(--foreground-muted)' }}>
              <div className="loading-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 