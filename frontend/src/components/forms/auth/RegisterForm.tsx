'use client';

import { FormEvent, useCallback, useEffect, useRef, useState } from 'react';
import Script from 'next/script';
import { useRegister } from '@/hooks/auth';
import { Form } from '@/components/forms/auth';

declare global {
	interface Window {
		turnstile?: {
			render: (container: HTMLElement, options: Record<string, unknown>) => string;
			reset: (widgetId?: string) => void;
			remove: (widgetId?: string) => void;
		};
	}
}

export default function RegisterForm() {
	const {
		first_name,
		start_year,
		email,
		password,
		re_password,
		isLoading,
		onChange,
		onSubmit,
		setCaptchaToken,
	} = useRegister();

	const siteKey = process.env.NEXT_PUBLIC_TURNSTILE_SITE_KEY ?? '';
	const [scriptLoaded, setScriptLoaded] = useState(false);
	const [turnstileReady, setTurnstileReady] = useState(false);
	const [initError, setInitError] = useState<string | null>(null);
	const [captchaMessage, setCaptchaMessage] = useState<string | null>(null);
	const captchaRef = useRef<HTMLDivElement | null>(null);
	const widgetIdRef = useRef<string | null>(null);

	const resetTurnstile = useCallback(() => {
		if (widgetIdRef.current && window.turnstile) {
			window.turnstile.reset(widgetIdRef.current);
		}
		setCaptchaToken(null);
	}, [setCaptchaToken]);

	const renderTurnstile = useCallback(() => {
		if (!siteKey || !window.turnstile || !captchaRef.current) return;
		if (widgetIdRef.current) {
			window.turnstile.reset(widgetIdRef.current);
			return;
		}

		widgetIdRef.current = window.turnstile.render(captchaRef.current, {
			sitekey: siteKey,
			action: 'signup',
			retry: 'auto',
			callback: (token: string) => {
				setCaptchaToken(token);
				setCaptchaMessage(null);
			},
			'error-callback': () => {
				setCaptchaToken(null);
				setCaptchaMessage('CAPTCHA could not be validated. Please try again.');
				resetTurnstile();
			},
			'expired-callback': () => {
				setCaptchaToken(null);
				setCaptchaMessage('CAPTCHA expired. Please try again.');
				resetTurnstile();
			},
			'refresh-expired': 'auto',
		});
	}, [resetTurnstile, setCaptchaToken, siteKey]);

	useEffect(() => {
		if (!scriptLoaded) return;

		let attempts = 0;
		const attemptRender = () => {
			if (window.turnstile) {
				setTurnstileReady(true);
				renderTurnstile();
				return;
			}

			attempts += 1;
			if (attempts > 30) {
				setInitError('CAPTCHA could not load. Check your ad/CSP settings and try again.');
				return;
			}
			window.setTimeout(attemptRender, 150);
		};

		attemptRender();
	}, [renderTurnstile, scriptLoaded]);

	const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
		if (!siteKey) {
			event.preventDefault();
			setCaptchaMessage('Signup CAPTCHA is not configured.');
			return;
		}

		const success = await onSubmit(event);
		if (!success) {
			resetTurnstile();
		}
	};

	const config = [
		{
			labelText: 'Email address',
			labelId: 'email',
			type: 'email',
			value: email,
			required: true,
		},
		{
			labelText: 'First name',
			labelId: 'first_name',
			type: 'text',
			value: first_name,
			required: true,
		},
		{
			labelText: 'Degree start year',
			labelId: 'start_year',
			type: 'select',
			value: start_year.toString(),
			required: true,
			options: ['2025'],
		},
		{
			labelText: 'Password',
			labelId: 'password',
			type: 'password',
			value: password,
			required: true,
		},
		{
			labelText: 'Confirm password',
			labelId: 're_password',
			type: 'password',
			value: re_password,
			required: true,
		},
	];

	return (
		<>
			{siteKey && (
				<Script
					src='https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit'
					strategy='afterInteractive'
					onLoad={() => setScriptLoaded(true)}
				/>
			)}
			<Form
				config={config}
				isLoading={isLoading}
				btnText='Sign up'
				onChange={onChange}
				onSubmit={handleSubmit}
					extraContent={
						siteKey ? (
							<div className='space-y-2'>
								<p className='sr-only' id='signup-captcha-label'>
									Complete the CAPTCHA challenge to finish signing up.
								</p>
								<div
									ref={captchaRef}
									className='flex justify-center'
									aria-labelledby='signup-captcha-label'
								/>
								{captchaMessage && (
									<p className='text-sm text-red-600'>{captchaMessage}</p>
								)}
								{initError && <p className='text-sm text-red-600'>{initError}</p>}
							</div>
						) : (
							<p className='text-sm text-red-600'>
								Signup CAPTCHA is not configured. Please try again later.
							</p>
						)
					}
			/>
		</>
	);
}