import ReactDOM from 'react-dom/client';
import { App } from 'antd';
import AdminApp from './App';
import { Provider } from 'react-redux';
import { store, persistor } from '@/store';
import { PersistGate } from 'redux-persist/integration/react';
// import { initUserInfo } from '@/hooks/useUserInfo';

import { DarkModeConfigProvider } from '@/components/DarkModeSwitch';
import { ThemeColorConfigProvider } from '@/components/ThemeColors';
import 'antd/dist/reset.css';
import './App.css';

// initUserInfo();

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <Provider store={store}>
    <PersistGate loading={null} persistor={persistor}>
      <DarkModeConfigProvider>
        <ThemeColorConfigProvider>
          <App
            message={{ maxCount: 1 }}
            notification={{ maxCount: 1, placement: 'bottom' }}
          >
            <AdminApp />
          </App>
        </ThemeColorConfigProvider>
      </DarkModeConfigProvider>
    </PersistGate>
  </Provider>
);
