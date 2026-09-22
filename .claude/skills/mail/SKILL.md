---
name: mail
description: Orchestratorul sistemului de email pe contacte. Folosește la `/mail <verb>` — init, sync, classify, draft, send, followup, campaign — sau când utilizatorul spune „citește inbox-ul", „cine mi-a scris", „răspunde-i lui X", „trimite oferta", „fă follow-up", „campanie pe clienți", „inițializează sistemul de email", check inbox, reply to, send offer, follow up, email campaign. Fără verb sau verb necunoscut → listează comenzile. Nu face nimic singur; rutează spre skill-ul `mail-<verb>`.
---

# /mail — orchestrator

Un skill = un verb. Tu doar rutezi.

| Comandă | Ce face | Skill |
|---|---|---|
| `/mail init [surse...]` | construiește `firma/`, `oferte/`, `reguli/`, `templates/` din surse sau interviu | `mail-init` |
| `/mail sync [query]` | citește Gmail → creează/actualizează `contacte/<email>/` | `mail-sync` |
| `/mail classify <email> \| --toate` | completează tip / segment / stadiu / personalitate | `mail-classify` |
| `/mail draft <email\|thread> [intenție]` | scrie un răspuns sau o ofertă ca Draft în Gmail | `mail-draft` |
| `/mail send <draft-id\|email>` | trimite un draft existent, după confirmare | `mail-send` |
| `/mail followup [--zile N] [--draft]` | cine n-a răspuns de N zile | `mail-followup` |
| `/mail campaign <filtru> oferta=<id>\|template=<id>` | drafturi în serie pe un segment | `mail-campaign` |

## Pași

1. Fără verb sau verb necunoscut → afișează tabelul de mai sus și oprește-te.
2. Verb ≠ `init` și `firma/profil.md` nu există → spune „Sistemul nu e inițializat" și propune `/mail init`. Oprește-te.
3. Citește `.claude/skills/mail-<verb>/SKILL.md` și urmează-l exact, cu argumentele primite.

Regulile globale sunt în `CLAUDE.md` (rădăcina proiectului). Se aplică tuturor verbelor.
