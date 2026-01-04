'use client';

import { useState, useRef, useEffect } from "react";

export default function NavbarResourcesDropdown() {
  const [open, setOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setOpen(false);
      }
    };

    if (open) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [open]);

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setOpen(!open)}
        className="text-gray-700 hover:text-gray-900 font-medium flex items-center gap-1"
      >
        Resources
        <svg
          className={`w-4 h-4 transition-transform ${open ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-56 bg-white border border-gray-200 rounded-lg shadow-lg overflow-hidden z-50">
          <a
            href="https://cs.uwaterloo.ca"
            target="_blank"
            rel="noopener noreferrer"
            className="block px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
          >
            UW CS Home Page
          </a>
          <a
            href="https://uwaterloo.ca/computer-science/advising"
            target="_blank"
            rel="noopener noreferrer"
            className="block px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 transition-colors border-t border-gray-100"
          >
            UW CS Advising
          </a>
        </div>
      )}
    </div>
  );
}