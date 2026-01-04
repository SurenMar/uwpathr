'use client';

import { useMemo } from 'react';
import { useGetUserCoursesQuery } from '@/store/features/progress/progressApiSlice';
import Spinner from '@/components/common/Spinner';

type CourseList = 'taken' | 'planned' | 'wishlist';

interface CourseSection {
    title: string;
    type: CourseList;
    description: string;
}

const COURSE_SECTIONS: CourseSection[] = [
    {
        title: 'Taken',
        type: 'taken',
        description: 'Courses you have already completed',
    },
    {
        title: 'Planned',
        type: 'planned',
        description: 'Courses you plan to take',
    },
    {
        title: 'Wishlist',
        type: 'wishlist',
        description: 'Courses you are interested in',
    },
];

export default function CoursesPage() {
    const { data: courses, isLoading, error } = useGetUserCoursesQuery();

    const groupedCourses = useMemo(() => {
        const initial: Record<CourseList, typeof courses> = {
            taken: [],
            planned: [],
            wishlist: [],
        };
        if (!courses) return initial;
        return courses.reduce(
            (acc, course) => {
                if (!acc[course.course_list]) {
                    acc[course.course_list] = [];
                }
                const courseList = acc[course.course_list];
                if (courseList) {
                    courseList.push(course);
                }
                return acc;
            },
            initial
        );
    }, [courses]);

    if (isLoading) {
        return (
            <main className='min-h-screen bg-gray-50'>
                <div className='mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8'>
                    <h1 className='text-3xl font-bold tracking-tight text-gray-900 mb-8'>
                        Your Courses
                    </h1>
                    <div className='flex items-center justify-center py-12'>
                        <Spinner />
                    </div>
                </div>
            </main>
        );
    }

    if (error) {
        return (
            <main className='min-h-screen bg-gray-50'>
                <div className='mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8'>
                    <h1 className='text-3xl font-bold tracking-tight text-gray-900 mb-8'>
                        Your Courses
                    </h1>
                    <div className='rounded-md bg-red-50 p-4'>
                        <div className='flex'>
                            <div className='flex-shrink-0'>
                                <svg
                                    className='h-5 w-5 text-red-400'
                                    viewBox='0 0 20 20'
                                    fill='currentColor'
                                >
                                    <path
                                        fillRule='evenodd'
                                        d='M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z'
                                        clipRule='evenodd'
                                    />
                                </svg>
                            </div>
                            <div className='ml-3'>
                                <h3 className='text-sm font-medium text-red-800'>
                                    Failed to load courses
                                </h3>
                                <p className='mt-2 text-sm text-red-700'>
                                    There was a problem retrieving your courses. Please try again later.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        );
    }

    const totalCourses = courses?.length ?? 0;

    return (
        <main className='min-h-screen bg-gray-50'>
            <div className='mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8'>
                <div className='mb-8'>
                    <h1 className='text-3xl font-bold tracking-tight text-gray-900'>
                        Your Courses
                    </h1>
                    <p className='mt-2 text-lg text-gray-600'>
                        Total: {totalCourses} course{totalCourses !== 1 ? 's' : ''}
                    </p>
                </div>

                <div className='grid gap-8'>
                    {COURSE_SECTIONS.map(section => {
                        const sectionCourses = groupedCourses[section.type] || [];
                        return (
                            <section
                                key={section.type}
                                className='overflow-hidden rounded-lg bg-white shadow'
                            >
                                <div className='border-b border-gray-200 px-6 py-4'>
                                    <h2 className='text-xl font-semibold text-gray-900'>
                                        {section.title}{' '}
                                        <span className='text-sm font-normal text-gray-600'>
                                            ({sectionCourses.length})
                                        </span>
                                    </h2>
                                    <p className='mt-1 text-sm text-gray-600'>
                                        {section.description}
                                    </p>
                                </div>

                                {sectionCourses.length === 0 ? (
                                    <div className='px-6 py-8 text-center'>
                                        <p className='text-gray-500'>
                                            No {section.title.toLowerCase()} courses yet.
                                        </p>
                                    </div>
                                ) : (
                                    <ul className='divide-y divide-gray-200'>
                                        {sectionCourses.map(userCourse => (
                                            <li
                                                key={userCourse.id}
                                                className='px-6 py-4 hover:bg-gray-50 transition-colors'
                                            >
                                                <div className='flex items-start justify-between'>
                                                    <div className='flex-1'>
                                                        <h3 className='font-semibold text-gray-900'>
                                                            {userCourse.course.code}
                                                        </h3>
                                                        <p className='mt-1 text-sm text-gray-600'>
                                                            {userCourse.course.title}
                                                        </p>
                                                        {userCourse.course.units && (
                                                            <p className='mt-1 text-xs text-gray-500'>
                                                                {userCourse.course.units} units
                                                            </p>
                                                        )}
                                                    </div>
                                                    {userCourse.course_list === 'taken' && (
                                                        <span className='ml-4 inline-flex items-center rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-800'>
                                                            Completed
                                                        </span>
                                                    )}
                                                    {userCourse.course_list === 'planned' && (
                                                        <span className='ml-4 inline-flex items-center rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-800'>
                                                            Planned
                                                        </span>
                                                    )}
                                                    {userCourse.course_list === 'wishlist' && (
                                                        <span className='ml-4 inline-flex items-center rounded-full bg-purple-100 px-3 py-1 text-sm font-medium text-purple-800'>
                                                            Wishlist
                                                        </span>
                                                    )}
                                                </div>
                                            </li>
                                        ))}
                                    </ul>
                                )}
                            </section>
                        );
                    })}
                </div>
            </div>
        </main>
    );
}