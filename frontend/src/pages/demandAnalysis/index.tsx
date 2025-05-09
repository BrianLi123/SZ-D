import React, { useState, useRef, useEffect } from 'react';
import { Button, Input } from 'antd';
import './index.css';
import { ButtonColorType } from 'antd/es/button';
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

  // 自动滚动到底部
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!inputValue.trim()) return;
    // 添加用户消息
    setMessages((prev) => [...prev, { text: inputValue, sender: 'user' }]);
    setInputValue('');

    // 模拟机器人响应
    setLoading(true);
    try {
      const response = await new Promise<string>((resolve) => {
        setTimeout(() => resolve('This is a bot response.'), 2000);
      });
      setMessages((prev) => [...prev, { text: response, sender: 'bot' }]);
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
