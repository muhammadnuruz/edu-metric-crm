"use client";

import { useEffect, useState } from "react";
import { api, getUserFromToken } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

interface GrantScore {
  id: number;
  student: number;
  student_name: string;
  student_id: string;
  group: string;
  semester: number;
  academic_score: number;
  attendance_score: number;
  assignment_score: number;
  activity_score: number;
  tutor_score: number;
  discipline_score: number;
  base_total: number;
  penalty_score: number;
  recovery_score: number;
  employment_score: number;
  final_score: number;
  gpa_percentage: number;
  gpa_eligible: boolean;
  status: string;
  rank: number;
}

export default function GrantsPage() {
  const [scores, setScores] = useState<GrantScore[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [calculating, setCalculating] = useState(false);
  const user = getUserFromToken();

  useEffect(() => {
    loadScores();
  }, []);

  const loadScores = () => {
    api.get<{ results: GrantScore[] }>("/grants/scores/?ordering=rank&page_size=100")
      .then((data) => setScores(data.results || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  const handleCalculate = async () => {
    setCalculating(true);
    try {
      await api.post("/grants/scores/calculate/", { semester_id: 1 });
      loadScores();
    } catch {
    } finally {
      setCalculating(false);
    }
  };

  const filtered = scores.filter(
    (s) =>
      s.student_name.toLowerCase().includes(search.toLowerCase()) ||
      s.group.toLowerCase().includes(search.toLowerCase()) ||
      s.student_id.includes(search)
  );

  const statusColors: Record<string, string> = {
    pending: "bg-gray-100 text-gray-700",
    calculated: "bg-blue-100 text-blue-700",
    approved: "bg-green-100 text-green-700",
    grant_active: "bg-emerald-100 text-emerald-700",
    grant_suspended: "bg-yellow-100 text-yellow-700",
    grant_cancelled: "bg-red-100 text-red-700",
  };

  const statusLabels: Record<string, string> = {
    pending: "Kutilmoqda",
    calculated: "Hisoblangan",
    approved: "Tasdiqlangan",
    grant_active: "Grant faol",
    grant_suspended: "To'xtatilgan",
    grant_cancelled: "Bekor",
  };

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Grant Reyting</h1>
          <p className="text-sm text-muted-foreground">Barcha talabalar grant ballarini boshqarish</p>
        </div>
        {user?.role === "admin" && (
          <button
            onClick={handleCalculate}
            disabled={calculating}
            className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-primary/90 disabled:opacity-50"
          >
            {calculating ? "Hisoblanmoqda..." : "Ballarni hisoblash"}
          </button>
        )}
      </div>

      <div className="mb-4">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Ism, guruh yoki ID bo'yicha qidirish..."
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
                    <th className="px-3 py-3 text-left text-xs font-medium text-muted-foreground">#</th>
                    <th className="px-3 py-3 text-left text-xs font-medium text-muted-foreground">Talaba</th>
                    <th className="px-3 py-3 text-left text-xs font-medium text-muted-foreground">ID</th>
                    <th className="px-3 py-3 text-left text-xs font-medium text-muted-foreground">Guruh</th>
                    <th className="px-3 py-3 text-center text-xs font-medium text-muted-foreground">Akademik</th>
                    <th className="px-3 py-3 text-center text-xs font-medium text-muted-foreground">Davomat</th>
                    <th className="px-3 py-3 text-center text-xs font-medium text-muted-foreground">Topshiriq</th>
                    <th className="px-3 py-3 text-center text-xs font-medium text-muted-foreground">Faollik</th>
                    <th className="px-3 py-3 text-center text-xs font-medium text-muted-foreground">Tyutor</th>
                    <th className="px-3 py-3 text-center text-xs font-medium text-muted-foreground">Intizom</th>
                    <th className="px-3 py-3 text-center text-xs font-medium text-muted-foreground">Jami</th>
                    <th className="px-3 py-3 text-center text-xs font-medium text-muted-foreground">Jarima</th>
                    <th className="px-3 py-3 text-center text-xs font-medium text-muted-foreground">Yakuniy</th>
                    <th className="px-3 py-3 text-center text-xs font-medium text-muted-foreground">GPA</th>
                    <th className="px-3 py-3 text-center text-xs font-medium text-muted-foreground">Holat</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((s) => (
                    <tr key={s.id} className="border-b transition-colors hover:bg-muted/30">
                      <td className="px-3 py-2.5">
                        <span className={`inline-flex h-6 w-6 items-center justify-center rounded-full text-[10px] font-bold ${
                          s.rank === 1 ? "bg-amber-400 text-white" :
                          s.rank === 2 ? "bg-gray-300 text-gray-800" :
                          s.rank === 3 ? "bg-amber-600 text-white" :
                          "bg-muted text-muted-foreground"
                        }`}>{s.rank}</span>
                      </td>
                      <td className="px-3 py-2.5 font-medium">{s.student_name}</td>
                      <td className="px-3 py-2.5 text-muted-foreground">{s.student_id}</td>
                      <td className="px-3 py-2.5 text-muted-foreground">{s.group}</td>
                      <td className="px-3 py-2.5 text-center">{s.academic_score}</td>
                      <td className="px-3 py-2.5 text-center">{s.attendance_score}</td>
                      <td className="px-3 py-2.5 text-center">{s.assignment_score}</td>
                      <td className="px-3 py-2.5 text-center">{s.activity_score}</td>
                      <td className="px-3 py-2.5 text-center">{s.tutor_score}</td>
                      <td className="px-3 py-2.5 text-center">{s.discipline_score}</td>
                      <td className="px-3 py-2.5 text-center font-medium">{s.base_total}</td>
                      <td className="px-3 py-2.5 text-center">
                        {s.penalty_score < 0 && <span className="text-red-600">{s.penalty_score}</span>}
                        {s.recovery_score > 0 && <span className="text-green-600 ml-1">+{s.recovery_score}</span>}
                      </td>
                      <td className="px-3 py-2.5 text-center">
                        <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-bold ${
                          s.final_score >= 80 ? "bg-green-100 text-green-700" :
                          s.final_score >= 60 ? "bg-yellow-100 text-yellow-700" :
                          "bg-red-100 text-red-700"
                        }`}>{s.final_score}</span>
                      </td>
                      <td className="px-3 py-2.5 text-center">
                        <span className={`text-xs ${s.gpa_eligible ? "text-green-600" : "text-red-600 font-bold"}`}>
                          {s.gpa_percentage}%
                        </span>
                      </td>
                      <td className="px-3 py-2.5 text-center">
                        <span className={`inline-flex rounded-full px-2 py-0.5 text-[10px] font-medium ${statusColors[s.status] || "bg-gray-100"}`}>
                          {statusLabels[s.status] || s.status}
                        </span>
                      </td>
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
