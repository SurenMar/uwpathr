'use client';

import Link from 'next/link';
import { useState, ChangeEvent, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import { useRegisterMutation } from '@/store/features/auth/authApiSlice';
import { toast } from 'react-toastify';
import Spinner from '@/components/utils/Spinner';

export default function Page() {
  const router = useRouter();
  const [register, { isLoading }] = useRegisterMutation();

  const [formData, setFormData] = useState({
    email: '',
    first_name: '',
    start_year: '',
    password: '',
    confirm_password: '',
  });

  const { email, first_name, start_year, password, confirm_password } = formData;

  const onChange = (event: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = event.target;

    setFormData({ ...formData, [name]: value });
  };

  const onSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    
    register({
      first_name,
      start_year,
      email,
      password,
      re_password: confirm_password,
    })
    .unwrap()
    .then(() => {
      toast.success('Registration successful!');
      router.push('/auth/login');
    })
    .catch(() => {
      toast.error('Registration failed. Please try again.');
    });
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8">
        {/* Header */}
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-bold tracking-tight text-gray-900">
            Create your account
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Join UWPathr to start planning your degree
          </p>
        </div>

        {/* Form */}
        <form 
          className="space-y-6 bg-white py-8 px-6 rounded-lg shadow"
          onSubmit={onSubmit}
        >
          {/* Email Field */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              value={email}
              onChange={onChange}
              autoComplete="email"
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="you@example.com"
            />
          </div>

          {/* First Name Field */}
          <div>
            <label htmlFor="first_name" className="block text-sm font-medium text-gray-700">
              First name
            </label>
            <input
              id="first_name"
              name="first_name"
              type="text"
              value={first_name}
              onChange={onChange}
              autoComplete="given-name"
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="John"
            />
          </div>

          {/* Start Year Field */}
          <div>
            <label htmlFor="start_year" className="block text-sm font-medium text-gray-700">
              Start year
            </label>
            <select
              id="start_year"
              name="start_year"
              value={start_year}
              onChange={onChange}
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Select a year</option>
              <option value="2025">2025</option>
            </select>
          </div>

          {/* Password Field */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              value={password}
              onChange={onChange}
              autoComplete="new-password"
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="••••••••"
            />
          </div>

          {/* Confirm Password Field */}
          <div>
            <label htmlFor="confirm_password" className="block text-sm font-medium text-gray-700">
              Confirm password
            </label>
            <input
              id="confirm_password"
              name="confirm_password"
              type="password"
              value={confirm_password}
              onChange={onChange}
              autoComplete="new-password"
              required
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="••••••••"
            />
          </div>

          {/* Submit Button */}
          <div>
            <button
              type="submit"
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              {isLoading ? <Spinner sm /> : 'Register'}
            </button>
          </div>
        </form>

        {/* Footer Link */}
        <p className="text-center text-sm text-gray-600">
          Already have an account?{' '}
          <Link href="/auth/login" className="font-medium text-blue-600 hover:text-blue-500">
            Sign in
          </Link>
        </p>
      </div>
    </main>
  );
}