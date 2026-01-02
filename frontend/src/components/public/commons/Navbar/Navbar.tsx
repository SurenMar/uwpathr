import Link from "next/link";
import NavbarResourcesDropdown from "./NavbarResourcesDropdown";

export default function Navbar() {
  return (
    <nav className="w-full h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6">
      <Link href="/">
        <h1 className="text-2xl font-bold text-gray-800 hover:text-gray-600 cursor-pointer">UWPathr</h1>
      </Link>
      <div className="flex gap-4">
        <NavbarResourcesDropdown />
        <Link href="/auth/login" className="text-gray-700 hover:text-gray-900 font-medium">
          Login
        </Link>
        <Link href="/auth/register" className="text-gray-700 hover:text-gray-900 font-medium">
          Register
        </Link>
      </div>
    </nav>
  );
}