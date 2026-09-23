# email-ai

Sistem de email organizat pe contacte, pentru Claude Code. Citește inbox-ul, ține o fișă per contact,
îl clasifică (tip relație · segment · stadiu · personalitate) și pregătește răspunsuri și oferte
personalizate din template-urile și ofertele firmei. Trimiterea e un pas separat, cu confirmare.

## Pornire

```
cd email-ai
claude
> /mail setup                           # instalează ce lipsește, verifică Gmail
> /mail init /cale/catre/documente     # folder, PDF-uri, URL-uri; fără argument → interviu
> /mail sync                            # inbox → contacte/<email>/
> /mail classify --toate
> /mail process                         # pe rând: ce a zis, cine e, ce-i răspund
> /mail draft ana@firma.ro "răspunde la întrebarea de preț"
> /mail send ana@firma.ro
```

Necesită connector-ul Gmail activ în Claude (claude.ai → Gmail). Outlook: când există connector, se
schimbă doar `mail-sync` și `mail-send`.

## Comenzi

| Comandă | Ce face |
|---|---|
| `/mail setup` | Python + Gmail + proiect verificate; predă la /mail init |
| `/mail init [surse]` | construiește `firma/`, `oferte/`, `reguli/`, `templates/` |
| `/mail sync [--zile N] [query]` | Gmail (default 360 zile, fără marketing) → `contacte/<email>/` |
| `/mail process [<email> \| --toate]` | emailurile pe rând: ce a zis, cine e, variante de răspuns |
| `/mail classify <email> \| --toate` | tip, segment, stadiu, personalitate |
| `/mail draft <email\|thread> [intenție]` | un Draft în Gmail, din template + ofertă |
| `/mail send <draft-id\|email>` | trimite un draft, după confirmare |
| `/mail followup [--zile N] [--draft]` | cine n-a răspuns |
| `/mail campaign <filtru> oferta=<id>` | drafturi în serie pe un segment |

## Organizare

```
CLAUDE.md                 reguli globale
.claude/skills/mail-*/    un skill = un verb
scripts/index.py          generează contacte/_index.md + templates/_catalog.md, validează schema
firma/  oferte/  reguli/  templates/  contacte/     ← date, gitignored, generate de /mail init și /mail sync
```

Schema fiecărui fișier: `.claude/skills/mail-init/assets/SCHEMA.md`. Biblioteca de template-uri (77
marketing + 20 discuții 1:1, toate în română): `.claude/skills/mail-init/assets/templates/`.

Verificare: `python3 scripts/index.py --check`.
