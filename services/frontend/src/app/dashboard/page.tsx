"use client";

import { useEffect, useState } from "react";
import { getUserFromToken, api } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { StatsCard } from "@/components/dashboard/stats-card";
import { ScoreCard } from "@/components/dashboard/score-card";
import {
  Users, GraduationCap, Calendar, FileText, Award,
  Shield, AlertTriangle, Briefcase, BarChart3, TrendingUp,
} from "lucide-react";

interface GrantScoreData {
  rank: number;
  academic_score: number;
  attendance_score: number;
  assignment_score: number;
  activity_score: number;
  tutor_score: number;
  discipline_score: number;
  penalty_score: number;
  recovery_score: number;
  employment_score: number;
  base_total: number;
  final_score: number;
  gpa_percentage: number;
  gpa_eligible: boolean;
  status: string;
}

interface DashboardStats {
  total_students: number;
  eligible_count: number;
  average_score: number;
  max_score: number;
  min_score: number;
}

function StudentDashboard() {
  const [score, setScore] = useState<GrantScoreData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get<{ results: GrantScoreData[] }>("/grants/scores/")
      .then((data) => setScore(data.results?.[0] || null))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="animate-pulse text-muted-foreground">Yuklanmoqda...</div>;

  if (!score) {
    return (
      <div>
        <h1 className="mb-6 text-2xl font-bold">Bosh sahifa</h1>
        <Card>
          <CardContent className="p-12 text-center text-muted-foreground">
            Hali grant ballari hisoblanmagan. Iltimos, keyinroq tekshiring.
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <div className="flex items-center gap-4">
          <div className="rounded-full bg-primary/10 px-4 py-2 text-sm font-medium text-primary">
            Rank: #{score.rank}
          </div>
          <div className={`rounded-full px-4 py-2 text-sm font-medium ${
            score.gpa_eligible ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
          }`}>
            GPA: {score.gpa_percentage}% {score.gpa_eligible ? "✓" : "✗"}
          </div>
        </div>
      </div>

      <div className="mb-6 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatsCard
          title="Umumiy ball"
          value={score.final_score}
          subtitle={`Asosiy: ${score.base_total}/100`}
          icon={<BarChart3 className="h-6 w-6" />}
        />
        <StatsCard
          title="Rank"
          value={`#${score.rank}`}
          subtitle={score.status === "grant_active" ? "Grant faol" : score.status}
          icon={<TrendingUp className="h-6 w-6" />}
          trend="up"
        />
        <StatsCard
          title="GPA"
          value={`${score.gpa_percentage}%`}
          subtitle={score.gpa_eligible ? "Minimal shart bajarilgan" : "80% dan past!"}
          icon={<GraduationCap className="h-6 w-6" />}
          trend={score.gpa_eligible ? "up" : "down"}
        />
        <StatsCard
          title="Jarima"
          value={score.penalty_score}
          subtitle={`Tiklanish: +${score.recovery_score}`}
          icon={<AlertTriangle className="h-6 w-6" />}
          trend={score.penalty_score < 0 ? "down" : "neutral"}
        />
      </div>

      <h2 className="mb-4 text-lg font-semibold">Ball taqsimoti</h2>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <ScoreCard label="Akademik natija" score={score.academic_score} maxScore={40} icon={<GraduationCap className="h-4 w-4" />} color="bg-blue-600" />
        <ScoreCard label="Davomat" score={score.attendance_score} maxScore={20} icon={<Calendar className="h-4 w-4" />} color="bg-green-600" />
        <ScoreCard label="Topshiriqlar" score={score.assignment_score} maxScore={15} icon={<FileText className="h-4 w-4" />} color="bg-purple-600" />
        <ScoreCard label="Faollik" score={score.activity_score} maxScore={10} icon={<Award className="h-4 w-4" />} color="bg-orange-600" />
        <ScoreCard label="Tyutor bahosi" score={score.tutor_score} maxScore={5} icon={<Users className="h-4 w-4" />} color="bg-teal-600" />
        <ScoreCard label="Intizom" score={score.discipline_score} maxScore={10} icon={<Shield className="h-4 w-4" />} color="bg-indigo-600" />
      </div>

      {score.employment_score > 0 && (
        <div className="mt-4">
          <ScoreCard label="Bandlik bonusi" score={score.employment_score} maxScore={10} icon={<Briefcase className="h-4 w-4" />} color="bg-emerald-600" />
        </div>
      )}
    </div>
  );
}

function AdminDashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get<DashboardStats>("/grants/scores/dashboard_stats/")
      .then(setStats)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="animate-pulse text-muted-foreground">Yuklanmoqda...</div>;

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">Admin Dashboard</h1>
      <div className="mb-6 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatsCard
          title="Jami talabalar"
          value={stats?.total_students || 0}
          icon={<Users className="h-6 w-6" />}
        />
        <StatsCard
          title="Grant uchun layoqatli"
          value={stats?.eligible_count || 0}
          subtitle={`${stats?.total_students ? Math.round((stats.eligible_count / stats.total_students) * 100) : 0}% layoqatli`}
          icon={<Award className="h-6 w-6" />}
          trend="up"
        />
        <StatsCard
          title="O'rtacha ball"
          value={stats?.average_score || 0}
          icon={<BarChart3 className="h-6 w-6" />}
        />
        <StatsCard
          title="Eng yuqori ball"
          value={stats?.max_score || 0}
          icon={<TrendingUp className="h-6 w-6" />}
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Tezkor harakatlar</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <a href="/dashboard/grants" className="flex items-center gap-3 rounded-lg border p-3 transition-colors hover:bg-muted">
              <BarChart3 className="h-5 w-5 text-primary" />
              <div>
                <p className="font-medium">Grant reytingini ko'rish</p>
                <p className="text-xs text-muted-foreground">Barcha talabalar reytingi</p>
              </div>
            </a>
            <a href="/dashboard/students" className="flex items-center gap-3 rounded-lg border p-3 transition-colors hover:bg-muted">
              <Users className="h-5 w-5 text-primary" />
              <div>
                <p className="font-medium">Talabalarni boshqarish</p>
                <p className="text-xs text-muted-foreground">Profil, guruh, holat</p>
              </div>
            </a>
            <a href="/dashboard/activities" className="flex items-center gap-3 rounded-lg border p-3 transition-colors hover:bg-muted">
              <Award className="h-5 w-5 text-primary" />
              <div>
                <p className="font-medium">Faoliyatlarni tasdiqlash</p>
                <p className="text-xs text-muted-foreground">Kutilayotgan arizalar</p>
              </div>
            </a>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Ball tizimi</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {[
                { label: "Akademik natija", max: 40, color: "bg-blue-500" },
                { label: "Davomat", max: 20, color: "bg-green-500" },
                { label: "Topshiriqlar", max: 15, color: "bg-purple-500" },
                { label: "Faollik va Sertifikatlar", max: 10, color: "bg-orange-500" },
                { label: "Tyutor bahosi", max: 5, color: "bg-teal-500" },
                { label: "Intizom", max: 10, color: "bg-indigo-500" },
              ].map((item) => (
                <div key={item.label} className="flex items-center gap-3">
                  <div className={`h-3 w-3 rounded-full ${item.color}`} />
                  <span className="flex-1 text-sm">{item.label}</span>
                  <span className="text-sm font-medium">{item.max} ball</span>
                </div>
              ))}
              <div className="border-t pt-2">
                <div className="flex justify-between text-sm font-semibold">
                  <span>Jami</span>
                  <span>100 ball</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function ParentDashboard() {
  const [children, setChildren] = useState<Array<{
    id: number;
    first_name: string;
    last_name: string;
    student_profile: {
      student_id: string;
      group: string;
      course: number;
      status: string;
      grant_status: string;
    } | null;
  }>>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getMyChildren()
      .then((data) => setChildren(data as typeof children))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="animate-pulse text-muted-foreground">Yuklanmoqda...</div>;

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">Ota-ona paneli</h1>

      {children.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-2">
          {children.map((child) => (
            <Card key={child.id}>
              <CardContent className="p-6">
                <div className="mb-4 flex items-center gap-3">
                  <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-lg font-bold text-primary">
                    {child.first_name[0]}{child.last_name[0]}
                  </div>
                  <div>
                    <p className="font-semibold">{child.first_name} {child.last_name}</p>
                    {child.student_profile && (
                      <p className="text-sm text-muted-foreground">
                        {child.student_profile.group} | {child.student_profile.course}-kurs
                      </p>
                    )}
                  </div>
                </div>
                {child.student_profile && (
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Talaba ID</span>
                      <span className="font-medium">{child.student_profile.student_id}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Holat</span>
                      <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                        child.student_profile.status === "grant" ? "bg-green-100 text-green-700" : "bg-blue-100 text-blue-700"
                      }`}>
                        {child.student_profile.status === "grant" ? "Grant" : "Kontrakt"}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Grant holati</span>
                      <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                        child.student_profile.grant_status === "active" ? "bg-green-100 text-green-700" :
                        child.student_profile.grant_status === "suspended" ? "bg-yellow-100 text-yellow-700" :
                        "bg-red-100 text-red-700"
                      }`}>
                        {child.student_profile.grant_status === "active" ? "Faol" :
                         child.student_profile.grant_status === "suspended" ? "To'xtatilgan" : "Bekor"}
                      </span>
                    </div>
                  </div>
                )}
                <div className="mt-4 flex gap-2">
                  <a href="/dashboard/academic" className="flex-1 rounded-md border px-3 py-2 text-center text-xs font-medium transition-colors hover:bg-muted">Akademik</a>
                  <a href="/dashboard/attendance" className="flex-1 rounded-md border px-3 py-2 text-center text-xs font-medium transition-colors hover:bg-muted">Davomat</a>
                  <a href="/dashboard/grants" className="flex-1 rounded-md border px-3 py-2 text-center text-xs font-medium transition-colors hover:bg-muted">Grant reyting</a>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <CardContent className="p-12 text-center text-muted-foreground">
            Sizga biriktirilgan farzand topilmadi. Iltimos, admin bilan bog&apos;laning.
          </CardContent>
        </Card>
      )}
    </div>
  );
}

