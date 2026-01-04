'use client';

import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useRetrieveUserQuery, useLogoutMutation } from "@/store/features/auth/authApiSlice";
import { useAppDispatch } from "@/store/hooks";
import { logout as logoutAction } from "@/store/features/auth/authSlice";
import { apiSlice } from "@/store/services/apiSlice";

export default function TopbarUserDropdown() {
  const [open, setOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const isMountedRef = useRef(true);
  const router = useRouter();
  const dispatch = useAppDispatch();
  const { data: user } = useRetrieveUserQuery();
  const [logout] = useLogoutMutation();

  // Get display name: use first_name if available, otherwise email prefix
  const displayName = user?.first_name || user?.email?.split('@')[0] || 'Me';

  useEffect(() => {
    isMountedRef.current = true;
    return () => {
      isMountedRef.current = false;
    };
  }, []);

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

  const handleLogout = () => {
    setOpen(false);
    
    // Dispatch state changes first
    dispatch(logoutAction());
    dispatch(apiSlice.util.resetApiState());
    
    // Call logout API without waiting for response
    logout(undefined);
    
    // Navigate immediately
    router.replace('/');
  };

  return (
    <div className="relative flex items-center gap-2" ref={dropdownRef}>
      <span className="text-gray-700 font-medium">{displayName}</span>
      <button
        onClick={() => setOpen(!open)}
        className="p-1 rounded hover:bg-gray-100 transition-colors"
        aria-label="User menu"
      >
        <svg
          className={`w-5 h-5 text-gray-600 transition-transform ${open ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {open && (
        <div className="absolute right-0 top-full mt-2 w-48 bg-white border border-gray-200 rounded-lg shadow-lg overflow-hidden z-50">
          <button
            onClick={handleLogout}
            className="w-full text-left px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
          >
            Logout
          </button>
          <button
            className="w-full text-left px-4 py-3 text-sm text-red-600 hover:bg-red-50 transition-colors border-t border-gray-100"
          >
            Delete Account
          </button>
        </div>
      )}
    </div>
  );
}