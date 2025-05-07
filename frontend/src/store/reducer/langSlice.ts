import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { RootState } from '@/store';
import config from '@/config';

export interface Language {
  lang: string;
}

const initialState: Language = {
  lang: localStorage.getItem('i18nextLng') || config.lang
};

export const langSlice = createSlice({
  name: 'language',
  initialState,
  reducers: {
    setLanguage: (state, action: PayloadAction<string>) => {
      state.lang = action.payload;
    }
  }
});

export const { setLanguage } = langSlice.actions;

export const selectLanguage = (state: RootState) => state.language.lang;

export default langSlice.reducer;
