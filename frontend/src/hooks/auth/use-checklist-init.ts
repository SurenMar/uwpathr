import { useEffect, useRef } from 'react';
import { useRetrieveUserChecklistsQuery, useCreateChecklistMutation } from '@/store/features/auth/authApiSlice';
import { useAppSelector } from '@/store/hooks';

export default function useChecklistInit() {
	const isAuthenticated = useAppSelector(state => state.auth.isAuthenticated);
	const { data: checklists, isLoading, refetch } = useRetrieveUserChecklistsQuery(undefined, {
		skip: !isAuthenticated,
	});
	const [createChecklist] = useCreateChecklistMutation();
	const hasCreatedChecklist = useRef(false);

	useEffect(() => {
		if (!isAuthenticated || isLoading || !checklists) return;

		// Check if user doesn't have a checklist
		if (checklists.length === 0 && !hasCreatedChecklist.current) {
			hasCreatedChecklist.current = true;
			// Create a checklist, then refetch to get the updated list
			createChecklist({ specialization: 3, year: 2025 })
				.unwrap()
				.then(() => {
					// Refetch to get the newly created checklist
					refetch();
				})
				.catch((error) => {
					console.error('Failed to create checklist:', error);
					hasCreatedChecklist.current = false;
				});
		}
	}, [isAuthenticated, isLoading, checklists, createChecklist, refetch]);

	return { checklists, isLoading };
}