function KomendantDashboard() {
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">Komendant paneli</h1>
      <p className="mb-6 text-muted-foreground">Yotoqxona talabalarining faolligi, tarbiyasi va yurish-turishini baholash</p>
      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Yotoqxona boshqaruvi</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <a href="/dashboard/evaluations" className="flex items-center gap-3 rounded-lg border p-3 transition-colors hover:bg-muted">
              <Award className="h-5 w-5 text-primary" />
              <div>
                <p className="font-medium">Talabalarni baholash</p>
                <p className="text-xs text-muted-foreground">Yotoqxona faolligi, tarbiya, yurish-turish</p>
              </div>
            </a>
            <a href="/dashboard/discipline" className="flex items-center gap-3 rounded-lg border p-3 transition-colors hover:bg-muted">
              <Shield className="h-5 w-5 text-indigo-500" />
              <div>
                <p className="font-medium">Intizom yozuvlari</p>
                <p className="text-xs text-muted-foreground">Yotoqxona qoidalariga rioya</p>
              </div>
            </a>
            <a href="/dashboard/penalties" className="flex items-center gap-3 rounded-lg border p-3 transition-colors hover:bg-muted">
              <AlertTriangle className="h-5 w-5 text-orange-500" />
              <div>
                <p className="font-medium">Jarima berish</p>
                <p className="text-xs text-muted-foreground">Tartib buzganlar uchun jarima</p>
              </div>
            </a>
            <a href="/dashboard/recovery" className="flex items-center gap-3 rounded-lg border p-3 transition-colors hover:bg-muted">
              <TrendingUp className="h-5 w-5 text-green-500" />
              <div>
                <p className="font-medium">Tiklanish vazifalari</p>
                <p className="text-xs text-muted-foreground">50% jarima qaytarish imkoniyati</p>
              </div>
            </a>
            <a href="/dashboard/students" className="flex items-center gap-3 rounded-lg border p-3 transition-colors hover:bg-muted">
              <Users className="h-5 w-5 text-primary" />
              <div>
                <p className="font-medium">Talabalar ro&apos;yxati</p>
                <p className="text-xs text-muted-foreground">Yotoqxonadagi talabalar</p>
              </div>
            </a>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Baholash mezonlari</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3 text-sm">
              <div className="rounded-lg bg-blue-50 p-3">
                <p className="font-medium text-blue-700">Korporativ madaniyat (0-1 ball)</p>
                <p className="text-blue-600">Yotoqxona madaniyatiga rioya</p>
              </div>
              <div className="rounded-lg bg-green-50 p-3">
                <p className="font-medium text-green-700">Ijtimoiy faollik (0-1 ball)</p>
                <p className="text-green-600">Tadbirlarda qatnashish</p>
              </div>
              <div className="rounded-lg bg-purple-50 p-3">
                <p className="font-medium text-purple-700">Intizom (0-1 ball)</p>
                <p className="text-purple-600">Tartib-qoidalarga rioya</p>
              </div>
              <div className="rounded-lg bg-orange-50 p-3">
                <p className="font-medium text-orange-700">Yotoqxona hayoti (0-1 ball)</p>
                <p className="text-orange-600">Faollik va mas&apos;uliyat</p>
              </div>
              <div className="rounded-lg bg-teal-50 p-3">
                <p className="font-medium text-teal-700">Soft skills (0-1 ball)</p>
                <p className="text-teal-600">Muloqot va hamkorlik</p>
              </div>
              <div className="border-t pt-2">
                <div className="flex justify-between font-semibold">
                  <span>Jami maksimal</span>
                  <span>5 ball</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const [role, setRole] = useState<string | null>(null);

  useEffect(() => {
    const user = getUserFromToken();
    if (user) setRole(user.role);
  }, []);

  if (!role) return null;

  if (role === "admin" || role === "manager") return <AdminDashboard />;
  if (role === "parent") return <ParentDashboard />;
  if (role === "komendant") return <KomendantDashboard />;
  if (role === "tutor") return <KomendantDashboard />;
  return <StudentDashboard />;
}
