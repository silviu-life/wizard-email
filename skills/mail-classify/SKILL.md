---
name: mail-classify
description: Completează fișa unui contact — tip relație, segment, stadiu, personalitate, ce vrea — din istoricul emailurilor și `reguli/segmente.md`. Folosește la `/wizard-email:mail classify <email>` sau `/wizard-email:mail classify --toate`, „clasifică contactele", „ce fel de client e X", „pune-l pe X în segment", classify contacts, tag contact, what segment is X. Nu citește Gmail (asta e `mail-sync`), nu scrie emailuri.
---

# /wizard-email:mail classify — tip · segment · stadiu · personalitate

> **Înainte de orice:** citește `${CLAUDE_PLUGIN_ROOT}/skills/mail/reguli.md` — unde stau datele (`$DATA`) și regulile dure.

Citește întâi, nu recita: `reguli/schema.md` (valorile permise), `reguli/segmente.md` (semnalele),
`firma/profil.md` (ca să știi ce vindem). Apoi, per contact, `profile.md` + `istoric.md` complet.

## Pas 1 — ținta

- `<email>` → un contact.
- `--toate` → toate rândurile din `contacte/_index.md` cu `tip` sau `segment` gol (`—`).
- fără argument → întreabă.

## Pas 2 — per contact, deduce din text, nu din impresie

Pentru fiecare câmp notează dovada (o frază din istoric) și încrederea (mare / medie / mică):

- **tip**: `lead` (întreabă, nu a cumpărat) · `client` (a plătit, e în program) · `fost-client` ·
  `partener` · `furnizor` (ne vinde el nouă) · `ignora` (spam uman, recrutori, cereri irelevante).
- **segment**: potrivește `semnale:` din `reguli/segmente.md` cu textul. Două segmente la egalitate →
  ambiguitate, nu alegi tu.
- **stadiu**: `nou` (o singură interacțiune, fără răspuns de la noi) · `in-discutie` (schimb de mesaje) ·
  `oferta-trimisa` (istoricul are `trimis` cu `oferta:`) · `negociere` (discută preț/rate/termen) ·
  `castigat` (a plătit) · `pierdut` (a refuzat explicit sau tăcere > 30 zile după ofertă).
- **Personalitate și stil**: lungimea mesajelor lui, tu/dumneavoastră, folosește cifre?, ton (grăbit,
  politicos, sceptic), ora la care scrie. Fiecare punct cu `[DOCUMENTAT]` (se vede în text) sau `[DEDUS]`.
- **Ce vrea / durerea**: în cuvintele lui, citat scurt, `[DOCUMENTAT]`.
- **Decizii**: doar ce s-a stabilit explicit (preț discutat, termen).

Câmp fără dovadă → rămâne gol. Nu inventezi.

## Pas 3 — ambiguitățile, o singură întrebare

Adună toate cazurile cu încredere mică sau egalitate și pune UNA singură AskUserQuestion la final (o
întrebare per contact ambiguu, în același apel, max 4; restul într-un al doilea apel). Nu întrerupe după
fiecare contact.

## Pas 4 — scrie

Actualizează frontmatter-ul (`tip`, `segment`, `stadiu`, `actualizat` = azi) și secțiunile din corp.
Adaugă în `istoric.md`:
```
## <azi> · clasificat · tip:<tip> segment:<segment> stadiu:<stadiu>
<dovezile, o linie>
```
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/index.py"`. Raport: tabel contact | tip | segment | stadiu | încredere. STOP.
