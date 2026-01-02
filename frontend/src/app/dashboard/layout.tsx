import { Sidebar } from "@/components/dashboard/commons/Sidebar";
import { Topbar } from "@/components/dashboard/commons/Topbar";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({
  children,
}: DashboardLayoutProps) {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex flex-col flex-1">
        <header>
          <Topbar />
        </header>
        <main className="flex-1 overflow-auto bg-gray-50">
          {children}
        </main>
      </div>
    </div>
  );
}