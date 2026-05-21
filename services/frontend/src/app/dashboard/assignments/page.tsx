"use client";

import { useEffect, useState } from "react";
import { api, getUserFromToken } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";

interface AssignmentSubmission {
  id: number;
  assignment_title: string;
  assignment_type: string;
  student: number;
  student_name: string;
  submitted_at: string;
  status: string;
  quality_score: number;
  deadline_score: number;
  independence_score: number;
  total_score: number;
  graded_by_name: string | null;
}

const typeLabels: Record<string, string> = {
  homework: "Uy vazifasi",
  project: "Loyiha",
  lab: "Laboratoriya",
};

export default function AssignmentsPage() {
  const [submissions, setSubmissions] = useState<AssignmentSubmission[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("");
  const user = getUserFromToken();
  const isTeacher = user?.role === "teacher" || user?.role === "admin";

  useEffect(() => {
    api.get<{ results: AssignmentSubmission[] }>("/assignments/submissions/?page_size=100")
      .then((data) => setSubmissions(data.results || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const filtered = submissions.filter((s) => !filter || s.status === filter);

  const statusColors: Record<string, string> = {
    pending: "bg-yellow-100 text-yellow-700",
    graded: "bg-green-100 text-green-700",
    returned: "bg-blue-100 text-blue-700",
    plagiarism: "bg-red-100 text-red-700",
  };

  const statusLabels: Record<string, string> = {
    pending: "Kutilmoqda",
    graded: "Baholangan",
    returned: "Qaytarilgan",
    plagiarism: "Plagiat",
  };

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold">Topshiriqlar</h1>
        <p className="text-sm text-muted-foreground">Topshiriq va loyihalar (max 15 ball)</p>
      </div>

      <div className="mb-4 flex gap-2">
        {["", "pending", "graded", "returned", "plagiarism"].map((f) => (
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
      ) : (
        <Card>
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b bg-muted/50">
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Talaba</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Topshiriq</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Turi</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Sifat</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Muddat</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Mustaqillik</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Jami</th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-muted-foreground">Holat</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground">Sana</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((s) => (
                    <tr key={s.id} className="border-b transition-colors hover:bg-muted/30">
                      <td className="px-4 py-3 font-medium">{s.student_name}</td>
                      <td className="px-4 py-3">{s.assignment_title}</td>
                      <td className="px-4 py-3 text-center">
                        <span className="rounded bg-muted px-2 py-0.5 text-xs">{typeLabels[s.assignment_type] || s.assignment_type}</span>
                      </td>
                      <td className="px-4 py-3 text-center">{s.quality_score}</td>
                      <td className="px-4 py-3 text-center">{s.deadline_score}</td>
                      <td className="px-4 py-3 text-center">{s.independence_score}</td>
                      <td className="px-4 py-3 text-center font-bold">{s.total_score}</td>
                      <td className="px-4 py-3 text-center">
                        <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${statusColors[s.status] || "bg-gray-100"}`}>
                          {statusLabels[s.status] || s.status}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-muted-foreground">{new Date(s.submitted_at).toLocaleDateString("uz")}</td>
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
