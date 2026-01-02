import Navbar from "@/components/marketing/commons/Navbar";
import Footer from "@/components/marketing/commons/Footer";

export default function MarketingLayout({
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

