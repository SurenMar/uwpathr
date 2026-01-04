'use client';

import { useState, useRef, useEffect } from 'react';

interface Course {
  id: string;
  code: string;
  number: string;
  title: string;
  units?: number;
}

interface SearchCoursesModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function SearchCoursesModal({ isOpen, onClose }: SearchCoursesModalProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [courses, setCourses] = useState<{ available: Course[]; filtered: Course[]; loading: boolean }>({
    available: [],
    filtered: [],
    loading: false,
  });
  const modalRef = useRef<HTMLDivElement>(null);

  // Fetch all courses (not just taken) to show available courses
  useEffect(() => {
    if (isOpen && courses.available.length === 0) {
      setCourses(prev => ({ ...prev, loading: true }));
      const url = `${process.env.NEXT_PUBLIC_HOST}/api/courses/?limit=10000`;
      fetch(url)
        .then(res => {
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          return res.json();
        })
        .then(data => {
          // Handle both paginated and non-paginated responses
          const courseList = Array.isArray(data) ? data : (data.results || []);
          setCourses(prev => ({
            ...prev,
            available: courseList,
            loading: false,
          }));
        })
        .catch(err => {
          console.error('Failed to fetch courses:', err);
          setCourses(prev => ({ ...prev, loading: false }));
        });
    }
  }, [isOpen, courses.available.length]);

  // Filter courses based on search term
  useEffect(() => {
    const parts = searchTerm.trim().split(/\s+/);
    const codePart = parts[0]?.toLowerCase() || '';
    const numberPart = parts[1]?.toLowerCase() || '';

    const filtered = courses.available.filter(course => {
      // First filter by code
      if (!course.code.toLowerCase().startsWith(codePart)) {
        return false;
      }
      // Then filter by number if provided
      if (numberPart && !course.number.toLowerCase().startsWith(numberPart)) {
        return false;
      }
      return true;
    });
    setCourses(prev => ({ ...prev, filtered }));
  }, [searchTerm, courses.available]);

  // Handle click outside modal
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (modalRef.current && !modalRef.current.contains(event.target as Node)) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [isOpen, onClose]);

  // Handle Escape key
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      return () => document.removeEventListener('keydown', handleEscape);
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-900/5 backdrop-blur-sm flex items-center justify-center z-50">
      <div
        ref={modalRef}
        className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[80vh] overflow-hidden flex flex-col"
      >
        <div className="border-b border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">Search Courses</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search by code and number..."
            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            autoFocus
          />
        </div>

        <div className="flex-1 overflow-y-auto p-6">
          {courses.loading ? (
            <div className="text-center text-gray-500 py-8">Loading courses...</div>
          ) : courses.filtered.length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              {searchTerm ? 'No courses found' : 'Start typing to search'}
            </div>
          ) : (
            <div className="space-y-1">
              {courses.filtered.map((course) => (
                <div
                  key={course.id}
                  className="p-3 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
                >
                  <div className="font-medium text-gray-900 text-sm">
                    {course.code} {course.number}
                  </div>
                  <div className="text-xs text-gray-600 mt-0.5">{course.title}</div>
                  {course.units && (
                    <div className="text-xs text-gray-500 mt-1">{course.units} units</div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
