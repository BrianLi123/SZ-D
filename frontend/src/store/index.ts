import {
  configureStore,
  combineReducers,
  ThunkAction,
  Action
} from '@reduxjs/toolkit';
// 持久化数据
import {
  persistStore,
  persistReducer,
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER
} from 'redux-persist';
import storage from 'redux-persist/lib/storage';
// import storageSession from 'redux-persist/lib/storage/session';
import counterReducer from './reducer/counterSlice';
import userSlice from './reducer/userSlice';
import layoutSlice from './reducer/layoutSlice';
import loadingReducer from './reducer/loadingSlice';
import langSlice from './reducer/langSlice';

const rootReducer = combineReducers({
  loading: loadingReducer,
  counter: counterReducer,
  language: persistReducer({ key: 'language', storage }, langSlice),
  user: persistReducer(
    {
      key: 'user',
      storage,
      blacklist: ['status']
    },
    userSlice
  ),
  layout: persistReducer(
    {
      key: 'layout',
      storage
    },
    layoutSlice
  )
});

const persistConfig = {
  key: 'root',
  version: 1,
  storage,
  blacklist: ['user', 'layout', 'counter', 'loading', 'language']
};

const persistedReducer = persistReducer(persistConfig, rootReducer);

export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // 忽略了 Redux Persist 调度的所有操作类型。这样做是为了在浏览器控制台读取a non-serializable value was detected in the state时不会出现错误。
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER]
      }
    })
});

export const persistor = persistStore(store);

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
