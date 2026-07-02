#!/usr/bin/env python3
"""Second targeted search + fetch known foundational papers by ID."""
import arxiv, json, sys, time

QUERIES = [
    "emergent misalignment narrow finetuning broadly misaligned",
    "universal transferable adversarial attacks aligned language models",
    "refusal single direction language model activation",
    "sleeper agents deceptive LLM safety training persist",
    "fine-tuning compromises safety alignment language model",
    "how does LLM safety training fail jailbroken",
    "model organisms misalignment interpretability",
    "quantifying alignment robustness threshold escalating attack",
    "safety guardrails robustness intervention intensity LLM",
    "activation steering induce behavior language model alignment",
]
KNOWN_IDS = [
    "2502.17424", "2412.14093", "2406.11717", "2307.15043", "2307.02483",
    "2310.03693", "2401.05566", "2311.03348", "2402.04249", "2404.01099",
    "2311.16119", "2308.03825", "2310.08419", "2310.06987", "2409.11445",
    "2408.02416", "2311.09096", "2306.03341", "2405.05610", "2312.06681",
]

seen = {}
client = arxiv.Client(page_size=50, delay_seconds=3, num_retries=3)
for q in QUERIES:
    try:
        for r in client.results(arxiv.Search(query=q, max_results=20,
                                sort_by=arxiv.SortCriterion.Relevance)):
            aid = r.get_short_id().split('v')[0]
            if aid in seen:
                seen[aid]['queries'].append(q); continue
            seen[aid] = {'arxiv_id': aid, 'title': r.title.strip().replace('\n',' '),
                'authors':[a.name for a in r.authors][:6], 'year': r.published.year,
                'published': r.published.isoformat(),
                'abstract': r.summary.strip().replace('\n',' '),
                'pdf_url': r.pdf_url, 'categories': r.categories, 'queries':[q]}
    except Exception as e:
        print(f"ERR '{q}': {e}", file=sys.stderr)
    time.sleep(1)

# fetch known IDs
try:
    for r in client.results(arxiv.Search(id_list=KNOWN_IDS)):
        aid = r.get_short_id().split('v')[0]
        if aid in seen: seen[aid]['queries'].append('KNOWN'); continue
        seen[aid] = {'arxiv_id': aid, 'title': r.title.strip().replace('\n',' '),
            'authors':[a.name for a in r.authors][:6], 'year': r.published.year,
            'published': r.published.isoformat(),
            'abstract': r.summary.strip().replace('\n',' '),
            'pdf_url': r.pdf_url, 'categories': r.categories, 'queries':['KNOWN']}
except Exception as e:
    print(f"ERR known ids: {e}", file=sys.stderr)

papers = list(seen.values())
papers.sort(key=lambda p:(len(p['queries']), p['year']), reverse=True)
with open('paper_search_results/arxiv_merged2.json','w') as f:
    json.dump(papers, f, indent=2)
print(f"TOTAL: {len(papers)}")
for p in papers:
    k = 'K' if 'KNOWN' in p['queries'] else ' '
    print(f"[{k}][{len(p['queries'])}q][{p['year']}] {p['arxiv_id']}  {p['title'][:80]}")
