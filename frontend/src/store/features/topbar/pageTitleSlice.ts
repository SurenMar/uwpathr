import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface PageTitleState {
  title: string;
}

const initialState: PageTitleState = {
  title: 'Dashboard',
};

const pageTitleSlice = createSlice({
  name: 'pageTitle',
  initialState,
  reducers: {
    setPageTitle: (state, action: PayloadAction<string>) => {
      state.title = action.payload;
    },
  },
});

export const { setPageTitle } = pageTitleSlice.actions;
export default pageTitleSlice.reducer;
