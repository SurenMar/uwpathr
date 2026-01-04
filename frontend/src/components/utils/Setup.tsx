'use client';

import { useVerify, useChecklistInit } from '@/hooks/auth';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export default function Setup() {
	useVerify();
	useChecklistInit();

	return <ToastContainer />;
}