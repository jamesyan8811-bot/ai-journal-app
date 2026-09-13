import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { AppShell, PageHeader, Panel, CornerBrackets } from "@/components/AppShell";
import { posts } from "@/lib/club-data";

export const Route = createFileRoute("/channels")({
  head: () => ({
    meta: [
      { title: "Discussion Channels — James AI Journal Club" },
      { name: "description", content: "Live discussion channels where members share questions, reactions and project ideas about frontier AI." },
    ],
  }),
  component: Channels,
});

function Channels() {
  const channels = useMemo(
    () => ["All", ...Array.from(new Set(posts.map((p) => p.channel)))],
    [],
  );
  const [chan, setChan] = useState("All");
  const [upvotes, setUpvotes] = useState<Record<number, boolean>>({});
  const list = posts.filter((p) => chan === "All" || p.channel === chan);

  return (
    <AppShell>
      <PageHeader
        eyebrow="// 03 · signal.streams"
        title="Discussion Channels"
        description="Broadcast lines for questions, reactions and project ideas from every JAJC member."
      />

      <div className="mb-8 flex flex-wrap gap-2">
        {channels.map((c) => (
          <button
            key={c}
            onClick={() => setChan(c)}
            className={`rounded-full border px-4 py-1.5 font-mono text-[11px] uppercase tracking-widest transition ${
              chan === c
                ? "border-primary bg-primary/20 text-primary glow-cyan"
                : "border-border bg-surface/50 text-muted-foreground hover:text-foreground"
            }`}
          >
            #{c === "All" ? "all" : c}
          </button>
        ))}
      </div>

      <div className="space-y-4">
        {list.map((p, i) => {
          const boosted = !!upvotes[i];
          const count = p.upvotes + (boosted ? 1 : 0);
          return (
            <Panel key={i} className="p-6">
              <CornerBrackets />
              <div className="grid gap-4 sm:grid-cols-[auto_minmax(0,1fr)_auto] sm:items-start">
                <button
                  onClick={() => setUpvotes((u) => ({ ...u, [i]: !u[i] }))}
                  className={`flex h-14 w-14 shrink-0 flex-col items-center justify-center rounded-md border transition ${
                    boosted
                      ? "border-primary bg-primary/20 text-primary glow-cyan"
                      : "border-border bg-surface/50 text-muted-foreground hover:text-foreground"
                  }`}
                >
                  <span className="text-sm">▲</span>
                  <span className="font-mono text-xs">{count}</span>
                </button>

                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="rounded-sm border border-primary/40 bg-primary/10 px-2 py-0.5 font-mono text-[10px] uppercase tracking-widest text-primary">
                      #{p.channel}
                    </span>
                    <span className="font-mono text-[10px] uppercase tracking-[0.28em] text-muted-foreground">
                      {p.topic}
                    </span>
                  </div>
                  <p className="mt-3 font-display text-lg leading-snug text-foreground">
                    {p.body}
                  </p>
                  <div className="mt-3 flex flex-wrap items-center gap-2 font-mono text-[11px] text-muted-foreground">
                    <span className="text-accent">@{p.author}</span>
                    <span>·</span>
                    <span>{p.date}</span>
                  </div>
                </div>

                <button className="rounded-md border border-border bg-surface/60 px-3 py-2 font-mono text-[10px] uppercase tracking-widest text-muted-foreground transition hover:border-accent/60 hover:text-accent">
                  Reply
                </button>
              </div>
            </Panel>
          );
        })}
      </div>
    </AppShell>
  );
}