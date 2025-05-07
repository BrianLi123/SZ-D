import { createAsyncThunk, createSlice, PayloadAction } from '@reduxjs/toolkit';
import { RootState } from '@/store';
import { fetchLogin } from '@/services/api';
import { PURGE } from 'redux-persist';

export interface UserState {
  userInfo: API.UserInfo;
  token: string | undefined;
  isLogin: boolean;
}

const initialState: UserState = {
  userInfo: {},
  token: undefined,
  isLogin: false
};

export const login = createAsyncThunk(
  'user/fetchLogin',
  async (params: Expand<API.LoginParams>) => {
    // const response = await fetchLogin(params);
    const response = await Promise.resolve({
      "SessionKey": "jgtcmvrsvieexigzkfxrexsmwrebgxjemjdstcintteksnprbgyjnwgkmjitgwygtvpxwvzxqdgqietmlwasdfjowt",
      "UserInfo": {
        "ID": 33,
        "Name": "Admin",
        "Avatar": "http://dummyimage.com/60x60/50B347/FFF&text=Avatar",
        "Email": "c.hhbkha@blsxfr.ph",
        "Phone": "17332263899",
        "Address": "黑龙江省 大庆市 红岗区",
        "CreateTime": "1987-07-15"
      },
      MenuItems: []
    });
    return response;
  }
);

export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setToken: (state, action: PayloadAction<string>) => {
      state.token = action.payload;
    },
    setUserInfo: (state, action: PayloadAction<API.UserInfo>) => {
      state.userInfo = action.payload;
    }
  },

  extraReducers: (builder) => {
    builder
      .addCase(login.fulfilled, (state, action) => {
        const { UserInfo, SessionKey, MenuItems = [] } = action.payload;
        state.userInfo = UserInfo;
        state.token = SessionKey;
        state.isLogin = true;
      })
      .addCase(login.rejected, (state) => {
        state.isLogin = false;
      })
      .addCase(PURGE, (state) => {
        // 不能用这种赋值为一个新对象的方式更新state，因为state是一个Immutable对象。
        // state = {
        //   userInfo: {} as User,
        //   token: undefined,
        //   isLogin: false
        // };
        // 可以用这种方式更新
        state.userInfo = {};
        state.token = undefined;
        state.isLogin = false;
      });
  }
});

export const { setToken, setUserInfo } = userSlice.actions;

export const selectToken = (state: RootState) => state.user.token;
export const selectUserInfo = (state: RootState) => state.user.userInfo;

export default userSlice.reducer;
