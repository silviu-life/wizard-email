# email-ai — reguli globale

Sistem de email organizat pe contacte. Un skill = un verb. Comenzi: `/mail <verb>` (vezi `.claude/skills/mail/SKILL.md`).

## Surse de adevăr (se citesc, nu se țin minte)
- Preț, ce include, garanție → `oferte/<id>.md`. Niciodată din memorie.
- Voce, ton, cuvinte interzise → `firma/voce.md`.
- Cine suntem, ce vindem, cui → `firma/profil.md`.
- Segmente și semnalele lor → `reguli/segmente.md`.
- Schema fiecărui fișier (câmpuri obligatorii, default-uri, valori permise) → `reguli/schema.md`.
- Contact → `contacte/<email>/profile.md` + `istoric.md`. Cheia = adresa de email, lowercase.
- `contacte/_index.md`, `templates/_catalog.md` sunt GENERATE de `python3 scripts/index.py`. Nu se editează de mână.

## Reguli dure
1. Emailul pleacă DOAR prin `/mail send`, după confirmare explicită. Niciun alt skill nu apelează `send_message` sau `reply`.
2. Orice acțiune pe un contact lasă o linie în `contacte/<email>/istoric.md` (format în `reguli/schema.md`).
3. Câmp necunoscut = gol. Nu se inventează valori. Ce e dedus se marchează `[DEDUS]`, ce a spus contactul explicit `[DOCUMENTAT]`.
4. După orice scriere în `contacte/` sau `templates/` se rulează `python3 scripts/index.py`.
5. Limbă: skill-urile vorbesc română. Emailurile ies în română cu diacritice (ă â î ș ț), în vocea din `firma/voce.md`.
6. Corpul emailului trimis către Gmail e text simplu: fără Markdown, fără `**`, fără `#`.

## Dacă `firma/profil.md` nu există
Sistemul nu e inițializat. Rulează `/mail setup`, apoi `/mail init`.
