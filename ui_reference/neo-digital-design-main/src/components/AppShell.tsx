import { Link, useRouterState } from "@tanstack/react-router";
import { navItems } from "@/lib/club-data";
import type { ReactNode } from "react";

export function AppShell({ children }: { children: ReactNode }) {
  const pathname = useRouterState({ select: (s) => s.location.pathname });

  return (
    <div className="relative min-h-screen w-full overflow-x-hidden">
      {/* Ambient grid */}
      <div className="pointer-events-none fixed inset-0 holo-grid opacity-40" />
      {/* Scanline */}
      <div className="pointer-events-none fixed inset-x-0 top-0 h-32 animate-scanline">
        <div className="h-px w-full bg-gradient-to-r from-transparent via-cyan-glow/60 to-transparent blur-[1px]" />
      </div>

      <div className="relative flex min-h-screen w-full">
        {/* Sidebar */}
        <aside className="sticky top-0 hidden h-screen w-72 shrink-0 border-r border-border/60 bg-sidebar/70 backdrop-blur-xl md:flex md:flex-col">
          <div className="px-6 pt-8">
            <div className="flex items-center gap-3">
              <BrandMark />
              <div className="min-w-0">
                <div className="font-mono text-[10px] uppercase tracking-[0.28em] text-primary/80">
                  Node · JAJC-001
                </div>
                <div className="truncate font-display text-lg font-semibold text-holo">
                  James AI Journal Club
                </div>
              </div>
            </div>
          </div>

          <nav className="mt-10 flex-1 space-y-1 px-3">
            <div className="px-3 pb-2 font-mono text-[10px] uppercase tracking-[0.3em] text-muted-foreground">
              // Explore
            </div>
            {navItems.map((item) => {
              const active = pathname === item.to;
              return (
                <Link
                  key={item.to}
                  to={item.to}
                  className={`group relative flex items-center gap-3 rounded-md px-3 py-2.5 text-sm transition-all ${
                    active
                      ? "bg-surface-2/80 text-foreground"
                      : "text-muted-foreground hover:bg-surface/60 hover:text-foreground"
                  }`}
                >
                  <span
                    className={`absolute left-0 top-1/2 h-6 w-[2px] -translate-y-1/2 rounded-full transition-all ${
                      active
                        ? "bg-gradient-to-b from-cyan-glow to-violet-glow shadow-[0_0_12px_var(--cyan-glow)]"
                        : "bg-transparent"
                    }`}
                  />
                  <span className="font-mono text-[10px] text-primary/60">{item.code}</span>
                  <span className={active ? "font-medium tracking-wide" : "tracking-wide"}>
                    {item.label}
                  </span>
                  {active && (
                    <span className="ml-auto h-1.5 w-1.5 rounded-full bg-cyan-glow shadow-[0_0_10px_var(--cyan-glow)] animate-pulse-glow" />
                  )}
                </Link>
              );
            })}
          </nav>

          <div className="px-6 pb-8">
            <div className="rounded-md border border-border/60 bg-surface/40 p-4">
              <div className="font-mono text-[10px] uppercase tracking-[0.28em] text-primary/70">
                Status
              </div>
              <div className="mt-2 flex items-center gap-2 text-xs text-muted-foreground">
                <span className="h-1.5 w-1.5 rounded-full bg-cyan-glow shadow-[0_0_8px_var(--cyan-glow)]" />
                Prototype for a high-school AI journal club.
              </div>
            </div>
          </div>
        </aside>

        {/* Main */}
        <main className="relative flex-1 min-w-0">
          <header className="sticky top-0 z-20 flex items-center justify-between border-b border-border/50 bg-background/60 px-6 py-4 backdrop-blur-xl md:px-10">
            <div className="flex items-center gap-3 md:hidden">
              <BrandMark />
              <div className="font-display text-sm font-semibold text-holo">JAJC</div>
            </div>
            <div className="hidden items-center gap-3 md:flex">
              <span className="font-mono text-[10px] uppercase tracking-[0.3em] text-muted-foreground">
                {pathname === "/" ? "// system.overview" : `// ${pathname.slice(1)}`}
              </span>
              <span className="h-1 w-1 rounded-full bg-primary/60" />
              <span className="font-mono text-[10px] uppercase tracking-[0.3em] text-primary/80">
                v2026.07
              </span>
            </div>
            <button className="group relative rounded-md border border-primary/40 bg-primary/10 px-4 py-1.5 font-mono text-[11px] uppercase tracking-[0.28em] text-primary transition-all hover:bg-primary/20 hover:glow-cyan">
              Fork
            </button>
          </header>

          <div className="mx-auto max-w-6xl px-6 py-10 md:px-10 md:py-14">{children}</div>
        </main>
      </div>
    </div>
  );
}

function BrandMark() {
  return (
    <div className="relative grid h-10 w-10 shrink-0 place-items-center rounded-md border border-primary/40 bg-gradient-to-br from-primary/25 to-accent/25">
      <div className="absolute inset-0 rounded-md animate-pulse-glow shadow-[inset_0_0_20px_var(--cyan-glow)]" />
      <svg viewBox="0 0 24 24" className="relative h-5 w-5 text-primary" fill="none" stroke="currentColor" strokeWidth="1.6">
        <circle cx="12" cy="12" r="3" />
        <circle cx="12" cy="12" r="8" strokeOpacity="0.5" />
        <path d="M12 4v3M12 17v3M4 12h3M17 12h3" strokeLinecap="round" />
      </svg>
    </div>
  );
}

export function PageHeader({
  eyebrow,
  title,
  description,
}: {
  eyebrow: string;
  title: string;
  description?: string;
}) {
  return (
    <div className="relative mb-10">
      <div className="font-mono text-[11px] uppercase tracking-[0.32em] text-primary/80">
        {eyebrow}
      </div>
      <h1 className="mt-3 font-display text-4xl font-bold leading-tight text-holo md:text-6xl">
        {title}
      </h1>
      {description && (
        <p className="mt-4 max-w-3xl text-base leading-relaxed text-muted-foreground md:text-lg">
          {description}
        </p>
      )}
      <div className="mt-6 h-px w-full bg-gradient-to-r from-cyan-glow/60 via-violet-glow/40 to-transparent" />
    </div>
  );
}

export function Panel({
  children,
  className = "",
  glow = "cyan",
}: {
  children: ReactNode;
  className?: string;
  glow?: "cyan" | "violet" | "none";
}) {
  return (
    <div className={`relative rounded-lg holo-panel ${className}`}>
      {glow !== "none" && (
        <div
          className={`pointer-events-none absolute -inset-px rounded-lg opacity-0 transition-opacity duration-500 ${
            glow === "cyan"
              ? "bg-[radial-gradient(400px_circle_at_var(--x,50%)_var(--y,0%),oklch(0.70_0.22_150/0.18),transparent_60%)]"
              : "bg-[radial-gradient(400px_circle_at_var(--x,50%)_var(--y,0%),oklch(0.55_0.18_160/0.18),transparent_60%)]"
          }`}
        />
      )}
      {children}
    </div>
  );
}

export function CornerBrackets() {
  return (
    <>
      <span className="pointer-events-none absolute -left-px -top-px h-3 w-3 border-l border-t border-primary/70" />
      <span className="pointer-events-none absolute -right-px -top-px h-3 w-3 border-r border-t border-primary/70" />
      <span className="pointer-events-none absolute -bottom-px -left-px h-3 w-3 border-b border-l border-accent/70" />
      <span className="pointer-events-none absolute -bottom-px -right-px h-3 w-3 border-b border-r border-accent/70" />
    </>
  );
}