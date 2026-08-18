# UnitRamp — Full Website Redesign

Production-oriented redesign of the UnitRamp website around the **PLAY ENGINEERING** concept.

## Goal

Preserve the scale and business logic of the current UnitRamp site while replacing the former one-page commercial presentation with a multi-page product experience for turnkey parks, catalogue discovery, projects, articles and contacts.

## Implemented routes

- `/` — corporate/product home
- `/katalog/` — catalogue with category filters, search and verified product cards
- `/projects/` — project archive with city/year search
- `/info/` — article archive
- `/contacts/` — verified contacts, legal details and project brief
- `/services/` — consulting, staff training and estimate review
- `/batutnyj-centr-pod-klyuch/`
- `/nindzya-park-pod-klyuch/`
- `/aktiviti-park-pod-klyuch/`
- `/ulichnye-batutnye-areny/`
- `/touch-arena-pod-klyuch/`
- `/skalodromy-pod-klyuch/`

## Content source

Facts, contacts, category counts, product names, project metrics and article titles are taken from the current public UnitRamp website. Unverified facts are not invented.

The source site currently states **670 catalogue products**. The redesign repository contains the recovered category taxonomy plus the verified product records collected during the migration pass. Legacy URLs not yet mirrored use a GitHub-preview fallback to the corresponding live `unitramp.ru` path instead of a dead 404.

## Stack

Static HTML + CSS + vanilla JavaScript, intentionally dependency-free for reliable GitHub Pages deployment.

## QA

The repository includes a CI quality workflow that checks JavaScript syntax, required routes, SEO files and basic content invariants.

## Local preview

```bash
python3 -m http.server 8080
```

## Deployment

Pushes to `main` are published to `gh-pages` by `.github/workflows/pages.yml`.
