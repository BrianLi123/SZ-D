import React, { useState, useRef, useEffect } from 'react';
import { Button, Upload, Input } from 'antd';
import type { UploadFile, UploadProps } from 'antd';
import './index.css';
const { TextArea } = Input;

interface Message {
  text: string;
  sender: 'user' | 'bot';
}

const ChatBox: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [fileList, setFileList] = useState<UploadFile[]>([]);
  const [uploading, setUploading] = useState(false);
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
  const props: UploadProps = {
    listType: 'text',
    onRemove: (file) => {
      const index = fileList.indexOf(file);
      const newFileList = fileList.slice();
      newFileList.splice(index, 1);
      setFileList(newFileList);
    },
    beforeUpload: (file) => {
      setFileList([...fileList, file]);
      return false;
    },
    fileList,
    // 自定义文件列表项的显示内容
    itemRender: (originNode, file, fileList) => {
      return (
        <div
          style={{
            // display: 'flex',
            // justifyContent: 'space-between',
            // alignItems: 'center',
            width: '116px'
          }}
        >
          {originNode} {/* 原始文件节点（文件名、操作按钮等） */}
        </div>
      );
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
        </div>
        <div className="chat-input">
          <Upload {...props}>
            <Button type="primary">上传业务文档</Button>
          </Upload>
          <TextArea
            placeholder="Ask a question..."
            // rows={1}
            autoSize={{ maxRows: 1 }}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <Button type="primary" onClick={sendMessage}>
            Send
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ChatBox;
