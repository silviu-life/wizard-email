---
name: mail-followup
description: Găsește contactele care n-au răspuns de N zile (ofertă trimisă sau discuție în curs) și, la cerere, le pregătește drafturi de follow-up. Folosește la `/wizard-email:mail followup [--zile N] [--draft]`, „cine nu mi-a răspuns", „ce follow-up-uri am de făcut", „urmărire", who hasn't replied, pending follow-ups. Nu trimite nimic.
---

# /wizard-email:mail followup — cine tace

> **Înainte de orice:** citește `${CLAUDE_PLUGIN_ROOT}/skills/mail/reguli.md` — unde stau datele (`$DATA`) și regulile dure.

## Pas 1 — candidații

Din `contacte/_index.md`: rânduri cu `stadiu` ∈ {`oferta-trimisa`, `in-discutie`} și `ultima_interactiune`
mai veche de N zile (default 4). Ignoră `tip: ignora`.

## Pas 2 — confirmă că n-a răspuns

Per candidat, unealta Gmail `search_threads` cu `query: "from:<email> newer_than:<N>d"`,
`view: THREAD_VIEW_METADATA_ONLY`. Dacă apare ceva → a răspuns, dar `mail-sync` n-a rulat: scoate-l din
listă și notează „rulează `/wizard-email:mail sync`".

## Pas 3 — raport

Tabel: contact | stadiu | zile de tăcere | ultimul eveniment din istoric | follow-up-uri deja trimise
(numără intrările `trimis` cu `template:discutii/follow-up-*`). Sortat după zile, descrescător.
Contact cu ≥ 2 follow-up-uri trimise → marchează „propune `inchidere-thread`", nu al treilea follow-up.

## Pas 4 — `--draft` (opțional)

Pentru fiecare contact din tabel, aplică pașii 1-4 din `${CLAUDE_PLUGIN_ROOT}/skills/mail-draft/SKILL.md` cu intenția
„follow-up" (template `discutii/follow-up-dupa-oferta` dacă stadiul e `oferta-trimisa`, altfel
`discutii/follow-up-bland`; `discutii/inchidere-thread` dacă are deja 2 follow-up-uri). Zero trimiteri.
Raport final: contact | draft:<id>. STOP.
