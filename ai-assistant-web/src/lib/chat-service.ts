export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export function createChatStream(
  { messages }: { messages: Message[] },
  onContent: (content: string) => void,
  onError: (error: string) => void,
  onComplete: () => void
): (() => void) {
  let abortController = new AbortController();
  let isAborted = false;

  // 异步执行请求
  (async () => {
    try {
      // 调用本地API端点
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: messages,
          stream: true
        }),
        signal: abortController.signal
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      // 检查是否为流式响应
      if (response.headers.get('content-type')?.includes('text/event-stream')) {
        // 处理Server-Sent Events流
        const reader = response.body?.getReader();
        const decoder = new TextDecoder();

        if (!reader) {
          throw new Error('Unable to read response stream');
        }

        let accumulatedContent = '';

        try {
          while (true) {
            if (isAborted) break;
            
            const { done, value } = await reader.read();
            
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const data = line.slice(6);
                
                if (data === '[DONE]') {
                  onComplete();
                  return;
                }
                
                try {
                  const parsed = JSON.parse(data);
                  if (parsed.choices?.[0]?.delta?.content) {
                    accumulatedContent += parsed.choices[0].delta.content;
                    onContent(accumulatedContent);
                  }
                } catch (e) {
                  // 忽略解析错误，继续处理下一行
                  continue;
                }
              }
            }
          }
        } finally {
          reader.releaseLock();
        }
      } else {
        // 处理非流式响应
        const data = await response.json();
        if (data.content) {
          onContent(data.content);
          onComplete();
        } else if (data.error) {
          onError(`Error: ${data.error}`);
        }
      }
    } catch (error) {
      if (!isAborted) {
        console.error('Error creating chat stream:', error);
        onError(`Could not connect to the AI service. ${error instanceof Error ? error.message : 'Unknown error'}`);
      }
    }
  })();

  // 返回清理函数
  return () => {
    isAborted = true;
    abortController.abort();
  };
} 