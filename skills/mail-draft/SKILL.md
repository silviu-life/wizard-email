---
name: mail-draft
description: Scrie un răspuns sau o ofertă personalizată pentru un contact, ca Draft în Gmail, din template-urile din `templates/` și ofertele din `oferte/`. Folosește la `/wizard-email:mail draft <email|thread-id> [intenție]`, „răspunde-i lui X", „scrie-i o ofertă lui X", „pregătește un răspuns", „fă un draft", reply to X, draft an offer, write back. NU trimite niciodată — trimiterea e `/wizard-email:mail send`. Pentru mai multe contacte deodată, `mail-campaign`.
---

# /wizard-email:mail draft — un email, un contact, un Draft în Gmail

> **Înainte de orice:** citește `${CLAUDE_PLUGIN_ROOT}/skills/mail/reguli.md` — unde stau datele (`$DATA`) și regulile dure.

**Regula de limbă, o dată:** emailul e în română cu diacritice, în vocea din `firma/voce.md`.
**Regula dură:** nu apelezi niciodată `send_message` sau `reply`. Doar `create_draft`.

## Pas 1 — contextul, în ordinea asta, doar cât trebuie

1. `contacte/<email>/profile.md` și `istoric.md` (tot). Dacă ai primit un thread id, găsește contactul
   prin `grep -rl "thread:<id>" contacte/`. Dacă nu există contact → rulează întâi logica din `mail-sync`
   pentru acel thread, apoi continuă.
2. `firma/profil.md` (semnătură), `firma/voce.md` (tot), `firma/obiectii.md` doar dacă istoricul conține o obiecție.
3. `oferte/_catalog.md`. Alegi oferta: cea cerută explicit în intenție > cea din „Decizii" > `oferta_implicita`
   a segmentului > niciuna. Citești DOAR `oferte/<id>.md` al ofertei alese.
4. `templates/_catalog.md`. Alegi UN template: intenția + `stadii` conține stadiul contactului (sau e gol) +
   `segmente` conține segmentul (sau e gol). Prioritate `discutii/` pentru răspunsuri; `marketing/` doar
   când intenția e explicit de campanie/nurture. Citești DOAR acel fișier. Niciun template potrivit →
   scrii fără template, în voce, și spui asta.

Câmpuri goale: `segment` gol → template cu `segmente: []`; dacă intenția cere ofertă și segmentul e gol,
pune o AskUserQuestion cu segmentele din `reguli/segmente.md`. `nume` gol → „Salut," fără prenume.
Ofertă fără `garantie` → nu pomenești garanția. Nimic inventat.

## Pas 2 — scrie

- Completezi placeholder-ele template-ului din contact / firmă / ofertă. Prețul, ratele, garanția: copiate
  verbatim din `oferte/<id>.md`. Niciodată din memorie.
- Apoi adaptezi proza la „Personalitate și stil": lungime, tu/dumneavoastră, cifre dacă le vrea.
- Răspunzi la ce a întrebat el ultima dată (ultimul `primit` din istoric), nu generic.
- Respectă `lungime` din template. O singură întrebare sau un singur pas la final.
- Corpul e **text simplu**: fără `**`, `#`, liste Markdown, emoji. Paragrafe scurte separate prin linie goală.

## Pas 3 — Draft în Gmail

Unealta Gmail `create_draft`:
- `to: [<email>]`, `subject`, `body` (text simplu).
- Dacă e răspuns la un thread: `replyToMessageId` = `msg:<id>` din ultima intrare `primit` a istoricului
  și subiectul rămâne cel al thread-ului (cu `Re:`).
Ia `id`-ul draftului din răspuns.

## Pas 4 — istoric și raport

`istoric.md` +=
```
## <azi> · draft · <intenție, 3-6 cuvinte> · draft:<id> · template:<id> [· oferta:<id>]
```
`profile.md`: `urmatorul_pas: "trimite draft <id>"`, `actualizat` = azi. `stadiu` NU se schimbă (se schimbă la send).
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/index.py"`.
Raport: contact, template ales, ofertă aleasă, subiect, corpul complet al draftului, `draft:<id>`, și
propoziția „Rămâne draft în Gmail. Trimiți toate drafturile la final cu `/wizard-email:mail send`." STOP.
