"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard, Users, GraduationCap, Calendar, FileText,
  Award, Shield, AlertTriangle, RefreshCw, Briefcase,
  BarChart3, MessageSquare, ClipboardCheck, LogOut,
} from "lucide-react";
import { api } from "@/lib/api";

interface NavItem {
  label: string;
  href: string;
  icon: React.ReactNode;
  roles: string[];
}

const navItems: NavItem[] = [
  { label: "Bosh sahifa", href: "/dashboard", icon: <LayoutDashboard className="h-4 w-4" />, roles: ["admin", "teacher", "tutor", "komendant", "manager", "parent", "student"] },
  { label: "Talabalar", href: "/dashboard/students", icon: <Users className="h-4 w-4" />, roles: ["admin", "teacher", "tutor", "komendant", "manager"] },
  { label: "Akademik", href: "/dashboard/academic", icon: <GraduationCap className="h-4 w-4" />, roles: ["admin", "manager", "teacher", "student", "parent"] },
  { label: "Davomat", href: "/dashboard/attendance", icon: <Calendar className="h-4 w-4" />, roles: ["admin", "manager", "teacher", "student", "parent"] },
  { label: "Topshiriqlar", href: "/dashboard/assignments", icon: <FileText className="h-4 w-4" />, roles: ["admin", "manager", "teacher", "student", "parent"] },
  { label: "Faoliyat", href: "/dashboard/activities", icon: <Award className="h-4 w-4" />, roles: ["admin", "manager", "student", "parent"] },
  { label: "Baholash", href: "/dashboard/evaluations", icon: <ClipboardCheck className="h-4 w-4" />, roles: ["admin", "manager", "tutor", "komendant", "teacher", "student"] },
  { label: "Jarimalar", href: "/dashboard/penalties", icon: <AlertTriangle className="h-4 w-4" />, roles: ["admin", "manager", "teacher", "tutor", "komendant", "student"] },
  { label: "Tiklanish", href: "/dashboard/recovery", icon: <RefreshCw className="h-4 w-4" />, roles: ["admin", "manager", "teacher", "tutor", "komendant", "student"] },
  { label: "Bandlik", href: "/dashboard/employment", icon: <Briefcase className="h-4 w-4" />, roles: ["admin", "manager", "student"] },
  { label: "Grant reyting", href: "/dashboard/grants", icon: <BarChart3 className="h-4 w-4" />, roles: ["admin", "manager", "teacher", "tutor", "komendant", "parent", "student"] },
  { label: "Intizom", href: "/dashboard/discipline", icon: <Shield className="h-4 w-4" />, roles: ["admin", "manager", "tutor", "komendant"] },
  { label: "Fikr-mulohaza", href: "/dashboard/feedback", icon: <MessageSquare className="h-4 w-4" />, roles: ["admin", "manager", "teacher", "student"] },
];

export function Sidebar({ role, fullName }: { role: string; fullName: string }) {
  const pathname = usePathname();
  const filtered = navItems.filter((item) => item.roles.includes(role));

  const roleLabels: Record<string, string> = {
    admin: "Administrator",
    teacher: "O'qituvchi",
    tutor: "Tyutor",
    komendant: "Komendant",
    manager: "Unicron Manager",
    parent: "Ota-ona",
    student: "Talaba",
  };

  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 border-r bg-white">
      <div className="flex h-full flex-col">
        <div className="border-b p-6">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary text-sm font-bold text-primary-foreground">
              EM
            </div>
            <div>
              <h2 className="text-lg font-semibold">EduMetric</h2>
              <p className="text-xs text-muted-foreground">Grant Management</p>
            </div>
          </div>
        </div>

        <nav className="flex-1 overflow-y-auto p-4">
          <ul className="space-y-1">
            {filtered.map((item) => (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={cn(
                    "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                    pathname === item.href
                      ? "bg-primary/10 text-primary"
                      : "text-muted-foreground hover:bg-muted hover:text-foreground"
                  )}
                >
                  {item.icon}
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        <div className="border-t p-4">
          <div className="mb-3 rounded-lg bg-muted p-3">
            <p className="text-sm font-medium">{fullName}</p>
            <p className="text-xs text-muted-foreground">{roleLabels[role] || role}</p>
          </div>
          <button
            onClick={() => api.logout()}
            className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm text-muted-foreground transition-colors hover:bg-destructive/10 hover:text-destructive"
          >
            <LogOut className="h-4 w-4" />
            Chiqish
          </button>
        </div>
      </div>
    </aside>
  );
}
