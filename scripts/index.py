#!/usr/bin/env python3
"""Generează contacte/_index.md și templates/_catalog.md din frontmatter-e și validează după SCHEMA.md.

Folosire:  python3 scripts/index.py [--root DIR]   (default: folderul proiectului)
           python3 scripts/index.py --check         (self-check pe assets-urile din mail-init)
Exit 1 dacă există probleme de validare (câmp obligatoriu lipsă sau valoare nepermisă).
"""
import re, sys, shutil, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / ".claude/skills/mail-init/assets"

# Regulile de validare. Sursa umană e assets/SCHEMA.md; ținem-le sincronizate manual.
# ponytail: reguli hardcodate; parsăm SCHEMA.md dacă apar >2 tipuri noi de fișiere.
STADII = ["nou", "in-discutie", "oferta-trimisa", "negociere", "castigat", "pierdut"]
TIPURI = ["lead", "client", "fost-client", "partener", "furnizor", "ignora"]
CATEGORII = ["discutii", "01_customer_acquisition", "02_lead_nurturing",
             "03_conversion_sales", "04_customer_success", "05_community_engagement"]
RULES = {
    "contact": {"required": ["email", "creat", "sursa"],
                "allowed": {"tip": TIPURI, "stadiu": STADII, "sursa": ["gmail", "import", "manual"]}},
    "template": {"required": ["id", "categorie", "scop"],
                 "allowed": {"categorie": CATEGORII, "oferta": ["true", "false"]}},
}


def frontmatter(path):
    """YAML minimal: `cheie: valoare` pe o linie, liste inline [a, b], ghilimele opționale.
    ponytail: parser pe o linie; PyYAML dacă apar valori multi-linie."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        k, sep, v = line.partition(":")
        if not sep or not k.strip() or line.startswith(" "):
            continue
        v = v.split("  #")[0].strip()          # comentariu inline
        v = v.strip('"').strip("'")
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip().strip('"').strip("'") for x in v[1:-1].split(",") if x.strip()]
        fm[k.strip()] = v
    return fm


def validate(kind, fm, rel):
    probs = []
    if fm is None:
        return [(rel, "frontmatter", "lipsește sau e malformat")]
    for k in RULES[kind]["required"]:
        if not fm.get(k):
            probs.append((rel, k, "obligatoriu, lipsește"))
    for k, allowed in RULES[kind]["allowed"].items():
        v = fm.get(k, "")
        if v and str(v) not in allowed:
            probs.append((rel, k, f"valoare nepermisă „{v}” (permise: {', '.join(allowed)})"))
    return probs


def cell(v):
    if isinstance(v, list):
        v = ", ".join(v)
    return (v or "—").replace("|", "\\|")


def build(root):
    problems = []
    # --- contacte
    contacte = root / "contacte"
    rows = []
    if contacte.is_dir():
        for p in sorted(contacte.glob("*/profile.md")):
            rel = p.relative_to(root).as_posix()
            fm = frontmatter(p)
            pr = validate("contact", fm, rel)
            if fm is not None and fm.get("email") and fm["email"] != p.parent.name:
                pr.append((rel, "email", f"diferă de numele folderului „{p.parent.name}”"))
            problems += pr
            fm = fm or {}
            rows.append((fm.get("ultima_interactiune", "") or fm.get("creat", ""),
                         ("⚠ " if pr else "") + cell(p.parent.name), cell(fm.get("nume")), cell(fm.get("firma")),
                         cell(fm.get("tip")), cell(fm.get("segment")), cell(fm.get("stadiu", "nou")),
                         cell(fm.get("ultima_interactiune")), cell(fm.get("urmatorul_pas_data"))))
        rows.sort(key=lambda r: r[0], reverse=True)
        out = ["# Contacte", "", "Generat de `scripts/index.py`. Nu edita de mână.", "",
               "| email | nume | firmă | tip | segment | stadiu | ultima interacțiune | următorul pas |",
               "|---|---|---|---|---|---|---|---|"]
        out += ["| " + " | ".join(r[1:]) + " |" for r in rows]
        (contacte / "_index.md").write_text("\n".join(out) + problems_section([p for p in problems if p[0].startswith("contacte/")]) + "\n", encoding="utf-8")
    # --- templates
    templates = root / "templates"
    trows = []
    if templates.is_dir():
        for p in sorted(templates.rglob("*.md")):
            if p.name.startswith("_"):
                continue
            rel = p.relative_to(root).as_posix()
            fm = frontmatter(p)
            pr = validate("template", fm, rel)
            expected = p.relative_to(templates).as_posix()[:-3]
            if fm is not None and fm.get("id") and fm["id"] != expected:
                pr.append((rel, "id", f"ar trebui să fie „{expected}”"))
            problems += pr
            fm = fm or {}
            trows.append((("⚠ " if pr else "") + cell(fm.get("id") or expected), cell(fm.get("categorie")),
                          cell(fm.get("scop")), cell(fm.get("cand")), cell(fm.get("stadii")), cell(fm.get("oferta", "false"))))
        out = ["# Catalog template-uri", "", "Generat de `scripts/index.py`. Nu edita de mână. "
               "Alege de aici, apoi citește UN singur fișier.", "",
               "| id | categorie | scop | când | stadii | ofertă |", "|---|---|---|---|---|---|"]
        out += ["| " + " | ".join(r) + " |" for r in trows]
        (templates / "_catalog.md").write_text("\n".join(out) + problems_section([p for p in problems if p[0].startswith("templates/")]) + "\n", encoding="utf-8")
    return len(rows), len(trows), problems


def problems_section(problems):
    if not problems:
        return ""
    out = ["", "", "## Probleme", "", "| fișier | câmp | problemă |", "|---|---|---|"]
    out += [f"| {a} | {b} | {c} |" for a, b, c in problems]
    return "\n".join(out)


def check():
    """Self-check: rulează pe assets într-un folder temporar; nimic din assets nu e modificat."""
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        shutil.copytree(ASSETS / "exemple/contacte", tmp / "contacte")
        shutil.copytree(ASSETS / "templates", tmp / "templates")
        n, t, problems = build(tmp)
        idx = (tmp / "contacte/_index.md").read_text(encoding="utf-8")
        cat = (tmp / "templates/_catalog.md").read_text(encoding="utf-8")
        assert n == 2 and "| ana.popescu@exemplu.ro | Ana Popescu |" in idx, idx
        assert "⚠ incomplet@test.ro" in idx
        bad = {(p[1], p[2].split(" ")[0]) for p in problems if "incomplet@test.ro" in p[0]}
        assert bad == {("sursa", "obligatoriu,"), ("stadiu", "valoare")}, bad
        assert not [p for p in problems if "incomplet@test.ro" not in p[0]], problems
        assert t >= 77 and "| marketing/01_customer_acquisition/cold_outreach/01_problem_solver |" in cat
        print(f"OK: {n} contacte, {t} template-uri, {len(problems)} probleme (toate din fixture-ul incomplet)")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--check" in args:
        check()
        sys.exit(0)
    root = Path(args[args.index("--root") + 1]) if "--root" in args else ROOT
    n, t, problems = build(root)
    print(f"contacte: {n} · template-uri: {t} · probleme: {len(problems)}")
    for rel, k, msg in problems:
        print(f"  ⚠ {rel} · {k} · {msg}")
    sys.exit(1 if problems else 0)
