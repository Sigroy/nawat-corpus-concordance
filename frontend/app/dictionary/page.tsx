import { BookOpen, Search } from "lucide-react";

import { searchDictionary } from "@/lib/api";
import { fallbackEntries } from "@/lib/fallback";

export default async function DictionaryPage({ searchParams }: { searchParams: { q?: string } }) {
  let entries = fallbackEntries;
  let apiUnavailable = false;
  try {
    entries = await searchDictionary(searchParams.q);
  } catch {
    apiUnavailable = true;
  }

  return (
    <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6">
      <div className="mb-6 flex items-center gap-3">
        <span className="flex h-10 w-10 items-center justify-center rounded-md bg-claret text-white">
          <BookOpen className="h-5 w-5" aria-hidden="true" />
        </span>
        <div>
          <p className="text-sm font-semibold uppercase text-claret">Lexicon</p>
          <h1 className="text-3xl font-semibold text-ink">Dictionary</h1>
        </div>
      </div>

      <form action="/dictionary" className="rounded-md border border-line bg-bone p-4 shadow-soft">
        <label className="block">
          <span className="mb-1 block text-xs font-semibold uppercase text-moss">Search entries</span>
          <span className="relative block">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-moss" />
            <input
              name="q"
              defaultValue={searchParams.q ?? ""}
              placeholder="lemma or spelling"
              className="h-11 w-full rounded-md border border-line bg-white pl-9 pr-3 text-base text-ink outline-none focus:border-teal focus:ring-2 focus:ring-teal/15"
            />
          </span>
        </label>
      </form>

      {apiUnavailable ? (
        <div className="mt-4 rounded-md border border-gold/40 bg-gold/10 px-4 py-3 text-sm text-ink">
          Backend API is not reachable; showing local sample data.
        </div>
      ) : null}

      <div className="mt-6 grid gap-4">
        {entries.map((entry) => (
          <article key={entry.id} className="rounded-md border border-line bg-bone p-5 shadow-sm">
            <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <h2 className="text-2xl font-semibold text-ink">{entry.headword}</h2>
                <p className="mt-1 text-sm text-moss">
                  {entry.part_of_speech || "part of speech pending"} · {entry.status}
                </p>
              </div>
              <span className="rounded-md border border-line bg-paper px-2 py-1 text-xs font-semibold text-moss">
                {entry.forms.length} form{entry.forms.length === 1 ? "" : "s"}
              </span>
            </div>
            <div className="mt-4 flex flex-wrap gap-2">
              {entry.forms.map((form) => (
                <span key={form.id} className="rounded-md border border-line bg-white px-2 py-1 text-sm text-ink">
                  {form.form}
                </span>
              ))}
            </div>
          </article>
        ))}
      </div>
    </main>
  );
}
