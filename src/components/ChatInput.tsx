"use client";

import React, { useState, useRef, useEffect } from 'react';
import { PaperAirplaneIcon } from '@heroicons/react/24/outline';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

export function ChatInput({ onSendMessage, disabled = false, placeholder = "输入您的消息..." }: ChatInputProps) {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const adjustHeight = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 120) + 'px';
    }
  };

  useEffect(() => {
    adjustHeight();
  }, [message]);

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="flex items-end gap-3 p-3 rounded border"
        style={{ 
          background: 'var(--surface)',
          borderColor: 'var(--border)'
        }}>
        
        {/* 文本输入区域 */}
        <div className="flex-1">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            placeholder={placeholder}
            rows={1}
            className="w-full resize-none p-2 text-sm border rounded"
            style={{
              background: 'var(--background)',
              color: 'var(--foreground)',
              borderColor: 'var(--border)',
              minHeight: '36px',
              maxHeight: '120px'
            }}
            onFocus={(e) => {
              e.target.style.borderColor = 'var(--primary)';
            }}
            onBlur={(e) => {
              e.target.style.borderColor = 'var(--border)';
            }}
          />
        </div>

        {/* 发送按钮 */}
        <button
          type="submit"
          disabled={disabled || !message.trim()}
          className="btn-primary p-2 rounded"
        >
          <PaperAirplaneIcon className="w-4 h-4" />
        </button>
      </div>

      {/* 底部提示 */}
      <div className="flex items-center justify-between mt-2 px-1">
        <div className="flex items-center gap-3 text-xs" style={{ color: 'var(--foreground-muted)' }}>
          <span>Enter 发送</span>
          <span>Shift+Enter 换行</span>
        </div>
        
        {disabled && (
          <div className="flex items-center gap-1 text-xs" style={{ color: 'var(--foreground-muted)' }}>
            <div className="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <span>AI思考中...</span>
          </div>
        )}
      </div>
    </form>
  );
} 