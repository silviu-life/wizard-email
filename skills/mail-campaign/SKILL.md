---
name: mail-campaign
description: Outbound — filtrează contactele după tip / segment / stadiu și pregătește un draft personalizat pentru fiecare, dintr-o ofertă sau un template. Folosește la `/wizard-email:mail campaign <filtru> oferta=<id>|template=<id>`, „trimite oferta X la toți clienții", „campanie pe segmentul Y", „scrie tuturor leadurilor", email campaign, bulk offer, send to all. Produce doar drafturi; nimic nu pleacă fără `/wizard-email:mail send` (care le trimite în lot, după confirmare).
---

# /wizard-email:mail campaign — drafturi în serie

> **Înainte de orice:** citește `${CLAUDE_PLUGIN_ROOT}/skills/mail/reguli.md` — unde stau datele (`$DATA`) și regulile dure.

## Pas 1 — filtrul

Argumente `cheie=valoare`: `tip`, `segment`, `stadiu` (oricare combinație, toate obligatorii ca AND) plus
exact unul din `oferta=<id>` sau `template=<id>`. Lipsă filtru sau lipsă ofertă/template → întreabă.
Din `contacte/_index.md` selectează rândurile care se potrivesc. Exclude `tip: ignora` și rândurile cu `⚠`.

## Pas 2 — confirmare ÎNAINTE de orice draft

Arată lista (email | nume | segment | stadiu) și numărul. AskUserQuestion: „Pregătesc N drafturi?" —
Da / Nu / „Scot pe cineva". Nu → STOP.

## Pas 3 — per contact

Aplică pașii 1-4 din `${CLAUDE_PLUGIN_ROOT}/skills/mail-draft/SKILL.md`, cu:
- oferta fixată la `oferta=<id>` (sau, dacă s-a dat `template=`, oferta după regulile din mail-draft);
- template-ul fixat la `template=<id>` (sau, dacă s-a dat `oferta=`, ales din `templates/_catalog.md`
  după segment + stadiu, preferând `marketing/` pentru contacte fără istoric de discuție și `discutii/`
  pentru cele cu).
Personalizarea per contact rămâne obligatorie: fiecare draft se scrie din fișa lui, nu se copiază.
Contact cu `segment` gol → sare peste el și îl listează la final („de clasificat").

## Pas 4 — raport

Tabel: contact | template | ofertă | draft:<id>. Plus lista celor săriți și de ce.
„Le trimiți pe toate cu `/wizard-email:mail send` (sau unul cu `/wizard-email:mail send <email>`)." Zero apeluri de trimitere. STOP.
