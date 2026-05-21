import { Archive, CalendarDays } from "lucide-react";
import Link from "next/link";

import type { Source } from "@/lib/types";

export function SourceCard({ source }: { source: Source }) {
  return (
    <Link href={`/sources/${source.id}`} className="block rounded-md border border-line bg-bone p-5 shadow-sm hover:border-teal">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <h2 className="truncate text-lg font-semibold text-ink">{source.title}</h2>
          <p className="mt-1 text-sm text-moss">{source.author || "Unknown author"}</p>
        </div>
        <span className="rounded-md border border-line bg-paper px-2 py-1 text-xs font-semibold text-moss">
          {source.source_type}
        </span>
      </div>
      <div className="mt-4 flex flex-wrap gap-3 text-sm text-moss">
        <span className="inline-flex items-center gap-1">
          <CalendarDays className="h-4 w-4" aria-hidden="true" />
          {source.year ?? "n.d."}
        </span>
        <span className="inline-flex items-center gap-1">
          <Archive className="h-4 w-4" aria-hidden="true" />
          {source.document_count} document{source.document_count === 1 ? "" : "s"}
        </span>
      </div>
      {source.citation ? <p className="mt-4 line-clamp-2 text-sm leading-6 text-ink/75">{source.citation}</p> : null}
    </Link>
  );
}
