import { useEffect, useRef } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAppDispatch } from '@/store/hooks';
import { setAuth } from '@/store/features/auth/authSlice';
import { useCreateChecklistMutation } from '@/store/features/auth/authApiSlice';
import { toast } from 'react-toastify';

export default function useSocialAuth(authenticate: (credentials: { provider: string; state: string; code: string }) => Promise<void>, provider: string) {
	const dispatch = useAppDispatch();
	const router = useRouter();
	const searchParams = useSearchParams();
	const [createChecklist] = useCreateChecklistMutation();

	const effectRan = useRef(false);

	useEffect(() => {
		const state = searchParams.get('state');
		const code = searchParams.get('code');

		if (state && code && !effectRan.current) {
			authenticate({ provider, state, code })
				.then(() => {
					dispatch(setAuth());
					// Create checklist for new user
					createChecklist({ specialization: 3, year: 2025 })
						.unwrap()
						.then(() => {
							toast.success('Logged in');
							router.push('/dashboard');
						})
						.catch(() => {
							// Checklist creation failed, but user was authenticated successfully
							toast.success('Logged in');
							router.push('/dashboard');
						});
				})
				.catch(() => {
					toast.error('Failed to log in');
					router.push('/auth/login');
				});
		}

		return () => {
			effectRan.current = true;
		};
	}, [authenticate, provider, dispatch, router, searchParams, createChecklist]);
}