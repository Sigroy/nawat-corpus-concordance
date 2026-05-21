export type Source = {
  id: number;
  slug: string;
  title: string;
  short_title: string;
  author: string;
  year: number | null;
  source_type: string;
  genre: string;
  citation: string;
  document_count: number;
  publication_info?: string;
  rights_notes?: string;
  permissions_url?: string;
  external_url?: string;
  editorial_notes?: string;
  documents?: DocumentSummary[];
};

export type DocumentSummary = {
  id: number;
  title: string;
  description: string;
  document_type: string;
  original_file_name: string;
  pages: PageSummary[];
};

export type PageSummary = {
  id: number;
  page_number: number;
  label: string;
  is_reviewed: boolean;
};

export type KwicHit = {
  token_id: number;
  left_context: string;
  match: string;
  right_context: string;
  sentence: string;
  citation: string;
  source_title: string;
  source_author: string;
  source_year: number | null;
  page_number: number | null;
};

export type ConcordanceResponse = {
  query: string;
  match_mode?: string;
  sort?: string;
  count: number;
  results: KwicHit[];
  detail?: string;
};

export type HitDetail = {
  hit: KwicHit;
  context: {
    id: number;
    text: string;
    paragraph_text: string;
    page_number: number | null;
    tokens: Array<{
      id: number;
      original: string;
      normalized: string;
      normalized_unaccented: string;
    }>;
  };
};

export type Entry = {
  id: number;
  headword: string;
  normalized_headword: string;
  part_of_speech: string;
  status: string;
  forms: Array<{
    id: number;
    form: string;
    kind: string;
    grammatical_description: string;
    source_title: string | null;
  }>;
};
