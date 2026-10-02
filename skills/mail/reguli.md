# wizard-email — reguli globale

Se aplică tuturor skill-urilor `mail-*`. Un skill = un verb. Comenzi: `/wizard-email:mail <verb>`.

## Unde stau datele (global, accesibile din orice folder)
Rulează o dată pe sesiune: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/index.py" --where`. Afișează
folderul de date (`$DATA`, implicit `~/wizard-email`, schimbabil cu variabila `WIZARD_EMAIL_HOME`).
Toate căile din skill-uri (`firma/`, `oferte/`, `reguli/`, `templates/`, `contacte/`) sunt relative la
`$DATA`, NU la folderul curent. La Read/Write/Edit folosește calea absolută afișată.

## Surse de adevăr (se citesc, nu se țin minte)
- Preț, ce include, garanție → `oferte/<id>.md`. Niciodată din memorie.
- Voce, ton, cuvinte interzise → `firma/voce.md`.
- Cine suntem, ce vindem, cui → `firma/profil.md`.
- Segmente și semnalele lor → `reguli/segmente.md`.
- Schema fiecărui fișier (câmpuri obligatorii, default-uri, valori permise) → `reguli/schema.md`.
- Contact → `contacte/<email>/profile.md` + `istoric.md`. Cheia = adresa de email, lowercase.
- `contacte/_index.md`, `templates/_catalog.md` sunt GENERATE de `index.py`. Nu se editează de mână.

## Reguli dure
1. Implicit se fac doar drafturi în Gmail. Emailul pleacă DOAR prin `/wizard-email:mail send` (rulat la final, trimite în lot toate drafturile netrimise), după confirmare explicită. Niciun alt skill nu apelează `send_message` sau `reply`.
2. Orice acțiune pe un contact lasă o linie în `contacte/<email>/istoric.md` (format în `reguli/schema.md`).
3. Câmp necunoscut = gol. Nu se inventează valori. Ce e dedus se marchează `[DEDUS]`, ce a spus contactul explicit `[DOCUMENTAT]`.
4. După orice scriere în `contacte/` sau `templates/` se rulează `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/index.py"`.
5. Limbă: skill-urile vorbesc română. Emailurile ies în română cu diacritice (ă â î ș ț), în vocea din `firma/voce.md`.
6. Corpul emailului trimis către Gmail e text simplu: fără Markdown, fără `**`, fără `#`.

## Dacă `$DATA/firma/profil.md` nu există
Sistemul nu e inițializat. Rulează `/wizard-email:mail setup`, apoi `/wizard-email:mail init`.
