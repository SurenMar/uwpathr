import { apiSlice } from '@/store/services/apiSlice';

// Types for Course and UserCourse
interface Course {
    id: number;
    code: string;
    number: number;
    title: string;
    description?: string;
    units?: number;
    category?: string[];
    uwflow_liked_rating?: number;
    uwflow_easy_ratings?: number;
    uwflow_useful_ratings?: number;
    num_uwflow_ratings?: number;
}

interface UserCourse {
    id: number;
    created_at: string;
    updated_at: string;
    course: Course;
    course_list: 'taken' | 'planned' | 'wishlist';
    prereqs_met?: boolean | null;
}

interface GetUserCoursesParams {
    course_list?: 'taken' | 'planned' | 'wishlist';
}

const progressApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getUserCourses: builder.query<UserCourse[], GetUserCoursesParams | void>({
            query: (params) => {
                const url = new URL('/user-courses/', `${process.env.NEXT_PUBLIC_HOST}/api`);
                
                if (params && 'course_list' in params && params.course_list) {
                    url.searchParams.append('course_list', params.course_list);
                }
                
                return url.pathname + url.search;
            },
            providesTags: [{ type: 'UserCourses' as const }],
        }),
        createUserCourse: builder.mutation<
            UserCourse,
            { course_id: number; course_list: 'taken' | 'planned' | 'wishlist' }
        >({
            query: ({ course_id, course_list }) => ({
                url: '/progress/user-courses/',
                method: 'POST',
                body: { course: course_id, course_list },
            }),
            invalidatesTags: [{ type: 'UserCourses' as const }],
        }),
        deleteUserCourse: builder.mutation<void, number>({
            query: (userCourseId) => ({
                url: `/progress/user-courses/${userCourseId}/`,
                method: 'DELETE',
            }),
            invalidatesTags: ['UserCourses'],
        }),
    }),
});

export const {
    useGetUserCoursesQuery,
    useCreateUserCourseMutation,
    useDeleteUserCourseMutation,
} = progressApiSlice;