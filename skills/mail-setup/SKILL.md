---
name: mail-setup
description: Pregătește calculatorul pentru sistemul de email — verifică și instalează Python 3 (Windows, Mac, Linux), verifică connector-ul Gmail din claude.ai validează pluginul și pregătește folderul global de date, apoi predă la `/wizard-email:mail init`. Folosește la `/wizard-email:mail setup`, „instalează ce trebuie", „pregătește-mi calculatorul", „nu merge python", „verifică dacă e totul instalat", „am instalat pluginul, ce fac acum", set up, install requirements. Rulabil oricând, de câte ori vrei. Nu citește și nu trimite emailuri, nu scrie în `firma/` sau `contacte/`.
---

# /wizard-email:mail setup — calculatorul gata de lucru

> **Înainte de orice:** citește `${CLAUDE_PLUGIN_ROOT}/skills/mail/reguli.md` — unde stau datele (`$DATA`) și regulile dure.

**Regula de limbă, o dată:** vorbești română, pe înțelesul unui om care n-a mai deschis un terminal.
Explici fiecare pas într-o frază înainte să-l rulezi. Nu ceri nimic ce poți verifica singur.

## Pas 1 — sistemul de operare

`uname -s`. `MINGW*` / `MSYS*` / `CYGWIN*` → **Windows** (Git Bash). `Darwin` → **Mac**. `Linux` → **Linux**.

## Pas 2 — Python 3

Test (singurul considerat valid, pentru că stub-ul Microsoft Store poate exista fără Python):
```bash
python3 -c "import sys; assert sys.version_info >= (3, 8); print(sys.version.split()[0])"
```
Exit 0 → `Python: OK (<versiune>)`, sari la Pas 3. Altfel, după OS. Orice STOP din pasul ăsta afișează
întâi raportul (Pas 6) cu `Python: FIX (<ce faci>)`, `Gmail: —`, `Plugin: —`, `Date: —` (se verifică la rularea următoare).

**Windows**
1. Dacă `py -3 --version` sau `python --version` (versiune ≥ 3.8, nu mesajul „Python was not found")
   funcționează, Python există dar lipsește comanda `python3` → mergi la 3.
2. Altfel spune „Instalez Python 3.13 din Microsoft Store, prin winget (1-2 minute)" și rulează:
   ```bash
   winget install --id 9PNRBTZXMB4Z --source msstore --accept-package-agreements --accept-source-agreements
   ```
   `winget` lipsă sau eșuat → cere-i să instaleze manual: Microsoft Store → caută „Python 3.13" → Get.
   Apoi: „Închide Claude Code (scrie /exit), deschide-l din nou (din orice folder) și rulează iar
   `/wizard-email:mail setup`." STOP.
3. Shim, când Python există sub alt nume (`<cmd>` = `py -3` sau `python`, primul care a mers):
   ```bash
   mkdir -p ~/bin && printf '#!/bin/sh\nexec <cmd> "$@"\n' > ~/bin/python3 && chmod +x ~/bin/python3
   grep -q 'HOME/bin' ~/.bashrc 2>/dev/null || echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
   ```
   Reia testul cu `~/bin/python3` în loc de `python3`. Merge → „Închide Claude Code (/exit), deschide-l
   din nou și rulează iar `/wizard-email:mail setup`." STOP.

**Mac**
- Pe un Mac nou, testul poate deschide fereastra Apple „install the command line developer tools". Spune-i:
  „Dacă a apărut o fereastră care îți cere să instalezi Command Line Tools, apasă Install. Durează 10-20 de
  minute și aduce și Python. Când termină, redeschide Claude Code și rulează iar `/wizard-email:mail setup`." STOP.
  Dacă a apăsat Cancel sau fereastra n-a apărut, continuă mai jos.
- `brew --version` merge → `brew install python`, apoi reia testul.
- Fără Homebrew → deschide `https://www.python.org/downloads/macos/` (`open <url>`), spune-i să descarce
  „macOS 64-bit universal2 installer", să-l ruleze cu Continue, Agree, Install și parola Mac-ului, apoi să
  redeschidă Claude Code și să ruleze iar `/wizard-email:mail setup`. STOP.

**Linux** → `sudo apt install -y python3` (sau managerul distribuției), reia testul.

## Pas 3 — Gmail

Apelează unealta Gmail `list_labels` (doar citește etichetele, nu atinge emailurile).
- Răspunde cu o listă → `Gmail: OK`.
- Unealta nu există sau dă eroare de autorizare → `Gmail: FIX` și explică, numerotat:
  1. Deschide claude.ai în browser, cu același cont cu care ai intrat în Claude Code.
  2. Settings → Connectors → Gmail → Connect → alege contul de Gmail al firmei → Allow.
  3. Revino aici, scrie `/mcp` și verifică că apare Gmail. Dacă nu apare: `/exit`, deschide iar `claude`.
  4. Rulează din nou `/wizard-email:mail setup`.

## Pas 4 — pluginul

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/index.py" --check`. Exit 0 → `Plugin: OK`. Altfel `Plugin: FIX` + primele 5 linii de
eroare și sugestia: „Reinstalează pluginul: `/plugin uninstall wizard-email`, apoi `/plugin install wizard-email@wizard-email`."

## Pas 5 — folderul de date (global)

Spune: „Datele tale (firma, ofertele, contactele) stau într-un singur folder, accesibil din orice proiect."
Rulează `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/index.py" --setup`. Creează folderul (`$DATA`) și îl adaugă
în `~/.claude/settings.json` la `permissions.additionalDirectories`, ca să nu ceară aprobare la fiecare
scriere. Exit 0 → `Date: OK (<cale>)`. Altfel `Date: FIX` + mesajul scriptului.

**Date vechi:** dacă folderul curent are `firma/profil.md` (versiunea veche, pe proiect) și `$DATA/firma/`
nu există → AskUserQuestion „Mut datele din <folder curent> în <$DATA>?". Da → pentru fiecare dintre
`firma oferte reguli templates contacte` care există: `mv "<folder curent>/<x>" "$DATA/"`, apoi
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/index.py"`. Nu muta nimic fără „da".

## Pas 6 — raport

Exact patru linii, apoi următorul pas:
```
Python: OK|FIX (<detaliu>)
Gmail: OK|FIX|—
Plugin: OK|FIX|—
Date: OK (<cale>)|FIX|—
```
Toate OK → „Calculatorul e gata. Următorul pas: `/wizard-email:mail init` — construim profilul firmei și vocea ta."
Dacă `$DATA/firma/profil.md` există deja → „Sistemul e deja inițializat. Poți rula `/wizard-email:mail sync`."
Orice FIX → repetă doar instrucțiunea pentru acel FIX. STOP.
