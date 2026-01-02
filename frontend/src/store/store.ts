import { configureStore } from '@reduxjs/toolkit';
import pageTitleReducer from './features/topbar/pageTitleSlice';
import authReducer from './features/auth/authSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    pageTitle: pageTitleReducer,
  },
  devTools: process.env.NODE_ENV !== 'production',
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
