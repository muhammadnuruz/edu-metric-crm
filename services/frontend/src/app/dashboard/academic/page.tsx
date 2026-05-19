"use client";

import { useEffect, useState } from "react";
import { api, getUserFromToken } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";

interface AcademicRecord {
  id: number;
  student: number;
  student_name: string;
  subject_name: string;
  semester_name: string;
  grade_percentage: number;
  gpa_score: number;
  created_at: string;
}

export default function AcademicPage() {
  const [records, setRecords] = useState<AcademicRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const user = getUserFromToken();

  useEffect(() => {
    api.get<{ results: AcademicRecord[] }>("/academic/records/?page_size=100")
      .then((data) => setRecords(data.results || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const filtered = records.filter(
    (r) =>
      r.student_name.toLowerCase().includes(search.toLowerCase()) ||
      r.subject_name.toLowerCase().includes(search.toLowerCase())
  );

  const gradeColor = (pct: number) =>
    pct >= 80 ? "text-green-700 bg-green-100" :
    pct >= 60 ? "text-yellow-700 bg-yellow-100" :
    "text-red-700 bg-red-100";

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold">Akademik Natijalar</h1>
        <p className="text-sm text-muted-foreground">GPA va fan bo&apos;yicha baholar (max 40 ball)</p>
      </div>

      <div className="mb-4">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Talaba yoki fan bo'yicha qidirish..."
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
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Fan</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Semestr</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Baho (%)</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">GPA Ball</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Sana</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((r) => (
                    <tr key={r.id} className="border-b transition-colors hover:bg-muted/30">
                      <td className="px-4 py-3 font-medium">{r.student_name}</td>
                      <td className="px-4 py-3">{r.subject_name}</td>
                      <td className="px-4 py-3 text-muted-foreground">{r.semester_name}</td>
                      <td className="px-4 py-3 text-center">
                        <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${gradeColor(r.grade_percentage)}`}>
                          {r.grade_percentage}%
                        </span>
                      </td>
                      <td className="px-4 py-3 text-center font-bold">{r.gpa_score}/40</td>
                      <td className="px-4 py-3 text-muted-foreground">{new Date(r.created_at).toLocaleDateString("uz")}</td>
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
