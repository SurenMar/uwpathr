import { useState, ChangeEvent, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import { useAppDispatch } from '@/store/hooks';
import { useLoginMutation, useRetrieveUserChecklistsQuery, useCreateChecklistMutation } from '@/store/features/auth/authApiSlice';
import { setAuth } from '@/store/features/auth/authSlice';
import { toast } from 'react-toastify';

export default function useLogin() {
	const router = useRouter();
	const dispatch = useAppDispatch();
	const [login, { isLoading }] = useLoginMutation();
	const [createChecklist] = useCreateChecklistMutation();

	const [formData, setFormData] = useState({
		email: '',
		password: '',
	});

	const { email, password } = formData;

	const onChange = (event: ChangeEvent<HTMLInputElement>) => {
		const { name, value } = event.target;

		setFormData({ ...formData, [name]: value });
	};

	const onSubmit = (event: FormEvent<HTMLFormElement>) => {
		event.preventDefault();

		login({ email, password })
			.unwrap()
			.then(() => {
				dispatch(setAuth());
				
				// After login, check if user has a checklist
				// This will be handled by a separate effect/component
				toast.success('Logged in');
				router.push('/dashboard');
			})
			.catch(() => {
				toast.error('Failed to log in');
			});
	};

	return {
		email,
		password,
		isLoading,
		onChange,
		onSubmit,
	};
}