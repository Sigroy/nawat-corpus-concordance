import { ArrowLeft, ExternalLink, FileText } from "lucide-react";
import Link from "next/link";
import { notFound } from "next/navigation";

import { getSource } from "@/lib/api";
import { fallbackSources } from "@/lib/fallback";
import type { Source } from "@/lib/types";

async function loadSource(id: string): Promise<Source | null> {
  try {
    return await getSource(id);
  } catch {
    return fallbackSources.find((source) => String(source.id) === id) ?? null;
  }
}

export default async function SourceDetailPage({ params }: { params: { id: string } }) {
  const source = await loadSource(params.id);
  if (!source) {
    notFound();
  }

  return (
    <main className="mx-auto max-w-5xl px-4 py-8 sm:px-6">
      <Link href="/sources" className="mb-5 inline-flex items-center gap-2 text-sm font-semibold text-moss hover:text-teal">
        <ArrowLeft className="h-4 w-4" aria-hidden="true" />
        Sources
      </Link>
      <section className="rounded-md border border-line bg-bone p-6 shadow-soft">
        <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase text-teal">{source.source_type}</p>
            <h1 className="mt-1 text-3xl font-semibold text-ink">{source.title}</h1>
            <p className="mt-2 text-base text-moss">
              {source.author || "Unknown author"}
              {source.year ? `, ${source.year}` : ""}
            </p>
          </div>
          {source.external_url ? (
            <a
              href={source.external_url}
              className="inline-flex items-center gap-2 rounded-md border border-line px-3 py-2 text-sm font-semibold text-ink hover:border-teal"
            >
              <ExternalLink className="h-4 w-4" aria-hidden="true" />
              Open
            </a>
          ) : null}
        </div>

        <dl className="mt-6 grid gap-4 md:grid-cols-2">
          <Info label="Genre" value={source.genre || "Unspecified"} />
          <Info label="Documents" value={String(source.document_count)} />
          <Info label="Publication" value={source.publication_info || "Unspecified"} />
          <Info label="Rights" value={source.rights_notes || "Unspecified"} />
        </dl>

        {source.citation ? (
          <div className="mt-6 rounded-md border border-line bg-paper p-4">
            <h2 className="text-sm font-semibold uppercase text-moss">Citation</h2>
            <p className="mt-2 text-sm leading-6 text-ink">{source.citation}</p>
          </div>
        ) : null}
      </section>

      <section className="mt-6">
        <h2 className="mb-3 text-xl font-semibold text-ink">Documents</h2>
        <div className="grid gap-3">
          {(source.documents ?? []).map((document) => (
            <div key={document.id} className="rounded-md border border-line bg-bone p-4">
              <div className="flex items-center gap-3">
                <FileText className="h-5 w-5 text-teal" aria-hidden="true" />
                <div>
                  <h3 className="font-semibold text-ink">{document.title}</h3>
                  <p className="text-sm text-moss">
                    {document.document_type} · {document.pages.length} page{document.pages.length === 1 ? "" : "s"}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}

function Info({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-xs font-semibold uppercase text-moss">{label}</dt>
      <dd className="mt-1 text-sm leading-6 text-ink">{value}</dd>
    </div>
  );
}
