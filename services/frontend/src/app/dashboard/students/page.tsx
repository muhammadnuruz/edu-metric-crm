"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface Student {
  id: number;
  user: {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    phone: string;
    is_active: boolean;
  };
  student_id: string;
  group: string;
  course: number;
  semester: number;
  status: string;
  grant_status: string;
  mentor_name: string | null;
  tutor_name: string | null;
}

export default function StudentsPage() {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [filterGroup, setFilterGroup] = useState("");
  const [filterStatus, setFilterStatus] = useState("");

  useEffect(() => {
    api.get<{ results: Student[] }>("/auth/students/?page_size=100")
      .then((data) => setStudents(data.results || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const groups = [...new Set(students.map((s) => s.group))].sort();

  const filtered = students.filter((s) => {
    const name = `${s.user.first_name} ${s.user.last_name}`.toLowerCase();
    const matchSearch = name.includes(search.toLowerCase()) || s.student_id.includes(search);
    const matchGroup = !filterGroup || s.group === filterGroup;
    const matchStatus = !filterStatus || s.status === filterStatus;
    return matchSearch && matchGroup && matchStatus;
  });

  const grantStatusColors: Record<string, string> = {
    active: "bg-green-100 text-green-700",
    suspended: "bg-yellow-100 text-yellow-700",
    cancelled: "bg-red-100 text-red-700",
  };

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold">Talabalar</h1>
        <p className="text-sm text-muted-foreground">Talabalar ro&apos;yxati va profillari</p>
      </div>

      <div className="mb-4 flex flex-wrap gap-3">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Ism yoki ID bo'yicha qidirish..."
          className="flex h-10 w-64 rounded-md border border-input bg-white px-3 py-2 text-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        />
        <select
          value={filterGroup}
          onChange={(e) => setFilterGroup(e.target.value)}
          className="flex h-10 rounded-md border border-input bg-white px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        >
          <option value="">Barcha guruhlar</option>
          {groups.map((g) => <option key={g} value={g}>{g}</option>)}
        </select>
        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
          className="flex h-10 rounded-md border border-input bg-white px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        >
          <option value="">Barcha holatlar</option>
          <option value="grant">Grant</option>
          <option value="contract">Kontrakt</option>
        </select>
      </div>

      {loading ? (
        <div className="py-20 text-center text-muted-foreground">Yuklanmoqda...</div>
      ) : (
        <Card>
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b bg-muted/50">
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">ID</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Ism</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Guruh</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Kurs</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Holat</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Grant</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Mentor</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Tyutor</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((s) => (
                    <tr key={s.id} className="border-b transition-colors hover:bg-muted/30">
                      <td className="px-4 py-3 text-muted-foreground">{s.student_id}</td>
                      <td className="px-4 py-3 font-medium">{s.user.first_name} {s.user.last_name}</td>
                      <td className="px-4 py-3">{s.group}</td>
                      <td className="px-4 py-3 text-center">{s.course}</td>
                      <td className="px-4 py-3 text-center">
                        <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${
                          s.status === "grant" ? "bg-green-100 text-green-700" : "bg-blue-100 text-blue-700"
                        }`}>
                          {s.status === "grant" ? "Grant" : "Kontrakt"}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${
                          grantStatusColors[s.grant_status] || "bg-gray-100"
                        }`}>
                          {s.grant_status === "active" ? "Faol" : s.grant_status === "suspended" ? "To'xtatilgan" : "Bekor"}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm text-muted-foreground">{s.mentor_name || "-"}</td>
                      <td className="px-4 py-3 text-sm text-muted-foreground">{s.tutor_name || "-"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
