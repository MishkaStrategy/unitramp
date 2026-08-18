# UnitRamp — Full Website Redesign

Production-oriented redesign of the UnitRamp website around the **PLAY ENGINEERING** concept.

## Goal

Preserve the scale and business logic of the current UnitRamp site while replacing the former one-page commercial presentation with a multi-page product experience for turnkey parks, catalogue discovery, projects, articles, franchises, reviews and contacts.

## Implemented routes

- `/` — corporate/product home
- `/katalog/` — synchronized catalogue with category filters, search, sorting and load-more
- 29 original catalogue category/subcategory routes generated during deploy
- original product paths generated from the current public catalogue snapshot
- `/projects/` — project archive with city/year search
- `/info/` — article archive
- `/contacts/` — verified contacts, legal details and project brief with required privacy consent
- `/services/` — consulting, staff training and estimate review
- `/franchises/` — source-backed franchise overview
- `/reviews/` — source-backed customer review index
- `/batutnyj-centr-pod-klyuch/`
- `/nindzya-park-pod-klyuch/`
- `/aktiviti-park-pod-klyuch/`
- `/ulichnye-batutnye-areny/`
- `/touch-arena-pod-klyuch/`
- `/skalodromy-pod-klyuch/`

## Catalogue reconciliation

The public UnitRamp catalogue currently advertises **670 products**. The automated source crawl on 2026-08-18 recovered **659 unique publicly linked product URLs across 29 category/subcategory pages with zero fetch failures**.

That difference is retained explicitly instead of inventing 11 SKUs. Some live category counters are internally inconsistent with their currently rendered product grids (for example, the current mats page renders fewer items than an older counter). The deploy therefore treats the current accessible product URLs as the authoritative snapshot while continuing to show the source-declared 670 count as a separate figure.

`./scripts/crawl_unitramp.py` rebuilds the source-backed product dataset. `./scripts/generate_category_pages.py` preserves the current catalogue category routes. GitHub Actions requires at least 650 accessible product records before publication.

## Content source

Facts, contacts, category data, product names, project metrics, franchise data, review authors and article titles are taken from the current public UnitRamp website. Unverified facts and testimonials are not invented.

Legacy URLs not yet mirrored use a GitHub-preview fallback to the corresponding live `unitramp.ru` path instead of a dead 404.

## Stack

Static HTML + CSS + vanilla JavaScript for the client experience, plus Python build-time synchronization for the catalogue. The browser runtime stays dependency-light; requests/BeautifulSoup are used only in CI/deploy.

## QA

CI checks:

- JavaScript syntax;
- required routes and SEO files;
- source-backed catalogue crawl (`>=650` accessible records);
- preserved category pages;
- explicit privacy consent on the lead form;
- placeholder-content regression checks.

## Local preview

```bash
python3 -m http.server 8080
```

To refresh the catalogue locally:

```bash
python3 -m pip install requests beautifulsoup4
python3 scripts/crawl_unitramp.py --output generated-catalog.js --report data/catalog-report.json --generate-pages --min-count 650
python3 scripts/generate_category_pages.py
```

## Deployment

Pushes to `main` trigger `.github/workflows/pages.yml`. The workflow refreshes the catalogue, generates original product/category paths, commits the generated snapshot inside the runner and force-publishes that snapshot to `gh-pages`.
