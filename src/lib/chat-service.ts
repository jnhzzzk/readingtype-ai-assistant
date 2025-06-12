export interface Message {
  id?: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp?: Date;
}

export interface ChatStreamResponse {
  id: string;
  content: string;
  done: boolean;
}

export function createChatStream(
  request: { messages: Message[] },
  onContent: (content: string) => void,
  onError: (error: string) => void,
  onComplete: () => void
): () => void {
  let abortController = new AbortController();
  let isAborted = false;

  const startStream = async () => {
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ messages: request.messages }),
        signal: abortController.signal,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('No response body');
      }

      const decoder = new TextDecoder();
      let buffer = '';
      let fullContent = '';

      while (true) {
        if (isAborted) {
          reader.cancel();
          break;
        }

        const { done, value } = await reader.read();
        
        if (done) {
          break;
        }

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.trim() === '' || isAborted) continue;
          
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            
            if (data === '[DONE]') {
              onComplete();
              return;
            }

            try {
              const parsed = JSON.parse(data);
              if (parsed.choices && parsed.choices[0]?.delta?.content) {
                const content = parsed.choices[0].delta.content;
                fullContent += content;
                onContent(fullContent);
              }
            } catch (e) {
              console.error('Error parsing JSON:', e);
            }
          }
        }
      }

      if (!isAborted) {
        onComplete();
      }
    } catch (error) {
      if (!isAborted) {
        console.error('Error in chat stream:', error);
        onError(error instanceof Error ? error.message : '未知错误');
      }
    }
  };

  // 检查API响应格式，如果不是流式响应，则直接处理
  const handleNonStreamResponse = async () => {
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ messages: request.messages }),
        signal: abortController.signal,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.content) {
        // 模拟打字机效果
        const content = data.content;
        let currentText = '';
        
        for (let i = 0; i < content.length; i++) {
          if (isAborted) break;
          
          currentText += content[i];
          onContent(currentText);
          
          // 添加小延迟来模拟打字机效果
          if (i % 10 === 0) {
            await new Promise(resolve => setTimeout(resolve, 50));
          }
        }
        
        if (!isAborted) {
          onComplete();
        }
      } else if (data.error) {
        onError(data.error);
      }
    } catch (error) {
      if (!isAborted) {
        console.error('Error in chat request:', error);
        onError(error instanceof Error ? error.message : '未知错误');
      }
    }
  };

  // 启动请求，优先尝试非流式响应
  handleNonStreamResponse();

  // 返回清理函数
  return () => {
    isAborted = true;
    abortController.abort();
  };
}

export function createMessage(role: 'user' | 'assistant' | 'system', content: string): Message {
  return {
    id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
    role,
    content,
    timestamp: new Date(),
  };
} 