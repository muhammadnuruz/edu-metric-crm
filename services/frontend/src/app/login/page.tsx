"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export default function LoginPage() {
  const router = useRouter();
  const [tab, setTab] = useState<"login" | "phone">("login");
  const [username, setUsername] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      if (tab === "phone") {
        await api.phoneLogin(phone, password);
      } else {
        await api.login(username, password);
      }
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Xatolik yuz berdi");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-primary text-2xl font-bold text-primary-foreground">
            EM
          </div>
          <CardTitle className="text-2xl">EduMetric</CardTitle>
          <CardDescription>PDP University Grant Management System</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="mb-4 flex rounded-lg bg-muted p-1">
            <button
              type="button"
              onClick={() => { setTab("login"); setError(""); }}
              className={`flex-1 rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                tab === "login" ? "bg-white shadow-sm" : "text-muted-foreground hover:text-foreground"
              }`}
            >
              Login
            </button>
            <button
              type="button"
              onClick={() => { setTab("phone"); setError(""); }}
              className={`flex-1 rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                tab === "phone" ? "bg-white shadow-sm" : "text-muted-foreground hover:text-foreground"
              }`}
            >
              Telefon raqam
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="rounded-md bg-destructive/10 p-3 text-sm text-destructive">
                {error}
              </div>
            )}

            {tab === "login" ? (
              <div className="space-y-2">
                <label htmlFor="username" className="text-sm font-medium">
                  Login
                </label>
                <input
                  id="username"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                  placeholder="Foydalanuvchi nomi"
                  required
                />
              </div>
            ) : (
              <div className="space-y-2">
                <label htmlFor="phone" className="text-sm font-medium">
                  Telefon raqam
                </label>
                <input
                  id="phone"
                  type="tel"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                  placeholder="+998 90 123 45 67"
                  required
                />
              </div>
            )}

            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium">
                Parol
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                placeholder="Parol"
                required
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="inline-flex h-10 w-full items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 disabled:opacity-50"
            >
              {loading ? "Kirish..." : "Kirish"}
            </button>

            {tab === "phone" && (
              <p className="text-center text-xs text-muted-foreground">
                Ota-onalar uchun telefon raqam orqali kirish
              </p>
            )}

            <div className="text-center">
              <a href="/rating" className="text-sm text-primary hover:underline">
                Ochiq reytingni ko'rish
              </a>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
