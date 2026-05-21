"use client";

import { useState, useEffect, useRef } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Send, User as UserIcon, BrainCircuit, Loader2 } from "lucide-react";
import { api, getUserFromToken } from "@/lib/api";

export default function AdvisorPage() {
  const [messages, setMessages] = useState<{ role: "user" | "assistant"; text: string }[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [role, setRole] = useState<string | null>(null);
  const [children, setChildren] = useState<any[]>([]);
  const [selectedChildId, setSelectedChildId] = useState<string | undefined>(undefined);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const user = getUserFromToken();
    if (user) {
      setRole(user.role);
      if (user.role === "parent") {
        api.getMyChildren().then(data => {
          setChildren(data);
          if (data.length > 0 && data[0].student_profile) {
            setSelectedChildId(data[0].student_profile.student_id as string);
          }
        });
      }
    }
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setMessages((prev) => [...prev, { role: "user", text: userMessage }]);
    setInput("");
    setLoading(true);

    try {
      const res = await api.sendAdvisorMessage(userMessage, selectedChildId as any);
      setMessages((prev) => [...prev, { role: "assistant", text: res.reply }]);
    } catch (error: any) {
      setMessages((prev) => [...prev, { role: "assistant", text: `Xatolik yuz berdi: ${error.message || "Ulanishda xatolik."}` }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-[calc(100vh-6rem)] flex-col max-w-5xl mx-auto">
      <div className="mb-4 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <BrainCircuit className="h-6 w-6 text-purple-600" />
            AI Akademik Maslahatchi
          </h1>
          <p className="text-muted-foreground text-sm mt-1">Grant va akademik natijalar bo'yicha sun'iy intellekt yordamchisi</p>
        </div>
        
        {role === "parent" && children.length > 0 && (
          <div className="shrink-0 bg-white p-2 rounded-lg border shadow-sm flex items-center gap-2">
            <span className="text-sm font-medium text-muted-foreground">Farzandni tanlang:</span>
            <select 
              className="rounded-md border-0 bg-gray-50 p-1.5 text-sm font-semibold focus:ring-2 focus:ring-primary outline-none cursor-pointer"
              value={selectedChildId}
              onChange={(e) => setSelectedChildId(e.target.value)}
            >
              {children.map(child => (
                <option key={child.id} value={child.student_profile?.student_id}>
                  {child.first_name} {child.last_name}
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      <Card className="flex flex-1 flex-col overflow-hidden shadow-lg border-primary/10">
        <CardContent className="flex flex-1 flex-col p-0">
          <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6 bg-[#f8fafc]">
            {messages.length === 0 ? (
              <div className="flex h-full flex-col items-center justify-center text-center text-muted-foreground animate-in fade-in duration-700">
                <div className="mb-6 rounded-full bg-purple-100 p-6 shadow-sm ring-8 ring-purple-50">
                  <BrainCircuit className="h-10 w-10 text-purple-600" />
                </div>
                <h3 className="text-xl font-semibold text-slate-800">Men bilan suhbatlashing</h3>
                <p className="max-w-md mt-3 text-sm text-slate-500 leading-relaxed">
                  Men EduMetric AI yordamchisiman. Grantingiz xavf ostidami, qanday qilib qo'shimcha ball yig'ish yoki jarimalarni qoplash mumkinligi haqida so'rang.
                </p>
                <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-lg">
                  <button onClick={() => setInput("Grantim xavf ostida emi? Iltimos, ma'lumot bering.")} className="p-3 text-sm border rounded-xl hover:bg-purple-50 hover:border-purple-200 hover:text-purple-700 text-left transition-colors bg-white shadow-sm">
                    "Grantim xavf ostidami?"
                  </button>
                  <button onClick={() => setInput("Jarima ballarimni qanday qilib tiklasam (recovery) bo'ladi?")} className="p-3 text-sm border rounded-xl hover:bg-purple-50 hover:border-purple-200 hover:text-purple-700 text-left transition-colors bg-white shadow-sm">
                    "Jarimalarni qanday yopaman?"
                  </button>
                </div>
              </div>
            ) : (
              messages.map((msg, i) => (
                <div key={i} className={`flex gap-3 md:gap-4 ${msg.role === "user" ? "flex-row-reverse" : ""}`}>
                  <div className={`flex h-8 w-8 md:h-10 md:w-10 shrink-0 items-center justify-center rounded-full shadow-sm ${msg.role === "user" ? "bg-primary text-primary-foreground" : "bg-gradient-to-br from-purple-100 to-purple-200 text-purple-700"}`}>
                    {msg.role === "user" ? <UserIcon className="h-4 w-4 md:h-5 md:w-5" /> : <BrainCircuit className="h-4 w-4 md:h-5 md:w-5" />}
                  </div>
                  <div className={`max-w-[85%] md:max-w-[75%] rounded-2xl px-4 py-3 md:px-5 md:py-4 ${msg.role === "user" ? "bg-primary text-primary-foreground rounded-tr-none shadow-md" : "bg-white border border-slate-100 shadow-md rounded-tl-none"}`}>
                    <div className="whitespace-pre-wrap text-[14px] md:text-[15px] leading-relaxed break-words">{msg.text}</div>
                  </div>
                </div>
              ))
            )}
            {loading && (
              <div className="flex gap-3 md:gap-4">
                <div className="flex h-8 w-8 md:h-10 md:w-10 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-purple-100 to-purple-200 text-purple-700 shadow-sm">
                  <BrainCircuit className="h-4 w-4 md:h-5 md:w-5" />
                </div>
                <div className="max-w-[85%] rounded-2xl bg-white border border-slate-100 shadow-md px-5 py-4 rounded-tl-none flex items-center gap-3">
                  <Loader2 className="h-4 w-4 animate-spin text-purple-600" />
                  <span className="text-sm font-medium text-slate-500">Maslahatchi o'ylamoqda...</span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          
          <div className="border-t bg-white p-4">
            <form 
              onSubmit={(e) => { e.preventDefault(); handleSend(); }}
              className="flex gap-2 relative max-w-5xl mx-auto items-end"
            >
              <textarea
                placeholder="Savolingizni yozing..."
                className="flex-1 max-h-32 min-h-[52px] rounded-2xl border border-slate-200 bg-slate-50 px-5 py-3.5 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500 transition-all resize-none shadow-inner"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSend();
                  }
                }}
                disabled={loading}
                rows={1}
              />
              <button
                type="submit"
                disabled={!input.trim() || loading}
                className="flex h-[52px] w-[52px] shrink-0 items-center justify-center rounded-2xl bg-primary text-primary-foreground shadow-md transition-all hover:bg-primary/90 active:scale-95 disabled:opacity-50 disabled:pointer-events-none"
              >
                <Send className="h-5 w-5 ml-1" />
              </button>
            </form>
            <div className="text-center mt-2">
              <span className="text-[11px] text-slate-400">AI tomonidan berilgan maslahatlar xato bo'lishi mumkin.</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
