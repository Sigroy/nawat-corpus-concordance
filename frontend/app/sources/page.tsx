import { Library } from "lucide-react";

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

export default async function SourcesPage() {
  const sources = await loadSources();

  return (
    <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6">
      <div className="mb-6 flex items-center gap-3">
        <span className="flex h-10 w-10 items-center justify-center rounded-md bg-teal text-white">
          <Library className="h-5 w-5" aria-hidden="true" />
        </span>
        <div>
          <p className="text-sm font-semibold uppercase text-teal">Library</p>
          <h1 className="text-3xl font-semibold text-ink">Sources</h1>
        </div>
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {sources.map((source) => (
          <SourceCard key={source.id} source={source} />
        ))}
      </div>
    </main>
  );
}
