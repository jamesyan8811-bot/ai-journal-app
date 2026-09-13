import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { AppShell, PageHeader, Panel, CornerBrackets } from "@/components/AppShell";
import { members, videos } from "@/lib/club-data";

export const Route = createFileRoute("/recommender")({
  head: () => ({
    meta: [
      { title: "Video Recommender — James AI Journal Club" },
      { name: "description", content: "Personalized frontier AI video recommendations powered by a supervised recommender and reinforcement feedback loop." },
    ],
  }),
  component: Recommender,
});

function Recommender() {
  const [memberId, setMemberId] = useState(members[0].id);
  const [hideWatched, setHideWatched] = useState(true);
  const [feedback, setFeedback] = useState<Record<string, "like" | "skip" | undefined>>({});
  const member = useMemo(() => members.find((m) => m.id === memberId)!, [memberId]);

  const list = useMemo(() => {
    return videos
      .map((v) => {
        let score = v.score;
        if (member.topics.includes(v.topic)) score += 0.25;
        if (v.level === member.level) score += 0.1;
        if (v.minutes <= member.budgetMin / 3) score += 0.05;
        return { ...v, score: Math.min(0.99, Math.round(score * 100) / 100) };
      })
      .filter((v) => (hideWatched ? !member.watched.includes(v.id) : true))
      .sort((a, b) => b.score - a.score);
  }, [member, hideWatched]);

  return (
    <AppShell>
      <PageHeader
        eyebrow="// 01 · personalized.feed"
        title="Personalized Frontier AI Videos"
        description="The AI brain blends member profile, watch history and topic weights to surface the next best video."
      />

      <div className="grid gap-6 lg:grid-cols-3">
        <Panel className="p-6 lg:col-span-2">
          <label className="font-mono text-[10px] uppercase tracking-[0.3em] text-primary/80">
            Sample member profile
          </label>
          <select
            value={memberId}
            onChange={(e) => setMemberId(e.target.value)}
            className="mt-2 w-full rounded-md border border-border bg-input px-4 py-3 font-mono text-sm text-foreground outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/40"
          >
            {members.map((m) => (
              <option key={m.id} value={m.id} className="bg-background">
                {m.id} — {m.name} (grade {m.grade})
              </option>
            ))}
          </select>

          <div className="mt-5 flex items-center gap-3 text-sm text-foreground/90">
            <button
              onClick={() => setHideWatched(!hideWatched)}
              className={`relative grid h-5 w-5 place-items-center rounded border transition ${
                hideWatched
                  ? "border-primary bg-primary/20 glow-cyan"
                  : "border-border bg-surface"
              }`}
              aria-label="toggle watched"
            >
              {hideWatched && (
                <svg viewBox="0 0 24 24" className="h-3.5 w-3.5 text-primary" fill="none" stroke="currentColor" strokeWidth="3">
                  <path d="M4 12l5 5L20 6" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              )}
            </button>
            <span>Hide videos this member already watched</span>
          </div>

          <div className="mt-6 rounded-md border border-primary/30 bg-primary/5 p-4">
            <div className="font-mono text-[10px] uppercase tracking-[0.28em] text-primary/80">
              Profile signal
            </div>
            <div className="mt-2 flex flex-wrap gap-x-4 gap-y-2 text-sm">
              <Meta k="Topics" v={member.topics.join(" · ")} />
              <Meta k="Level" v={member.level} />
              <Meta k="Budget" v={`${member.budgetMin} min`} />
            </div>
          </div>
        </Panel>

        <Panel className="p-6" glow="violet">
          <div className="font-mono text-[10px] uppercase tracking-[0.3em] text-accent">
            Model state
          </div>
          <div className="mt-4 space-y-3">
            {[
              { l: "Candidates", v: videos.length },
              { l: "After filters", v: list.length },
              { l: "Feedback events", v: Object.keys(feedback).length },
            ].map((s) => (
              <div key={s.l} className="flex items-baseline justify-between border-b border-border/40 pb-2 last:border-none">
                <span className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">{s.l}</span>
                <span className="font-display text-2xl font-semibold text-holo">{s.v}</span>
              </div>
            ))}
          </div>
        </Panel>
      </div>

      <h2 className="mt-12 font-display text-2xl font-semibold text-foreground">
        <span className="font-mono text-sm text-primary/80">›</span> Top recommendations
      </h2>

      <div className="mt-6 space-y-4">
        {list.map((v, i) => {
          const state = feedback[v.id];
          return (
            <div key={v.id} className="relative overflow-hidden rounded-lg holo-panel p-6">
              <CornerBrackets />
              <div className="grid gap-6 lg:grid-cols-[1fr_auto]">
                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="font-mono text-[10px] uppercase tracking-[0.3em] text-primary/70">
                      Rank {String(i + 1).padStart(2, "0")}
                    </span>
                    <span className="rounded-sm border border-primary/40 bg-primary/10 px-2 py-0.5 font-mono text-[10px] uppercase tracking-widest text-primary">
                      {v.topic}
                    </span>
                    <span className="rounded-sm border border-accent/40 bg-accent/10 px-2 py-0.5 font-mono text-[10px] uppercase tracking-widest text-accent">
                      {v.level}
                    </span>
                  </div>
                  <h3 className="mt-3 font-display text-xl font-semibold text-foreground">
                    {v.title}
                  </h3>
                  <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{v.desc}</p>

                  <div className="mt-5 grid grid-cols-2 gap-2 sm:grid-cols-4">
                    <Stat k="Est." v={`${v.minutes} min`} />
                    <Stat k="Topic" v={v.topic} />
                    <Stat k="Level" v={v.level} />
                    <Stat k="Score" v={v.score.toFixed(2)} accent />
                  </div>

                  <div className="mt-4">
                    <div className="mb-1 flex justify-between font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
                      <span>relevance</span>
                      <span>{Math.round(v.score * 100)}%</span>
                    </div>
                    <div className="h-1.5 w-full overflow-hidden rounded-full bg-surface">
                      <div
                        className="h-full rounded-full bg-gradient-to-r from-cyan-glow to-violet-glow"
                        style={{ width: `${Math.min(100, v.score * 100)}%` }}
                      />
                    </div>
                  </div>

                  <button className="mt-5 inline-flex items-center gap-2 rounded-md border border-primary/50 bg-primary/10 px-4 py-2 font-mono text-[11px] uppercase tracking-[0.28em] text-primary transition hover:bg-primary/20 hover:glow-cyan">
                    <span>▷</span> Open video resource
                  </button>
                </div>

                <div className="flex flex-col justify-start gap-3 lg:min-w-[160px]">
                  <div className="font-mono text-[10px] uppercase tracking-[0.28em] text-muted-foreground">
                    Teach the app
                  </div>
                  <button
                    onClick={() => setFeedback((f) => ({ ...f, [v.id]: f[v.id] === "like" ? undefined : "like" }))}
                    className={`rounded-md border px-4 py-2.5 font-mono text-xs uppercase tracking-widest transition ${
                      state === "like"
                        ? "border-primary bg-primary/20 text-primary glow-cyan"
                        : "border-border bg-surface/60 text-foreground hover:border-primary/60"
                    }`}
                  >
                    ◆ Like
                  </button>
                  <button
                    onClick={() => setFeedback((f) => ({ ...f, [v.id]: f[v.id] === "skip" ? undefined : "skip" }))}
                    className={`rounded-md border px-4 py-2.5 font-mono text-xs uppercase tracking-widest transition ${
                      state === "skip"
                        ? "border-accent bg-accent/20 text-accent glow-violet"
                        : "border-border bg-surface/60 text-foreground hover:border-accent/60"
                    }`}
                  >
                    ✕ Not for me
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </AppShell>
  );
}

function Meta({ k, v }: { k: string; v: string }) {
  return (
    <span className="font-mono text-xs text-muted-foreground">
      <span className="text-primary/80">{k}:</span> <span className="text-foreground">{v}</span>
    </span>
  );
}

function Stat({ k, v, accent }: { k: string; v: string; accent?: boolean }) {
  return (
    <div className="rounded-md border border-border/60 bg-surface/40 px-3 py-2">
      <div className="font-mono text-[9px] uppercase tracking-widest text-muted-foreground">{k}</div>
      <div className={`mt-0.5 text-sm ${accent ? "font-display font-semibold text-holo" : "text-foreground"}`}>{v}</div>
    </div>
  );
}