"use client";

import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import {
  GraduationCap, BarChart3, Shield, Calendar, Award,
  FileText, Users, Briefcase, ChevronDown, ChevronUp, Trophy,
  Star, TrendingUp, ArrowRight,
} from "lucide-react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://10.50.2.39:8080/api/v1";

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

function RankBadge({ rank }: { rank: number }) {
  if (rank === 1) return <div className="flex h-8 w-8 items-center justify-center rounded-full bg-yellow-400 text-white"><Trophy className="h-4 w-4" /></div>;
  if (rank === 2) return <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-300 text-gray-700"><Trophy className="h-4 w-4" /></div>;
  if (rank === 3) return <div className="flex h-8 w-8 items-center justify-center rounded-full bg-amber-600 text-white"><Trophy className="h-4 w-4" /></div>;
  return <div className="flex h-8 w-8 items-center justify-center rounded-full bg-muted text-sm font-bold text-muted-foreground">{rank}</div>;
}

export default function LandingPage() {
  const [scores, setScores] = useState<PublicScore[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [selectedGroup, setSelectedGroup] = useState("all");
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    fetch(`${API_BASE}/grants/scores/public_rating/`)
      .then((r) => r.json())
      .then(setScores)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const groups = ["all", ...Array.from(new Set(scores.map((s) => s.group))).sort()];

  const filtered = scores.filter((s) => {
    const matchSearch = s.student_name.toLowerCase().includes(search.toLowerCase()) ||
      s.group.toLowerCase().includes(search.toLowerCase());
    const matchGroup = selectedGroup === "all" || s.group === selectedGroup;
    return matchSearch && matchGroup;
  });

  const displayed = showAll ? filtered : filtered.slice(0, 10);
  const top3 = scores.slice(0, 3);

  const scoringItems = [
    { label: "Akademik natija", max: 40, icon: <GraduationCap className="h-5 w-5" />, color: "text-blue-600", bg: "bg-blue-50" },
    { label: "Davomat", max: 20, icon: <Calendar className="h-5 w-5" />, color: "text-green-600", bg: "bg-green-50" },
    { label: "Topshiriqlar", max: 15, icon: <FileText className="h-5 w-5" />, color: "text-purple-600", bg: "bg-purple-50" },
    { label: "Faollik", max: 10, icon: <Award className="h-5 w-5" />, color: "text-orange-600", bg: "bg-orange-50" },
    { label: "Tyutor bahosi", max: 5, icon: <Users className="h-5 w-5" />, color: "text-teal-600", bg: "bg-teal-50" },
    { label: "Intizom", max: 10, icon: <Shield className="h-5 w-5" />, color: "text-indigo-600", bg: "bg-indigo-50" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <header className="sticky top-0 z-50 border-b bg-white/90 backdrop-blur-md">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-3">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary text-sm font-bold text-white shadow-lg shadow-primary/25">
              EM
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight">EduMetric</h1>
              <p className="text-[11px] text-muted-foreground">PDP University</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <a href="#rating" className="hidden rounded-lg px-4 py-2 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground sm:inline-flex">
              Reyting
            </a>
            <a href="#scoring" className="hidden rounded-lg px-4 py-2 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground sm:inline-flex">
              Ball tizimi
            </a>
            <a
              href="/login"
              className="inline-flex items-center gap-2 rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-white shadow-lg shadow-primary/25 transition-all hover:bg-primary/90 hover:shadow-xl hover:shadow-primary/30"
            >
              Kirish <ArrowRight className="h-4 w-4" />
            </a>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden px-6 py-16 md:py-24">
        <div className="absolute inset-0 -z-10">
          <div className="absolute left-1/4 top-1/4 h-72 w-72 rounded-full bg-blue-200/30 blur-3xl" />
          <div className="absolute bottom-1/4 right-1/4 h-72 w-72 rounded-full bg-indigo-200/30 blur-3xl" />
        </div>
        <div className="mx-auto max-w-4xl text-center">
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border bg-white px-4 py-1.5 text-sm text-muted-foreground shadow-sm">
            <Star className="h-4 w-4 text-yellow-500" />
            <span>Shaffof baholash tizimi</span>
          </div>
          <h2 className="mb-4 text-4xl font-bold tracking-tight md:text-5xl lg:text-6xl">
            Grant <span className="bg-gradient-to-r from-primary to-indigo-600 bg-clip-text text-transparent">Reytingi</span>
          </h2>
          <p className="mx-auto mb-8 max-w-2xl text-lg text-muted-foreground">
            PDP University talabalarining grant ball reytingi. Akademik natija, davomat, faollik va boshqa ko&apos;rsatkichlar asosida baholanadi.
          </p>
          <div className="flex items-center justify-center gap-6 text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <Users className="h-4 w-4 text-primary" />
              <span><strong className="text-foreground">{scores.length}</strong> talaba</span>
            </div>
            <div className="flex items-center gap-2">
              <TrendingUp className="h-4 w-4 text-green-600" />
              <span><strong className="text-foreground">{scores.filter(s => s.final_score >= 80).length}</strong> grant layoqatli</span>
            </div>
            <div className="flex items-center gap-2">
              <BarChart3 className="h-4 w-4 text-indigo-600" />
              <span><strong className="text-foreground">{groups.length - 1}</strong> guruh</span>
            </div>
          </div>
        </div>
      </section>

      {/* Top 3 Podium */}
      {top3.length >= 3 && (
        <section className="px-6 pb-12">
          <div className="mx-auto grid max-w-3xl grid-cols-3 gap-4">
            {[top3[1], top3[0], top3[2]].map((s, i) => {
              const order = [2, 1, 3][i];
              const heights = ["h-28", "h-36", "h-24"];
              const colors = ["from-gray-200 to-gray-300", "from-yellow-300 to-yellow-400", "from-amber-500 to-amber-600"];
              const textColors = ["text-gray-700", "text-white", "text-white"];
              return (
                <div key={s.rank} className={`flex flex-col items-center ${i === 1 ? "md:-mt-4" : ""}`}>
                  <div className="mb-3 text-center">
                    <div className={`mx-auto mb-2 flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br ${colors[i]} text-xl font-bold ${textColors[i]} ${i === 1 ? "ring-4 ring-yellow-200" : ""} shadow-lg`}>
                      {order}
                    </div>
                    <p className="text-sm font-semibold">{s.student_name}</p>
                    <p className="text-xs text-muted-foreground">{s.group}</p>
                  </div>
                  <div className={`flex w-full items-center justify-center rounded-xl bg-gradient-to-br ${colors[i]} ${heights[i]} shadow-lg`}>
                    <span className={`text-3xl font-bold ${textColors[i]}`}>{s.final_score}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </section>
      )}

      {/* Rating Table */}
      <section id="rating" className="px-6 pb-12">
        <div className="mx-auto max-w-7xl">
          <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h3 className="text-2xl font-bold">To&apos;liq reyting</h3>
              <p className="text-sm text-muted-foreground">Barcha talabalar reytingi</p>
            </div>
            <div className="flex gap-3">
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Ism yoki guruh..."
                className="flex h-10 w-48 rounded-lg border bg-white px-4 py-2 text-sm shadow-sm transition-shadow focus:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/20"
              />
              <select
                value={selectedGroup}
                onChange={(e) => setSelectedGroup(e.target.value)}
                className="flex h-10 rounded-lg border bg-white px-3 py-2 text-sm shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/20"
              >
                {groups.map((g) => (
                  <option key={g} value={g}>{g === "all" ? "Barcha guruhlar" : g}</option>
                ))}
              </select>
            </div>
          </div>

          {loading ? (
            <div className="py-20 text-center text-muted-foreground">Yuklanmoqda...</div>
          ) : (
            <Card className="overflow-hidden shadow-lg">
              <CardContent className="p-0">
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b bg-muted/50">
                        <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground">#</th>
                        <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground">Talaba</th>
                        <th className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground">Guruh</th>
                        <th className="px-4 py-3 text-center text-xs font-semibold text-muted-foreground">Akademik<br/><span className="font-normal">/40</span></th>
                        <th className="px-4 py-3 text-center text-xs font-semibold text-muted-foreground">Davomat<br/><span className="font-normal">/20</span></th>
                        <th className="px-4 py-3 text-center text-xs font-semibold text-muted-foreground">Topshiriq<br/><span className="font-normal">/15</span></th>
                        <th className="px-4 py-3 text-center text-xs font-semibold text-muted-foreground">Faollik<br/><span className="font-normal">/10</span></th>
                        <th className="px-4 py-3 text-center text-xs font-semibold text-muted-foreground">Tyutor<br/><span className="font-normal">/5</span></th>
                        <th className="px-4 py-3 text-center text-xs font-semibold text-muted-foreground">Intizom<br/><span className="font-normal">/10</span></th>
                        <th className="px-4 py-3 text-center text-xs font-semibold text-muted-foreground">Jami</th>
                        <th className="px-4 py-3 text-center text-xs font-semibold text-muted-foreground">Yakuniy</th>
                      </tr>
                    </thead>
                    <tbody>
                      {displayed.map((s) => (
                        <tr key={s.rank} className={`border-b transition-colors hover:bg-primary/5 ${s.rank <= 3 ? "bg-amber-50/50" : ""}`}>
                          <td className="px-4 py-3"><RankBadge rank={s.rank} /></td>
                          <td className="px-4 py-3 text-sm font-medium">{s.student_name}</td>
                          <td className="px-4 py-3"><span className="rounded-md bg-muted px-2 py-1 text-xs font-medium">{s.group}</span></td>
                          <td className="px-4 py-3 text-center text-sm">{s.academic_score}</td>
                          <td className="px-4 py-3 text-center text-sm">{s.attendance_score}</td>
                          <td className="px-4 py-3 text-center text-sm">{s.assignment_score}</td>
                          <td className="px-4 py-3 text-center text-sm">{s.activity_score}</td>
                          <td className="px-4 py-3 text-center text-sm">{s.tutor_score}</td>
                          <td className="px-4 py-3 text-center text-sm">{s.discipline_score}</td>
                          <td className="px-4 py-3 text-center text-sm font-semibold">{s.base_total}</td>
                          <td className="px-4 py-3 text-center">
                            <span className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-bold ${
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
                {filtered.length > 10 && (
                  <div className="border-t p-4 text-center">
                    <button
                      onClick={() => setShowAll(!showAll)}
                      className="inline-flex items-center gap-2 rounded-lg border px-6 py-2.5 text-sm font-medium transition-all hover:bg-muted hover:shadow-sm"
                    >
                      {showAll ? "Kamroq ko'rsatish" : `Barchasini ko'rish (${filtered.length})`}
                      {showAll ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
                    </button>
                  </div>
                )}
              </CardContent>
            </Card>
          )}
          <p className="mt-3 text-center text-sm text-muted-foreground">
            Jami: {filtered.length} talaba
          </p>
        </div>
      </section>

      {/* Scoring System */}
      <section id="scoring" className="px-6 pb-16">
        <div className="mx-auto max-w-7xl">
          <div className="mb-8 text-center">
            <h3 className="text-2xl font-bold">Ball tizimi</h3>
            <p className="mt-1 text-muted-foreground">100 ballik asosiy + bonus/jarima</p>
          </div>

          <div className="mb-8 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {scoringItems.map((item) => (
              <Card key={item.label} className="transition-all hover:shadow-md">
                <CardContent className="p-5">
                  <div className="mb-3 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className={`rounded-lg ${item.bg} p-2 ${item.color}`}>{item.icon}</div>
                      <span className="font-medium">{item.label}</span>
                    </div>
                    <span className="text-lg font-bold">{item.max}</span>
                  </div>
                  <Progress value={item.max} className="h-2" />
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="grid gap-4 md:grid-cols-3">
            <Card className="border-red-200 bg-red-50/50">
              <CardContent className="p-5">
                <h4 className="mb-2 font-semibold text-red-700">Jarima</h4>
                <p className="text-sm text-red-600">Maksimal <strong>-20 ball</strong></p>
                <p className="mt-1 text-xs text-red-500">Tartib buzish, kechikish, qoidalar buzilishi</p>
              </CardContent>
            </Card>
            <Card className="border-green-200 bg-green-50/50">
              <CardContent className="p-5">
                <h4 className="mb-2 font-semibold text-green-700">Tiklanish</h4>
                <p className="text-sm text-green-600">Maksimal <strong>+10 ball</strong></p>
                <p className="mt-1 text-xs text-green-500">Jarimaning 50% ni qaytarish mumkin</p>
              </CardContent>
            </Card>
            <Card className="border-blue-200 bg-blue-50/50">
              <CardContent className="p-5">
                <h4 className="mb-2 font-semibold text-blue-700">Bandlik bonusi</h4>
                <p className="text-sm text-blue-600">Maksimal <strong>+10 ball</strong></p>
                <p className="mt-1 text-xs text-blue-500">Stajyorlik, part-time, full-time ish</p>
              </CardContent>
            </Card>
          </div>

          <Card className="mt-8">
            <CardContent className="p-6">
              <h4 className="mb-4 text-lg font-semibold">Grant shartlari</h4>
              <div className="grid gap-4 md:grid-cols-3">
                <div className="flex items-start gap-3">
                  <div className="rounded-lg bg-primary/10 p-2 text-primary"><TrendingUp className="h-5 w-5" /></div>
                  <div>
                    <p className="font-medium">Minimal ball</p>
                    <p className="text-sm text-muted-foreground">80 ball va undan yuqori</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="rounded-lg bg-primary/10 p-2 text-primary"><GraduationCap className="h-5 w-5" /></div>
                  <div>
                    <p className="font-medium">GPA minimal</p>
                    <p className="text-sm text-muted-foreground">80% va undan yuqori</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <div className="rounded-lg bg-primary/10 p-2 text-primary"><Briefcase className="h-5 w-5" /></div>
                  <div>
                    <p className="font-medium">Grant qoplaydi</p>
                    <p className="text-sm text-muted-foreground">O&apos;qish, yotoqxona, ovqat</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-white py-8">
        <div className="mx-auto max-w-7xl px-6 text-center">
          <div className="mb-4 flex items-center justify-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-xs font-bold text-white">EM</div>
            <span className="font-semibold">EduMetric</span>
          </div>
          <p className="text-sm text-muted-foreground">PDP University Grant Management System</p>
        </div>
      </footer>
    </div>
  );
}
