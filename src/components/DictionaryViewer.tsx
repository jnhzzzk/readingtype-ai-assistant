"use client";

import React, { useState, useMemo } from 'react';
import { 
  MagnifyingGlassIcon,
  BookOpenIcon,
  XMarkIcon,
  ChevronDownIcon,
  ChevronRightIcon
} from '@heroicons/react/24/outline';
import { 
  readingTypeDictionary, 
  searchDictionary, 
  DictionaryField, 
  DictionaryValue 
} from '@/lib/reading-type-dictionary';

interface DictionaryViewerProps {
  isOpen: boolean;
  onClose: () => void;
}

export function DictionaryViewer({ isOpen, onClose }: DictionaryViewerProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedFields, setExpandedFields] = useState<Set<number>>(new Set([1, 3, 7])); // 默认展开一些字段
  const [viewMode, setViewMode] = useState<'browse' | 'search'>('browse');

  // 搜索结果
  const searchResults = useMemo(() => {
    if (!searchQuery.trim()) return [];
    return searchDictionary(searchQuery);
  }, [searchQuery]);

  // 切换字段展开状态
  const toggleField = (position: number) => {
    const newExpanded = new Set(expandedFields);
    if (newExpanded.has(position)) {
      newExpanded.delete(position);
    } else {
      newExpanded.add(position);
    }
    setExpandedFields(newExpanded);
  };

  // 处理搜索
  const handleSearch = (query: string) => {
    setSearchQuery(query);
    setViewMode(query.trim() ? 'search' : 'browse');
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4" 
      style={{ background: 'rgba(0, 0, 0, 0.5)' }}>
      <div className="w-full max-w-5xl h-[90vh] sm:h-[85vh] max-h-screen rounded-lg border flex flex-col" 
        style={{ 
          background: 'var(--surface)',
          borderColor: 'var(--border)'
        }}>
        
        {/* 头部 */}
        <div className="flex items-center justify-between p-2 sm:p-4 border-b flex-shrink-0" 
          style={{ borderColor: 'var(--border)' }}>
          <div className="flex items-center gap-3">
            <BookOpenIcon className="w-5 h-5" style={{ color: 'var(--primary)' }} />
            <h2 className="text-base sm:text-lg font-semibold" style={{ color: 'var(--foreground)' }}>
              ReadingType编码字典
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded transition-colors"
            style={{ background: 'var(--surface-secondary)' }}
          >
            <XMarkIcon className="w-4 h-4" style={{ color: 'var(--foreground)' }} />
          </button>
        </div>

        {/* 搜索栏 */}
        <div className="p-2 sm:p-4 border-b flex-shrink-0" style={{ borderColor: 'var(--border)' }}>
          <div className="relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4" 
              style={{ color: 'var(--foreground-muted)' }} />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => handleSearch(e.target.value)}
              placeholder="搜索编码、英文名称或中文含义..."
              className="w-full pl-10 pr-4 py-2 text-sm rounded border"
              style={{
                background: 'var(--background)',
                color: 'var(--foreground)',
                borderColor: 'var(--border)'
              }}
              onFocus={(e) => {
                e.target.style.borderColor = 'var(--primary)';
              }}
              onBlur={(e) => {
                e.target.style.borderColor = 'var(--border)';
              }}
            />
          </div>
        </div>

        {/* 内容区域 */}
        <div 
          className="flex-1 overflow-y-scroll dictionary-content p-2 sm:p-4" 
          style={{ 
            minHeight: 0,
            scrollbarWidth: 'thin',
            scrollbarColor: 'var(--border) var(--surface-secondary)'
          }}
        >
          {viewMode === 'search' ? (
            // 搜索结果
            <div>
              <p className="text-sm mb-4" style={{ color: 'var(--foreground-secondary)' }}>
                找到 {searchResults.length} 个结果
              </p>
              {searchResults.length > 0 ? (
                <div className="space-y-3">
                  {searchResults.map((result, index) => (
                    <div key={index} className="p-3 rounded border" 
                      style={{ 
                        background: 'var(--surface-secondary)',
                        borderColor: 'var(--border)'
                      }}>
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <span className="text-xs px-2 py-1 rounded" 
                            style={{ 
                              background: 'var(--primary)', 
                              color: 'var(--background)' 
                            }}>
                            位置{result.field.position}
                          </span>
                          <span className="ml-2 font-medium text-sm" 
                            style={{ color: 'var(--foreground)' }}>
                            {result.field.name} ({result.field.englishName})
                          </span>
                        </div>
                      </div>
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 sm:gap-3 text-sm">
                        <div>
                          <span className="font-medium" style={{ color: 'var(--foreground)' }}>
                            编码：
                          </span>
                          <span style={{ color: 'var(--foreground-secondary)' }}>
                            {result.value.code}
                          </span>
                        </div>
                        <div>
                          <span className="font-medium" style={{ color: 'var(--foreground)' }}>
                            英文：
                          </span>
                          <span style={{ color: 'var(--foreground-secondary)' }}>
                            {result.value.english}
                          </span>
                        </div>
                        <div>
                          <span className="font-medium" style={{ color: 'var(--foreground)' }}>
                            中文：
                          </span>
                          <span style={{ color: 'var(--foreground-secondary)' }}>
                            {result.value.chinese}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <p className="text-sm" style={{ color: 'var(--foreground-muted)' }}>
                    未找到匹配的结果
                  </p>
                </div>
              )}
            </div>
          ) : (
            // 浏览模式
            <div className="space-y-4">
              {readingTypeDictionary.map((field) => (
                <div key={field.position} className="border rounded" 
                  style={{ borderColor: 'var(--border)' }}>
                  
                  {/* 字段标题 */}
                  <button
                    onClick={() => toggleField(field.position)}
                    className="w-full p-3 sm:p-4 text-left flex items-center justify-between transition-colors"
                    style={{ background: 'var(--surface-secondary)' }}
                  >
                    <div>
                      <div className="flex items-center gap-3">
                        <span className="text-xs px-2 py-1 rounded" 
                          style={{ 
                            background: 'var(--primary)', 
                            color: 'var(--background)' 
                          }}>
                          位置{field.position}
                        </span>
                        <span className="font-medium text-sm sm:text-base" style={{ color: 'var(--foreground)' }}>
                          {field.name}
                        </span>
                        <span className="text-xs sm:text-sm" style={{ color: 'var(--foreground-secondary)' }}>
                          ({field.englishName})
                        </span>
                      </div>
                      <p className="text-xs mt-1" style={{ color: 'var(--foreground-muted)' }}>
                        {field.description}
                      </p>
                    </div>
                    {expandedFields.has(field.position) ? (
                      <ChevronDownIcon className="w-4 h-4" style={{ color: 'var(--foreground-muted)' }} />
                    ) : (
                      <ChevronRightIcon className="w-4 h-4" style={{ color: 'var(--foreground-muted)' }} />
                    )}
                  </button>

                  {/* 字段值列表 */}
                  {expandedFields.has(field.position) && (
                    <div className="border-t" style={{ borderColor: 'var(--border)' }}>
                      <div className="p-2 sm:p-4">
                        <div className="grid gap-2">
                          {field.values.map((value, index) => (
                            <div key={index} 
                              className="grid grid-cols-1 sm:grid-cols-3 gap-2 sm:gap-3 py-2 px-3 rounded text-sm transition-colors"
                              style={{ background: 'var(--background)' }}
                            >
                              <div className="font-mono font-medium" 
                                style={{ color: 'var(--primary)' }}>
                                {value.code}
                              </div>
                              <div style={{ color: 'var(--foreground-secondary)' }}>
                                {value.english}
                              </div>
                              <div style={{ color: 'var(--foreground)' }}>
                                {value.chinese}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 底部说明 */}
        <div className="p-2 sm:p-4 border-t text-center flex-shrink-0" style={{ borderColor: 'var(--border)' }}>
          <p className="text-xs" style={{ color: 'var(--foreground-muted)' }}>
            ReadingType编码字典 - IEC61968-9-2024标准
          </p>
        </div>
      </div>
    </div>
  );
} 