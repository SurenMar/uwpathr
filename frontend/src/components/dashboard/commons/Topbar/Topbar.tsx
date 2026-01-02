"use client";

import TopbarUserDropdown from "./TopbarUserDropdown";
import { useAppSelector } from "@/store/hooks";

export default function Topbar() {
  const pageTitle = useAppSelector((state) => state.pageTitle.title);

  return (
    <nav className="w-full h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6">
      <h1 className="text-2xl font-bold text-gray-800">{pageTitle}</h1>
      <div className="flex gap-4">
       <TopbarUserDropdown />
      </div>
    </nav>
  );
}