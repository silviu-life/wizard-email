---
name: mail-sync
description: Citește Gmail și creează sau actualizează fișele din `contacte/<email>/` (profile.md + istoric.md). Folosește la `/mail sync [query]`, „citește inbox-ul", „cine mi-a scris", „adu emailurile noi", „sincronizează contactele", sync inbox, pull emails, who emailed me. Doar citește și înregistrează. Nu clasifică (`mail-classify`), nu scrie drafturi (`mail-draft`).
---

# /mail sync — inbox → contacte/

Citește `reguli/schema.md` (secțiunile `profile.md` și `istoric.md`) înainte să scrii orice.

## Pas 1 — ce cauți

Query implicit: `in:inbox newer_than:7d -category:promotions -category:social`. Dacă utilizatorul dă un
query Gmail sau un interval („ultimele 3 zile"), îl traduci în sintaxă Gmail (`newer_than:3d`).
Adresa proprie: din `firma/profil.md` („Email propriu"). Fără ea, oprește-te și cere-o.

## Pas 2 — listează thread-urile

Unealta Gmail `search_threads` cu `query`, `view: THREAD_VIEW_MINIMAL`, `pageSize: 50`. Paginează cu
`pageToken` până se termină. Din fiecare thread ia sender-ul mesajelor.

**Ignoră** expeditorii care se potrivesc pe: `noreply`, `no-reply`, `notification`, `notifications`,
`mailer-daemon`, `newsletter`, `donotreply`, `@calendar-`, `@docs.google.com`, `@accounts.`, plus orice
adresă din lista „Ignoră" din `firma/profil.md` dacă există. Ignoră thread-urile în care singurul
expeditor ești tu.

## Pas 3 — per thread relevant

`get_thread` cu `messageFormat: PLAIN_TEXT`. Pentru fiecare adresă expeditoare ≠ a ta (lowercase):

- `contacte/<email>/` **nu există** → creează `profile.md` după schemă: `email`, `nume` (din display name
  al header-ului From; gol dacă lipsește), `sursa: gmail`, `creat` = azi, `stadiu: nou`, restul gol.
  Secțiunile din corp goale. Creează `istoric.md` gol.
- **există** → schimbi doar `actualizat` și `ultima_interactiune` (= data celui mai nou mesaj primit).

Apoi `istoric.md`: pentru fiecare mesaj al contactului al cărui `msg:<id>` NU apare deja în fișier, adaugă:
```
## <data mesajului> · primit · "<subiect>" · thread:<threadId> · msg:<messageId>
<2-3 linii: ce cere, ce semnale (buget, urgență, obiecție, întrebare de preț)>
```
Mesajele tale din același thread NU se adaugă (istoricul e despre ce primești și ce trimiți prin sistem).
Intrările se pun în ordine cronologică.

## Pas 4 — index și raport

`python3 scripts/index.py`. Raportează un tabel scurt: contact | nou/actualizat | mesaje adăugate | tip
(gol = de clasificat). La final: „N contacte au `tip` gol → `/mail classify --toate`". STOP.

## Ce NU faci
- Nu completezi `tip`, `segment`, personalitate. Nu ghicești nimic.
- Nu scrii drafturi, nu trimiți, nu pui etichete în Gmail.
