import { ChangeEvent } from 'react';
import Link from 'next/link';

interface Props {
	labelId: string;
	type: string;
	onChange: (event: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => void;
	value: string;
	children: React.ReactNode;
	link?: {
		linkText: string;
		linkUrl: string;
	};
	required?: boolean;
	options?: string[];
}

export default function Input({
	labelId,
	type,
	onChange,
	value,
	children,
	link,
	required = false,
	options,
}: Props) {
	return (
		<div>
			<div className='flex justify-between align-center'>
				<label
					htmlFor={labelId}
					className='block text-sm font-medium leading-6 text-gray-900'
				>
					{children}
				</label>
				{link && (
					<div className='text-sm'>
						<Link
							className='font-semibold text-indigo-600 hover:text-indigo-500'
							href={link.linkUrl}
						>
							{link.linkText}
						</Link>
					</div>
				)}
			</div>
			<div className='mt-2'>
				{type === 'select' ? (
					<select
						id={labelId}
						className='block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
						name={labelId}
						onChange={onChange}
						value={value}
						required={required}
					>
						{options?.map((option) => (
							<option key={option} value={option}>
								{option}
							</option>
						))}
					</select>
				) : (
					<input
						id={labelId}
						className='block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'
						name={labelId}
						type={type}
						onChange={onChange}
						value={value}
						required={required}
					/>
				)}
			</div>
		</div>
	);
}