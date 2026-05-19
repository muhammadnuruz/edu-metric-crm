"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";

interface ScoreCardProps {
  label: string;
  score: number;
  maxScore: number;
  icon: React.ReactNode;
  color?: string;
}

export function ScoreCard({ label, score, maxScore, icon, color = "bg-primary" }: ScoreCardProps) {
  const percentage = maxScore > 0 ? (score / maxScore) * 100 : 0;

  return (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <div className={cn("flex h-8 w-8 items-center justify-center rounded-lg text-white", color)}>
              {icon}
            </div>
            <span className="text-sm font-medium text-muted-foreground">{label}</span>
          </div>
          <span className="text-lg font-bold">
            {score}<span className="text-sm font-normal text-muted-foreground">/{maxScore}</span>
          </span>
        </div>
        <Progress value={percentage} className="h-2" />
      </CardContent>
    </Card>
  );
}
