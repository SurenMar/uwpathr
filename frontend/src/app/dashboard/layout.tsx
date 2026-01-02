import { Sidebar } from "@/components/dashboard/commons/Sidebar";
import { Topbar } from "@/components/dashboard/commons/Topbar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
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