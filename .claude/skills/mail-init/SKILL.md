---
name: mail-init
description: Inițializează sau actualizează datele firmei pentru sistemul de email — `firma/` (profil, voce, dovezi, obiecții), `oferte/`, `reguli/segmente.md`, `reguli/schema.md` și biblioteca `templates/`. Folosește la `/mail init`, „configurează sistemul de email", „pune datele firmei", „importă ofertele din documentele mele", „adaugă o ofertă nouă", set up email system, import offers. Din surse date de utilizator (foldere, fișiere, URL-uri) sau prin interviu. Nu citește inbox-ul (asta e `mail-sync`).
---

# /mail init — datele firmei

Scrii fișierele pe care le citesc toate celelalte skill-uri. Formatul exact e în `assets/SCHEMA.md`.
Exemplele de formă sunt în `assets/exemple/`. Citește-le, nu le recita.

**Regula de limbă, o dată:** tot ce scrii e în română cu diacritice.

## Pas 0 — ce există deja

Listează `firma/`, `oferte/`, `reguli/`, `templates/`. Dacă există ceva, ești în mod **actualizare**:
nu suprascrii nimic fără să arăți diff-ul. Dacă nu există nimic, ești în mod **inițializare**.

## Pas 1 — alege modul (AskUserQuestion, o singură întrebare)

- **Din surse**: utilizatorul dă căi sau URL-uri (folder, fișiere, site, Notion).
- **Interviu**: nu are surse; îl întrebi tu.
Dacă argumentele comenzii conțin deja o cale/URL, sari întrebarea: modul e „din surse".

## Pas 2a — din surse

Sursele pot fi orice: un folder de Markdown, PDF-uri, un site, o pagină Notion, un CSV de prețuri. Nu
presupui nicio structură și niciun nume de fișier. Procedura:

1. Inventariază: `find <folder> -type f` (sau lista de URL-uri). Pentru fiecare fișier text, `grep -n '^#'`
   ca să vezi secțiunile. Nu citi fișiere întregi; citește doar feliile care răspund la subiectele de mai jos.
2. Caută, în ordinea asta, felii despre:

| Subiect (ce cauți) | Semne în heading-uri / text | Țintă |
|---|---|---|
| produse, prețuri, ce include, garanție, rate, activ/inactiv | „preț", „ofertă", „produs", „pachet", „tarif", valută, „garanție", „rate" | `oferte/<id>.md`, un fișier per produs cu preț |
| cui vindem: segmente, persona, dureri, ce îi trădează | „audiență", „cui", „segment", „persona", „client ideal", „dureri", „obiective" | `reguli/segmente.md` |
| cine suntem, poziționare, diferențiatori | „despre", „cine suntem", „misiune", „poziționare", „de ce noi" | `firma/profil.md` |
| voce, ton, reguli de scris, cuvinte interzise | „voce", „ton", „stil", „brand", „cum scriem", „nu spunem" | `firma/voce.md` |
| dovezi: cifre, testimoniale, studii de caz | „rezultate", „testimoniale", „cazuri", „dovezi", cifre cu % sau valută | `firma/dovezi.md` |
| obiecții și răspunsuri | „obiecții", „de ce nu", „întrebări frecvente", „FAQ" | `firma/obiectii.md` |

3. Un subiect fără nicio felie găsită → fișierul țintă se scrie cu ce ai (poate fi doar un heading) și
   întrebi utilizatorul acel lucru, în stil interviu (Pas 2b), doar pentru subiectul lipsă.

Reguli:
- Prețul se copiază **verbatim** din sursă, cu valuta din sursă. Nu rotunjești, nu convertești.
- Două surse cu prețuri diferite pentru același produs → nu alegi tu: listează ambele cu sursa și data și
  întreabă. Dacă o sursă se declară explicit „sursa de adevăr" pentru prețuri, aceea bate.
- Păstrezi marcajele `[DOCUMENTAT]` / `[DEDUS]` dacă sursa le are; dacă nu, ce e citat explicit e
  `[DOCUMENTAT]`, ce deduci tu e `[DEDUS]`.
- `verificat_la` = data declarată în sursă (frontmatter, „actualizat la", data documentului); dacă nu
  există, gol. Nu pui data de azi.
- Un produs fără preț sau marcat inactiv → `activ: false`, nu îl omiți.
- `sursa:` pe fiecare ofertă = calea sau URL-ul relativ la ce a dat utilizatorul, plus secțiunea.

## Pas 2b — interviu

O întrebare pe mesaj, în ordinea asta. Răspunsurile intră direct în fișiere.
1. Ce vinzi? Pentru fiecare produs: nume, preț exact, ce include, garanție, activ sau nu.
2. Cui vinzi? 2-5 segmente: cine sunt, după ce îi recunoști într-un email, ce ofertă li se potrivește.
3. Cine semnează emailurile și cum (prenume? titlu?). Care e adresa ta de email (o folosește `mail-sync` ca să te excludă).
4. Cum vorbești? Tu/dumneavoastră, cald/formal, 3 cuvinte pe care nu le folosești niciodată.
5. Ce dovezi ai? Cifre, testimoniale, studii de caz.
6. Care sunt cele 3-5 obiecții pe care le auzi cel mai des și cum răspunzi.

## Pas 3 — `firma/profil.md` conține obligatoriu

- Nume firmă, ce facem (o frază), cui (segmentele, pe scurt), poziționare.
- **Semnătură**: cum se semnează emailurile.
- **Email propriu**: adresa (sau adresele) din care trimiți. `mail-sync` o citește de aici.

## Pas 4 — template-urile și schema

- `cp -rn .claude/skills/mail-init/assets/templates/. templates/` — copiază DOAR ce lipsește. Ce a
  modificat utilizatorul rămâne neatins.
- `cp -n .claude/skills/mail-init/assets/SCHEMA.md reguli/schema.md`.

## Pas 5 — rezumat și confirmare, ÎNAINTE de Write

Arată: ce fișiere vei scrie/actualiza, câte oferte (cu preț și activ/inactiv), câte segmente, câte
template-uri copiate. În mod actualizare, arată diff-ul pe fiecare fișier existent. AskUserQuestion:
„Scriu?" Abia apoi scrii.

## Pas 6 — index și oprire

`python3 scripts/index.py`. Raportează exit code-ul și problemele, dacă sunt. Scrie `oferte/_catalog.md`
(tabel `id | nume | preț | segmente țintă | activ`) din frontmatter-ele ofertelor. STOP.
