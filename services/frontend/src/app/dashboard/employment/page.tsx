"use client";

import { useEffect, useState } from "react";
import { api, getUserFromToken } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface EmploymentRecord {
  id: number;
  student: number;
  student_name: string;
  employment_type: string;
  company_name: string;
  position: string;
  start_date: string;
  proof_url: string;
  bonus_score: number;
  verified: boolean;
  verified_by_name: string | null;
}

const typeLabels: Record<string, string> = {
  internship: "Amaliyot (Internship)",
  part_time: "Yarim stavka (Part-time)",
  full_time: "To'liq ish (Full-time)",
};

const typeScores: Record<string, string> = {
  internship: "0-5 ball",
  part_time: "5-7 ball",
  full_time: "7-10 ball",
};

export default function EmploymentPage() {
  const [records, setRecords] = useState<EmploymentRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const user = getUserFromToken();
  const isStudent = user?.role === "student";
  const canApprove = user?.role === "admin" || user?.role === "manager";

  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    semester: 1,
    employment_type: "internship",
    company_name: "",
    position: "",
    start_date: "",
    proof_url: "",
  });

  useEffect(() => {
    loadRecords();
  }, []);

  const loadRecords = () => {
    api.get<{ results: EmploymentRecord[] }>("/grants/employment/?page_size=100")
      .then((data) => setRecords(data.results || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post("/grants/employment/", formData);
      setShowForm(false);
      setFormData({ semester: 1, employment_type: "internship", company_name: "", position: "", start_date: "", proof_url: "" });
      loadRecords();
    } catch {}
  };

  const handleVerify = async (id: number) => {
    try {
      await api.post(`/grants/employment/${id}/verify/`, { action: "approve", score: 5 });
      loadRecords();
    } catch {}
  };

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Bandlik</h1>
          <p className="text-sm text-muted-foreground">Ish tajribasi va amaliyot (bonus max +10 ball)</p>
        </div>
        {isStudent && (
          <button
            onClick={() => setShowForm(!showForm)}
            className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary/90"
          >
            {showForm ? "Bekor qilish" : "+ Ish qo'shish"}
          </button>
        )}
      </div>

      {showForm && (
        <Card className="mb-6">
          <CardHeader><CardTitle className="text-lg">Yangi ish yozuvi</CardTitle></CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="grid gap-4 md:grid-cols-2">
              <div>
                <label className="mb-1 block text-sm font-medium">Ish turi</label>
                <select
                  value={formData.employment_type}
                  onChange={(e) => setFormData({ ...formData, employment_type: e.target.value })}
                  className="flex h-10 w-full rounded-md border border-input bg-white px-3 py-2 text-sm"
                >
                  {Object.entries(typeLabels).map(([k, v]) => (
                    <option key={k} value={k}>{v} — {typeScores[k]}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Semestr ID</label>
                <input
                  type="number"
                  min={1}
                  value={formData.semester}
                  onChange={(e) => setFormData({ ...formData, semester: Number(e.target.value) })}
                  className="flex h-10 w-full rounded-md border border-input bg-white px-3 py-2 text-sm"
                  required
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Kompaniya</label>
                <input
                  type="text"
                  value={formData.company_name}
                  onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
                  className="flex h-10 w-full rounded-md border border-input bg-white px-3 py-2 text-sm"
                  required
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Lavozim</label>
                <input
                  type="text"
                  value={formData.position}
                  onChange={(e) => setFormData({ ...formData, position: e.target.value })}
                  className="flex h-10 w-full rounded-md border border-input bg-white px-3 py-2 text-sm"
                  required
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Boshlanish sanasi</label>
                <input
                  type="date"
                  value={formData.start_date}
                  onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                  className="flex h-10 w-full rounded-md border border-input bg-white px-3 py-2 text-sm"
                  required
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

      {loading ? (
        <div className="py-20 text-center text-muted-foreground">Yuklanmoqda...</div>
      ) : records.length === 0 ? (
        <Card><CardContent className="py-12 text-center text-muted-foreground">Bandlik yozuvlari topilmadi</CardContent></Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {records.map((r) => (
            <Card key={r.id}>
              <CardContent className="p-4">
                <div className="mb-2 flex items-start justify-between">
                  <span className="rounded bg-muted px-2 py-0.5 text-xs font-medium">{typeLabels[r.employment_type]}</span>
                  <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${r.verified ? "bg-green-100 text-green-700" : "bg-yellow-100 text-yellow-700"}`}>
                    {r.verified ? "Tasdiqlangan" : "Tasdiqlanmagan"}
                  </span>
                </div>
                <h3 className="mb-1 font-medium">{r.position}</h3>
                <p className="mb-1 text-sm text-muted-foreground">{r.company_name}</p>
                <p className="mb-1 text-sm text-muted-foreground">{r.student_name}</p>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-bold text-blue-600">+{r.bonus_score} ball</span>
                  <span className="text-xs text-muted-foreground">{new Date(r.start_date).toLocaleDateString("uz")}</span>
                </div>
                {r.proof_url && (
                  <a href={r.proof_url} target="_blank" rel="noopener noreferrer" className="mt-2 block text-xs text-primary hover:underline">
                    Tasdiq havolasi
                  </a>
                )}
                {canApprove && !r.verified && (
                  <button
                    onClick={() => handleVerify(r.id)}
                    className="mt-3 w-full rounded bg-green-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-green-700"
                  >
                    Tasdiqlash
                  </button>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
