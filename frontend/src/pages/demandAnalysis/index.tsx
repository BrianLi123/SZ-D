import React, { useState, useRef, useEffect } from 'react';
import { Button, Input } from 'antd';
import './index.css';
import { getChatStream } from '@/services/chat';
const { TextArea } = Input;

interface Message {
  text: string;
  sender: 'user' | 'bot';
}

const ChatBox: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [colorChangeFlag, setColorChangeFlag] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  function parseData(data: string): any {
    const regex = /data:.*?"token":\s*"([^"]*)"}/g;
    let chunkStr = data.replace(regex, '$1');
    return chunkStr;
  }
  const readerEventStream = async (answer: any) => {
    console.log('answer', answer);
    if (answer?.body) {
      // 检查流是否被锁定
      if (answer.body.locked) {
        return;
      }
      // 流式数据获取
      const reader = answer.body?.getReader();
      const decoder = new TextDecoder(); // 用于解码二进制流
      let buffer: any = [];
      let isProcessing = false;
      let ansText = '';
      let messagesCopy = [...messages];
      messagesCopy[messages.length] = { sender: 'bot' } as Message;
      const processBuffer = () => {
        if (buffer.length > 0) {
          const char = buffer.shift();
          ansText += char;
          messagesCopy[messages.length].text = ansText;
          setMessages(messagesCopy);
          setTimeout(processBuffer, 15);
        } else {
          isProcessing = false;
        }
      };
      try {
        // 循环读取响应流
        while (true) {
          const { done, value } = await reader.read();
          if (done) {
            reader.releaseLock(); // 释放流
            break;
          }
          // 解码数据
          let chunk = decoder.decode(value, { stream: true });
          console.log('chunk', chunk);
          chunk = parseData(chunk);
          if (chunk.includes('[DONE]')) {
            console.log('chunkDONE', chunk.split('[DONE]'));
          }
          if (chunk.trim() === '[DONE]') {
            reader.cancel(); // 结束关闭流
            break;
          }

          buffer.push(...chunk.split('\n\n'));
          // console.log("chunk", chunk, chunk.split("\n\n"));
          if (!isProcessing) {
            isProcessing = true;
            processBuffer();
          }
        }
      } catch (error) {
        console.error('Error reading stream:', error);
      }
    }
  };

  const sendMessage = async () => {
    if (!inputValue.trim()) return;
    // 添加用户消息
    setMessages((prev) => [...prev, { text: inputValue, sender: 'user' }]);
    setInputValue('');

    // 模拟机器人响应
    setLoading(true);
    try {
      const params = {
        approach: '',
        chatroomID: 'fwagwe',
        history: [
          {
            user: inputValue
          }
        ]
      };
      const res = await getChatStream(params);
      console.log('getChatStream-res', res);

      if (res?.body) {
        //   const response = res.data;
        //   console.log('response', response);
        //   setMessages((prev) => [...prev, { text: response, sender: 'bot' }]);
        // 处理事件流数据接收和逐字打印
        readerEventStream(res);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && e.shiftKey) {
      // Shift + Enter 换行
      return;
    }
    if (e.key === 'Enter') {
      e.preventDefault();
      sendMessage();
    }
  };

  // 自动滚动到底部
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="chat-box">
      <div className="chat-messages">
        <div className="chat-messages-list">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${
                message.sender === 'user' ? 'user' : 'bot'
              }`}
            >
              {message.text}
            </div>
          ))}
          {loading && <div className="message bot">Generating answer...</div>}
          <div ref={messagesEndRef} />
        </div>
        <div className="chat-input">
          <Button
            color={colorChangeFlag ? 'primary' : undefined}
            className="chat-button"
            shape="round"
            variant="filled"
            onClick={() => setColorChangeFlag(!colorChangeFlag)}
          >
            深度思考
          </Button>
          <TextArea
            placeholder="Ask a question..."
            autoSize={{ maxRows: 1 }}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <Button type="primary" loading={loading} onClick={sendMessage}>
            Send
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ChatBox;
