import request from './axios';

export const testApi = async () => {
  const res = await request.post('/chat/hkt2', {});
  console.log('res', res);
  return res;
};

// {
//   approach: '',
//   chatroomID: 'fwagwe',
//   history: [
//     {
//       // bot:'hi',
//       user: '如何評估自己的退休生活需要，以決定是否需要作額外的強積金供款？'
//     }
//   ]
// }
// export const getChatStream = async (params: any) => {
//   const res = await request.post('/chat/stream', params);
//   return res;
// };
export const getChatStream = async (params: any) => {
  const response = await fetch('http://localhost:3004/api/chat/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(params)
  });
  return response;
};

export const getChatUpload = async (params: any) => {
  const res = await request.post('/chat/upload', params);
  console.log('res', res);
  return res;
};
