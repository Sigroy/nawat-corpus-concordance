import { ExternalLink } from "lucide-react";
import Link from "next/link";

import type { KwicHit } from "@/lib/types";

type KwicTableProps = {
  hits: KwicHit[];
  query: string;
  selectedHit?: string;
};

export function KwicTable({ hits, query, selectedHit }: KwicTableProps) {
  if (!query) {
    return (
      <div className="rounded-md border border-dashed border-line bg-bone p-8 text-center text-sm text-moss">
        Enter a Nawat form to search the approved corpus.
      </div>
    );
  }

  if (hits.length === 0) {
    return (
      <div className="rounded-md border border-line bg-bone p-8 text-center">
        <p className="font-semibold text-ink">No concordance lines found.</p>
        <p className="mt-1 text-sm text-moss">Try a variant spelling, contains match, or a broader source filter.</p>
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-md border border-line bg-bone shadow-soft">
      <div className="kwic-grid hidden border-b border-line bg-paper px-4 py-3 text-xs font-semibold uppercase text-moss md:grid">
        <span className="text-right">Left</span>
        <span className="text-center">Match</span>
        <span>Right</span>
        <span>Source</span>
      </div>
      <div className="divide-y divide-line">
        {hits.map((hit) => {
          const href = `/concordance?q=${encodeURIComponent(query)}&hit=${hit.token_id}`;
          const isSelected = selectedHit === String(hit.token_id);
          return (
            <Link
              key={hit.token_id}
              href={href}
              className={`kwic-grid grid gap-3 px-4 py-3 text-sm transition hover:bg-paper ${
                isSelected ? "bg-teal/10" : "bg-bone"
              }`}
            >
              <span className="text-left text-ink/80 md:text-right">{hit.left_context}</span>
              <span className="flex justify-start md:justify-center">
                <mark className="rounded-md bg-gold/20 px-2 py-1 font-semibold text-ink ring-1 ring-gold/30">
                  {hit.match}
                </mark>
              </span>
              <span className="text-ink/80">{hit.right_context}</span>
              <span className="flex min-w-0 items-center gap-2 text-moss">
                <ExternalLink className="h-4 w-4 shrink-0" aria-hidden="true" />
                <span className="truncate">
                  {hit.source_title}
                  {hit.page_number ? `, p. ${hit.page_number}` : ""}
                </span>
              </span>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
