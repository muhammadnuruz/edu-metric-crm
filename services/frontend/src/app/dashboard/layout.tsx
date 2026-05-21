"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getUserFromToken } from "@/lib/api";
import { Sidebar } from "@/components/dashboard/sidebar";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [user, setUser] = useState<{ role: string; fullName: string } | null>(null);

  useEffect(() => {
    const u = getUserFromToken();
    if (!u) {
      router.replace("/login");
      return;
    }
    setUser(u);
  }, [router]);

  if (!user) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="animate-pulse text-muted-foreground">Yuklanmoqda...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50/50">
      <Sidebar role={user.role} fullName={user.fullName} />
      <main className="md:ml-64 min-h-screen p-4 md:p-8 pt-20 md:pt-8">{children}</main>
    </div>
  );
}
