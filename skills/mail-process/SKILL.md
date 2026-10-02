---
name: mail-process
description: Procesează emailurile primite, unul câte unul — ce a spus contactul, contextul lui (fișă, istoric, stadiu, ofertă potrivită) și 2-4 variante de răspuns dintre care alegi; apoi predă la `mail-draft`. Folosește la `/wizard-email:mail process [<email> | --toate]`, „hai să-mi procesez emailurile", „ce am de răspuns", „ia-le pe rând", „ce a zis X și ce-i răspund", process my inbox, what did X say, triage replies. Nu citește Gmail direct (rulează `mail-sync` întâi), nu trimite.
---

# /wizard-email:mail process — emailurile pe rând: ce a zis · cine e · ce-i răspund

> **Înainte de orice:** citește `${CLAUDE_PLUGIN_ROOT}/skills/mail/reguli.md` — unde stau datele (`$DATA`) și regulile dure.

**Regula de limbă, o dată:** vorbești română. Variantele de răspuns sunt idei, nu emailuri scrise;
emailul îl scrie `mail-draft` după ce alegi.

## Pas 0 — ce e „neprocesat"

Un contact are un email neprocesat când ultima intrare din `istoric.md` este `primit` (nu e urmată de
`procesat`, `draft`, `trimis`). Coada: toate contactele din `contacte/_index.md` cu asta adevărat, fără
`tip: ignora`, sortate cu cel mai vechi `primit` întâi (cine așteaptă de mai mult, primul).
- `<email>` → doar el.
- `--toate` sau fără argument → coada întreagă. Arată la început: „N emailuri de procesat", lista scurtă.

## Pas 1 — per email, citește doar cât trebuie

`profile.md`, `istoric.md` (tot), `reguli/segmente.md` (dacă `segment` e gol), `oferte/_catalog.md`,
`templates/_catalog.md`, `firma/profil.md`. Nu citi template-uri sau oferte întregi aici.

## Pas 2 — prezintă, în exact trei blocuri

**1. Ce a spus** — ultimul mesaj primit: 2-4 linii rezumat + un citat scurt cu cuvintele lui exacte
(întrebarea sau obiecția). Dacă a pus mai multe întrebări, listează-le numerotat.

**2. Cine e** — tabel scurt: nume · firmă/rol · tip · segment · stadiu · de când vorbiți · câte
schimburi · ultima ofertă trimisă (dacă e) · „Decizii" din profil · 1-2 note de personalitate.
Câmp gol → „—" și, dacă `tip` sau `segment` lipsesc, propune o clasificare pe loc (semnalele din
`reguli/segmente.md`), marcată `[DEDUS]`, pe care o scrii dacă utilizatorul acceptă opțiunea.

**3. Cum poți răspunde** — 2-4 variante, fiecare o linie: **intenție** → template `discutii/<id>` (+
ofertă `<id>` dacă e cazul) → esența în 10-15 cuvinte. Alege-le după `stadii`/`segmente` din catalog și
după ce a întrebat el. Tipic:
- a întrebat de preț → `raspuns-intrebare-pret` cu oferta segmentului / `programare-call` / `cerere-informatii-lipsa`
- obiecție → `obiectie-pret` · `obiectie-timp` · `obiectie-ma-mai-gandesc` / `refuz-politicos`
- întrebare factuală → `raspuns-intrebare-simpla` / `raspuns-nu-stiu-inca`
- a acceptat / a plătit → `bun-venit-dupa-plata` / `recap-dupa-call`
- nemulțumire → `raspuns-reclamatie`
- nu e treaba noastră → `refuz-politicos` / opțiunea „Ignoră"
Prima variantă e recomandarea ta, cu un motiv de 5-10 cuvinte.

## Pas 3 — alegerea (în chat, NU AskUserQuestion)

Cele trei blocuri sunt ultimul mesaj din tură: după ele nu mai chemi niciun tool. Textul scris înaintea
unui tool call (mai ales AskUserQuestion) e comprimat de Claude Code într-un rezumat de o linie, iar
utilizatorul nu vede tabelul.

Sub variante adaugi mereu `**N.** Notă, fără răspuns · **I.** Ignoră contactul`, apoi o linie:
„Răspunde cu `1`, `2`, `3`, `N`, `I` sau scrie liber ce vrei." și te oprești. Răspunsul liber e o
intenție proprie.

## Pas 4 — acțiunea

- Variantă de răspuns → aplică `${CLAUDE_PLUGIN_ROOT}/skills/mail-draft/SKILL.md` cu intenția, template-ul și oferta
  alese (nu le realege). Draftul rezultat se arată integral. Nu trimiți.
- „Notă, fără răspuns" → cere o linie, scrie în `istoric.md`: `## <azi> · procesat · notă: <text>`.
- „Ignoră contactul" → `tip: ignora` în profil, `## <azi> · procesat · ignorat`.
În toate cazurile, după `draft` sau `procesat`, contactul iese din coadă. Dacă ai scris clasificarea
propusă la Pas 2, adaugă și `## <azi> · clasificat · ...`.

## Pas 5 — următorul

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/index.py"`, apoi treci la următorul email din coadă. Între emailuri nu întrebi „continui?";
utilizatorul oprește când vrea.

## Pas 6 — final (coada golită SAU utilizatorul s-a oprit)

Tabel contact | decizie | draft:<id> sau —. Dacă s-a creat cel puțin un draft, ultima linie e obligatoriu:

> N drafturi în Gmail, nimic n-a plecat. Le trimiți pe toate cu `/wizard-email:mail send`

Fără drafturi → „Niciun draft creat." STOP.
