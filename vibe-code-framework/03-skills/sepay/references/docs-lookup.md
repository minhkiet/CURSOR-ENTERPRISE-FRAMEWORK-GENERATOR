# Docs lookup, beyond the cheap path in SKILL.md

Docs map line `/vi/<section>/<slug>#<anchor> "<Heading>"` maps to: MCP page id `<section>/<slug>`, markdown URL `https://developer.sepay.vn/vi/<section>/<slug>.md`, and `sed` on the heading.

## SePay MCP tools, only if the session already has them

Never install or configure MCP yourself, and never ask for it just to read docs.

- `search_docs` exists → use it, then read only the hit's section.
- Else `list_docs` with `section` set (skip the call without it) → `fetch_content` with the page id. It returns a whole page: prefer the `curl | sed` path when you only need one section.
- Account data tools (`list_transactions`, `get_transaction`, `list_bank_accounts`, `list_virtual_accounts`, `list_webhooks`, `list_webhook_logs`, `get_webhook_report`) answer questions about the user's real data. Use them instead of guessing.
- User needs real account data and has no SePay MCP: suggest connecting it once, as in `SKILL.md` › Tools worth suggesting.

## Keep reads small

- Code samples come in up to 8 languages; keep only the user's (plus JSON) with this filter after the `sed` (halves long sections):

  ```bash
  … | awk -v L=php '/^[ \t]*```/{if(b){b=0;if(k)print;next}b=1;l=$0;sub(/^[ \t]*```/,"",l);k=(l==L||l=="json"||l=="");if(k)print;next} !b||k'
  ```
  `L` = `php`, `javascript`, `python`, `java`, `go`, `bash`…
- Section with `###` subsections: list them (`grep '^###'`), read one (`sed -n '/^### <Sub>/,/^##/p'`).
- Long pages (read one step only): `einvoice-api/v1/bat-dau-nhanh`, `einvoice-api/v1/xuat-hoa-don-dien-tu`, `speaker-api/bat-dau-nhanh`, `bankhub/thong-tin-sandbox`, `sepay-api/v2/don-hang/bat-dau-nhanh`.
- Headings of a page: `curl -sL <url>.md | grep '^##'`.
- Last-resort index (search returns nothing): `curl -sL https://developer.sepay.vn/llms.txt | grep -i '/vi/.*<word>'`. It is ~100 KB, so grep it, never read it whole. Never download `llms-full.txt` (~2 MB, the whole site).

## Missing code samples

Some `.md` exports print `<!-- No code tabs available -->` where the web page has tabbed code. Then use the language pages (`/vi/sepay-webhooks/lap-trinh-webhooks/lap-trinh-webhook` PHP, `…/lap-trinh-webhook-nodejs` Node.js, SDK pages), ask a fetch tool for just that block from the HTML page, or write the code from the documented rules.

## English pages

Same paths under `/en/`, but anchors come from English headings, so the map's anchors do not apply. Swap `/vi/` → `/en/`, list headings (`grep '^##'`), pick the one matching the Vietnamese heading (same structure and order), read it. Or search with `locale=en`: hits carry English anchors.

## `sepay` CLI installed

`sepay <command> --help` and `sepay help <topic>` (`environment`, `errors`, `exit-codes`, `glossary`) match the installed version; payloads and APIs come from the docs. See `cli.md`.

## Find an API endpoint

1. Section from the product's docs map.
2. Search `q=<action> <object>&section=<section>`, or MCP `get_endpoint` if present.
3. Read only that endpoint page's parameters / request / response and one code sample.
4. Present parameters as a table plus one sample; cite the page.

## Changelog

`https://developer.sepay.vn/vi/changelog` (HTML only, no `.md`); search excludes it. Read it only for "what changed".
