"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://10.30.1.219:8080/api/v1";

interface PublicScore {
  rank: number;
  student_name: string;
  group: string;
  academic_score: number;
  attendance_score: number;
  assignment_score: number;
  activity_score: number;
  tutor_score: number;
  discipline_score: number;
  base_total: number;
  final_score: number;
  status: string;
}

export default function PublicRatingPage() {
  const [scores, setScores] = useState<PublicScore[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/grants/scores/public_rating/`)
      .then((r) => r.json())
      .then(setScores)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const filtered = scores.filter(
    (s) =>
      s.student_name.toLowerCase().includes(search.toLowerCase()) ||
      s.group.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <header className="border-b bg-white/80 backdrop-blur-sm">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary text-sm font-bold text-white">
              EM
            </div>
            <div>
              <h1 className="text-lg font-bold">EduMetric</h1>
              <p className="text-xs text-muted-foreground">PDP University Grant Reyting</p>
            </div>
          </div>
          <a
            href="/login"
            className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-primary/90"
          >
            Kirish
          </a>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-8">
        <div className="mb-8 text-center">
          <h2 className="text-3xl font-bold">Grant Reytingi</h2>
          <p className="mt-2 text-muted-foreground">
            Talabalarning grant ball reytingi - shaffof baholash tizimi
          </p>
        </div>

        <div className="mb-6 flex items-center gap-4">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Ism yoki guruh bo'yicha qidirish..."
            className="flex h-10 w-full max-w-md rounded-md border border-input bg-white px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
          <div className="text-sm text-muted-foreground">
            Jami: {filtered.length} talaba
          </div>
        </div>

        {loading ? (
          <div className="py-20 text-center text-muted-foreground">Yuklanmoqda...</div>
        ) : filtered.length === 0 ? (
          <Card>
            <CardContent className="py-20 text-center text-muted-foreground">
              Ma&apos;lumot topilmadi
            </CardContent>
          </Card>
        ) : (
          <Card>
            <CardContent className="p-0">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b bg-muted/50">
                      <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">#</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Talaba</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Guruh</th>
                      <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Akademik<br/><span className="text-[10px]">/40</span></th>
                      <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Davomat<br/><span className="text-[10px]">/20</span></th>
                      <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Topshiriq<br/><span className="text-[10px]">/15</span></th>
                      <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Faollik<br/><span className="text-[10px]">/10</span></th>
                      <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Tyutor<br/><span className="text-[10px]">/5</span></th>
                      <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Intizom<br/><span className="text-[10px]">/10</span></th>
                      <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Jami</th>
                      <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Yakuniy</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filtered.map((s, i) => (
                      <tr
                        key={i}
                        className={`border-b transition-colors hover:bg-muted/30 ${
                          s.rank <= 3 ? "bg-amber-50/50" : ""
                        }`}
                      >
                        <td className="px-4 py-3">
                          <span className={`inline-flex h-7 w-7 items-center justify-center rounded-full text-xs font-bold ${
                            s.rank === 1 ? "bg-amber-400 text-white" :
                            s.rank === 2 ? "bg-gray-300 text-gray-800" :
                            s.rank === 3 ? "bg-amber-600 text-white" :
                            "bg-muted text-muted-foreground"
                          }`}>
                            {s.rank}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-sm font-medium">{s.student_name}</td>
                        <td className="px-4 py-3 text-sm text-muted-foreground">{s.group}</td>
                        <td className="px-4 py-3 text-center text-sm">{s.academic_score}</td>
                        <td className="px-4 py-3 text-center text-sm">{s.attendance_score}</td>
                        <td className="px-4 py-3 text-center text-sm">{s.assignment_score}</td>
                        <td className="px-4 py-3 text-center text-sm">{s.activity_score}</td>
                        <td className="px-4 py-3 text-center text-sm">{s.tutor_score}</td>
                        <td className="px-4 py-3 text-center text-sm">{s.discipline_score}</td>
                        <td className="px-4 py-3 text-center text-sm font-medium">{s.base_total}</td>
                        <td className="px-4 py-3 text-center">
                          <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-bold ${
                            s.final_score >= 80 ? "bg-green-100 text-green-700" :
                            s.final_score >= 60 ? "bg-yellow-100 text-yellow-700" :
                            "bg-red-100 text-red-700"
                          }`}>
                            {s.final_score}
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

        <div className="mt-8 grid gap-4 md:grid-cols-3">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-base">Ball tizimi</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between"><span>Akademik natija</span><span className="font-medium">40 ball</span></div>
                <div className="flex justify-between"><span>Davomat</span><span className="font-medium">20 ball</span></div>
                <div className="flex justify-between"><span>Topshiriqlar</span><span className="font-medium">15 ball</span></div>
                <div className="flex justify-between"><span>Faollik</span><span className="font-medium">10 ball</span></div>
                <div className="flex justify-between"><span>Tyutor bahosi</span><span className="font-medium">5 ball</span></div>
                <div className="flex justify-between"><span>Intizom</span><span className="font-medium">10 ball</span></div>
                <div className="flex justify-between border-t pt-2 font-semibold"><span>Jami</span><span>100 ball</span></div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-base">Bonus va Jarima</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between"><span>Jarima (max)</span><span className="font-medium text-red-600">-20 ball</span></div>
                <div className="flex justify-between"><span>Tiklanish (max)</span><span className="font-medium text-green-600">+10 ball</span></div>
                <div className="flex justify-between"><span>Bandlik bonusi</span><span className="font-medium text-blue-600">+10 ball</span></div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-base">Grant shartlari</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 text-sm">
                <p>Minimal o&apos;tish balli: <strong>80 ball</strong></p>
                <p>GPA minimal: <strong>80%</strong></p>
                <p>Grant qoplaydi: o&apos;qish, yotoqxona, ovqat</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
