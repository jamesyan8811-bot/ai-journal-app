import { createFileRoute, Link } from "@tanstack/react-router";
import { AppShell, PageHeader, Panel, CornerBrackets } from "@/components/AppShell";
import { stats, navItems } from "@/lib/club-data";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "James AI Journal Club — Frontier AI Learning Hub" },
      { name: "description", content: "Prototype learning community where students discover frontier AI videos, subscribe to tutorials, and see how an AI brain personalizes learning." },
    ],
  }),
  component: Index,
});

function Index() {
  return (
    <AppShell>
      <PageHeader
        eyebrow="// system.overview"
        title="James AI Journal Club"
        description="A prototype learning community where students discover frontier AI videos, subscribe to tutorials, discuss ideas, and see how an AI brain can personalize learning."
      />

      {/* Stat grid */}
      <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
        {stats.map((s, i) => (
          <div key={s.label} className="relative overflow-hidden rounded-lg holo-panel p-5">
            <CornerBrackets />
            <div className="font-mono text-[10px] uppercase tracking-[0.3em] text-primary/70">
              {String(i + 1).padStart(2, "0")} · {s.label}
            </div>
            <div className="mt-3 font-display text-4xl font-bold text-holo md:text-5xl">
              {s.value}
            </div>
            <div className="mt-3 h-px w-full bg-gradient-to-r from-cyan-glow/60 to-transparent" />
          </div>
        ))}
      </div>

      {/* Concept + Architecture */}
      <div className="mt-12 grid gap-6 lg:grid-cols-5">
        <Panel className="p-8 lg:col-span-3">
          <div className="flex items-center gap-3">
            <span className="h-1.5 w-1.5 rounded-full bg-cyan-glow shadow-[0_0_10px_var(--cyan-glow)]" />
            <h2 className="font-display text-2xl font-semibold">App concept</h2>
          </div>
          <ol className="mt-6 space-y-4">
            {[
              "Students watch short, up-to-date AI learning resources written at a high-school level.",
              "Members subscribe to tutorials and sessions led by James and guest mentors.",
              "Channels let students post questions, reactions, and project ideas.",
              "The AI brain recommends content, explains difficult topics, and improves from feedback.",
            ].map((line, i) => (
              <li key={i} className="flex gap-4">
                <span className="mt-0.5 font-mono text-xs font-medium text-primary">
                  0{i + 1}
                </span>
                <span className="text-sm leading-relaxed text-foreground/90">{line}</span>
              </li>
            ))}
          </ol>
        </Panel>

        <Panel className="p-8 lg:col-span-2" glow="violet">
          <div className="flex items-center gap-3">
            <span className="h-1.5 w-1.5 rounded-full bg-violet-glow shadow-[0_0_10px_var(--violet-glow)]" />
            <h2 className="font-display text-2xl font-semibold">AI brain architecture</h2>
          </div>
          <div className="mt-6 space-y-3">
            {[
              { l: "Input", t: "Open resources · club videos · survey data" },
              { l: "Layer 01", t: "Supervised recommender" },
              { l: "Layer 02", t: "High-school explanation engine + concept layer" },
              { l: "Feedback", t: "Reinforcement loop from likes / skips / subscriptions" },
            ].map((n, i) => (
              <div key={i}>
                <div className="relative rounded-md border border-border/60 bg-surface/50 p-3">
                  <div className="font-mono text-[10px] uppercase tracking-[0.28em] text-primary/70">
                    {n.l}
                  </div>
                  <div className="mt-1 text-sm text-foreground/90">{n.t}</div>
                </div>
                {i < 3 && (
                  <div className="my-1 flex justify-center">
                    <div className="h-4 w-px bg-gradient-to-b from-cyan-glow to-violet-glow" />
                  </div>
                )}
              </div>
            ))}
          </div>
        </Panel>
      </div>

      {/* Navigate */}
      <div className="mt-12">
        <div className="mb-4 font-mono text-[11px] uppercase tracking-[0.3em] text-muted-foreground">
          // navigate the system
        </div>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {navItems.slice(1).map((n) => (
            <Link
              key={n.to}
              to={n.to}
              className="group relative overflow-hidden rounded-lg holo-panel p-5 transition-all hover:-translate-y-0.5"
            >
              <CornerBrackets />
              <div className="flex items-center justify-between">
                <span className="font-mono text-[10px] uppercase tracking-[0.3em] text-primary/70">
                  {n.code}
                </span>
                <span className="font-mono text-xs text-primary opacity-0 transition-opacity group-hover:opacity-100">
                  →
                </span>
              </div>
              <div className="mt-3 font-display text-lg font-semibold text-foreground">
                {n.label}
              </div>
              <div className="mt-4 h-px w-full bg-gradient-to-r from-cyan-glow/40 via-violet-glow/30 to-transparent transition-all group-hover:from-cyan-glow group-hover:via-violet-glow" />
            </Link>
          ))}
        </div>
      </div>
    </AppShell>
  );
}
