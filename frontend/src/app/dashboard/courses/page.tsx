'use client';

import { useMemo, useState } from 'react';
import { useGetUserCoursesQuery, useDeleteUserCourseMutation } from '@/store/features/progress/progressApiSlice';
import Spinner from '@/components/common/Spinner';
import CoursePathModal from '@/components/dashboard/courses/CoursePathModal';

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
    const { data: courses, isLoading, error, refetch } = useGetUserCoursesQuery();
    const [expandedCodes, setExpandedCodes] = useState<Record<string, boolean>>({});
    const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({
        taken: true,
        planned: true,
        wishlist: true,
    });
    const [deleteUserCourse] = useDeleteUserCourseMutation();
    const [deletingIds, setDeletingIds] = useState<Set<number>>(new Set());
    const [pathModalOpen, setPathModalOpen] = useState(false);
    const [selectedCourseForPath, setSelectedCourseForPath] = useState<{
        id: number;
        name: string;
    } | null>(null);

    const handleRemoveCourse = async (userCourseId: number) => {
        setDeletingIds(prev => new Set([...prev, userCourseId]));
        try {
            await deleteUserCourse(userCourseId).unwrap();
        } catch (err) {
            console.error('Failed to remove course:', err);
            setDeletingIds(prev => {
                const newSet = new Set(prev);
                newSet.delete(userCourseId);
                return newSet;
            });
        }
    };

    const handleOpenPathModal = (courseId: number, courseName: string) => {
        setSelectedCourseForPath({ id: courseId, name: courseName });
        setPathModalOpen(true);
    };

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
                                <div className={`${bgColor} px-6 py-5 rounded-t-lg border-b-4 ${section.type === 'taken' ? 'border-green-400' : section.type === 'planned' ? 'border-blue-400' : 'border-red-400'} flex items-center justify-between cursor-pointer`}
                                     onClick={() => setExpandedSections(prev => ({
                                         ...prev,
                                         [section.type]: !prev[section.type]
                                     }))}
                                >
                                    <div>
                                        <div className="flex items-center gap-3">
                                            <svg
                                                className={`w-5 h-5 transition-transform ${expandedSections[section.type] ? 'rotate-90' : ''}`}
                                                fill='none'
                                                stroke='currentColor'
                                                viewBox='0 0 24 24'
                                            >
                                                <path strokeLinecap='round' strokeLinejoin='round' strokeWidth={2} d='M9 5l7 7-7 7' />
                                            </svg>
                                            <h2 className={`text-2xl font-bold ${textColor}`}>
                                                {section.title}
                                            </h2>
                                        </div>
                                        <p className={`mt-1 text-sm ${section.type === 'taken' ? 'text-green-700' : section.type === 'planned' ? 'text-blue-700' : 'text-red-700'}`}>
                                            {section.description}
                                        </p>
                                    </div>
                                    <p className='text-sm font-medium text-gray-700'>
                                        {sectionCourses.length} course{sectionCourses.length !== 1 ? 's' : ''}
                                    </p>
                                </div>

                                {expandedSections[section.type] && (
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
                                                        <div className='ml-auto flex items-center gap-2'>
                                                            {(section.type === 'planned' || section.type === 'wishlist') && (
                                                                <button
                                                                    onClick={() => handleOpenPathModal(userCourse.course.id, `${userCourse.course.code} ${userCourse.course.number}`)}
                                                                    className='inline-flex items-center gap-2 px-3 py-1 text-sm font-medium rounded-md bg-blue-100 text-blue-800 hover:bg-blue-200 transition-colors'
                                                                >
                                                                    {userCourse.has_course_path ? 'View Path' : 'Create Path'}
                                                                </button>
                                                            )}
                                                            <button
                                                                onClick={() => handleRemoveCourse(userCourse.id)}
                                                                disabled={deletingIds.has(userCourse.id)}
                                                                className='inline-flex items-center gap-2 px-3 py-1 text-sm font-medium rounded-md bg-gray-200 text-gray-800 hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors'
                                                            >
                                                                {deletingIds.has(userCourse.id) ? (
                                                                    <>
                                                                        <svg className='w-4 h-4 animate-spin' fill='none' stroke='currentColor' viewBox='0 0 24 24'>
                                                                            <circle cx='12' cy='12' r='10' stroke='currentColor' strokeWidth='2' fill='none' opacity='0.25' />
                                                                            <path fill='currentColor' d='M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z' />
                                                                        </svg>
                                                                        Removing...
                                                                    </>
                                                                ) : (
                                                                    <>
                                                                        <svg className='w-4 h-4' fill='none' stroke='currentColor' viewBox='0 0 24 24'>
                                                                            <path strokeLinecap='round' strokeLinejoin='round' strokeWidth={2} d='M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16' />
                                                                        </svg>
                                                                        Remove
                                                                    </>
                                                                )}
                                                            </button>
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
                                )}
                            </section>
                        );
                    })}
                </div>
            </div>

            <CoursePathModal
                isOpen={pathModalOpen}
                onClose={() => {
                    setPathModalOpen(false);
                    setSelectedCourseForPath(null);
                }}
                courseId={selectedCourseForPath?.id || 0}
                courseName={selectedCourseForPath?.name || ''}
            />
        </main>
    );
}