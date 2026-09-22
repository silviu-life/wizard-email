# Schema fișierelor — sursa unică

Fiecare skill citește fișierul ăsta înainte să scrie. `scripts/index.py` validează după el.
Regula generală: **câmp opțional gol sau absent = „nu știm încă" / „oricare"**. Nu se inventează valori.

## `contacte/<email>/profile.md` (frontmatter YAML)

| Câmp | Obligatoriu | Default | Valori permise |
|---|---|---|---|
| `email` | da | — | adresa lowercase, identică cu numele folderului |
| `creat` | da | — | `YYYY-MM-DD` |
| `sursa` | da | — | `gmail` · `import` · `manual` |
| `nume` | nu | `""` (din header From) | text |
| `firma` | nu | `""` | text |
| `rol` | nu | `""` | text |
| `tip` | nu | `""` | `lead` · `client` · `fost-client` · `partener` · `furnizor` · `ignora` |
| `segment` | nu | `""` | un `id` din `reguli/segmente.md` |
| `stadiu` | nu | `nou` | `nou` · `in-discutie` · `oferta-trimisa` · `negociere` · `castigat` · `pierdut` |
| `actualizat` | nu | `=creat` | `YYYY-MM-DD` |
| `ultima_interactiune` | nu | `=creat` | `YYYY-MM-DD` |
| `urmatorul_pas` | nu | `""` | text scurt |
| `urmatorul_pas_data` | nu | `""` | `YYYY-MM-DD` |

Corp (secțiuni fixe, pot fi goale): `## Personalitate și stil`, `## Ce vrea / durerea`, `## Decizii`, `## Note`.
Ce e dedus se marchează `[DEDUS]`, ce a spus contactul explicit `[DOCUMENTAT]`.

## `contacte/<email>/istoric.md`

Cronologic, o intrare per eveniment, cea mai veche sus. Format fix al titlului:
```
## YYYY-MM-DD · <eveniment> · <descriere scurtă> · <referințe>
```
- `eveniment`: `primit` · `trimis` · `draft` · `procesat` (decizie luată în `mail-process` fără draft: notă sau ignorat) · `clasificat` · `nota` · `call`
- referințe: `thread:<id>`, `msg:<id>`, `draft:<id>`, `template:<id>`, `oferta:<id>` — câte se aplică
- sub titlu: 1-3 linii de rezumat. La `trimis` se notează și schimbarea de stadiu: `→ stadiu: oferta-trimisa`

## `oferte/<id>.md`

| Câmp | Obligatoriu | Default | Valori permise |
|---|---|---|---|
| `id` | da | — | slug, identic cu numele fișierului |
| `nume` | da | — | text |
| `pret` | da | — | text cu valută, exact ca în sursă (ex. `1.497 €`) |
| `activ` | da | — | `true` · `false` |
| `pret_ancora` | nu | `""` | text |
| `rate` | nu | `""` | text (ex. `3 rate, prima 499 €`) |
| `garantie` | nu | `""` | text verbatim din sursă |
| `segmente_tinta` | nu | `[]` (= oricare) | listă de `id` din `reguli/segmente.md` |
| `stadii_recomandate` | nu | `[]` | listă de stadii |
| `sursa` | nu | `""` | cale sau URL |
| `verificat_la` | nu | `""` | `YYYY-MM-DD` |

Corp: `## Ce include`, `## Argumente`, `## Obiecții specifice`. `oferte/_catalog.md` e generat de `mail-init`.

## `templates/**/*.md`

| Câmp | Obligatoriu | Default | Valori permise |
|---|---|---|---|
| `id` | da | — | calea relativă fără `.md` (ex. `discutii/follow-up-bland`) |
| `categorie` | da | — | `discutii` · `01_customer_acquisition` · `02_lead_nurturing` · `03_conversion_sales` · `04_customer_success` · `05_community_engagement` |
| `scop` | da | — | o frază |
| `cand` | nu | `""` | o frază: situația în care se folosește |
| `ton` | nu | `""` | 3-5 cuvinte |
| `lungime` | nu | `""` | ex. `60-100 cuvinte` |
| `segmente` | nu | `[]` (= oricare) | listă de `id` |
| `stadii` | nu | `[]` (= oricare) | listă de stadii |
| `oferta` | nu | `false` | `true` dacă emailul cere o ofertă din `oferte/` |

Corp: `# Titlu`, `**Subiect**: [...]`, `---`, textul emailului cu `[placeholder-e descriptive]`, `---`,
`**Placeholder-uri pentru AI**`, `**Note de personalizare**`. Placeholder-ele NU sunt mustache: le
completează `mail-draft` din contact / firmă / ofertă, apoi adaptează proza.

## `reguli/segmente.md`

Un segment = o secțiune `## <id>` cu:
- `descriere:` (obligatoriu) — cine e, într-o frază
- `semnale:` (opțional) — listă: cuvinte, context, tip de întrebare care îl trădează în email
- `oferta_implicita:` (opțional) — `id` din `oferte/`

## `firma/`

`profil.md` (ce facem, cui, poziționare, diferențiatori, cine semnează emailurile și cum),
`voce.md` (reguli de ton, cuvinte interzise), `dovezi.md` (testimoniale, cifre), `obiectii.md` (obiecție → răspuns).
Fără frontmatter obligatoriu. `mail-init` le scrie; skill-urile le citesc.
