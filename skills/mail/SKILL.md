---
name: mail
description: Orchestratorul sistemului de email pe contacte. Folosește la `/wizard-email:mail <verb>` — setup, init, sync, process, classify, draft, send, followup, campaign — sau când utilizatorul spune „citește inbox-ul", „cine mi-a scris", „ce am de răspuns", „procesează emailurile", „răspunde-i lui X", „trimite oferta", „fă follow-up", „campanie pe clienți", „inițializează sistemul de email", „instalează ce trebuie", check inbox, reply to, send offer, follow up, email campaign. Fără verb sau verb necunoscut → listează comenzile. Nu face nimic singur; rutează spre skill-ul `mail-<verb>`.
---

# /wizard-email:mail — orchestrator

> **Înainte de orice:** citește `${CLAUDE_PLUGIN_ROOT}/skills/mail/reguli.md` — unde stau datele (`$DATA`) și regulile dure.

Un skill = un verb. Tu doar rutezi.

| Comandă | Ce face | Skill |
|---|---|---|
| `/wizard-email:mail setup` | verifică/instalează Python, verifică Gmail, pregătește folderul de date | `mail-setup` |
| `/wizard-email:mail init [surse...]` | construiește `firma/`, `oferte/`, `reguli/`, `templates/` din surse sau interviu | `mail-init` |
| `/wizard-email:mail sync [--zile N] [query]` | citește Gmail (default 360 zile, fără marketing) → `contacte/<email>/` | `mail-sync` |
| `/wizard-email:mail process [<email> \| --toate]` | emailurile pe rând: ce a zis, cine e, variante de răspuns | `mail-process` |
| `/wizard-email:mail classify <email> \| --toate` | completează tip / segment / stadiu / personalitate | `mail-classify` |
| `/wizard-email:mail draft <email\|thread> [intenție]` | scrie un răspuns sau o ofertă ca Draft în Gmail | `mail-draft` |
| `/wizard-email:mail send <draft-id\|email>` | trimite un draft existent, după confirmare | `mail-send` |
| `/wizard-email:mail followup [--zile N] [--draft]` | cine n-a răspuns de N zile | `mail-followup` |
| `/wizard-email:mail campaign <filtru> oferta=<id>\|template=<id>` | drafturi în serie pe un segment | `mail-campaign` |

## Pași

1. Fără verb sau verb necunoscut → afișează tabelul de mai sus și oprește-te.
2. Verb ∉ {`setup`, `init`} și `$DATA/firma/profil.md` nu există → spune „Sistemul nu e inițializat" și propune `/wizard-email:mail setup`, apoi `/wizard-email:mail init`. Oprește-te.
3. Citește `${CLAUDE_PLUGIN_ROOT}/skills/mail-<verb>/SKILL.md` și urmează-l exact, cu argumentele primite.
