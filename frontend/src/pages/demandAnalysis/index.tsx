import React, { useState, useRef, useEffect, Fragment } from 'react';
import { Button, Input } from 'antd';
import './index.css';
import { getChatStream } from '@/services/chat';

import Answer from './components/Answer';
const { TextArea } = Input;

const ChatBox: React.FC = () => {
  const [messages, setMessages] = useState<[string, any][]>([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [colorChangeFlag, setColorChangeFlag] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const sendMessage = async () => {
    if (!inputValue.trim()) return;
    // 添加用户消息
    setMessages([...messages, [inputValue, '']]);
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

      if (res?.body) {
        // 处理事件流数据接收和逐字打印
        setMessages([...messages, [inputValue, res]]);
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
            <Fragment key={index}>
              <div className="message user">{message[0]}</div>
              {!loading && (
                <div className="message bot">
                  <Answer ansIndex={index} answer={message[1]} setMessages={setMessages} />
                </div>
              )}
            </Fragment>
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
