"use client";

import { useEffect, useState } from "react";
import { api, getUserFromToken } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface Activity {
  id: number;
  student: number;
  student_name: string;
  category: string;
  title: string;
  description: string;
  proof_url: string;
  score: number;
  status: string;
  max_category_score: number;
  created_at: string;
}

const categoryLabels: Record<string, string> = {
  competition: "Musobaqa",
  startup: "Startup",
  mentoring: "Mentorlik",
  cert_pdp: "PDP Sertifikat",
  cert_national: "Milliy IT sertifikat",
  cert_language: "Til sertifikati",
  cert_international: "Xalqaro IT sertifikat",
  volunteering: "Volontyorlik",
  soft_skills: "Soft Skills",
  networking: "Networking",
  project_participant: "Loyiha ishtirokchisi",
  direction_assistant: "Yo'nalish yordamchisi",
  strategic_assistant: "Strategik yordamchi",
};

export default function ActivitiesPage() {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("");
  const user = getUserFromToken();
  const canApprove = user?.role === "admin" || user?.role === "manager";
  const isStudent = user?.role === "student";

  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    category: "competition",
    title: "",
    description: "",
    proof_url: "",
    semester: 1,
  });

  useEffect(() => { loadActivities(); }, []);

  const loadActivities = () => {
    const params = filter ? `?status=${filter}` : "";
    api.get<{ results: Activity[] }>(`/activities/items/${params}`)
      .then((data) => setActivities(data.results || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post("/activities/items/", formData);
      setShowForm(false);
      setFormData({ category: "competition", title: "", description: "", proof_url: "", semester: 1 });
      loadActivities();
    } catch {}
  };

  const handleVerify = async (id: number, action: string, score?: number) => {
    try {
      await api.post(`/activities/items/${id}/verify/`, { action, score: score || 0 });
      loadActivities();
    } catch {}
  };

  const statusColors: Record<string, string> = {
    pending: "bg-yellow-100 text-yellow-700",
    approved: "bg-green-100 text-green-700",
    rejected: "bg-red-100 text-red-700",
  };

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Faoliyat va Sertifikatlar</h1>
          <p className="text-sm text-muted-foreground">
            {isStudent ? "O'z yutuqlaringizni kiriting" : "Talabalar faoliyatini boshqarish"}
          </p>
        </div>
        {isStudent && (
          <button
            onClick={() => setShowForm(!showForm)}
            className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary/90"
          >
            {showForm ? "Bekor qilish" : "+ Yutuq qo'shish"}
          </button>
        )}
      </div>

      {showForm && (
        <Card className="mb-6">
          <CardHeader><CardTitle className="text-lg">Yangi yutuq</CardTitle></CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="grid gap-4 md:grid-cols-2">
              <div>
                <label className="mb-1 block text-sm font-medium">Kategoriya</label>
                <select
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="flex h-10 w-full rounded-md border border-input bg-white px-3 py-2 text-sm"
                >
                  {Object.entries(categoryLabels).map(([k, v]) => (
                    <option key={k} value={k}>{v}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Sarlavha</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="flex h-10 w-full rounded-md border border-input bg-white px-3 py-2 text-sm"
                  required
                />
              </div>
              <div className="md:col-span-2">
                <label className="mb-1 block text-sm font-medium">Tavsif</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="flex min-h-[80px] w-full rounded-md border border-input bg-white px-3 py-2 text-sm"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Tasdiqlovchi havola</label>
                <input
                  type="url"
                  value={formData.proof_url}
                  onChange={(e) => setFormData({ ...formData, proof_url: e.target.value })}
                  className="flex h-10 w-full rounded-md border border-input bg-white px-3 py-2 text-sm"
                  placeholder="https://..."
                />
              </div>
              <div className="flex items-end">
                <button type="submit" className="rounded-lg bg-primary px-6 py-2 text-sm font-medium text-white hover:bg-primary/90">
                  Yuborish
                </button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      <div className="mb-4 flex gap-2">
        {["", "pending", "approved", "rejected"].map((f) => (
          <button
            key={f}
            onClick={() => { setFilter(f); setLoading(true); setTimeout(loadActivities, 0); }}
            className={`rounded-lg px-3 py-1.5 text-sm font-medium transition-colors ${
              filter === f ? "bg-primary text-white" : "bg-muted text-muted-foreground hover:bg-muted/80"
            }`}
          >
            {f === "" ? "Barchasi" : f === "pending" ? "Kutilmoqda" : f === "approved" ? "Tasdiqlangan" : "Rad etilgan"}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="py-20 text-center text-muted-foreground">Yuklanmoqda...</div>
      ) : activities.length === 0 ? (
        <Card><CardContent className="py-12 text-center text-muted-foreground">Faoliyatlar topilmadi</CardContent></Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {activities.map((a) => (
            <Card key={a.id}>
              <CardContent className="p-4">
                <div className="mb-2 flex items-start justify-between">
                  <span className="rounded bg-muted px-2 py-0.5 text-xs font-medium">
                    {categoryLabels[a.category] || a.category}
                  </span>
                  <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${statusColors[a.status]}`}>
                    {a.status === "pending" ? "Kutilmoqda" : a.status === "approved" ? "Tasdiqlangan" : "Rad etilgan"}
                  </span>
                </div>
                <h3 className="mb-1 font-medium">{a.title}</h3>
                <p className="mb-2 text-xs text-muted-foreground">{a.student_name}</p>
                {a.description && <p className="mb-2 text-sm text-muted-foreground line-clamp-2">{a.description}</p>}
                {a.proof_url && (
                  <a href={a.proof_url} target="_blank" rel="noopener noreferrer" className="mb-2 block text-xs text-primary hover:underline">
                    Tasdiq havolasi
                  </a>
                )}
                <div className="flex items-center justify-between">
                  <span className="text-sm font-bold">{a.score}/{a.max_category_score} ball</span>
                  <span className="text-xs text-muted-foreground">{new Date(a.created_at).toLocaleDateString("uz")}</span>
                </div>
                {canApprove && a.status === "pending" && (
                  <div className="mt-3 flex gap-2">
                    <button
                      onClick={() => handleVerify(a.id, "approve", a.max_category_score)}
                      className="flex-1 rounded bg-green-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-green-700"
                    >
                      Tasdiqlash
                    </button>
                    <button
                      onClick={() => handleVerify(a.id, "reject")}
                      className="flex-1 rounded bg-red-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-red-700"
                    >
                      Rad etish
                    </button>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
