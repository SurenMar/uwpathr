import { useEffect } from 'react';
import { useAppDispatch } from '@/store/hooks';
import { setAuth, finishInitialLoad } from '@/store/features/auth/authSlice';
import { useVerifyMutation } from '@/store/features/auth/authApiSlice';

export default function useVerify() {
	const dispatch = useAppDispatch();

	const [verify] = useVerifyMutation();

	useEffect(() => {
		verify(undefined)
			.unwrap()
			.then(() => {
				dispatch(setAuth());
			})
			.catch(() => {
				// Token verification failed, will be handled by logout state
			})
			.finally(() => {
				dispatch(finishInitialLoad());
			});
	}, [verify, dispatch]);
}