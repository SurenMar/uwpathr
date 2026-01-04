import { apiSlice } from '@/store/services/apiSlice';

interface User {
	first_name: string;
	start_year: string;
	email: string;
}

interface SocialAuthArgs {
	provider: string;
	state: string;
	code: string;
}

interface CreateUserResponse {
	success: boolean;
	user: User;
}

interface UserChecklistNode {
	id: string;
	title: string;
	requirement_type: string;
	units_required: number | null;
	units_gathered: number | null;
	children: UserChecklistNode[];
	completed: boolean;
	original_checkbox: string;
}

interface UserChecklist {
	id: string;
	year: number;
	specialization: number;
	units_required: number;
	taken_course_units: number;
	planned_course_units: number;
	nodes: UserChecklistNode[];
}

interface Course {
	id: string;
	code: string;
	number: string;
}

interface CheckboxAllowedCoursesResponse {
	id: string;
	target_checkbox: string;
	courses: Course[];
}

const authApiSlice = apiSlice.injectEndpoints({
	endpoints: builder => ({
		retrieveUser: builder.query<User, void>({
			query: () => '/users/me/',
		}),
		retrieveUserChecklists: builder.query<UserChecklist[], void>({
			query: () => '/user-checklists/',
		}),
		retrieveCheckboxAllowedCourses: builder.query<CheckboxAllowedCoursesResponse[], string>({
			query: (checkboxId) => `/checkbox-allowed-courses/?target_checkbox=${checkboxId}`,
		}),
		socialAuthenticate: builder.mutation<
			CreateUserResponse,
			SocialAuthArgs
		>({
			query: ({ provider, state, code }) => ({
				url: `/o/${provider}/?state=${encodeURIComponent(
					state
				)}&code=${encodeURIComponent(code)}`,
				method: 'POST',
				headers: {
					Accept: 'application/json',
					'Content-Type': 'application/x-www-form-urlencoded',
				},
			}),
		}),
		login: builder.mutation({
			query: ({ email, password }) => ({
				url: '/jwt/create/',
				method: 'POST',
				body: { email, password },
			}),
		}),
		register: builder.mutation({
			query: ({
				first_name,
        start_year,
				email,
				password,
				re_password,
			}) => ({
				url: '/users/',
				method: 'POST',
				body: { first_name, start_year, email, password, re_password },
			}),
		}),
		verify: builder.mutation({
			query: () => ({
				url: '/jwt/verify/',
				method: 'POST',
			}),
		}),
		logout: builder.mutation({
			query: () => ({
				url: '/logout/',
				method: 'POST',
			}),
		}),
		createChecklist: builder.mutation({
			query: ({ specialization, year }: { specialization: number; year: number }) => ({
				url: '/user-checklists/',
				method: 'POST',
				body: { specialization, year },
			}),
		}),
		createUserCourse: builder.mutation<void, { courseId: string }>({ 
			query: ({ courseId }) => ({
				url: '/user-courses/',
				method: 'POST',
				body: { course: courseId, course_list: 'taken' },
			}),
		}),
		updateCheckboxNode: builder.mutation<void, { nodeId: string; selectedCourseId: string | null }>({ 
			query: ({ nodeId, selectedCourseId }) => ({
				url: `/user-checklist-nodes/${nodeId}/`,
				method: 'PATCH',
				body: { selected_course: selectedCourseId },
			}),
			async onQueryStarted({ nodeId, selectedCourseId }, { dispatch, queryFulfilled }) {
				// First, create the user course if we're setting a course
				if (selectedCourseId) {
					try {
						await dispatch(
							authApiSlice.endpoints.createUserCourse.initiate({ courseId: selectedCourseId })
						).unwrap();
					} catch (err) {
						console.error('Failed to create user course:', err);
						throw err;
					}
				}

				try {
					await queryFulfilled;
					// Refetch the user checklists after updating
					dispatch(authApiSlice.endpoints.retrieveUserChecklists.initiate());
				} catch (err) {
					console.error('Failed to update checkbox node:', err);
				}
			},
		}),
	})
});

export const {
	useRetrieveUserQuery,
	useRetrieveUserChecklistsQuery,
	useRetrieveCheckboxAllowedCoursesQuery,
	useSocialAuthenticateMutation,
	useLoginMutation,
	useRegisterMutation,
	useVerifyMutation,
	useLogoutMutation,
	useCreateChecklistMutation,
	useCreateUserCourseMutation,
	useUpdateCheckboxNodeMutation,
} = authApiSlice;