"""Gera painel/index.html a partir de painel/posts.json + o que existe nas pastas.

Rodar:  python painel/gerar.py   (de qualquer pasta)
A verdade (status, datas, notas, pendências, números, decisões) mora no posts.json.
Imagens, vídeos, legendas e roteiros são lidos das pastas de cada post.
O visual e o comportamento ficam em _modelo.html (recebe os dados como JSON).
"""
import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAINEL = ROOT / "painel"
IMG = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
VID = {".mp4", ".mov", ".webm"}
SKIP_DIRS = {"mock-cru", "fonte", "prints", "captura"}

STATUS = {
    "ideia": "ideia",
    "roteiro": "roteiro",
    "material": "falta gravar/narrar",
    "aprovar": "pra você aprovar",
    "pronto": "pronto pra postar",
    "postado": "postado",
    "confirmar": "confirmar se saiu",
    "reserva": "reserva",
    "arquivo": "arquivo",
}
e = html.escape


def md(text: str) -> str:
    """Markdown mínimo: títulos, tabelas, listas, negrito, itálico, código, parágrafos."""
    def inline(s: str) -> str:
        s = e(s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
        s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
        return s

    out, lines, i = [], text.replace("\r\n", "\n").split("\n"), 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", ln)
        if m:
            lvl = min(len(m.group(1)) + 2, 6)
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1
            continue
        if ln.lstrip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            if rows:
                head, body = rows[0], rows[1:]
                t = "<div class='tw'><table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
                t += "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
                out.append(t + "</tbody></table></div>")
            continue
        if re.match(r"^\s*([-*]|\d+\.)\s+", ln):
            ordered = bool(re.match(r"^\s*\d+\.", ln))
            items = []
            while i < len(lines) and re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                item = re.sub(r"^\s*([-*]|\d+\.)\s+", "", lines[i])
                i += 1
                while i < len(lines) and lines[i].startswith("   ") and lines[i].strip():
                    item += " " + lines[i].strip()
                    i += 1
                items.append(f"<li>{inline(item)}</li>")
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue
        para = [ln]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||\s*([-*]|\d+\.)\s)", lines[i]):
            para.append(lines[i])
            i += 1
        out.append("<p>" + "<br>".join(inline(p) for p in para) + "</p>")
    return "\n".join(out)


def url(p: Path) -> str:
    return "../" + p.relative_to(ROOT).as_posix()


def collect(pasta: str | None) -> dict:
    res = {"slides": [], "folhas": [], "videos": [], "extras": []}
    if not pasta or not (ROOT / pasta).is_dir():
        return res
    d = ROOT / pasta
    for f in sorted(d.rglob("*")):
        rel_parts = f.relative_to(d).parts
        if not f.is_file() or any(part in SKIP_DIRS for part in rel_parts[:-1]):
            continue
        ext = f.suffix.lower()
        item = {"url": url(f), "nome": f.relative_to(d).as_posix()}
        if ext in VID:
            res["videos"].append(item)
        elif ext in IMG:
            if f.stem.startswith("folha"):
                res["folhas"].append(item)
            elif f.parent == d:
                res["slides"].append(item)
            else:
                res["extras"].append(item)
    return res


def read(pasta: str | None, name: str | None) -> str | None:
    if not pasta or not name:
        return None
    p = ROOT / pasta / name
    return p.read_text(encoding="utf-8") if p.is_file() else None


def main():
    cfg = json.loads((PAINEL / "posts.json").read_text(encoding="utf-8"))
    items = []
    for p in cfg["posts"]:
        m = collect(p.get("pasta"))
        rot = read(p.get("pasta"), p.get("roteiro"))
        capa = ROOT / p["pasta"] / p["capa"] if p.get("capa") and p.get("pasta") else None
        thumb = {"url": url(capa)} if capa and capa.is_file() else (m["slides"] or [x for x in m["extras"] if x["nome"].count("/") == 1] or m["extras"] or [None])[0]
        items.append({
            **{k: p.get(k) for k in ("id", "tipo", "titulo", "data", "ate", "hora", "status", "meta", "notas", "pendencias", "metricas", "fonte")},
            "statusLabel": STATUS.get(p.get("status"), p.get("status")),
            "pasta": url(ROOT / p["pasta"]) + "/" if p.get("pasta") and (ROOT / p["pasta"]).is_dir() else None,
            "legenda": (read(p.get("pasta"), p.get("legenda")) or "").strip() or None,
            "roteiroHtml": md(rot) if rot else None,
            "roteiroNome": p.get("roteiro"),
            "thumb": thumb["url"] if thumb else None,
            **m,
        })
    plano = cfg["semana"].get("plano")
    data = {
        "gerado": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "semana": cfg["semana"],
        "decisoes": cfg.get("decisoes", []),
        "aprendizados": cfg.get("aprendizados", []),
        "planoHtml": md((ROOT / plano).read_text(encoding="utf-8")) if plano and (ROOT / plano).is_file() else "",
        "posts": items,
    }
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    tpl = (PAINEL / "_modelo.html").read_text(encoding="utf-8")
    (PAINEL / "index.html").write_text(tpl.replace("/*__DATA__*/null", blob), encoding="utf-8")
    print(f"painel/index.html · {len(items)} posts")


if __name__ == "__main__":
    main()
