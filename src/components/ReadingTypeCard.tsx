"use client";

import React from 'react';
import { ClipboardIcon, InformationCircleIcon } from '@heroicons/react/24/outline';

interface ReadingTypeInfo {
  name?: string;
  reading_type_id?: string;
  description?: string;
  category?: string;
  created_at?: string;
  fields?: Array<{
    position: number;
    name: string;
    chinese_name: string;
    value: number | string;
    description: string;
  }>;
}

interface ReadingTypeCardProps {
  readingType: ReadingTypeInfo;
  showFields?: boolean;
}

export function ReadingTypeCard({ readingType, showFields = false }: ReadingTypeCardProps) {
  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      // 可以添加一个toast提示
    } catch (err) {
      console.error('复制失败:', err);
    }
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4 shadow-sm hover:shadow-md transition-shadow">
      {/* 头部信息 */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-1">
            {readingType.name || '未命名编码'}
          </h3>
          {readingType.description && (
            <p className="text-sm text-gray-600 mb-2">{readingType.description}</p>
          )}
        </div>
        {readingType.category && (
          <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-md">
            {readingType.category}
          </span>
        )}
      </div>

      {/* ReadingTypeID */}
      {readingType.reading_type_id && (
        <div className="bg-gray-50 rounded-md p-3 mb-3">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-gray-500 mb-1">ReadingType ID</p>
              <p className="font-mono text-sm text-gray-900">{readingType.reading_type_id}</p>
            </div>
            <button
              onClick={() => copyToClipboard(readingType.reading_type_id!)}
              className="p-1 text-gray-400 hover:text-gray-600 rounded transition-colors"
              title="复制编码"
            >
              <ClipboardIcon className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

      {/* 字段详情 */}
      {showFields && readingType.fields && readingType.fields.length > 0 && (
        <div className="border-t pt-3">
          <h4 className="text-sm font-medium text-gray-700 mb-2 flex items-center">
            <InformationCircleIcon className="h-4 w-4 mr-1" />
            字段详情
          </h4>
          <div className="space-y-2">
            {readingType.fields.map((field) => (
              <div key={field.position} className="flex justify-between items-start text-xs">
                <div className="flex-1">
                  <span className="font-medium text-gray-700">
                    {field.position}. {field.chinese_name}
                  </span>
                  <span className="text-gray-500 ml-1">({field.name})</span>
                </div>
                <div className="text-right flex-shrink-0 ml-2">
                  <span className="font-mono text-gray-900">{field.value}</span>
                  {field.description && (
                    <div className="text-gray-500 mt-1">{field.description}</div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 时间戳 */}
      {readingType.created_at && (
        <div className="text-xs text-gray-400 mt-3 pt-2 border-t">
          创建时间: {readingType.created_at}
        </div>
      )}
    </div>
  );
} 