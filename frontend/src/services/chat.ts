import request from './axios';

export const testApi = async () => {
  const res = await request.post('/chat/hkt2', {});
  console.log('res', res);
  return res;
};

export const getChatStream = async () => {
  const res = await request.post('/chat/stream', {
    approach: '',
    chatroomID: 'fwagwe',
    history: [
      {
        // bot:'hi',
        user: '如何評估自己的退休生活需要，以決定是否需要作額外的強積金供款？'
      }
    ]
  });
  console.log('res', res);
  return res;
};
export const getChatUpload = async (params: any) => {
  const res = await request.post('/chat/upload', params);
  console.log('res', res);
  return res;
};
