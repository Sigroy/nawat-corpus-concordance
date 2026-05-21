import { BookOpen, Database, FileSearch, Library } from "lucide-react";
import Link from "next/link";

import { SearchPanel } from "@/components/search-panel";
import { SourceCard } from "@/components/source-card";
import { getSources } from "@/lib/api";
import { fallbackSources } from "@/lib/fallback";

async function loadSources() {
  try {
    return await getSources();
  } catch {
    return fallbackSources;
  }
}

export default async function HomePage() {
  const sources = await loadSources();

  return (
    <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:py-10">
      <section className="grid gap-8 lg:grid-cols-[1.05fr_0.95fr] lg:items-start">
        <div>
          <div className="mb-5 inline-flex items-center gap-2 rounded-md border border-line bg-bone px-3 py-2 text-sm font-medium text-moss">
            <FileSearch className="h-4 w-4 text-teal" aria-hidden="true" />
            Concordance Nawat
          </div>
          <h1 className="max-w-3xl text-4xl font-semibold leading-tight text-ink sm:text-5xl">
            Search Nawat words in real textual context.
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-7 text-ink/70">
            KWIC concordance, source citations, and a lexicon-ready data model for Nawat language documentation.
          </p>
          <div className="mt-7">
            <SearchPanel sources={sources} />
          </div>
        </div>
        <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-1">
          <Metric icon={Database} label="Sources" value={String(sources.length)} />
          <Metric icon={Library} label="Corpus" value="Curated" />
          <Metric icon={BookOpen} label="Lexicon" value="Ready" />
        </div>
      </section>

      <section className="mt-10">
        <div className="mb-4 flex items-center justify-between gap-3">
          <h2 className="text-xl font-semibold text-ink">Source Library</h2>
          <Link href="/sources" className="rounded-md border border-line bg-bone px-3 py-2 text-sm font-semibold text-ink hover:border-teal">
            View all
          </Link>
        </div>
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {sources.slice(0, 3).map((source) => (
            <SourceCard key={source.id} source={source} />
          ))}
        </div>
      </section>
    </main>
  );
}

function Metric({ icon: Icon, label, value }: { icon: typeof Database; label: string; value: string }) {
  return (
    <div className="rounded-md border border-line bg-bone p-5 shadow-sm">
      <div className="flex items-center justify-between gap-3">
        <span className="text-sm font-semibold uppercase text-moss">{label}</span>
        <Icon className="h-5 w-5 text-teal" aria-hidden="true" />
      </div>
      <p className="mt-3 text-3xl font-semibold text-ink">{value}</p>
    </div>
  );
}
