// 文章显示
import ReactMarkdown from 'react-markdown';
// 划线、表、任务列表和直接url等的语法扩展
import remarkGfm from 'remark-gfm';
// 解析标签，支持html语法
import rehypeRaw from 'rehype-raw';

interface AnswerProps {
  ansIndex: number;
  answer: any;
  containerRef: React.RefObject<HTMLDivElement>;
  setMessages: React.Dispatch<React.SetStateAction<any[]>>;
}
export default function Answer({
  ansIndex,
  answer,
  containerRef,
  setMessages
}: AnswerProps) {
  const [displalyAnswer, setDisplalyAnswer] = useState('');
  const [doneFlag, setDoneFlag] = useState(false);
  const [autoScroll, setAutoScroll] = useState(true); // 是否启用自动滚动

  function parseData(data: string): any {
    const regex = /data:.*?"token":\s*"([^"]*)"}/g;
    let chunkStr = data.replace(regex, '$1');
    return chunkStr;
  }

  // 处理流式数据和和逐字打印
  useEffect(() => {
    const readerEventStream = async (answer: any) => {
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

        const processBuffer = () => {
          let timer: ReturnType<typeof setTimeout> | undefined;
          if (timer !== undefined) {
            clearTimeout(timer); // 清除之前的定时器
          }
          if (buffer.length > 0) {
            let char = buffer.shift();
            char = char.replace(/\\n/g, '  \n'); // 替换换行符
            setDisplalyAnswer((prev) => {
              const newText = prev + char;
              return newText;
            });
            timer = setTimeout(processBuffer, 15);
          } else {
            isProcessing = false;
            setDoneFlag(true);
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
            // 主动取消流，终止后续读取。（注：早于流自然结束）
            if (chunk.trim() === 'data: [DONE]') {
              reader.cancel();
              break;
            }
            chunk = parseData(chunk);

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
    readerEventStream(answer);
  }, []);
  // 当 displalyAnswer 更新时触发滚动
  useEffect(() => {
    // 自动滚动函数 滚动到底部
    const scrollToBottom = () => {
      if (containerRef.current?.scrollIntoView) {
        containerRef.current.scrollTo({
          top: containerRef.current.scrollHeight
        });
      }
    };

    if (autoScroll && containerRef.current) {
      scrollToBottom();
    }
  }, [displalyAnswer, doneFlag]);
  // 监听用户滚动事件。手动滚动超过10 则停止跟随(更新时新增内容)滚动
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    const handleScroll = () => {
      // 判断用户是否手动滚动
      const { scrollTop, scrollHeight, clientHeight } = container;
      const isAtBottom = scrollHeight - (scrollTop + clientHeight) < 10; // 10 是容差范围
      // 如果用户滚动到底部，则恢复自动滚动；否则停止自动滚动
      setAutoScroll(isAtBottom);
    };
    container.addEventListener('scroll', handleScroll);
    return () => {
      container.removeEventListener('scroll', handleScroll);
    };
  }, []);
  useEffect(() => {
    if (doneFlag) {
      setMessages((prev) => {
        prev[ansIndex][1] = displalyAnswer;
        return prev;
      });
    }
  }, [doneFlag]);

  return (
    <>
      <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw]}>
        {displalyAnswer}
      </ReactMarkdown>
    </>
  );
}
