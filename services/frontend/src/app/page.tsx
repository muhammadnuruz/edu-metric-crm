"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { getUserFromToken } from "@/lib/api";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    const user = getUserFromToken();
    if (user) {
      router.replace("/dashboard");
    } else {
      router.replace("/login");
    }
  }, [router]);

  return (
    <div className="flex h-screen items-center justify-center">
      <div className="animate-pulse text-lg text-muted-foreground">Yuklanmoqda...</div>
    </div>
  );
}
