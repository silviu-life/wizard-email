# wizard-email

Sistem de email organizat pe contacte, plugin pentru Claude Code. Citește inbox-ul, ține o fișă per contact,
îl clasifică (tip relație · segment · stadiu · personalitate) și pregătește răspunsuri și oferte
personalizate din template-urile și ofertele firmei. Trimiterea e un pas separat, cu confirmare.

## Instalare (Windows, Mac, Linux)

### Ce îți trebuie înainte

1. **Claude Code** instalat și logat cu contul tău claude.ai (`claude` în terminal pornește fără erori).
2. **Gmail conectat în claude.ai**: claude.ai → Settings → Connectors → Gmail → Connect → alegi contul
   firmei → Allow. Folosește același cont cu care intri în Claude Code.
3. **Python 3**: nu-l instala de mână. Îl verifică și îl instalează `/wizard-email:mail setup` (pasul 3).

### Pasul 1 — instalează pluginul

Deschide un terminal (Windows: Git Bash sau PowerShell · Mac: Terminal · Linux: orice terminal), pornește
`claude` din orice folder și scrie, pe rând:
```
/plugin marketplace add https://github.com/silviu-life/wizard-email.git
/plugin install wizard-email@wizard-email
```
Dacă te întreabă unde să-l instaleze, alege **User** (pentru tine, în orice folder).

Același lucru, direct din terminal, fără să pornești Claude Code:
```bash
claude plugin marketplace add https://github.com/silviu-life/wizard-email.git
claude plugin install wizard-email@wizard-email
```

### Pasul 2 — repornește Claude Code

`/exit`, apoi `claude`. Verifică: scrie `/wizard-email:mail` și trebuie să apară lista de comenzi.

### Pasul 3 — setup

```
/wizard-email:mail setup
```
Verifică Python (îl instalează dacă lipsește), conexiunea Gmail și pluginul, apoi creează folderul de date
`~/wizard-email`. La final afișează patru linii (`Python`, `Gmail`, `Plugin`, `Date`). Toate pe `OK`
înseamnă că poți trece la `/wizard-email:mail init`. Dacă una e `FIX`, urmează instrucțiunea afișată și
rulează setup din nou.

### Update și dezinstalare

```bash
claude plugin marketplace update wizard-email   # aduce versiunea nouă din GitHub
claude plugin update wizard-email@wizard-email
claude plugin uninstall wizard-email@wizard-email   # datele din ~/wizard-email rămân neatinse
```

## Pornire

```
/wizard-email:mail setup                           # Python, Gmail, folderul de date
/wizard-email:mail init /cale/catre/documente      # folder, PDF-uri, URL-uri; fără argument → interviu
/wizard-email:mail sync                            # inbox → contacte/<email>/
/wizard-email:mail classify --toate
/wizard-email:mail process                         # pe rând: ce a zis, cine e, ce-i răspund
/wizard-email:mail draft ana@firma.ro "răspunde la întrebarea de preț"
/wizard-email:mail send ana@firma.ro
```

## Unde stau datele

Global, într-un singur folder, indiferent din ce proiect pornești Claude Code:
`~/wizard-email` (Windows: `C:\Users\<tu>\wizard-email`). Alt loc → setează variabila `WIZARD_EMAIL_HOME`.
`python3 scripts/index.py --where` afișează folderul. Pluginul nu ține date în el, deci update-urile nu
ating nimic din ce e al tău.

Necesită connector-ul Gmail activ în Claude (claude.ai → Gmail). Outlook: când există connector, se
schimbă doar `mail-sync` și `mail-send`.

## Comenzi

| Comandă | Ce face |
|---|---|
| `/wizard-email:mail setup` | Python + Gmail + plugin + folderul de date; predă la init |
| `/wizard-email:mail init [surse]` | construiește `firma/`, `oferte/`, `reguli/`, `templates/` |
| `/wizard-email:mail sync [--zile N] [query]` | Gmail (default 360 zile, fără marketing) → `contacte/<email>/` |
| `/wizard-email:mail process [<email> \| --toate]` | emailurile pe rând: ce a zis, cine e, variante de răspuns |
| `/wizard-email:mail classify <email> \| --toate` | tip, segment, stadiu, personalitate |
| `/wizard-email:mail draft <email\|thread> [intenție]` | un Draft în Gmail, din template + ofertă |
| `/wizard-email:mail send <draft-id\|email>` | trimite un draft, după confirmare |
| `/wizard-email:mail followup [--zile N] [--draft]` | cine n-a răspuns |
| `/wizard-email:mail campaign <filtru> oferta=<id>` | drafturi în serie pe un segment |

## Organizare

```
.claude-plugin/            plugin.json + marketplace.json
skills/mail/reguli.md      reguli globale (le citește fiecare skill)
skills/mail-*/             un skill = un verb
scripts/index.py           generează contacte/_index.md + templates/_catalog.md, validează schema
~/wizard-email/{firma,oferte,reguli,templates,contacte}/   ← datele tale, create de init și sync
```

Schema fiecărui fișier: `skills/mail-init/assets/SCHEMA.md`. Biblioteca de template-uri (77
marketing + 20 discuții 1:1, toate în română): `skills/mail-init/assets/templates/`.

Verificare: `python3 scripts/index.py --check`. Test local fără instalare: `claude --plugin-dir .`.
