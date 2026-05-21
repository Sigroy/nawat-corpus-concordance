import { Search } from "lucide-react";

type SourceOption = {
  id: number;
  title: string;
  author: string;
  year: number | null;
};

type SearchPanelProps = {
  query?: string;
  match?: string;
  sort?: string;
  source?: string;
  sources?: SourceOption[];
  compact?: boolean;
};

export function SearchPanel({ query = "", match = "exact", sort = "source", source = "", sources = [], compact }: SearchPanelProps) {
  return (
    <form action="/concordance" className="rounded-md border border-line bg-bone p-4 shadow-soft sm:p-5">
      <div className="grid gap-3 lg:grid-cols-[1fr_auto_auto_auto]">
        <label className="block">
          <span className="mb-1 block text-xs font-semibold uppercase text-moss">Search corpus</span>
          <span className="relative block">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-moss" />
            <input
              name="q"
              defaultValue={query}
              placeholder="nawat, tajtaketza, ne..."
              className="h-11 w-full rounded-md border border-line bg-white pl-9 pr-3 text-base text-ink outline-none focus:border-teal focus:ring-2 focus:ring-teal/15"
            />
          </span>
        </label>
        <label className="block">
          <span className="mb-1 block text-xs font-semibold uppercase text-moss">Match</span>
          <select
            name="match"
            defaultValue={match}
            className="h-11 w-full rounded-md border border-line bg-white px-3 text-sm text-ink outline-none focus:border-teal focus:ring-2 focus:ring-teal/15"
          >
            <option value="exact">Exact</option>
            <option value="contains">Contains</option>
            <option value="prefix">Prefix</option>
            <option value="suffix">Suffix</option>
          </select>
        </label>
        <label className="block">
          <span className="mb-1 block text-xs font-semibold uppercase text-moss">Sort</span>
          <select
            name="sort"
            defaultValue={sort}
            className="h-11 w-full rounded-md border border-line bg-white px-3 text-sm text-ink outline-none focus:border-teal focus:ring-2 focus:ring-teal/15"
          >
            <option value="source">Source</option>
            <option value="left">Left context</option>
            <option value="right">Right context</option>
            <option value="year">Year</option>
          </select>
        </label>
        <button className="mt-5 inline-flex h-11 items-center justify-center rounded-md bg-teal px-5 text-sm font-semibold text-white shadow-sm hover:bg-ink">
          Search
        </button>
      </div>
      {!compact && sources.length > 0 ? (
        <label className="mt-3 block">
          <span className="mb-1 block text-xs font-semibold uppercase text-moss">Source filter</span>
          <select
            name="source"
            defaultValue={source}
            className="h-11 w-full rounded-md border border-line bg-white px-3 text-sm text-ink outline-none focus:border-teal focus:ring-2 focus:ring-teal/15"
          >
            <option value="">All sources</option>
            {sources.map((item) => (
              <option key={item.id} value={item.id}>
                {item.author ? `${item.author} - ` : ""}
                {item.title}
                {item.year ? ` (${item.year})` : ""}
              </option>
            ))}
          </select>
        </label>
      ) : null}
    </form>
  );
}
