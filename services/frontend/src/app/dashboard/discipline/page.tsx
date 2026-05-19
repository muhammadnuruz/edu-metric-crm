"use client";

import { useEffect, useState } from "react";
import { api, getUserFromToken } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface DisciplineRecord {
  id: number;
  student: number;
  student_name: string;
  semester_name: string;
  academic_honesty: number;
  dress_code: number;
  punctuality: number;
  respect: number;
  property_care: number;
  total_score: number;
  evaluated_by_name: string;
  created_at: string;
}

export default function DisciplinePage() {
  const [records, setRecords] = useState<DisciplineRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const user = getUserFromToken();
  const isAdmin = user?.role === "admin";

  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    student: "",
    academic_honesty: 2,
    dress_code: 2,
    punctuality: 2,
    respect: 2,
    property_care: 2,
  });

  useEffect(() => {
    api.get<{ results: DisciplineRecord[] }>("/evaluations/discipline/?page_size=100")
      .then((data) => setRecords(data.results || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post("/evaluations/discipline/", { ...formData, student: Number(formData.student) });
      setShowForm(false);
      setFormData({ student: "", academic_honesty: 2, dress_code: 2, punctuality: 2, respect: 2, property_care: 2 });
      const data = await api.get<{ results: DisciplineRecord[] }>("/evaluations/discipline/?page_size=100");
      setRecords(data.results || []);
    } catch {}
  };

  const filtered = records.filter((r) =>
    r.student_name.toLowerCase().includes(search.toLowerCase())
  );

  const scoreColor = (score: number, max: number) => {
    const pct = (score / max) * 100;
    return pct >= 80 ? "text-green-600" : pct >= 60 ? "text-yellow-600" : "text-red-600";
  };

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Intizom</h1>
          <p className="text-sm text-muted-foreground">Korporativ madaniyat va intizom (max 10 ball)</p>
        </div>
        {isAdmin && (
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
          <CardHeader><CardTitle className="text-lg">Yangi intizom bahosi</CardTitle></CardHeader>
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
              {([
                ["academic_honesty", "Akademik halollik", 2],
                ["dress_code", "Kiyim qoidasi", 2],
                ["punctuality", "Punktuallik", 2],
                ["respect", "Hurmat", 2],
                ["property_care", "Mol-mulk", 2],
              ] as const).map(([field, label, max]) => (
                <div key={field}>
                  <label className="mb-1 block text-sm font-medium">{label} (0-{max})</label>
                  <input
                    type="number"
                    min={0}
                    max={max}
                    value={formData[field]}
                    onChange={(e) => setFormData({ ...formData, [field]: Number(e.target.value) })}
                    className="flex h-10 w-full rounded-md border border-input bg-white px-3 py-2 text-sm"
                  />
                </div>
              ))}
              <div className="flex items-end">
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
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Halollik<br/><span className="text-[10px]">/2</span></th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Kiyim<br/><span className="text-[10px]">/2</span></th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Punktuallik<br/><span className="text-[10px]">/2</span></th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Hurmat<br/><span className="text-[10px]">/2</span></th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Mol-mulk<br/><span className="text-[10px]">/2</span></th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Jami</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Baholagan</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Sana</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((r) => (
                    <tr key={r.id} className="border-b transition-colors hover:bg-muted/30">
                      <td className="px-4 py-3 font-medium">{r.student_name}</td>
                      <td className={`px-4 py-3 text-center font-medium ${scoreColor(r.academic_honesty, 2)}`}>{r.academic_honesty}</td>
                      <td className={`px-4 py-3 text-center font-medium ${scoreColor(r.dress_code, 2)}`}>{r.dress_code}</td>
                      <td className={`px-4 py-3 text-center font-medium ${scoreColor(r.punctuality, 2)}`}>{r.punctuality}</td>
                      <td className={`px-4 py-3 text-center font-medium ${scoreColor(r.respect, 2)}`}>{r.respect}</td>
                      <td className={`px-4 py-3 text-center font-medium ${scoreColor(r.property_care, 2)}`}>{r.property_care}</td>
                      <td className="px-4 py-3 text-center font-bold">{r.total_score}/10</td>
                      <td className="px-4 py-3 text-muted-foreground">{r.evaluated_by_name}</td>
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
