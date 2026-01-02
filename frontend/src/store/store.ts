import { configureStore } from '@reduxjs/toolkit';
import pageTitleReducer from './pageTitleSlice';

export const store = configureStore({
  reducer: {
    pageTitle: pageTitleReducer,
  },
  devTools: process.env.NODE_ENV !== 'production',
});

export type AppStore = ReturnType<typeof makeStore>;
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = AppStore['dispatch'];

// export type RootState = ReturnType<typeof store.getState>;
// export type AppDispatch = typeof store.dispatch;
