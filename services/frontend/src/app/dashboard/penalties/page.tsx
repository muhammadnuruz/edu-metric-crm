"use client";

import { useEffect, useState } from "react";
import { api, getUserFromToken } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface Penalty {
  id: number;
  student: number;
  student_name: string;
  category: string;
  severity: string;
  points_deducted: number;
  description: string;
  issued_by_name: string;
  created_at: string;
}

const severityLabels: Record<string, string> = {
  light: "Yengil",
  medium: "O'rta",
  heavy: "Og'ir",
};

const severityColors: Record<string, string> = {
  light: "bg-yellow-100 text-yellow-700",
  medium: "bg-orange-100 text-orange-700",
  heavy: "bg-red-100 text-red-700",
};

const categoryLabels: Record<string, string> = {
  late_submission: "Kechikib topshirish",
  absence: "Sababsiz kelmagan",
  misconduct: "Noto'g'ri xulq",
  cheating: "Ko'chirish",
  plagiarism: "Plagiat",
  dress_code: "Kiyim qoidasi",
  property_damage: "Mol-mulk buzish",
  disrespect: "Hurmatni saqlmaslik",
  other: "Boshqa",
};

export default function PenaltiesPage() {
  const [penalties, setPenalties] = useState<Penalty[]>([]);
  const [loading, setLoading] = useState(true);
  const user = getUserFromToken();
  const isAdmin = user?.role === "admin";

  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    student: "",
    category: "late_submission",
    severity: "light",
    description: "",
  });

  useEffect(() => {
    api.get<{ results: Penalty[] }>("/penalties/penalties/?page_size=100")
      .then((data) => setPenalties(data.results || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post("/penalties/penalties/", { ...formData, student: Number(formData.student) });
      setShowForm(false);
      setFormData({ student: "", category: "late_submission", severity: "light", description: "" });
      const data = await api.get<{ results: Penalty[] }>("/penalties/penalties/?page_size=100");
      setPenalties(data.results || []);
    } catch {}
  };

  const totalDeducted = penalties.reduce((sum, p) => sum + p.points_deducted, 0);

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Jarimalar</h1>
          <p className="text-sm text-muted-foreground">Intizomiy jarimalar (max -20 ball)</p>
        </div>
        {isAdmin && (
          <button
            onClick={() => setShowForm(!showForm)}
            className="rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700"
          >
            {showForm ? "Bekor qilish" : "+ Jarima qo'shish"}
          </button>
        )}
      </div>

      {showForm && (
        <Card className="mb-6 border-red-200">
          <CardHeader><CardTitle className="text-lg text-red-700">Yangi jarima</CardTitle></CardHeader>
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
                <label className="mb-1 block text-sm font-medium">Darajasi</label>
                <select
                  value={formData.severity}
                  onChange={(e) => setFormData({ ...formData, severity: e.target.value })}
                  className="flex h-10 w-full rounded-md border border-input bg-white px-3 py-2 text-sm"
                >
                  {Object.entries(severityLabels).map(([k, v]) => (
                    <option key={k} value={k}>{v}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Tavsif</label>
                <input
                  type="text"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="flex h-10 w-full rounded-md border border-input bg-white px-3 py-2 text-sm"
                  required
                />
              </div>
              <div className="flex items-end">
                <button type="submit" className="rounded-lg bg-red-600 px-6 py-2 text-sm font-medium text-white hover:bg-red-700">
                  Jarima berish
                </button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

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
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Kategoriya</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Daraja</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Ball</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Tavsif</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Bergan</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Sana</th>
                  </tr>
                </thead>
                <tbody>
                  {penalties.map((p) => (
                    <tr key={p.id} className="border-b transition-colors hover:bg-muted/30">
                      <td className="px-4 py-3 font-medium">{p.student_name}</td>
                      <td className="px-4 py-3">{categoryLabels[p.category] || p.category}</td>
                      <td className="px-4 py-3 text-center">
                        <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${severityColors[p.severity]}`}>
                          {severityLabels[p.severity]}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-center font-bold text-red-600">-{p.points_deducted}</td>
                      <td className="px-4 py-3 text-muted-foreground">{p.description}</td>
                      <td className="px-4 py-3 text-muted-foreground">{p.issued_by_name}</td>
                      <td className="px-4 py-3 text-muted-foreground">{new Date(p.created_at).toLocaleDateString("uz")}</td>
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
