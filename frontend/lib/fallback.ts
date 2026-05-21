import type { ConcordanceResponse, Entry, Source } from "./types";

export const fallbackSources: Source[] = [
  {
    id: 1,
    slug: "king-schultze-2012-sample",
    title: "Tajtaketza Pal Ijtzalku",
    short_title: "Tajtaketza Pal Ijtzalku",
    author: "Alan R. King / Leonhard Schultze Jena",
    year: 2012,
    source_type: "story",
    genre: "oral narrative",
    citation: "King, Alan R. 2012. Tajtaketza Pal Ijtzalku.",
    document_count: 1
  }
];

export const fallbackConcordance: ConcordanceResponse = {
  query: "nawat",
  count: 1,
  results: [
    {
      token_id: 1,
      left_context: "Ashkan ajwituk ne tal",
      match: "Nawat",
      right_context: "nemi nikan",
      sentence: "Ashkan ajwituk ne tal. Nawat nemi nikan.",
      citation: "King, Alan R. 2012. Tajtaketza Pal Ijtzalku, p. 17",
      source_title: "Tajtaketza Pal Ijtzalku",
      source_author: "Alan R. King / Leonhard Schultze Jena",
      source_year: 2012,
      page_number: 17
    }
  ]
};

export const fallbackEntries: Entry[] = [
  {
    id: 1,
    headword: "nawat",
    normalized_headword: "nawat",
    part_of_speech: "",
    status: "attested",
    forms: [
      {
        id: 1,
        form: "náhuat",
        kind: "variant",
        grammatical_description: "",
        source_title: "Legacy lexicon data"
      }
    ]
  }
];
