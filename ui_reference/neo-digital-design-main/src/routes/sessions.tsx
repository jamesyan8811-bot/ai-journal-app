import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { AppShell, PageHeader, Panel, CornerBrackets } from "@/components/AppShell";
import { sessions } from "@/lib/club-data";

export const Route = createFileRoute("/sessions")({
  head: () => ({
    meta: [
      { title: "Sessions & Tutorials — James AI Journal Club" },
      { name: "description", content: "Subscribe to live AI sessions and hands-on tutorials led by James and guest mentors." },
    ],
  }),
  component: SessionsPage,
});

function SessionsPage() {
  const topics = useMemo(() => ["All", ...Array.from(new Set(sessions.map((s) => s.topic)))], []);
  const [topic, setTopic] = useState("All");
  const [subs, setSubs] = useState<Record<string, boolean>>({});
  const list = sessions.filter((s) => topic === "All" || s.topic === topic);

  return (
    <AppShell>
      <PageHeader
        eyebrow="// 02 · live.transmissions"
        title="Subscribe to AI Sessions & Tutorials"
        description="Reserve a slot in upcoming live sessions. Each broadcast is capacity-limited and streamed from the JAJC hub."
      />

      <Panel className="mb-8 p-6">
        <label className="font-mono text-[10px] uppercase tracking-[0.3em] text-primary/80">
          Filter by topic
        </label>
        <div className="mt-3 flex flex-wrap gap-2">
          {topics.map((t) => (
            <button
              key={t}
              onClick={() => setTopic(t)}
              className={`rounded-full border px-4 py-1.5 font-mono text-[11px] uppercase tracking-widest transition ${
                topic === t
                  ? "border-primary bg-primary/20 text-primary glow-cyan"
                  : "border-border bg-surface/50 text-muted-foreground hover:text-foreground"
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </Panel>

      <div className="grid gap-4 md:grid-cols-2">
        {list.map((s, i) => {
          const subscribed = !!subs[s.id];
          const seats = s.capacity - (subscribed ? 1 : 0);
          return (
            <div key={s.id} className="relative overflow-hidden rounded-lg holo-panel p-6">
              <CornerBrackets />
              <div className="flex items-start justify-between gap-4">
                <div className="min-w-0">
                  <div className="font-mono text-[10px] uppercase tracking-[0.3em] text-primary/70">
                    Session {String(i + 1).padStart(2, "0")} · {s.date}
                  </div>
                  <h3 className="mt-2 font-display text-xl font-semibold text-foreground">
                    {s.title}
                  </h3>
                </div>
                <div
                  className={`shrink-0 rounded-sm border px-2 py-0.5 font-mono text-[10px] uppercase tracking-widest ${
                    s.difficulty === "Beginner"
                      ? "border-primary/40 bg-primary/10 text-primary"
                      : s.difficulty === "Intermediate"
                      ? "border-accent/40 bg-accent/10 text-accent"
                      : "border-destructive/50 bg-destructive/10 text-destructive"
                  }`}
                >
                  {s.difficulty}
                </div>
              </div>

              <p className="mt-3 text-sm leading-relaxed text-muted-foreground">{s.desc}</p>

              <div className="mt-5 grid grid-cols-3 gap-2">
                <MiniStat k="Topic" v={s.topic} />
                <MiniStat k="Teacher" v={s.teacher} />
                <MiniStat k="Seats" v={String(seats)} />
              </div>

              <div className="mt-5 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span
                    className={`h-1.5 w-1.5 rounded-full ${
                      subscribed
                        ? "bg-cyan-glow shadow-[0_0_10px_var(--cyan-glow)] animate-pulse-glow"
                        : "bg-muted-foreground/50"
                    }`}
                  />
                  <span className="font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
                    {subscribed ? "subscribed" : "open"}
                  </span>
                </div>
                <button
                  onClick={() => setSubs((x) => ({ ...x, [s.id]: !x[s.id] }))}
                  className={`rounded-md border px-4 py-2 font-mono text-[11px] uppercase tracking-[0.28em] transition ${
                    subscribed
                      ? "border-accent bg-accent/20 text-accent glow-violet"
                      : "border-primary/50 bg-primary/10 text-primary hover:bg-primary/20 hover:glow-cyan"
                  }`}
                >
                  {subscribed ? "✓ Subscribed" : "+ Subscribe"}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </AppShell>
  );
}

function MiniStat({ k, v }: { k: string; v: string }) {
  return (
    <div className="rounded-md border border-border/60 bg-surface/40 px-3 py-2">
      <div className="font-mono text-[9px] uppercase tracking-widest text-muted-foreground">{k}</div>
      <div className="mt-0.5 truncate text-xs text-foreground">{v}</div>
    </div>
  );
}