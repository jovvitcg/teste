#!/usr/bin/env python3
"""
metrics.py - transforma o que o conector windsor.ai devolve do instagram
(get_data, connector "instagram") na tabela que o /ig-audit pede e no TSV
que o swipe.py lê.

o ponto é o mesmo do swipe.py: views cru não é evidência. este script calcula,
por post, o múltiplo sobre a mediana da própria conta, envios por alcance,
salvamentos por alcance, seguidores ganhos por alcance e, nos reels, a
retenção nos 3 segundos e o tempo médio assistido.

entrada: o json do get_data (o objeto inteiro com "result", ou só a lista).
campos esperados por post:
  timestamp, media_type, media_product_type, media_permalink, media_caption,
  media_reach, media_views, media_total_like_count, media_total_comments_count,
  media_saved, media_shares, media_reel_avg_watch_time, media_reel_skip_rate,
  media_follows

uso
  python3 metrics.py posts.json
  python3 metrics.py posts.json --followers 3200 --account @jovvi.tcg
  python3 metrics.py posts.json --tsv posts.tsv        # pro swipe.py
  python3 metrics.py posts.json --out audit.md         # relatório em markdown
  python3 metrics.py posts.json --json

sai com código 3 quando o conector devolveu números falsos (leituras
pausadas). nesse caso não há o que auditar, e a mensagem diz o que fazer.
"""

import argparse
import json
import os
import statistics
import sys

PAUSED_MARKERS = ("not your real numbers", "reads are paused")


