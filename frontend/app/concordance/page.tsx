import { HitDetail } from "@/components/hit-detail";
import { KwicTable } from "@/components/kwic-table";
import { SearchPanel } from "@/components/search-panel";
import { getHitDetail, getSources, searchConcordance } from "@/lib/api";
import { fallbackConcordance, fallbackSources } from "@/lib/fallback";
import type { ConcordanceResponse, HitDetail as HitDetailType, Source } from "@/lib/types";

type PageProps = {
  searchParams: {
    q?: string;
    match?: string;
    sort?: string;
    source?: string;
    hit?: string;
  };
};

async function loadData(params: PageProps["searchParams"]): Promise<{
  sources: Source[];
  concordance: ConcordanceResponse;
  detail: HitDetailType | null;
  apiUnavailable: boolean;
}> {
  let apiUnavailable = false;
  let sources = fallbackSources;
  let concordance: ConcordanceResponse = params.q
    ? { ...fallbackConcordance, query: params.q }
    : { query: "", count: 0, results: [] };
  let detail: HitDetailType | null = null;

  try {
    sources = await getSources();
    concordance = await searchConcordance(params);
    if (params.hit) {
      detail = await getHitDetail(params.hit);
    }
  } catch {
    apiUnavailable = true;
  }

  return { sources, concordance, detail, apiUnavailable };
}

export default async function ConcordancePage({ searchParams }: PageProps) {
  const { sources, concordance, detail, apiUnavailable } = await loadData(searchParams);

  return (
    <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6">
      <div className="mb-6 flex flex-col justify-between gap-3 lg:flex-row lg:items-end">
        <div>
          <p className="text-sm font-semibold uppercase text-teal">KWIC Search</p>
          <h1 className="mt-1 text-3xl font-semibold text-ink">Concordance</h1>
        </div>
        <p className="text-sm text-moss">{concordance.count} result{concordance.count === 1 ? "" : "s"}</p>
      </div>

      <SearchPanel
        query={searchParams.q}
        match={searchParams.match}
        sort={searchParams.sort}
        source={searchParams.source}
        sources={sources}
      />

      {apiUnavailable ? (
        <div className="mt-4 rounded-md border border-gold/40 bg-gold/10 px-4 py-3 text-sm text-ink">
          Backend API is not reachable; showing local sample data.
        </div>
      ) : null}

      <section className="mt-6 grid gap-5 xl:grid-cols-[1fr_360px]">
        <KwicTable hits={concordance.results} query={concordance.query || searchParams.q || ""} selectedHit={searchParams.hit} />
        <HitDetail detail={detail} />
      </section>
    </main>
  );
}
