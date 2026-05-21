import { BookMarked, FileText } from "lucide-react";

import type { HitDetail } from "@/lib/types";

type HitDetailProps = {
  detail?: HitDetail | null;
};

export function HitDetail({ detail }: HitDetailProps) {
  if (!detail) {
    return (
      <aside className="rounded-md border border-line bg-bone p-5 text-sm text-moss">
        Select a concordance line to inspect the sentence and paragraph context.
      </aside>
    );
  }

  return (
    <aside className="rounded-md border border-line bg-bone p-5 shadow-soft">
      <div className="mb-4 flex items-start gap-3">
        <span className="mt-1 flex h-9 w-9 items-center justify-center rounded-md bg-claret text-white">
          <BookMarked className="h-4 w-4" aria-hidden="true" />
        </span>
        <div className="min-w-0">
          <h2 className="text-base font-semibold text-ink">Context</h2>
          <p className="mt-1 text-sm text-moss">{detail.hit.citation}</p>
        </div>
      </div>
      <div className="rounded-md border border-line bg-white p-4">
        <div className="mb-2 flex items-center gap-2 text-xs font-semibold uppercase text-moss">
          <FileText className="h-4 w-4" aria-hidden="true" />
          Sentence
        </div>
        <p className="text-base leading-7 text-ink">{detail.context.text}</p>
      </div>
      <div className="mt-4">
        <h3 className="text-xs font-semibold uppercase text-moss">Paragraph</h3>
        <p className="mt-2 max-h-72 overflow-auto rounded-md border border-line bg-paper p-4 text-sm leading-6 text-ink/85">
          {detail.context.paragraph_text}
        </p>
      </div>
      <div className="mt-4 flex flex-wrap gap-2">
        {detail.context.tokens.map((token) => (
          <span
            key={token.id}
            className={`rounded-md border px-2 py-1 text-xs ${
              token.id === detail.hit.token_id
                ? "border-gold bg-gold/20 font-semibold text-ink"
                : "border-line bg-white text-moss"
            }`}
          >
            {token.original}
          </span>
        ))}
      </div>
    </aside>
  );
}
