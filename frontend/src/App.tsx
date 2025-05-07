import dayjs from 'dayjs';
import { Suspense } from 'react';
import { ConfigProvider, type ConfigProviderProps } from 'antd';
import { RouterProvider } from 'react-router-dom';
import router from '@/router/index';
import Loading from '@/components/Loading';
import 'dayjs/locale/zh-cn';
import 'dayjs/locale/zh-hk';

type Locale = ConfigProviderProps['locale'];

function AdminApp() {
  const lang = useAppSelector(selectLanguage);
  dayjs.locale(lang === 'hk' ? 'zh-hk' : lang);

  return (
    <ConfigProvider input={{ autoComplete: 'off' }}>
      <Suspense fallback={<Loading />}>
        <RouterProvider
          router={router}
          future={{
            v7_startTransition: true
          }}
        />
      </Suspense>
    </ConfigProvider>
  );
}

export default AdminApp;
