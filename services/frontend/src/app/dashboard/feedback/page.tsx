"use client";

import { useEffect, useState } from "react";
import { api, getUserFromToken } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface MentorFeedback {
  id: number;
  student: number;
  student_name: string;
  mentor_name: string;
  semester_name: string;
  technical_skills: string;
  participation: string;
  teamwork: string;
  initiative: string;
  comments: string;
  created_at: string;
}

const ratingLabels: Record<string, string> = {
  excellent: "A'lo",
  good: "Yaxshi",
  average: "O'rta",
  below_average: "O'rtadan past",
  poor: "Yomon",
};

const ratingColors: Record<string, string> = {
  excellent: "bg-green-100 text-green-700",
  good: "bg-blue-100 text-blue-700",
  average: "bg-yellow-100 text-yellow-700",
  below_average: "bg-orange-100 text-orange-700",
  poor: "bg-red-100 text-red-700",
};

export default function FeedbackPage() {
  const [feedbacks, setFeedbacks] = useState<MentorFeedback[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const user = getUserFromToken();
  const isTeacher = user?.role === "teacher";

  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    student: "",
    technical_skills: "good",
    participation: "good",
    teamwork: "good",
    initiative: "good",
    comments: "",
  });

  useEffect(() => {
    api.get<{ results: MentorFeedback[] }>("/evaluations/feedback/?page_size=100")
      .then((data) => setFeedbacks(data.results || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post("/evaluations/feedback/", { ...formData, student: Number(formData.student) });
      setShowForm(false);
      setFormData({ student: "", technical_skills: "good", participation: "good", teamwork: "good", initiative: "good", comments: "" });
      const data = await api.get<{ results: MentorFeedback[] }>("/evaluations/feedback/?page_size=100");
      setFeedbacks(data.results || []);
    } catch {}
  };

  const filtered = feedbacks.filter(
    (f) =>
      f.student_name.toLowerCase().includes(search.toLowerCase()) ||
      f.mentor_name.toLowerCase().includes(search.toLowerCase())
  );

  const RatingBadge = ({ rating }: { rating: string }) => (
    <span className={`inline-flex rounded-full px-2 py-0.5 text-[10px] font-medium ${ratingColors[rating] || "bg-gray-100"}`}>
      {ratingLabels[rating] || rating}
    </span>
  );

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Mentor Fikrlari</h1>
          <p className="text-sm text-muted-foreground">Mentor/o&apos;qituvchi tomonidan talaba haqida fikr-mulohaza</p>
        </div>
        {isTeacher && (
          <button
            onClick={() => setShowForm(!showForm)}
            className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary/90"
          >
            {showForm ? "Bekor qilish" : "+ Fikr bildirish"}
          </button>
        )}
      </div>

      {showForm && (
        <Card className="mb-6">
          <CardHeader><CardTitle className="text-lg">Yangi fikr-mulohaza</CardTitle></CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="grid gap-4 md:grid-cols-2">
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
              {([
                ["technical_skills", "Texnik ko'nikmalar"],
                ["participation", "Ishtirok"],
                ["teamwork", "Jamoaviylik"],
                ["initiative", "Tashabbuskorlik"],
              ] as const).map(([field, label]) => (
                <div key={field}>
                  <label className="mb-1 block text-sm font-medium">{label}</label>
                  <select
                    value={formData[field]}
                    onChange={(e) => setFormData({ ...formData, [field]: e.target.value })}
                    className="flex h-10 w-full rounded-md border border-input bg-white px-3 py-2 text-sm"
                  >
                    {Object.entries(ratingLabels).map(([k, v]) => (
                      <option key={k} value={k}>{v}</option>
                    ))}
                  </select>
                </div>
              ))}
              <div className="md:col-span-2">
                <label className="mb-1 block text-sm font-medium">Izoh</label>
                <textarea
                  value={formData.comments}
                  onChange={(e) => setFormData({ ...formData, comments: e.target.value })}
                  className="flex min-h-[80px] w-full rounded-md border border-input bg-white px-3 py-2 text-sm"
                />
              </div>
              <div>
                <button type="submit" className="rounded-lg bg-primary px-6 py-2 text-sm font-medium text-white hover:bg-primary/90">
                  Yuborish
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
          placeholder="Talaba yoki mentor bo'yicha qidirish..."
          className="flex h-10 w-full max-w-md rounded-md border border-input bg-white px-3 py-2 text-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        />
      </div>

      {loading ? (
        <div className="py-20 text-center text-muted-foreground">Yuklanmoqda...</div>
      ) : feedbacks.length === 0 ? (
        <Card><CardContent className="py-12 text-center text-muted-foreground">Fikr-mulohazalar topilmadi</CardContent></Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {filtered.map((f) => (
            <Card key={f.id}>
              <CardContent className="p-4">
                <div className="mb-3 flex items-start justify-between">
                  <div>
                    <h3 className="font-medium">{f.student_name}</h3>
                    <p className="text-xs text-muted-foreground">Mentor: {f.mentor_name}</p>
                  </div>
                  <span className="text-xs text-muted-foreground">{new Date(f.created_at).toLocaleDateString("uz")}</span>
                </div>
                <div className="mb-3 grid grid-cols-2 gap-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-muted-foreground">Texnik:</span>
                    <RatingBadge rating={f.technical_skills} />
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-muted-foreground">Ishtirok:</span>
                    <RatingBadge rating={f.participation} />
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-muted-foreground">Jamoa:</span>
                    <RatingBadge rating={f.teamwork} />
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-muted-foreground">Tashabbus:</span>
                    <RatingBadge rating={f.initiative} />
                  </div>
                </div>
                {f.comments && (
                  <p className="rounded bg-muted/50 p-2 text-sm text-muted-foreground">{f.comments}</p>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
