import { createFileRoute } from "@tanstack/react-router";
import type { ReactNode } from "react";
import { AppShell, PageHeader, Panel, CornerBrackets } from "@/components/AppShell";

export const Route = createFileRoute("/portfolio")({
  head: () => ({
    meta: [
      { title: "Portfolio Notes — James AI Journal Club" },
      { name: "description", content: "Ship this prototype to GitHub and Streamlit — portfolio-ready notes and next upgrades." },
    ],
  }),
  component: Portfolio,
});

function Portfolio() {
  const steps: ReactNode[] = [
    "Create a new GitHub repository.",
    <>Upload <Code>app.py</Code>, <Code>requirements.txt</Code>, <Code>README.md</Code>, <Code>.streamlit/</Code>, <Code>data/</Code> and <Code>notebooks/</Code>.</>,
    "Commit the files.",
    <>Deploy on Streamlit Community Cloud by selecting the repo and setting <Code>app.py</Code> as the entry file.</>,
  ];

  return (
    <AppShell>
      <PageHeader
        eyebrow="// 05 · deploy.manifest"
        title="GitHub & Streamlit Portfolio Notes"
        description="Use this prototype as a portfolio-ready starting point. The manifest below hands you a clean shipping path."
      />

      <div className="grid gap-6 lg:grid-cols-2">
        <Panel className="p-6">
          <CornerBrackets />
          <div className="font-mono text-[10px] uppercase tracking-[0.3em] text-primary/80">
            manifest.repo
          </div>
          <h2 className="mt-2 font-display text-xl font-semibold text-foreground">
            Suggested repository name
          </h2>
          <div className="mt-4 flex items-center gap-3 rounded-md border border-primary/40 bg-primary/5 px-4 py-3 font-mono text-sm">
            <span className="text-primary">$</span>
            <span className="text-foreground">ai-journal-club-app</span>
          </div>

          <h3 className="mt-8 font-display text-lg font-semibold text-foreground">Local run command</h3>
          <pre className="mt-3 overflow-x-auto rounded-md border border-border/60 bg-[oklch(0.15_0.02_150)] p-4 font-mono text-[13px] leading-relaxed">
<span className="text-muted-foreground"># install dependencies</span>{"\n"}<span className="text-primary">pip</span> install -r requirements.txt{"\n"}<span className="text-muted-foreground"># launch the app</span>{"\n"}<span className="text-primary">streamlit</span> run app.py
          </pre>
        </Panel>

        <Panel className="p-6" glow="violet">
          <CornerBrackets />
          <div className="font-mono text-[10px] uppercase tracking-[0.3em] text-accent">
            deploy.sequence
          </div>
          <h2 className="mt-2 font-display text-xl font-semibold text-foreground">GitHub upload</h2>
          <ol className="mt-4 space-y-3">
            {steps.map((line, i) => (
              <li key={i} className="flex gap-3 rounded-md border border-border/60 bg-surface/40 p-3">
                <span className="font-mono text-xs font-medium text-primary">0{i + 1}</span>
                <span className="text-sm text-foreground/90">{line}</span>
              </li>
            ))}
          </ol>
        </Panel>
      </div>

      <Panel className="mt-6 p-6">
        <CornerBrackets />
        <div className="font-mono text-[10px] uppercase tracking-[0.3em] text-primary/80">
          upgrade.queue
        </div>
        <h2 className="mt-2 font-display text-xl font-semibold text-foreground">Next upgrades</h2>
        <div className="mt-5 grid gap-3 md:grid-cols-2">
          {[
            "Replace sample CSVs with real club videos and session links.",
            "Add account login and a database such as SQLite, Firebase, or Supabase.",
            "Add moderation tools for discussion posts.",
            "Add a real LLM or retrieval system only after adding privacy and safety controls.",
          ].map((line, i) => (
            <div key={i} className="flex items-start gap-3 rounded-md border border-border/60 bg-surface/40 p-4">
              <span className="mt-1 h-2 w-2 shrink-0 rounded-full bg-gradient-to-br from-cyan-glow to-violet-glow shadow-[0_0_8px_var(--cyan-glow)]" />
              <span className="text-sm text-foreground/90">{line}</span>
            </div>
          ))}
        </div>
      </Panel>
    </AppShell>
  );
}

function Code({ children }: { children: ReactNode }) {
  return (
    <code className="rounded-sm border border-primary/30 bg-primary/10 px-1.5 py-0.5 font-mono text-[12px] text-primary">
      {children}
    </code>
  );
}