def load(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    data = json.loads(raw)
    if isinstance(data, dict):
        data = data.get("result", data.get("data", []))
    if not isinstance(data, list):
        sys.exit("entrada inválida: esperava uma lista de posts ou um objeto com \"result\"")
    return data


def paused_message(rows):
    for r in rows:
        for v in r.values():
            if isinstance(v, str) and any(m in v.lower() for m in PAUSED_MARKERS):
                return v
    return None


def num(v):
    try:
        return float(v) if v not in (None, "") else 0.0
    except (TypeError, ValueError):
        return 0.0


def hook_of(caption):
    if not caption or not str(caption).strip():
        return "(sem legenda)"
    first = str(caption).strip().splitlines()[0].strip()
    if not first:
        return "(sem legenda)"
    return first[:117] + "..." if len(first) > 120 else first


def counts(items):
    out = {}
    for p in items:
        out[p["type"] or "?"] = out.get(p["type"] or "?", 0) + 1
    return out


def build(rows, followers=None, account=""):
    posts = []
    for r in rows:
        views = num(r.get("media_views"))
        reach = num(r.get("media_reach"))
        is_reel = r.get("media_type") == "REEL" or r.get("media_product_type") == "REELS"
        skip_raw = r.get("media_reel_skip_rate")
        skip = num(skip_raw)
        if skip > 1:                     # a api ora manda 0-100, ora 0-1
            skip = skip / 100.0
        hold = (1 - skip) if (is_reel and skip_raw not in (None, "")) else None
        watch_ms = num(r.get("media_reel_avg_watch_time"))
        shares = num(r.get("media_shares"))
        saves = num(r.get("media_saved"))
        follows = num(r.get("media_follows"))
        posts.append({
            "date": (r.get("timestamp") or "")[:10],
            "type": r.get("media_type") or "",
            "permalink": r.get("media_permalink") or "",
            "hook": hook_of(r.get("media_caption")),
            "views": int(views),
            "reach": int(reach),
            "likes": int(num(r.get("media_total_like_count"))),
            "comments": int(num(r.get("media_total_comments_count"))),
            "saves": int(saves),
            "shares": int(shares),
            "follows": None if is_reel else int(follows),   # a api não dá follows pra reel
            "hold_3s": hold,
            "avg_watch_s": (watch_ms / 1000.0) if (is_reel and watch_ms) else None,
            "sends_per_reach": (shares / reach) if reach else None,
            "saves_per_reach": (saves / reach) if reach else None,
            "follows_per_reach": None if is_reel else ((follows / reach) if reach else None),
        })
    views_list = [p["views"] for p in posts if p["views"] > 0]
    median = statistics.median(views_list) if views_list else 0
    for p in posts:
        p["outlier"] = round(p["views"] / median, 2) if median else None
    ranked = sorted(posts, key=lambda p: -(p["outlier"] or 0))
    third = max(1, len(ranked) // 3)
    top, bottom = ranked[:third], ranked[-third:]

    def med(items, key):
        vals = [i[key] for i in items if i.get(key) is not None]
        return statistics.median(vals) if vals else None

    keys = ("hold_3s", "avg_watch_s", "sends_per_reach", "saves_per_reach", "follows_per_reach")
    return {
        "account": account,
        "followers": followers,
        "n": len(ranked),
        "median_views": median,
        "posts": ranked,
        "by_sends": sorted([p for p in posts if p["sends_per_reach"] is not None],
                           key=lambda p: -p["sends_per_reach"])[:5],
        "top_vs_bottom": {k: (med(top, k), med(bottom, k)) for k in keys},
        "formats": {"top": counts(top), "bottom": counts(bottom)},
    }


def pct(x):
    return f"{x * 100:5.1f}%" if x is not None else "    - "


def secs(x):
    return f"{x:5.1f}s" if x is not None else "    - "


def render(a, out=sys.stdout):
    head = (f"AUDIT  ·  {a['n']} posts  ·  {a['account'] or 'conta'}  ·  "
            f"mediana de views {int(a['median_views']):,}"
            + (f"  ·  seguidores {a['followers']:,}" if a["followers"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 96), file=out)
    print(f"  {'mult':>6}  {'views':>8}  {'alcance':>8}  {'env/alc':>7}  {'salv/alc':>8}  "
          f"{'seg/alc':>7}  {'hold3s':>6}  {'tempo':>6}  {'tipo':<8} {'data':<10} hook", file=out)
    for p in a["posts"]:
        mult = f"{p['outlier']:.1f}x" if p["outlier"] else "    ?"
        hold = f"{p['hold_3s'] * 100:5.0f}%" if p["hold_3s"] is not None else "    - "
        print(f"  {mult:>6}  {p['views']:>8,}  {p['reach']:>8,}  {pct(p['sends_per_reach']):>7}  "
              f"{pct(p['saves_per_reach']):>8}  {pct(p['follows_per_reach']):>7}  {hold:>6}  "
              f"{secs(p['avg_watch_s']):>6}  {p['type'][:8]:<8} {p['date']:<10} "
              f"\"{p['hook'][:60]}\"", file=out)
    print("-" * max(len(head), 96), file=out)
    print("TERÇO DE CIMA vs TERÇO DE BAIXO (mediana), ranqueado por múltiplo sobre a mediana de views",
          file=out)
    labels = {"hold_3s": "retenção aos 3s", "avg_watch_s": "tempo médio assistido",
              "sends_per_reach": "envios por alcance", "saves_per_reach": "salvamentos por alcance",
              "follows_per_reach": "seguidores por alcance"}
    fmt = {"hold_3s": pct, "avg_watch_s": secs, "sends_per_reach": pct,
           "saves_per_reach": pct, "follows_per_reach": pct}
    for k, (t, b) in a["top_vs_bottom"].items():
        print(f"  {labels[k]:<26} cima {fmt[k](t).strip():>7}   baixo {fmt[k](b).strip():>7}", file=out)
    print(f"  {'formato':<26} cima {a['formats']['top']}   baixo {a['formats']['bottom']}", file=out)
    if a["by_sends"]:
        print("\nTOP 5 POR ENVIOS POR ALCANCE (o sinal mais forte que um post ganha)", file=out)
        for p in a["by_sends"]:
            print(f"  {pct(p['sends_per_reach']).strip():>6}  {p['shares']:>5} envios / {p['reach']:>7,} alcance  "
                  f"\"{p['hook'][:70]}\"", file=out)
    notes = []
    if a["n"] < 10:
        notes.append(f"{a['n']} posts é pouco pra concluir. Dez é o mínimo, trinta é onde o padrão aparece.")
    t, b = a["top_vs_bottom"]["hold_3s"]
    if t is not None and b is not None and t - b >= 0.10:
        notes.append("Retenção aos 3s separa cima e baixo por 10 pontos ou mais: é o gancho, e o resto é distração.")
    notes.append("Views cru é o número menos útil da tela. Ranqueie por múltiplo e por envios por alcance.")
    print("", file=out)
    for n in notes:
        print(f"  - {n}", file=out)
    print("", file=out)


def to_tsv(a):
    lines = ["account\tfollowers\tmedian\tviews\thook"]
    for p in a["posts"]:
        if p["views"] > 0:
            lines.append("\t".join([
                a["account"] or "",
                str(a["followers"] or ""),
                str(int(a["median_views"])),
                str(p["views"]),
                p["hook"].replace("\t", " "),
            ]))
    return "\n".join(lines) + "\n"


def to_markdown(a):
    lines = ["# audit do instagram", "",
             f"{a['n']} posts de {a['account'] or 'conta'}. mediana de views {int(a['median_views']):,}."
             + (f" seguidores {a['followers']:,}." if a["followers"] else ""), "",
             "| mult | views | alcance | envios/alc | salv/alc | seg/alc | hold 3s | tempo | tipo | data | hook |",
             "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for p in a["posts"]:
        mult = f"{p['outlier']:.1f}x" if p["outlier"] else "?"
        hold = f"{p['hold_3s'] * 100:.0f}%" if p["hold_3s"] is not None else "-"
        lines.append(f"| {mult} | {p['views']:,} | {p['reach']:,} | {pct(p['sends_per_reach']).strip()} | "
                     f"{pct(p['saves_per_reach']).strip()} | {pct(p['follows_per_reach']).strip()} | {hold} | "
                     f"{secs(p['avg_watch_s']).strip()} | {p['type']} | {p['date']} | "
                     f"[{p['hook'][:60]}]({p['permalink']}) |")
    lines += ["", "## terço de cima vs terço de baixo", ""]
    for k, (t, b) in a["top_vs_bottom"].items():
        f = secs if k == "avg_watch_s" else pct
        lines.append(f"- {k}: cima {f(t).strip()}, baixo {f(b).strip()}")
    lines.append(f"- formato: cima {a['formats']['top']}, baixo {a['formats']['bottom']}")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Métricas do instagram (windsor.ai) na tabela do /ig-audit.")
    ap.add_argument("input", nargs="?", default="-", help="json do get_data, ou - pra stdin")
    ap.add_argument("--followers", type=int, help="followers_count do perfil (segunda consulta)")
    ap.add_argument("--account", default="@jovvi.tcg", help="handle, vai na coluna account do TSV")
    ap.add_argument("--tsv", help="escreve o TSV que o swipe.py lê")
    ap.add_argument("--out", help="escreve o relatório em markdown")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = load(args.input)
    msg = paused_message(rows)
    if msg:
        print("LEITURAS PAUSADAS NO WINDSOR.AI. estes não são números reais, não use.\n"
              f"  o conector disse: {msg}\n"
              "  o plano Free inclui 1 conta. desconecte as outras em https://onboard.windsor.ai/app/ "
              "(mantendo só o instagram @jovvi.tcg) ou faça upgrade, e rode de novo.",
              file=sys.stderr)
        sys.exit(3)
    if not rows:
        print("nenhum post no período. amplie o date_preset (ex.: last_180dT).", file=sys.stderr)
        sys.exit(2)
    if all(num(r.get("media_views")) == 0 and num(r.get("media_reach")) == 0 for r in rows):
        print("todos os posts vieram com views e alcance zero. isso é sinal de leitura pausada ou "
              "de conta sem permissão de insights. confira antes de auditar.", file=sys.stderr)
        sys.exit(3)

    a = build(rows, followers=args.followers, account=args.account)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    if args.tsv:
        path = os.path.expanduser(args.tsv)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        open(path, "w", encoding="utf-8").write(to_tsv(a))
        print(f"tsv escrito em {path}", file=sys.stderr)
    if args.out:
        path = os.path.expanduser(args.out)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        open(path, "w", encoding="utf-8").write(to_markdown(a))
        print(f"relatório escrito em {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
