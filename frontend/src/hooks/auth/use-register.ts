import { useState, ChangeEvent, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import { useRegisterMutation } from '@/store/features/auth/authApiSlice';
import { toast } from 'react-toastify';

export default function useRegister() {
	const router = useRouter();
	const [register, { isLoading }] = useRegisterMutation();

	const [formData, setFormData] = useState({
		first_name: '',
		start_year: 0,
		email: '',
		password: '',
		re_password: '',
	});

	const { first_name, start_year, email, password, re_password } = formData;

	const onChange = (event: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = event.target;

    setFormData({ ...formData, [name]: value });
  };

	const onSubmit = (event: FormEvent<HTMLFormElement>) => {
		event.preventDefault();

		register({ first_name, start_year, email, password, re_password })
			.unwrap()
			.then(() => {
				toast.success('You have registered successfully. Please login.');
				router.push('/auth/login');
			})
			.catch(() => {
				toast.error('Failed to register account');
			});
	};

	return {
		first_name,
		start_year,
		email,
		password,
		re_password,
		isLoading,
		onChange,
		onSubmit,
	};
}