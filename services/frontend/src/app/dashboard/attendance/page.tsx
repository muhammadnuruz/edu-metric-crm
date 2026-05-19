"use client";

import { useEffect, useState } from "react";
import { api, getUserFromToken } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";

interface AttendanceSummary {
  id: number;
  student: number;
  student_name: string;
  semester_name: string;
  total_classes: number;
  present_count: number;
  absent_count: number;
  late_count: number;
  excused_count: number;
  attendance_percentage: number;
  attendance_score: number;
}

export default function AttendancePage() {
  const [records, setRecords] = useState<AttendanceSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const user = getUserFromToken();
  const isAdmin = user?.role === "admin";
  const isTeacher = user?.role === "teacher";

  useEffect(() => {
    api.get<{ results: AttendanceSummary[] }>("/attendance/summary/?page_size=100")
      .then((data) => setRecords(data.results || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const filtered = records.filter((r) =>
    r.student_name.toLowerCase().includes(search.toLowerCase())
  );

  const pctColor = (pct: number) =>
    pct >= 90 ? "text-green-700 bg-green-100" :
    pct >= 70 ? "text-yellow-700 bg-yellow-100" :
    "text-red-700 bg-red-100";

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold">Davomat</h1>
        <p className="text-sm text-muted-foreground">Talabalar davomati va ballari (max 20 ball)</p>
      </div>

      <div className="mb-4">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Talaba bo'yicha qidirish..."
          className="flex h-10 w-full max-w-md rounded-md border border-input bg-white px-3 py-2 text-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        />
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
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Talaba</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Semestr</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Jami dars</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Qatnashdi</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Kelmadi</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Kechikdi</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Sababli</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Foiz</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Ball</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((r) => (
                    <tr key={r.id} className="border-b transition-colors hover:bg-muted/30">
                      <td className="px-4 py-3 font-medium">{r.student_name}</td>
                      <td className="px-4 py-3 text-muted-foreground">{r.semester_name}</td>
                      <td className="px-4 py-3 text-center">{r.total_classes}</td>
                      <td className="px-4 py-3 text-center text-green-600 font-medium">{r.present_count}</td>
                      <td className="px-4 py-3 text-center text-red-600 font-medium">{r.absent_count}</td>
                      <td className="px-4 py-3 text-center text-yellow-600">{r.late_count}</td>
                      <td className="px-4 py-3 text-center text-blue-600">{r.excused_count}</td>
                      <td className="px-4 py-3 text-center">
                        <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${pctColor(r.attendance_percentage)}`}>
                          {r.attendance_percentage}%
                        </span>
                      </td>
                      <td className="px-4 py-3 text-center font-bold">{r.attendance_score}/20</td>
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
