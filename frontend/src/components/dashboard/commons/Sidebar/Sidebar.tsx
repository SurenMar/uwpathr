import Link from "next/link";
import SidebarResourcesDropdown from "./SidebarResourcesDropdown";

export default function Sidebar() {
  return (
    <nav className="w-64 h-screen bg-white border-r border-gray-200 flex flex-col p-6">
      <Link href="/">
        <h1 className="text-2xl font-bold text-gray-800 hover:text-gray-600 cursor-pointer mb-8">UWPathr</h1>
      </Link>
      <div className="flex flex-col gap-4">
        <SidebarResourcesDropdown />
      </div>
    </nav>
  );
}