'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAppSelector } from '@/store/hooks';
import { Spinner } from '@/components/common';

interface Props {
	children: React.ReactNode;
}

export default function RequireAuth({ children }: Props) {
	const router = useRouter();
	const { isLoading, isAuthenticated } = useAppSelector(state => state.auth);

	useEffect(() => {
		if (!isLoading && !isAuthenticated) {
			router.replace('/');
		}
	}, [isLoading, isAuthenticated, router]);

	if (isLoading) {
		return (
			<div className='flex justify-center my-8'>
				<Spinner lg />
			</div>
		);
	}

	if (!isAuthenticated) {
		return (
			<div className='flex justify-center my-8'>
				<Spinner lg />
			</div>
		);
	}

	return <>{children}</>;
}