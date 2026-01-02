import Navbar from "@/components/public/commons/Navbar";
import Footer from "@/components/public/commons/Footer";

export default function PublicLayout({
  children 
}: { 
  children: React.ReactNode 
}) {
  return (
    <>
      <header><Navbar /></header>
      <main>{children}</main>
      <Footer />
    </>
  )
}

