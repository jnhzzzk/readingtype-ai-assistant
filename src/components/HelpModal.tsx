"use client";

import React from 'react';
import { XMarkIcon } from '@heroicons/react/24/outline';

interface HelpModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function HelpModal({ isOpen, onClose }: HelpModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* 背景遮罩 */}
      <div 
        className="absolute inset-0" 
        style={{ background: 'rgba(0, 0, 0, 0.5)' }}
        onClick={onClose}
      />
      
      {/* 弹窗内容 */}
      <div 
        className="relative w-full max-w-4xl max-h-[90vh] overflow-y-auto rounded-lg shadow-xl"
        style={{ background: 'var(--surface)' }}
      >
        {/* 头部 */}
        <div className="sticky top-0 z-10 flex items-center justify-between p-6 border-b"
          style={{ 
            background: 'var(--surface)',
            borderColor: 'var(--border)'
          }}>
          <h2 className="text-xl font-semibold" style={{ color: 'var(--foreground)' }}>
            ReadingType编码系统使用指南
          </h2>
          <button
            onClick={onClose}
            className="p-2 rounded transition-colors"
            style={{ background: 'var(--surface-secondary)' }}
          >
            <XMarkIcon className="w-5 h-5" style={{ color: 'var(--foreground)' }} />
          </button>
        </div>

        {/* 内容区域 */}
        <div className="p-6 space-y-6">
          {/* 系统介绍 */}
          <section>
            <h3 className="text-lg font-medium mb-3" style={{ color: 'var(--foreground)' }}>
              系统介绍
            </h3>
            <div className="p-4 rounded" style={{ background: 'var(--surface-secondary)' }}>
              <p className="text-sm" style={{ color: 'var(--foreground-secondary)' }}>
                ReadingType编码系统基于IEC61968-9-2024标准，用于标准化描述电力系统中的各种测量数据类型。
                本AI助手可以帮助您智能生成和解析16位ReadingType编码，简化编码管理工作。
              </p>
            </div>
          </section>

          {/* 编码结构 */}
          <section>
            <h3 className="text-lg font-medium mb-3" style={{ color: 'var(--foreground)' }}>
              编码结构说明
            </h3>
            <div className="p-4 rounded" style={{ background: 'var(--surface-secondary)' }}>
              <p className="text-sm mb-3" style={{ color: 'var(--foreground-secondary)' }}>
                ReadingType编码由16个位置组成，每个位置用点号分隔：
              </p>
              <div className="text-xs font-mono p-3 rounded" 
                style={{ 
                  background: 'var(--surface)',
                  color: 'var(--foreground)',
                  border: '1px solid var(--border)'
                }}>
                0.0.2.1.1.1.12.0.0.0.0.0.0.0.72.0
              </div>
              <div className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs" 
                style={{ color: 'var(--foreground-secondary)' }}>
                <div>• 位置1: 宏周期 (Macro Period)</div>
                <div>• 位置2: 聚合 (Aggregate)</div>
                <div>• 位置3: 测量周期 (Measure Period)</div>
                <div>• 位置4: 累积行为 (Accumulation Behaviour)</div>
                <div>• 位置5: 流向 (Flow Direction)</div>
                <div>• 位置6: 商品 (Commodity)</div>
                <div>• 位置7: 测量种类 (Measurement Kind)</div>
                <div>• 位置8: 谐波 (Harmonic)</div>
                <div>• 位置9: 参数分子 (Argument Numerator)</div>
                <div>• 位置10: 分时电价 (TOU)</div>
                <div>• 位置11: 关键峰值 (CPP)</div>
                <div>• 位置12: 用量阶梯 (Tier)</div>
                <div>• 位置13: 相位 (Phase)</div>
                <div>• 位置14: 倍增器 (Multiplier)</div>
                <div>• 位置15: 单位 (UOM)</div>
                <div>• 位置16: 货币 (Currency)</div>
              </div>
            </div>
          </section>

          {/* 智能编码功能 */}
          <section>
            <h3 className="text-lg font-medium mb-3" style={{ color: 'var(--foreground)' }}>
              智能编码功能
            </h3>
            <div className="space-y-4">
              {/* 生成编码 */}
              <div className="p-4 rounded" style={{ background: 'var(--surface-secondary)' }}>
                <h4 className="font-medium mb-2" style={{ color: 'var(--foreground)' }}>
                  🔧 生成编码
                </h4>
                <p className="text-sm mb-2" style={{ color: 'var(--foreground-secondary)' }}>
                  描述您的测量需求，AI将智能生成对应的ReadingType编码。
                </p>
                <div className="space-y-2">
                  <div className="text-xs">
                    <span className="font-medium" style={{ color: 'var(--foreground)' }}>示例输入：</span>
                    <div className="mt-1 p-2 rounded" 
                      style={{ 
                        background: 'var(--surface)',
                        border: '1px solid var(--border)',
                        color: 'var(--foreground-secondary)'
                      }}>
                      "我需要测量三相有功电能，15分钟间隔，A相，单位为千瓦时"
                    </div>
                  </div>
                  <div className="text-xs">
                    <span className="font-medium" style={{ color: 'var(--foreground)' }}>AI输出：</span>
                    <div className="mt-1 p-2 rounded" 
                      style={{ 
                        background: 'var(--surface)',
                        border: '1px solid var(--border)',
                        color: 'var(--foreground-secondary)'
                      }}>
                      ReadingType编码：0.0.2.1.1.1.12.0.0.0.0.0.129.3.72.0<br/>
                      并提供详细的字段解释
                    </div>
                  </div>
                </div>
              </div>

              {/* 解析编码 */}
              <div className="p-4 rounded" style={{ background: 'var(--surface-secondary)' }}>
                <h4 className="font-medium mb-2" style={{ color: 'var(--foreground)' }}>
                  🔍 解析编码
                </h4>
                <p className="text-sm mb-2" style={{ color: 'var(--foreground-secondary)' }}>
                  提供现有的ReadingType编码，AI将解析其含义和各字段定义。
                </p>
                <div className="space-y-2">
                  <div className="text-xs">
                    <span className="font-medium" style={{ color: 'var(--foreground)' }}>示例输入：</span>
                    <div className="mt-1 p-2 rounded" 
                      style={{ 
                        background: 'var(--surface)',
                        border: '1px solid var(--border)',
                        color: 'var(--foreground-secondary)'
                      }}>
                      "解析编码：0.0.2.1.1.1.12.0.0.0.0.0.129.3.72.0"
                    </div>
                  </div>
                  <div className="text-xs">
                    <span className="font-medium" style={{ color: 'var(--foreground)' }}>AI输出：</span>
                    <div className="mt-1 p-2 rounded" 
                      style={{ 
                        background: 'var(--surface)',
                        border: '1px solid var(--border)',
                        color: 'var(--foreground-secondary)'
                      }}>
                      详细解释每个位置的含义，如：<br/>
                      • 位置3(2): 15分钟间隔<br/>
                      • 位置7(12): 电能测量<br/>
                      • 位置13(129): A相对中性线<br/>
                      等等...
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* 编码字典 */}
          <section>
            <h3 className="text-lg font-medium mb-3" style={{ color: 'var(--foreground)' }}>
              编码字典功能
            </h3>
            <div className="p-4 rounded" style={{ background: 'var(--surface-secondary)' }}>
              <p className="text-sm mb-3" style={{ color: 'var(--foreground-secondary)' }}>
                点击"编码字典"按钮可以查看完整的字段定义和编码表，支持：
              </p>
              <ul className="text-xs space-y-1" style={{ color: 'var(--foreground-secondary)' }}>
                <li>• 📖 浏览所有16个位置的完整编码定义</li>
                <li>• 🔍 搜索特定编码或含义</li>
                <li>• 📋 查看中英文对照和详细说明</li>
                <li>• 🎯 快速定位所需的编码值</li>
              </ul>
            </div>
          </section>

          {/* 最佳实践 */}
          <section>
            <h3 className="text-lg font-medium mb-3" style={{ color: 'var(--foreground)' }}>
              使用建议
            </h3>
            <div className="p-4 rounded" style={{ background: 'var(--surface-secondary)' }}>
              <ul className="text-sm space-y-2" style={{ color: 'var(--foreground-secondary)' }}>
                <li>• <strong>详细描述：</strong>提供越详细的测量需求描述，生成的编码越准确</li>
                <li>• <strong>关键信息：</strong>包含设备类型、测量物理量、相位信息、时间间隔、单位等</li>
                <li>• <strong>分步操作：</strong>可以先生成基础编码，再根据需要调整特定字段</li>
                <li>• <strong>验证检查：</strong>生成编码后可以反向解析验证其正确性</li>
                <li>• <strong>字典参考：</strong>遇到不确定的字段可以查阅编码字典</li>
              </ul>
            </div>
          </section>

          {/* 技术规范 */}
          <section>
            <h3 className="text-lg font-medium mb-3" style={{ color: 'var(--foreground)' }}>
              技术规范
            </h3>
            <div className="p-4 rounded" style={{ background: 'var(--surface-secondary)' }}>
              <ul className="text-sm space-y-1" style={{ color: 'var(--foreground-secondary)' }}>
                <li>• <strong>标准依据：</strong>IEC61968-9-2024</li>
                <li>• <strong>编码格式：</strong>16位点分十进制格式</li>
                <li>• <strong>字符编码：</strong>UTF-8</li>
                <li>• <strong>数据类型：</strong>字符串形式的数值编码</li>
              </ul>
            </div>
          </section>
        </div>

        {/* 底部 */}
        <div className="sticky bottom-0 p-4 border-t text-center"
          style={{ 
            background: 'var(--surface)',
            borderColor: 'var(--border)'
          }}>
          <button
            onClick={onClose}
            className="px-6 py-2 rounded transition-colors"
            style={{ 
              background: 'var(--primary)',
              color: 'var(--background)'
            }}
          >
            开始使用
          </button>
        </div>
      </div>
    </div>
  );
} 