import Link from "next/link";
import TopbarUserDropdown from "./TopbarUserDropdown";

export default function Topbar() {
  return (
    <nav className="w-full h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6">
      <Link href="/">
        <h1 className="text-2xl font-bold text-gray-800 hover:text-gray-600 cursor-pointer">UWPathr</h1>
      </Link>
      <div className="flex gap-4">
       <TopbarUserDropdown />
      </div>
    </nav>
  );
}