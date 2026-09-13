import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { AppShell, PageHeader, Panel, CornerBrackets } from "@/components/AppShell";
import { brainTopics, feedbackWeights, members } from "@/lib/club-data";

export const Route = createFileRoute("/brain")({
  head: () => ({
    meta: [
      { title: "AI Brain Lab — James AI Journal Club" },
      { name: "description", content: "Turn advanced AI ideas into high-school explanations, and inspect the AI brain's live feedback weights." },
    ],
  }),
  component: Brain,
});

function Brain() {
  const topicKeys = Object.keys(brainTopics);
  const [topic, setTopic] = useState(topicKeys[0]);
  const [ctx, setCtx] = useState("");
  const [explanation, setExplanation] = useState<string | null>(null);
  const [memberId, setMemberId] = useState(members[0].id);

  const explain = () => {
    const base = brainTopics[topic];
    setExplanation(
      ctx.trim()
        ? `${base}\n\n// tailored: since you mentioned "${ctx.trim()}", imagine ${topic.toLowerCase()} applied right there — same idea, just fitted to your context.`
        : base,
    );
  };

  const maxW = useMemo(() => Math.max(...feedbackWeights.map((f) => f.weight)), []);

  return (
    <AppShell>
      <PageHeader
        eyebrow="// 04 · brain.lab"
        title="AI Brain Lab"
        description="Inspect the three-layer AI brain that powers JAJC. Translate advanced ideas into plain language and watch its feedback weights shift in real time."
      />

      <div className="grid gap-6 lg:grid-cols-2">
        <Panel className="p-6">
          <CornerBrackets />
          <div className="font-mono text-[10px] uppercase tracking-[0.3em] text-primary/80">
            explain.it_simply()
          </div>
          <h2 className="mt-2 font-display text-2xl font-semibold text-foreground">
            Frontier topic → high-school clarity
          </h2>

          <label className="mt-6 block font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
            Choose a topic
          </label>
          <select
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            className="mt-2 w-full rounded-md border border-border bg-input px-4 py-3 font-mono text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/40"
          >
            {topicKeys.map((t) => (
              <option key={t} value={t} className="bg-background">
                {t}
              </option>
            ))}
          </select>

          <label className="mt-4 block font-mono text-[10px] uppercase tracking-widest text-muted-foreground">
            Optional learner context
          </label>
          <textarea
            value={ctx}
            onChange={(e) => setCtx(e.target.value)}
            placeholder="Example: I like biology, robotics, or science fair projects."
            className="mt-2 min-h-24 w-full rounded-md border border-border bg-input px-4 py-3 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/40"
          />

          <button
            onClick={explain}
            className="mt-4 inline-flex items-center gap-2 rounded-md border border-primary/50 bg-primary/10 px-4 py-2.5 font-mono text-[11px] uppercase tracking-[0.28em] text-primary transition hover:bg-primary/20 hover:glow-cyan"
          >
            ▶ Explain it simply
          </button>

          {explanation && (
            <div className="mt-5 rounded-md border border-accent/40 bg-accent/5 p-4">
              <div className="font-mono text-[10px] uppercase tracking-[0.28em] text-accent">
                output stream
              </div>
              <p className="mt-2 whitespace-pre-line text-sm leading-relaxed text-foreground/90">
                {explanation}
              </p>
            </div>
          )}
        </Panel>

        <div className="space-y-6">
          <Panel className="p-6" glow="violet">
            <CornerBrackets />
            <h2 className="font-display text-2xl font-semibold text-foreground">Three AI layers</h2>
            <div className="mt-5 space-y-3">
              {[
                { n: "01", t: "Supervised ML", d: "Learns from surveys, watch history and likes to predict useful videos." },
                { n: "02", t: "Deep neural concept layer", d: "Represents advanced AI topics as patterns that can be simplified with analogies." },
                { n: "03", t: "Reinforcement learning", d: "Updates topic weights when students like, skip, or subscribe." },
              ].map((l) => (
                <div key={l.n} className="rounded-md border border-border/60 bg-surface/50 p-4">
                  <div className="flex items-center gap-3">
                    <span className="font-mono text-[10px] uppercase tracking-widest text-primary">{l.n}</span>
                    <span className="font-display text-sm font-semibold text-foreground">{l.t}</span>
                  </div>
                  <p className="mt-1.5 text-xs leading-relaxed text-muted-foreground">{l.d}</p>
                </div>
              ))}
            </div>
          </Panel>

          <Panel className="p-6">
            <CornerBrackets />
            <div className="flex flex-wrap items-center justify-between gap-4">
              <h2 className="font-display text-xl font-semibold text-foreground">
                Current feedback weights
              </h2>
              <select
                value={memberId}
                onChange={(e) => setMemberId(e.target.value)}
                className="rounded-md border border-border bg-input px-3 py-1.5 font-mono text-xs outline-none focus:border-primary"
              >
                {members.map((m) => (
                  <option key={m.id} value={m.id} className="bg-background">
                    {m.id}
                  </option>
                ))}
              </select>
            </div>

            <div className="mt-5 space-y-3">
              {feedbackWeights.map((f) => (
                <div key={f.topic}>
                  <div className="mb-1 flex justify-between font-mono text-[10px] uppercase tracking-widest">
                    <span className="text-foreground">{f.topic}</span>
                    <span className="text-primary">{f.weight.toFixed(2)}</span>
                  </div>
                  <div className="h-1.5 w-full overflow-hidden rounded-full bg-surface">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-cyan-glow to-violet-glow"
                      style={{ width: `${(f.weight / maxW) * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </Panel>
        </div>
      </div>

      <Panel className="mt-8 p-6">
        <CornerBrackets />
        <h2 className="font-display text-2xl font-semibold text-foreground">Responsible AI checklist</h2>
        <div className="mt-5 grid gap-3 md:grid-cols-2">
          {[
            "Show why each recommendation was made.",
            "Let students control their interests and delete feedback.",
            "Use human review before publishing official learning content.",
            "Avoid collecting sensitive personal data from minors.",
          ].map((line, i) => (
            <div key={i} className="flex items-start gap-3 rounded-md border border-border/60 bg-surface/40 p-4">
              <span className="mt-0.5 grid h-5 w-5 shrink-0 place-items-center rounded border border-primary bg-primary/20 text-primary glow-cyan">
                <svg viewBox="0 0 24 24" className="h-3 w-3" fill="none" stroke="currentColor" strokeWidth="3">
                  <path d="M4 12l5 5L20 6" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </span>
              <span className="text-sm text-foreground/90">{line}</span>
            </div>
          ))}
        </div>
      </Panel>
    </AppShell>
  );
}