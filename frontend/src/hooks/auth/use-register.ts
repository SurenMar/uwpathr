import { useState, ChangeEvent, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'react-toastify';
import { useRegisterMutation } from '@/store/features/auth/authApiSlice';

type SubmitResult = boolean;

export default function useRegister() {
	const router = useRouter();
	const [register, { isLoading }] = useRegisterMutation();
	const captchaEnabled = process.env.NEXT_PUBLIC_CAPTCHA_ENABLED === 'true';
	const [captchaToken, setCaptchaToken] = useState<string | null>(null);

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

		setFormData({ ...formData, [name]: name === 'start_year' ? Number(value) : value });
	};

	const parseErrorMessage = (error: unknown) => {
		if (error && typeof error === 'object' && 'data' in error) {
			const errData = (error as { data?: unknown }).data;
			if (errData && typeof errData === 'object') {
				const data = errData as Record<string, unknown>;
				if (typeof data.captcha === 'string') return data.captcha;
				if (Array.isArray(data.captcha) && typeof data.captcha[0] === 'string') return data.captcha[0];
				if (typeof data.detail === 'string') return data.detail;
			}
		}
		return 'Failed to register account';
	};

	const onSubmit = async (event: FormEvent<HTMLFormElement>): Promise<SubmitResult> => {
		event.preventDefault();

		if (captchaEnabled && !captchaToken) {
			toast.error('Please complete the CAPTCHA before signing up.');
			return false;
		}

		try {
			await register({
				first_name,
				start_year,
				email,
				password,
				re_password,
				...(captchaEnabled && captchaToken ? { captcha_token: captchaToken } : {}),
			}).unwrap();

			toast.success('You have registered successfully. Please login.');
			router.push('/auth/login');
			return true;
		} catch (error) {
			toast.error(parseErrorMessage(error));
			return false;
		} finally {
			setCaptchaToken(null);
		}
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
		setCaptchaToken,
		captchaToken,
	};
}