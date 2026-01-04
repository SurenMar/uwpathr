'use client';

import { useState, useRef, useEffect } from 'react';
import { useRetrieveUserChecklistsQuery, useRetrieveCheckboxAllowedCoursesQuery } from '@/store/features/auth/authApiSlice';
import { Spinner } from '@/components/common';

interface ChecklistNode {
  id: string;
  title: string;
  requirement_type: string;
  units_required: number | null;
  units_gathered: number | null;
  children: ChecklistNode[];
  completed: boolean;
}

interface Course {
  id: string;
  code: string;
  number: string;
}

function CourseSearchInput({ checkboxId }: { checkboxId: string }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  
  const { data: allowedCoursesData, isLoading, error } = useRetrieveCheckboxAllowedCoursesQuery(checkboxId);

  // Extract courses from the response
  const courses = allowedCoursesData && allowedCoursesData.length > 0 ? allowedCoursesData[0].courses : [];

  const filteredCourses = courses.filter(course => 
    searchTerm === '' || 
    course.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
    course.number.toLowerCase().includes(searchTerm.toLowerCase())
  );

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDropdown(false);
      }
    };

    if (showDropdown) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showDropdown]);

  return (
    <div className="relative" ref={dropdownRef}>
      <input
        type="text"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        onFocus={() => setShowDropdown(true)}
        placeholder="Search courses..."
        className="w-48 px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      {showDropdown && (
        <div className="absolute z-10 w-64 mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto">
          {isLoading ? (
            <div className="p-3 text-center text-sm text-gray-500">
              Loading courses...
            </div>
          ) : error ? (
            <div className="p-3 text-center text-sm text-red-500">
              Error loading courses
            </div>
          ) : filteredCourses.length === 0 ? (
            <div className="p-3 text-center text-sm text-gray-500">
              {courses.length > 0 ? 'No matching courses' : 'No courses found'}
            </div>
          ) : (
            filteredCourses.map((course) => (
              <button
                key={course.id}
                onClick={() => {
                  setSearchTerm(course.code);
                  setShowDropdown(false);
                }}
                className="w-full text-left px-3 py-2 hover:bg-gray-100 transition-colors"
              >
                <div className="font-medium text-sm">{course.code}</div>
                <div className="text-xs text-gray-600">{course.number}</div>
              </button>
            ))
          )}
        </div>
      )}
    </div>
  );
}

function ChecklistNodeComponent({ node, level = 0 }: { node: ChecklistNode; level?: number }) {
  const [isExpanded, setIsExpanded] = useState(true);
  const hasChildren = node.children && node.children.length > 0;
  
  const bgColor = node.requirement_type === 'head' ? 'bg-blue-50' : 
                  node.requirement_type === 'group' ? 'bg-gray-50' : 
                  'bg-white';
  
  return (
    <div className={`${bgColor} border-b border-gray-200`}>
      <div className={`py-3 px-4 flex items-center gap-3`} style={{ paddingLeft: `${level * 2 + 1}rem` }}>
        {hasChildren && (
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="flex-shrink-0 w-5 h-5 flex items-center justify-center hover:bg-gray-200 rounded transition-colors"
          >
            <svg
              className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-90' : ''}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        )}
        {!hasChildren && node.requirement_type === 'checkbox' && (
          <>
            <input
              type="checkbox"
              checked={node.completed}
              readOnly
              className="w-4 h-4 rounded border-gray-300 flex-shrink-0"
            />
            <CourseSearchInput checkboxId={node.id} />
          </>
        )}
        {!hasChildren && node.requirement_type !== 'checkbox' && (
          <div className="w-5" />
        )}
        <span className="font-medium text-gray-800">{node.title}</span>
        {node.requirement_type === 'group' && node.units_required !== null && (
          <span className="text-sm text-gray-600">
            {node.units_gathered ?? 0}/{node.units_required} Total Units
          </span>
        )}
        {node.requirement_type !== 'group' && node.units_required && (
          <span className="text-sm text-gray-600">({node.units_required} units)</span>
        )}
      </div>
      {hasChildren && isExpanded && (
        <div>
          {node.children.map((child) => (
            <ChecklistNodeComponent key={child.id} node={child} level={level + 1} />
          ))}
        </div>
      )}
    </div>
  );
}

export default function Checklist() {
  const { data: checklists, isLoading, error } = useRetrieveUserChecklistsQuery();

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <Spinner lg />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-lg">
        <p className="text-red-800">Failed to load checklist. Please try again.</p>
      </div>
    );
  }

  if (!checklists || checklists.length === 0) {
    return (
      <div className="p-6 bg-gray-50 border border-gray-200 rounded-lg">
        <p className="text-gray-600">No checklist found. Creating one for you...</p>
      </div>
    );
  }

  const checklist = checklists[0];

  return (
    <main className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">CS Checklist</h1>
        <div className="flex gap-4 text-sm text-gray-600">
          <span>Year: {checklist.year}</span>
          <span>•</span>
          <span>{checklist.taken_course_units}/{checklist.units_required} Total Units</span>
          <span>•</span>
          <span>Planned: {checklist.planned_course_units}</span>
        </div>
      </div>

      <div className="space-y-4">
        {checklist.nodes && checklist.nodes.length > 0 ? (
          checklist.nodes.map((node) => (
            <div key={node.id} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
              <ChecklistNodeComponent node={node} />
            </div>
          ))
        ) : (
          <div className="p-6 bg-gray-50 border border-gray-200 rounded-lg">
            <p className="text-gray-600">No checklist items found.</p>
          </div>
        )}
      </div>
    </main>
  );
}