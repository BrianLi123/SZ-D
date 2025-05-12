import { getChatUpload } from '@/services/chat';
import { Upload, Button } from 'antd';
import type { UploadFile, UploadProps } from 'antd';

export default function UploadDocument() {
  const [fileList, setFileList] = useState<UploadFile[]>([]);
  const [uploading, setUploading] = useState(false);
  const props: UploadProps = {
    listType: 'text',
    maxCount: 1,
    onRemove: (file) => {
      const index = fileList.indexOf(file);
      const newFileList = fileList.slice();
      newFileList.splice(index, 1);
      setFileList(newFileList);
    },
    beforeUpload: async (file) => {
      setUploading(true);
      try {
        // 手动上传
        const formData = new FormData();
        formData.append('file', file as Blob);
        const res = await getChatUpload(formData);
        if (res) {
          setFileList([file]);
          message.success(`${file.name} 上传成功`);
        }
        // console.log('response', response);
      } finally {
        setUploading(false);
      }
      return false;
    },
    fileList,
    // 自定义文件列表项的显示内容
    itemRender: (originNode) => {
      return <div style={{ width: '116px' }}>{originNode}</div>;
    }
  };
  return (
    <div>
      <Upload {...props}>
        <Button type="primary" loading={uploading}>
          上传业务文档
        </Button>
      </Upload>
    </div>
  );
}
