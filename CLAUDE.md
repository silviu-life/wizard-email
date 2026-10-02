# wizard-email — dezvoltare

Repo-ul ăsta e un plugin Claude Code (`.claude-plugin/`). Regulile de rulare ale sistemului sunt în
`skills/mail/reguli.md` (le citește fiecare skill). Datele utilizatorului NU stau aici, ci în
`~/wizard-email` (vezi `python3 scripts/index.py --where`).

Test local: `claude --plugin-dir .` apoi `/wizard-email:mail`. Verificare: `python3 scripts/index.py --check`.
La fiecare release: crește `version` în `.claude-plugin/plugin.json`.
