"use client";

import { useEffect, useState } from "react";
import { api, getUserFromToken } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface TutorEvaluation {
  id: number;
  student: number;
  student_name: string;
  tutor_name: string;
  semester_name: string;
  behavior_score: number;
  social_responsibility: number;
  communication: number;
  initiative: number;
  teamwork: number;
  total_score: number;
  comments: string;
  created_at: string;
}

export default function EvaluationsPage() {
  const [evaluations, setEvaluations] = useState<TutorEvaluation[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const user = getUserFromToken();
  const isTutor = user?.role === "tutor";

  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    student: "",
    behavior_score: 1,
    social_responsibility: 1,
    communication: 1,
    initiative: 1,
    teamwork: 1,
    comments: "",
  });

  useEffect(() => {
    api.get<{ results: TutorEvaluation[] }>("/evaluations/tutor/?page_size=100")
      .then((data) => setEvaluations(data.results || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post("/evaluations/tutor/", { ...formData, student: Number(formData.student) });
      setShowForm(false);
      setFormData({ student: "", behavior_score: 1, social_responsibility: 1, communication: 1, initiative: 1, teamwork: 1, comments: "" });
      const data = await api.get<{ results: TutorEvaluation[] }>("/evaluations/tutor/?page_size=100");
      setEvaluations(data.results || []);
    } catch {}
  };

  const filtered = evaluations.filter((e) =>
    e.student_name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Tyutor Baholash</h1>
          <p className="text-sm text-muted-foreground">Tyutor tomonidan talaba baholash (max 5 ball)</p>
        </div>
        {isTutor && (
          <button
            onClick={() => setShowForm(!showForm)}
            className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary/90"
          >
            {showForm ? "Bekor qilish" : "+ Baholash"}
          </button>
        )}
      </div>

      {showForm && (
        <Card className="mb-6">
          <CardHeader><CardTitle className="text-lg">Yangi baholash</CardTitle></CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="grid gap-4 md:grid-cols-3">
              <div>
                <label className="mb-1 block text-sm font-medium">Talaba ID</label>
                <input
                  type="number"
                  value={formData.student}
                  onChange={(e) => setFormData({ ...formData, student: e.target.value })}
                  className="flex h-10 w-full rounded-md border border-input bg-white px-3 py-2 text-sm"
                  required
                />
              </div>
              {(["behavior_score", "social_responsibility", "communication", "initiative", "teamwork"] as const).map((field) => (
                <div key={field}>
                  <label className="mb-1 block text-sm font-medium capitalize">
                    {field === "behavior_score" ? "Xulq" : field === "social_responsibility" ? "Ijtimoiy mas'uliyat" : field === "communication" ? "Muloqot" : field === "initiative" ? "Tashabbuskorlik" : "Jamoaviylik"}
                  </label>
                  <select
                    value={formData[field]}
                    onChange={(e) => setFormData({ ...formData, [field]: Number(e.target.value) })}
                    className="flex h-10 w-full rounded-md border border-input bg-white px-3 py-2 text-sm"
                  >
                    <option value={0}>0</option>
                    <option value={1}>1</option>
                  </select>
                </div>
              ))}
              <div className="md:col-span-3">
                <label className="mb-1 block text-sm font-medium">Izoh</label>
                <textarea
                  value={formData.comments}
                  onChange={(e) => setFormData({ ...formData, comments: e.target.value })}
                  className="flex min-h-[60px] w-full rounded-md border border-input bg-white px-3 py-2 text-sm"
                />
              </div>
              <div>
                <button type="submit" className="rounded-lg bg-primary px-6 py-2 text-sm font-medium text-white hover:bg-primary/90">
                  Saqlash
                </button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

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
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Tyutor</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Xulq</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Ijtimoiy</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Muloqot</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Tashabbus</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Jamoa</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Jami</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Sana</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((ev) => (
                    <tr key={ev.id} className="border-b transition-colors hover:bg-muted/30">
                      <td className="px-4 py-3 font-medium">{ev.student_name}</td>
                      <td className="px-4 py-3 text-muted-foreground">{ev.tutor_name}</td>
                      <td className="px-4 py-3 text-center">{ev.behavior_score}</td>
                      <td className="px-4 py-3 text-center">{ev.social_responsibility}</td>
                      <td className="px-4 py-3 text-center">{ev.communication}</td>
                      <td className="px-4 py-3 text-center">{ev.initiative}</td>
                      <td className="px-4 py-3 text-center">{ev.teamwork}</td>
                      <td className="px-4 py-3 text-center font-bold">{ev.total_score}/5</td>
                      <td className="px-4 py-3 text-muted-foreground">{new Date(ev.created_at).toLocaleDateString("uz")}</td>
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
