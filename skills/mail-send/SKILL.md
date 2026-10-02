---
name: mail-send
description: Trimite drafturile din Gmail, după confirmare explicită, și actualizează fișele contactelor. Fără argument trimite în lot toate drafturile netrimise (cele create în `process`, `draft`, `followup`, `campaign`); cu argument, doar unul. Folosește la `/wizard-email:mail send [<draft-id|email>]`, „trimite drafturile", „trimite tot", „trimite-i lui X", „dă-i send", send all drafts, send it. Singurul skill care trimite email. Nu compune și nu editează text — pentru asta e `/wizard-email:mail draft`.
---

# /wizard-email:mail send — singurul loc de unde pleacă un email

> **Înainte de orice:** citește `${CLAUDE_PLUGIN_ROOT}/skills/mail/reguli.md` — unde stau datele (`$DATA`) și regulile dure.

Draft netrimis = intrare `draft:<id>` din `contacte/<email>/istoric.md` care nu are după ea un `trimis`
cu același id.

## Pas 1 — găsește drafturile

- Fără argument sau `--toate` → **lot**: toate drafturile netrimise din `contacte/*/istoric.md`
  (`grep -l "· draft ·" "$DATA"/contacte/*/istoric.md`, apoi verifici fiecare id).
- `<draft-id>` → doar el.
- `<email>` → ultimul draft netrimis al contactului.
- Nimic găsit → „Nu există drafturi de trimis." STOP.

Unealta Gmail `get_draft` pentru fiecare id. Draft dispărut (șters din Gmail) → îl scoți din listă și îl
menționezi în raport.

## Pas 2 — confirmare, obligatoriu, o singură dată

Arată un tabel: # | destinatar | subiect | prima linie din corp. AskUserQuestion cu exact două opțiuni:
„Trimite toate (N)" / „Nu trimite" (la un singur draft: „Trimite" / „Nu trimite"). La „Other" utilizatorul
poate exclude unele („fără 2 și 5") → trimiți restul. Orice altceva → STOP fără să trimiți.
Dacă vrea modificări la un draft → „Modificările se fac cu `/wizard-email:mail draft`." și îl excluzi.

## Pas 3 — trimite, pe rând

Pentru fiecare draft confirmat: unealta Gmail `send_message` cu `draftId: <id>`. Nimic altceva în apel.
Ia `id` și `threadId` din răspuns și faci imediat Pas 4 pentru el, înainte de următorul (dacă se oprește
la jumătate, fișele reflectă exact ce a plecat). Eroare la un draft → o notezi și continui.

## Pas 4 — fișa (per draft trimis)

`istoric.md` +=
```
## <azi> · trimis · draft:<id> · thread:<threadId> · msg:<id>[ → stadiu: oferta-trimisa]
```
`profile.md`: `ultima_interactiune` = azi, `actualizat` = azi, `urmatorul_pas` = „follow-up dacă nu răspunde",
`urmatorul_pas_data` = azi + 4 zile. Dacă intrarea `draft` avea `oferta:<id>` și stadiul era `nou` sau
`in-discutie` → `stadiu: oferta-trimisa`. Altfel stadiul rămâne.
La final `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/index.py"`. Raport: tabel destinatar | trimis / exclus / eroare | thread. STOP.
