// 文章显示
import ReactMarkdown from 'react-markdown';
// 划线、表、任务列表和直接url等的语法扩展
import remarkGfm from 'remark-gfm';
// 解析标签，支持html语法
import rehypeRaw from 'rehype-raw';

interface AnswerProps {
  ansIndex: number;
  answer: any;
  setMessages: React.Dispatch<React.SetStateAction<any[]>>;
}
export default function Answer({ ansIndex, answer, setMessages }: AnswerProps) {
  const [displalyAnswer, setDisplalyAnswer] = useState('');

  function parseData(data: string): any {
    const regex = /data:.*?"token":\s*"([^"]*)"}/g;
    let chunkStr = data.replace(regex, '$1');
    return chunkStr;
  }

  useEffect(() => {
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

        const processBuffer = () => {
          let timer: ReturnType<typeof setTimeout> | undefined;
          if (timer !== undefined) {
            clearTimeout(timer); // 清除之前的定时器
          }
          if (buffer.length > 0) {
            let char = buffer.shift();
            char = char.replace(/\\n/g, '  \n'); // 替换换行符
            // setDisplalyAnswer((prev) => prev + char))
            setDisplalyAnswer((prev) => {
              const newText = prev + char;
              // 滚动到底部
              //   if (messagesEndRef.current) {
              //     messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
              //   }
              return newText;
            });
            timer = setTimeout(processBuffer, 15);
          } else {
            isProcessing = false;
            console.log('displalyAnswer', displalyAnswer);
            // setMessages((prev) => {
            //   prev[ansIndex][1] = chunkData;
            //   return prev;
            // });
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
  return (
    <>
      <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw]}>
        {displalyAnswer}
      </ReactMarkdown>
    </>
  );
}
