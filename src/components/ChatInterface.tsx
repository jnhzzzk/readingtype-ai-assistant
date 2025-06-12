"use client";

import React, { useState, useRef, useEffect } from 'react';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { QuickActions } from './QuickActions';
import { DictionaryViewer } from './DictionaryViewer';
import { HelpModal } from './HelpModal';
import { Message, createChatStream } from '../lib/chat-service';

import { 
  ClockIcon, 
  TrashIcon, 
  StopIcon,
  Bars3Icon,
  XMarkIcon,
  CodeBracketIcon 
} from '@heroicons/react/24/outline';

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'system',
      content: '你是ReadingType智能编码助手，专门帮助用户进行IEC61968-9-2024标准的ReadingType编码生成和管理。你可以:\n1. 基于描述智能生成新编码\n2. 验证和解析编码\n3. 解释字段含义和规范\n\n专注于根据您的量测需求描述，智能分析并生成准确的ReadingTypeID编码。请告诉我您需要什么帮助！'
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentResponse, setCurrentResponse] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isDictionaryOpen, setIsDictionaryOpen] = useState(false);
  const [isHelpOpen, setIsHelpOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<(() => void) | null>(null);
  const responseAddedRef = useRef(false);

  // 处理发送消息
  const handleSendMessage = async (content: string) => {
    if (isLoading) return;

    const userMessage: Message = { role: 'user', content };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    
    setIsLoading(true);
    setError(null);
    setCurrentResponse("");
    responseAddedRef.current = false;

    try {
      const cleanup = createChatStream(
        { messages: updatedMessages },
        (content) => {
          setCurrentResponse(content);
        },
        (error) => {
          setError(error);
          setIsLoading(false);
        },
        () => {
          setIsLoading(false);
          abortControllerRef.current = null;
        }
      );
      
      abortControllerRef.current = cleanup;
      
    } catch (err) {
      setError(err instanceof Error ? err.message : '未知错误');
      setIsLoading(false);
    }
  };

  const cancelRequest = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current();
      abortControllerRef.current = null;
    }
    setIsLoading(false);
    setCurrentResponse("");
    responseAddedRef.current = false;
  };

  const clearChat = () => {
    if (isLoading) {
      cancelRequest();
    }
    
    setMessages([
      {
        role: 'system',
        content: '你是ReadingType智能编码助手，专门帮助用户进行IEC61968-9-2024标准的ReadingType编码生成和管理。你可以:\n1. 基于描述智能生成新编码\n2. 验证和解析编码\n3. 解释字段含义和规范\n\n专注于根据您的量测需求描述，智能分析并生成准确的ReadingTypeID编码。请告诉我您需要什么帮助！'
      }
    ]);
    setError(null);
    setCurrentResponse("");
    responseAddedRef.current = false;
  };

  const handleQuickAction = (action: string, data?: string) => {
    if (isLoading) return;

    let message = '';
    switch (action) {
      case 'generate':
        message = '我需要生成新的ReadingType编码，请描述您的量测需求（设备类型、测量内容、相位、时间周期等）。';
        break;
      case 'quick-generate':
        message = data || '';
        break;
      default:
        return;
    }

    if (message) {
      handleSendMessage(message);
    }
  };

  const handleOpenDictionary = () => {
    setIsDictionaryOpen(true);
  };

  const handleCloseDictionary = () => {
    setIsDictionaryOpen(false);
  };

  const handleOpenHelp = () => {
    setIsHelpOpen(true);
  };

  const handleCloseHelp = () => {
    setIsHelpOpen(false);
  };

  useEffect(() => {
    if (!isLoading && currentResponse && !responseAddedRef.current) {
      setMessages(prev => [...prev, { role: 'assistant', content: currentResponse }]);
      responseAddedRef.current = true;
      setCurrentResponse("");
    }
  }, [isLoading, currentResponse]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, currentResponse]);

  return (
    <div className="flex h-screen" style={{ background: 'var(--background)' }}>
      {/* 侧边栏 */}
      <div className={`
        fixed inset-y-0 left-0 z-50 w-80 transform transition-transform duration-200 ease-in-out
        lg:relative lg:translate-x-0 lg:w-80
        ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex h-full flex-col border-r" 
          style={{ 
            background: 'var(--surface)',
            borderColor: 'var(--border)'
          }}>
          
          {/* 侧边栏头部 */}
          <div className="flex items-center justify-between p-4 border-b" 
            style={{ borderColor: 'var(--border)' }}>
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded flex items-center justify-center" 
                style={{ background: 'var(--primary)' }}>
                <CodeBracketIcon className="w-5 h-5" style={{ color: 'var(--background)' }} />
              </div>
              <div>
                <h1 className="text-lg font-semibold" style={{ color: 'var(--foreground)' }}>
                  ReadingType
                </h1>
                <p className="text-sm" style={{ color: 'var(--foreground-secondary)' }}>
                  AI编码助手
                </p>
              </div>
            </div>
            <button
              onClick={() => setIsSidebarOpen(false)}
              className="lg:hidden p-2 rounded transition-colors"
              style={{ background: 'var(--surface-secondary)' }}
            >
              <XMarkIcon className="w-4 h-4" style={{ color: 'var(--foreground)' }} />
            </button>
          </div>

          {/* 快速操作 */}
          <div className="flex-1 overflow-y-auto p-4">
            <QuickActions 
              onAction={handleQuickAction} 
              onDictionary={handleOpenDictionary}
              onHelp={handleOpenHelp}
            />
          </div>

          {/* 侧边栏底部控制 */}
          <div className="p-4 border-t" style={{ borderColor: 'var(--border)' }}>
            <button
              onClick={clearChat}
              className="w-full flex items-center gap-3 p-3 rounded transition-colors"
              style={{ 
                background: 'var(--surface-secondary)',
                color: 'var(--foreground)'
              }}
            >
              <TrashIcon className="w-4 h-4" />
              <span className="text-sm">清除对话</span>
            </button>
          </div>
        </div>
      </div>

      {/* 遮罩层 - 移动端 */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black bg-opacity-25 lg:hidden"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* 主聊天区域 */}
      <div className="flex-1 flex flex-col h-screen">
        {/* 顶部导航栏 */}
        <header className="flex items-center justify-between p-4 border-b" 
          style={{ 
            background: 'var(--surface)', 
            borderColor: 'var(--border)' 
          }}>
          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsSidebarOpen(true)}
              className="lg:hidden p-2 rounded transition-colors"
              style={{ background: 'var(--surface-secondary)' }}
            >
              <Bars3Icon className="w-4 h-4" style={{ color: 'var(--foreground)' }} />
            </button>
            
            <h2 className="text-lg font-medium" style={{ color: 'var(--foreground)' }}>
              智能对话
            </h2>
          </div>

          {/* 状态指示器 */}
          {isLoading && (
            <div className="flex items-center gap-2">
              <div className="loading-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <span className="text-sm" style={{ color: 'var(--foreground-secondary)' }}>
                AI思考中
              </span>
            </div>
          )}
        </header>

        {/* 消息列表 */}
        <div className="flex-1 overflow-y-auto p-4">
          <div className="max-w-4xl mx-auto">
            {messages.filter(msg => msg.role !== 'system').map((message, index) => (
              <ChatMessage 
                key={index} 
                message={message} 
                isLoading={false}
                useMarkdown={true}
              />
            ))}
            
            {isLoading && currentResponse && (
              <div className="flex items-start gap-4">
                <div className="w-8 h-8 rounded-full flex items-center justify-center" 
                  style={{ background: 'var(--surface-secondary)' }}>
                  <ClockIcon className="w-4 h-4" style={{ color: 'var(--foreground-muted)' }} />
                </div>
                <div className="message-bubble assistant flex-1">
                  <ChatMessage 
                    message={{ role: 'assistant', content: currentResponse }} 
                    isLoading={true}
                    useMarkdown={true}
                  />
                </div>
              </div>
            )}
            
            {isLoading && !currentResponse && (
              <div className="flex items-center gap-4">
                <div className="w-8 h-8 rounded-full flex items-center justify-center" 
                  style={{ background: 'var(--surface-secondary)' }}>
                  <ClockIcon className="w-4 h-4" style={{ color: 'var(--foreground-muted)' }} />
                </div>
                <div className="message-bubble assistant">
                  <div className="flex items-center gap-2">
                    <div className="loading-dots">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                    <span className="text-sm" style={{ color: 'var(--foreground-secondary)' }}>
                      AI正在分析您的需求...
                    </span>
                  </div>
                </div>
              </div>
            )}
            
            {error && (
              <div className="p-3 rounded border" style={{ 
                background: 'var(--surface-secondary)', 
                color: 'var(--error)',
                borderColor: 'var(--error)'
              }}>
                <p className="font-medium">出现错误</p>
                <p className="text-sm mt-1">{error}</p>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* 输入区域 */}
        <div className="border-t p-4" style={{ 
          background: 'var(--surface)', 
          borderColor: 'var(--border)' 
        }}>
          <div className="max-w-4xl mx-auto">
            <div className="relative">
              <ChatInput 
                onSendMessage={handleSendMessage} 
                disabled={isLoading}
                placeholder="描述您的量测需求，AI将为您生成ReadingType编码..."
              />
              {isLoading && (
                <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                  <button
                    onClick={cancelRequest}
                    className="btn-secondary !p-2 !bg-red-500 hover:!bg-red-600 !text-white !border-red-500"
                    title="停止生成"
                  >
                    <StopIcon className="w-4 h-4" />
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* 字典查看器 */}
      <DictionaryViewer 
        isOpen={isDictionaryOpen}
        onClose={handleCloseDictionary}
      />

      {/* 使用帮助弹窗 */}
      <HelpModal 
        isOpen={isHelpOpen}
        onClose={handleCloseHelp}
      />
    </div>
  );
} 