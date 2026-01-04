'use client';

import { useSocialAuthenticateMutation } from '@/store/features/auth/authApiSlice';
import { useSocialAuth } from '@/hooks/auth';
import { Spinner } from '@/components/common';

export default function Page() {
	const [googleAuthenticate] = useSocialAuthenticateMutation();
	useSocialAuth((credentials) => googleAuthenticate(credentials).then(() => {}), 'google-oauth2');

	return (
		<div className='my-8'>
			<Spinner lg />
		</div>
	);
}