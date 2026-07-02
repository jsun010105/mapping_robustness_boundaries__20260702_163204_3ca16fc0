#!/usr/bin/env python3
"""Manual paper search via arXiv + Semantic Scholar. Dedupes, ranks, prints JSON."""
import arxiv, json, sys, time, re

QUERIES = [
    "adversarial robustness large language model alignment",
    "jailbreak large language models defense robustness",
    "red teaming language models safety",
    "RLHF alignment robustness adversarial attacks",
    "measuring evaluating alignment robustness LLM",
    "adversarial prompting safety refusal language model",
    "emergent misalignment fine-tuning language model",
    "safety training generalization robustness LLM",
    "alignment faking language models",
    "prompt injection robustness LLM",
]

seen = {}
client = arxiv.Client(page_size=50, delay_seconds=3, num_retries=3)
for q in QUERIES:
    try:
        search = arxiv.Search(query=q, max_results=25,
                              sort_by=arxiv.SortCriterion.Relevance)
        for r in client.results(search):
            aid = r.get_short_id().split('v')[0]
            if aid in seen:
                seen[aid]['queries'].append(q)
                continue
            seen[aid] = {
                'arxiv_id': aid,
                'title': r.title.strip().replace('\n', ' '),
                'authors': [a.name for a in r.authors][:6],
                'year': r.published.year,
                'published': r.published.isoformat(),
                'abstract': r.summary.strip().replace('\n', ' '),
                'pdf_url': r.pdf_url,
                'categories': r.categories,
                'queries': [q],
            }
    except Exception as e:
        print(f"ERR query '{q}': {e}", file=sys.stderr)
    time.sleep(1)

papers = list(seen.values())
papers.sort(key=lambda p: (len(p['queries']), p['year']), reverse=True)
with open('paper_search_results/arxiv_merged.json', 'w') as f:
    json.dump(papers, f, indent=2)
print(f"TOTAL unique papers: {len(papers)}")
for p in papers:
    print(f"[{len(p['queries'])}q][{p['year']}] {p['arxiv_id']}  {p['title'][:85]}")
