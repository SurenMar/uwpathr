'use client';

import Link from "next/link";
import { usePathname } from "next/navigation";
import SidebarResourcesDropdown from "./SidebarResourcesDropdown";

export default function Sidebar() {
  const pathname = usePathname();

  const navItems = [
    {
      name: "Checklist",
      href: "/dashboard",
      isActive: pathname === "/dashboard",
    },
    {
      name: "My Courses",
      href: "/dashboard/courses",
      isActive: pathname.startsWith("/dashboard/courses"),
    },
  ];

  return (
    <nav className="w-64 h-screen bg-white border-r border-gray-200 flex flex-col p-6">
      <Link href="/">
        <h1 className="text-2xl font-bold text-gray-800 hover:text-gray-600 cursor-pointer mb-8">UWPathr</h1>
      </Link>
      <div className="flex flex-col gap-2">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`px-4 py-2 rounded-lg transition-colors ${
              item.isActive
                ? "bg-blue-50 text-blue-600 font-medium"
                : "text-gray-700 hover:bg-gray-100"
            }`}
          >
            {item.name}
          </Link>
        ))}
        <div className="mt-4">
          <SidebarResourcesDropdown />
        </div>
      </div>
    </nav>
  );
}