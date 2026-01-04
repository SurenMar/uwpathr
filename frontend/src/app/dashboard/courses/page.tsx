'use client';

import { useMemo, useState } from 'react';
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
    const [expandedCodes, setExpandedCodes] = useState<Record<string, boolean>>({});

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

    const coursesByCodeBySectionType = useMemo(() => {
        const result: Record<CourseList, Array<[string, typeof courses]>> = {
            taken: [],
            planned: [],
            wishlist: [],
        };

        Object.entries(groupedCourses).forEach(([sectionType, sectionCourses]) => {
            const grouped: Record<string, typeof sectionCourses> = {};
            sectionCourses.forEach(course => {
                if (!grouped[course.course.code]) {
                    grouped[course.course.code] = [];
                }
                grouped[course.course.code].push(course);
            });
            // Sort by code alphabetically
            result[sectionType as CourseList] = Object.entries(grouped).sort((a, b) => a[0].localeCompare(b[0]));
        });

        return result;
    }, [groupedCourses]);

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
                        const coursesByCode = coursesByCodeBySectionType[section.type];
                        
                        const bgColor = section.type === 'taken' ? 'bg-green-50' : 
                                       section.type === 'planned' ? 'bg-blue-50' : 
                                       'bg-red-50';
                        const textColor = section.type === 'taken' ? 'text-green-900' : 
                                         section.type === 'planned' ? 'text-blue-900' : 
                                         'text-red-900';
                        return (
                            <section key={section.type}>
                                <div className={`${bgColor} px-6 py-5 rounded-t-lg border-b-4 ${section.type === 'taken' ? 'border-green-400' : section.type === 'planned' ? 'border-blue-400' : 'border-red-400'}`}>
                                    <h2 className={`text-2xl font-bold ${textColor}`}>
                                        {section.title}
                                    </h2>
                                    <p className={`mt-1 text-sm ${section.type === 'taken' ? 'text-green-700' : section.type === 'planned' ? 'text-blue-700' : 'text-red-700'}`}>
                                        {section.description}
                                    </p>
                                    <p className='mt-2 text-sm font-medium text-gray-700'>
                                        {sectionCourses.length} course{sectionCourses.length !== 1 ? 's' : ''}
                                    </p>
                                </div>

                                <div className='overflow-hidden rounded-b-lg bg-white shadow'>
                                    {sectionCourses.length === 0 ? (
                                        <div className='px-6 py-8 text-center'>
                                            <p className='text-gray-500'>
                                                No {section.title.toLowerCase()} courses yet.
                                            </p>
                                        </div>
                                    ) : (
                                    <div className='p-4 space-y-6'>
                                        {coursesByCode.map(([code, coursesInCode]) => {
                                            const isExpanded = expandedCodes[code] !== false; // Default to expanded
                                            const toggleExpanded = () => {
                                                setExpandedCodes(prev => ({
                                                    ...prev,
                                                    [code]: !prev[code]
                                                }));
                                            };
                                            return (
                                            <div key={code}>
                                                <button
                                                    onClick={toggleExpanded}
                                                    className='w-full text-left flex items-center gap-2 px-2 py-2 mb-3 border-l-4 border-gray-400 hover:bg-gray-100 rounded transition-colors'
                                                >
                                                    <svg
                                                        className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-90' : ''}`}
                                                        fill='none'
                                                        stroke='currentColor'
                                                        viewBox='0 0 24 24'
                                                    >
                                                        <path strokeLinecap='round' strokeLinejoin='round' strokeWidth={2} d='M9 5l7 7-7 7' />
                                                    </svg>
                                                    <h3 className='text-lg font-semibold text-gray-700'>
                                                        {code}
                                                    </h3>
                                                </button>
                                                {isExpanded && (
                                                <ul className='space-y-3'>
                                                    {coursesInCode.map(userCourse => (
                                                        <li
                                                            key={userCourse.id}
                                                            className='px-6 py-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors ml-4'
                                                        >
                                                <div className='flex items-start justify-between'>
                                                    <div className='flex-1'>
                                                        <h3 className='font-semibold text-gray-900'>
                                                            {userCourse.course.code} {userCourse.course.number}
                                                        </h3>
                                                        <p className='mt-1 text-sm text-gray-600'>
                                                            {userCourse.course.title}
                                                        </p>
                                                        {userCourse.course.units && (
                                                            <p className='mt-2 text-xs text-gray-500'>
                                                                {userCourse.course.units} units
                                                            </p>
                                                        )}
                                                    </div>
                                                    <div className='flex items-center gap-6'>
                                                        <div className='flex items-center gap-6 text-xs text-gray-600'>
                                                            {userCourse.course.num_uwflow_ratings && userCourse.course.num_uwflow_ratings > 0 ? (
                                                                <>
                                                                    <div className='text-center'>
                                                                        <div className='font-semibold text-gray-900'>{userCourse.course.num_uwflow_ratings}</div>
                                                                        <div className='text-gray-500'>ratings</div>
                                                                    </div>
                                                                    {userCourse.course.uwflow_liked_rating !== null && (
                                                                        <div className='text-center'>
                                                                            <div className='font-semibold text-gray-900'>{userCourse.course.uwflow_liked_rating}%</div>
                                                                            <div className='text-gray-500'>liked</div>
                                                                        </div>
                                                                    )}
                                                                    {userCourse.course.uwflow_easy_ratings !== null && (
                                                                        <div className='text-center'>
                                                                            <div className='font-semibold text-gray-900'>{userCourse.course.uwflow_easy_ratings}%</div>
                                                                            <div className='text-gray-500'>easy</div>
                                                                        </div>
                                                                    )}
                                                                    {userCourse.course.uwflow_useful_ratings !== null && (
                                                                        <div className='text-center'>
                                                                            <div className='font-semibold text-gray-900'>{userCourse.course.uwflow_useful_ratings}%</div>
                                                                            <div className='text-gray-500'>useful</div>
                                                                        </div>
                                                                    )}
                                                                </>
                                                            ) : (
                                                                <div className='text-gray-400 text-center'>
                                                                    <div className='text-xs'>No ratings</div>
                                                                </div>
                                                            )}
                                                        </div>
                                                        <div className='ml-auto'>
                                                            {userCourse.course_list === 'taken' && (
                                                                <span className='inline-flex items-center rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-800'>
                                                                    Completed
                                                                </span>
                                                            )}
                                                            {userCourse.course_list === 'planned' && (
                                                                <span className='inline-flex items-center rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-800'>
                                                                    Planned
                                                                </span>
                                                            )}
                                                            {userCourse.course_list === 'wishlist' && (
                                                                <span className='inline-flex items-center rounded-full bg-red-100 px-3 py-1 text-sm font-medium text-red-800'>
                                                                    Wishlist
                                                                </span>
                                                            )}
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                        ))}
                                                </ul>
                                                )}
                                            </div>
                                            );
                                        })}
                                    </div>
                                )}
                                </div>
                            </section>
                        );
                    })}
                </div>
            </div>
        </main>
    );
}