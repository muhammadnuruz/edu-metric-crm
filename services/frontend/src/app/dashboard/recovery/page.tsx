"use client";

import { useEffect, useState } from "react";
import { api, getUserFromToken } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface Recovery {
  id: number;
  student: number;
  student_name: string;
  task_description: string;
  points_recovery: number;
  status: string;
  assigned_by_name: string;
  completed_at: string | null;
  created_at: string;
}

export default function RecoveryPage() {
  const [recoveries, setRecoveries] = useState<Recovery[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("");
  const user = getUserFromToken();
  const canApprove = user?.role === "admin" || user?.role === "manager";
  const isStudent = user?.role === "student";

  useEffect(() => {
    loadRecoveries();
  }, [filter]);

  const loadRecoveries = () => {
    const params = filter ? `?status=${filter}` : "";
    api.get<{ results: Recovery[] }>(`/penalties/recovery/${params}`)
      .then((data) => setRecoveries(data.results || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  const handleComplete = async (id: number) => {
    try {
      await api.post(`/penalties/recovery/${id}/complete/`, {});
      loadRecoveries();
    } catch {}
  };

  const statusColors: Record<string, string> = {
    assigned: "bg-blue-100 text-blue-700",
    in_progress: "bg-yellow-100 text-yellow-700",
    completed: "bg-green-100 text-green-700",
    rejected: "bg-red-100 text-red-700",
  };

  const statusLabels: Record<string, string> = {
    assigned: "Tayinlangan",
    in_progress: "Jarayonda",
    completed: "Bajarilgan",
    rejected: "Rad etilgan",
  };

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold">Tiklanish Vazifalari</h1>
        <p className="text-sm text-muted-foreground">Jarima ballini qaytarish vazifalari (max +10 ball)</p>
      </div>

      <div className="mb-4 flex gap-2">
        {["", "assigned", "in_progress", "completed"].map((f) => (
          <button
            key={f}
            onClick={() => { setFilter(f); setLoading(true); }}
            className={`rounded-lg px-3 py-1.5 text-sm font-medium transition-colors ${
              filter === f ? "bg-primary text-white" : "bg-muted text-muted-foreground hover:bg-muted/80"
            }`}
          >
            {f === "" ? "Barchasi" : statusLabels[f] || f}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="py-20 text-center text-muted-foreground">Yuklanmoqda...</div>
      ) : recoveries.length === 0 ? (
        <Card><CardContent className="py-12 text-center text-muted-foreground">Tiklanish vazifalari topilmadi</CardContent></Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {recoveries.map((r) => (
            <Card key={r.id}>
              <CardContent className="p-4">
                <div className="mb-2 flex items-start justify-between">
                  <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${statusColors[r.status]}`}>
                    {statusLabels[r.status] || r.status}
                  </span>
                  <span className="text-sm font-bold text-green-600">+{r.points_recovery} ball</span>
                </div>
                <p className="mb-1 font-medium">{r.student_name}</p>
                <p className="mb-3 text-sm text-muted-foreground">{r.task_description}</p>
                <div className="flex items-center justify-between text-xs text-muted-foreground">
                  <span>Tayinlagan: {r.assigned_by_name}</span>
                  <span>{new Date(r.created_at).toLocaleDateString("uz")}</span>
                </div>
                {isStudent && r.status === "assigned" && (
                  <button
                    onClick={() => handleComplete(r.id)}
                    className="mt-3 w-full rounded bg-green-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-green-700"
                  >
                    Bajarildi deb belgilash
                  </button>
                )}
                {canApprove && r.status === "in_progress" && (
                  <div className="mt-3 flex gap-2">
                    <button
                      onClick={() => handleComplete(r.id)}
                      className="flex-1 rounded bg-green-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-green-700"
                    >
                      Tasdiqlash
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
