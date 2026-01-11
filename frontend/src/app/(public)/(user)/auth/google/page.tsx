'use client';

import { Suspense } from 'react';
import { useSocialAuthenticateMutation } from '@/store/features/auth/authApiSlice';
import { useSocialAuth } from '@/hooks/auth';
import { Spinner } from '@/components/common';

function GoogleAuthContent() {
	const [googleAuthenticate] = useSocialAuthenticateMutation();
	useSocialAuth((credentials) => googleAuthenticate(credentials).then(() => {}), 'google-oauth2');

	return (
		<div className='my-8'>
			<Spinner lg />
		</div>
	);
}

export default function Page() {
	return (
		<Suspense fallback={<div className='my-8'><Spinner lg /></div>}>
			<GoogleAuthContent />
		</Suspense>
	);
}