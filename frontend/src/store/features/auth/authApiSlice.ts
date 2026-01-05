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

interface RegisterArgs {
	first_name: string;
	start_year: number;
	email: string;
	password: string;
	re_password: string;
	captcha_token: string;
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
			providesTags: ['UserChecklists'],
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
		register: builder.mutation<void, RegisterArgs>({
			query: ({
				first_name,
        start_year,
				email,
				password,
				re_password,
				captcha_token,
			}) => ({
				url: '/users/',
				method: 'POST',
				body: {
					first_name,
          start_year,
					email,
					password,
					re_password,
					captcha_token,
				},
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
		deleteAccount: builder.mutation({
			query: () => ({
				url: '/delete-account/',
				method: 'DELETE',
			}),
		}),
		createChecklist: builder.mutation({
			query: ({ specialization, year }: { specialization: number; year: number }) => ({
				url: '/user-checklists/',
				method: 'POST',
				body: { specialization, year },
			}),
		}),
		createUserCourse: builder.mutation<{ id: number }, { courseId: string; courseList?: 'taken' | 'planned' | 'wishlist' }>({ 
			query: ({ courseId, courseList = 'taken' }) => {
				console.log('createUserCourse mutation query called with:', { courseId, courseList });
				const body = { course: courseId, course_list: courseList };
				console.log('Request body:', body);
				return {
					url: '/user-courses/',
					method: 'POST',
					body,
				};
			},
			async onQueryStarted({ courseId }, { dispatch, queryFulfilled }) {
				try {
					await queryFulfilled;
					// Invalidate user courses cache to update the courses list
					dispatch(authApiSlice.util.invalidateTags(['UserCourses']));
				} catch (err) {
					console.error('Failed to create user course:', err);
				}
			},
		}),
		updateCheckboxNode: builder.mutation<void, { nodeId: string; userCourseId: number | null }>({ 
			query: ({ nodeId, userCourseId }) => ({
					url: `/user-checklist-nodes/${nodeId}/`,
					method: 'PATCH',
					body: { selected_course: userCourseId },
			}),
			async onQueryStarted({ nodeId, userCourseId }, { dispatch, queryFulfilled }) {
				try {
					await queryFulfilled;
					// Invalidate the user checklists cache to force a refetch of the updated checklist
					dispatch(authApiSlice.util.invalidateTags(['UserChecklists']));
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
	useDeleteAccountMutation,
	useCreateChecklistMutation,
	useCreateUserCourseMutation,
	useUpdateCheckboxNodeMutation,
} = authApiSlice;