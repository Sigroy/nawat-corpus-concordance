import type { ConcordanceResponse, Entry, HitDetail, Source } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    next: { revalidate: 5 }
  });
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status} ${response.statusText}`);
  }
  return response.json() as Promise<T>;
}

export async function searchConcordance(params: {
  q?: string;
  match?: string;
  sort?: string;
  source?: string;
}): Promise<ConcordanceResponse> {
  const search = new URLSearchParams();
  if (params.q) search.set("q", params.q);
  if (params.match) search.set("match", params.match);
  if (params.sort) search.set("sort", params.sort);
  if (params.source) search.set("source", params.source);
  const suffix = search.toString() ? `?${search}` : "";
  return getJson<ConcordanceResponse>(`/search/concordance${suffix}`);
}

export async function getHitDetail(tokenId: string): Promise<HitDetail> {
  return getJson<HitDetail>(`/concordance/${tokenId}`);
}

export async function getSources(): Promise<Source[]> {
  return getJson<Source[]>("/sources");
}

export async function getSource(id: string): Promise<Source> {
  return getJson<Source>(`/sources/${id}`);
}

export async function searchDictionary(q?: string): Promise<Entry[]> {
  const suffix = q ? `?q=${encodeURIComponent(q)}` : "";
  return getJson<Entry[]>(`/dictionary/search${suffix}`);
}
