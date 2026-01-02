import { createSlice } from '@reduxjs/toolkit';

interface AuthState {
  isAuthenticated: boolean;
  isLoading: boolean;
}

const initialState = {
  isAuthenticated: false,
  isLoading: true,
} as AuthState;

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setAuth(state) {
      state.isAuthenticated = true;
    },
    finishInitialLoad(state) {
      state.isLoading = false;
    },
    logout(state) {
      state.isAuthenticated = false;
    },
  },
});

export const { setAuth, finishInitialLoad, logout } = authSlice.actions;
export default authSlice.reducer;