---
name: mail-send
description: Trimite un draft existent din Gmail, după confirmare explicită, și actualizează fișa contactului. Folosește la `/mail send <draft-id|email>`, „trimite draftul", „trimite-i lui X", „dă-i send", send the draft, send it. Singurul skill care trimite email. Nu compune și nu editează text — pentru asta e `/mail draft`.
---

# /mail send — singurul loc de unde pleacă un email

## Pas 1 — găsește draftul

- `<draft-id>` → direct.
- `<email>` → ultima intrare `draft:<id>` din `contacte/<email>/istoric.md` care nu are după ea un `trimis` cu același id.
- Nimic găsit → „Nu există draft pentru X. Fă unul cu `/mail draft X`." STOP.

Unealta Gmail `get_draft` cu id-ul: verifică că există. Draft dispărut (șters din Gmail) → spune și STOP.

## Pas 2 — confirmare, obligatoriu

Arată: destinatar, subiect, primele 3 linii din corp. AskUserQuestion cu exact două opțiuni:
„Trimite" / „Nu trimite". Orice altceva decât „Trimite" → STOP fără să trimiți.
Dacă utilizatorul vrea modificări → „Modificările se fac cu `/mail draft`." STOP.

## Pas 3 — trimite

Unealta Gmail `send_message` cu `draftId: <id>`. Nimic altceva în apel. Ia `id` și `threadId` din răspuns.

## Pas 4 — fișa

`istoric.md` +=
```
## <azi> · trimis · draft:<id> · thread:<threadId> · msg:<id>[ → stadiu: oferta-trimisa]
```
`profile.md`: `ultima_interactiune` = azi, `actualizat` = azi, `urmatorul_pas` = „follow-up dacă nu răspunde",
`urmatorul_pas_data` = azi + 4 zile. Dacă intrarea `draft` avea `oferta:<id>` și stadiul era `nou` sau
`in-discutie` → `stadiu: oferta-trimisa`. Altfel stadiul rămâne.
`python3 scripts/index.py`. Raport: o linie — „Trimis către X, thread <id>". STOP.
