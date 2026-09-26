#!/usr/bin/env python3
"""
graph.py - puxa as métricas do @jovvi.tcg direto da api do instagram (a "api do
instagram com login do instagram", da meta), sem windsor, sem custo.

escreve os mesmos arquivos que o conector windsor escrevia, com os mesmos nomes
de campo, então o metrics.py lê sem mudar nada:

  instagram/data/posts.json             posts com insights (alcance, views, salvos, envios, tempo assistido)
  instagram/data/profile.json           seguidores, seguindo, posts, bio, link
  instagram/data/daily_reach.json       alcance e seguidores novos por dia
  instagram/data/daily_engagement.json  views, contas engajadas, curtidas, comentários, salvos, envios (total do período)
  instagram/data/audience.json          público por idade/gênero, país e cidade

o token vem da variável de ambiente IG_ACCESS_TOKEN (token de longa duração,
60 dias, gerado no painel do app em "configuração da api com login do
instagram" > "gerar tokens de acesso"). nunca vai em arquivo nem no chat.

uso
  python3 graph.py                          # últimos 90 dias de posts, 30 de diário
  python3 graph.py --days 180 --daily 30
  python3 graph.py --refresh                # renova o token e mostra a validade nova
  python3 graph.py --check                  # só confirma que o token funciona

sem dependências. só urllib.
"""

import argparse
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://graph.instagram.com/v23.0"
TOKEN_VAR = "IG_ACCESS_TOKEN"

# métricas por tipo de mídia. a api muda a lista de tempos em tempos, então o
# script tenta a lista cheia e, se a api reclamar, cai pra lista segura.
REEL_METRICS = ["reach", "views", "saved", "shares", "likes", "comments", "total_interactions",
                "ig_reels_avg_watch_time", "ig_reels_video_view_total_time"]
REEL_OPTIONAL = ["ig_reels_skip_rate"]           # se existir, vira a retenção aos 3s
FEED_METRICS = ["reach", "views", "saved", "shares", "likes", "comments", "total_interactions",
                "follows", "profile_visits", "profile_activity"]
FEED_SAFE = ["reach", "saved", "shares", "likes", "comments", "total_interactions"]
REEL_SAFE = ["reach", "saved", "shares", "likes", "comments", "total_interactions"]

ENGAGEMENT_TOTALS = ["views", "accounts_engaged", "likes", "comments", "saves", "shares",
                     "total_interactions", "profile_links_taps"]


class GraphError(Exception):
    pass


def get(base, path, token, **params):
    params["access_token"] = token
    url = f"{base}/{path.lstrip('/')}?{urllib.parse.urlencode(params, doseq=True)}"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            try:
                msg = json.loads(body).get("error", {}).get("message", body)
            except ValueError:
                msg = body
            if e.code in (429, 500, 502, 503) and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise GraphError(f"{e.code} em {path}: {msg}")
        except urllib.error.URLError as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise GraphError(f"rede em {path}: {e.reason}")


def paged(base, path, token, **params):
    """segue paging.next até acabar ou até o filtro de data mandar parar."""
    data = get(base, path, token, **params)
    while True:
        for item in data.get("data", []):
            yield item
        nxt = data.get("paging", {}).get("next")
        if not nxt:
            return
        with urllib.request.urlopen(nxt, timeout=60) as r:
            data = json.loads(r.read().decode("utf-8"))


def insights_for(base, media_id, product_type, token, want_skip=True):
    """devolve {metric: value} tentando a lista cheia e caindo pra segura."""
    is_reel = product_type == "REELS"
    attempts = []
    if is_reel:
        if want_skip:
            attempts.append(REEL_METRICS + REEL_OPTIONAL)
        attempts += [REEL_METRICS, REEL_SAFE]
    else:
        attempts += [FEED_METRICS, FEED_SAFE]
    last_err = None
    for metrics in attempts:
        try:
            data = get(base, f"{media_id}/insights", token, metric=",".join(metrics))
            out = {}
            for m in data.get("data", []):
                vals = m.get("values") or []
                out[m["name"]] = (vals[0].get("value") if vals else m.get("total_value", {}).get("value"))
            return out, None
        except GraphError as e:
            last_err = str(e)
            continue
    return {}, last_err


def fetch_posts(base, token, days, want_skip=True, log=print):
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)
    fields = "id,caption,media_type,media_product_type,permalink,timestamp,like_count,comments_count"
    rows, errors = [], []
    for m in paged(base, "me/media", token, fields=fields, limit=50):
        ts = dt.datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
        if ts < cutoff:
            break
        if m.get("media_product_type") == "STORY":
            continue
        ins, err = insights_for(base, m["id"], m.get("media_product_type"), token, want_skip)
        if err:
            errors.append({"id": m["id"], "permalink": m.get("permalink"), "error": err})
        skip = ins.get("ig_reels_skip_rate")
        rows.append({
            "timestamp": m["timestamp"],
            "media_type": m.get("media_type"),
            "media_product_type": m.get("media_product_type"),
            "media_permalink": m.get("permalink"),
            "media_caption": m.get("caption") or "",
            "media_reach": ins.get("reach"),
            "media_views": ins.get("views"),
            "media_total_like_count": m.get("like_count") if m.get("like_count") is not None else ins.get("likes"),
            "media_total_comments_count": m.get("comments_count") if m.get("comments_count") is not None else ins.get("comments"),
            "media_saved": ins.get("saved"),
            "media_shares": ins.get("shares"),
            "media_reel_avg_watch_time": ins.get("ig_reels_avg_watch_time"),
            "media_reel_total_watch_time": ins.get("ig_reels_video_view_total_time"),
            "media_reel_skip_rate": skip,
            "media_follows": ins.get("follows"),
            "media_profile_visits": ins.get("profile_visits"),
            "media_id": m["id"],
        })
        log(f"  {m['timestamp'][:10]}  {m.get('media_product_type'):<6} views={ins.get('views')} reach={ins.get('reach')}")
    return rows, errors


def fetch_profile(base, token):
    p = get(base, "me", token,
            fields="user_id,username,name,followers_count,follows_count,media_count,biography,website")
    return {"username": p.get("username"), "name": p.get("name"),
            "followers_count": p.get("followers_count"), "follows_count": p.get("follows_count"),
            "media_count": p.get("media_count"), "biography": p.get("biography"),
            "website": p.get("website"), "user_id": p.get("user_id") or p.get("id")}


def fetch_daily(base, token, days):
    until = dt.datetime.now(dt.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    since = until - dt.timedelta(days=days)
    out = {}
    for metric in ("reach", "follower_count"):
        try:
            data = get(base, "me/insights", token, metric=metric, period="day",
                       since=int(since.timestamp()), until=int(until.timestamp()))
        except GraphError as e:
            out.setdefault("_errors", []).append(str(e))
            continue
        for m in data.get("data", []):
            for v in m.get("values", []):
                day = v["end_time"][:10]
                out.setdefault(day, {"date": day})[metric] = v.get("value")
    rows = sorted((r for k, r in out.items() if k != "_errors"), key=lambda r: r["date"])
    return rows, out.get("_errors", [])


def fetch_engagement_totals(base, token, days):
    until = dt.datetime.now(dt.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    since = until - dt.timedelta(days=days)
    row = {"period": f"{since.date()} a {(until - dt.timedelta(days=1)).date()}"}
    errors = []
    for chunk in (ENGAGEMENT_TOTALS[:4], ENGAGEMENT_TOTALS[4:]):
        try:
            data = get(base, "me/insights", token, metric=",".join(chunk), period="day",
                       metric_type="total_value", since=int(since.timestamp()), until=int(until.timestamp()))
        except GraphError as e:
            errors.append(str(e))
            continue
        for m in data.get("data", []):
            row[m["name"]] = m.get("total_value", {}).get("value")
    return [row], errors


def fetch_audience(base, token):
    out, errors = {}, []
    for key, breakdown in (("gender_age", "age,gender"), ("country", "country"), ("city", "city")):
        try:
            data = get(base, "me/insights", token, metric="follower_demographics", period="lifetime",
                       metric_type="total_value", breakdown=breakdown)
        except GraphError as e:
            errors.append(str(e))
            continue
        result = {}
        for m in data.get("data", []):
            for bd in m.get("total_value", {}).get("breakdowns", []):
                for r in bd.get("results", []):
                    result[".".join(r.get("dimension_values", []))] = r.get("value")
        out[key] = result
    return out, errors


def refresh(base, token):
    data = get(base.rsplit("/v", 1)[0], "refresh_access_token", token, grant_type="ig_refresh_token")
    return data


def main():
    ap = argparse.ArgumentParser(description="Métricas do instagram direto da api da meta.")
    ap.add_argument("--days", type=int, default=90, help="janela de posts (padrão 90)")
    ap.add_argument("--daily", type=int, default=30, help="janela do diário da conta (padrão 30, máximo 30)")
    ap.add_argument("--out-dir", default="instagram/data")
    ap.add_argument("--base-url", default=BASE)
    ap.add_argument("--no-skip", action="store_true", help="não tenta a métrica de skip rate")
    ap.add_argument("--check", action="store_true", help="só valida o token")
    ap.add_argument("--refresh", action="store_true", help="renova o token de longa duração")
    args = ap.parse_args()

    token = os.environ.get(TOKEN_VAR)
    if not token:
        sys.exit(f"sem token: defina a variável de ambiente {TOKEN_VAR} (configurações do ambiente, "
                 "nunca no chat nem em arquivo do repositório)")
    base = args.base_url.rstrip("/")

    if args.refresh:
        data = refresh(base, token)
        days = int(data.get("expires_in", 0)) // 86400
        print(f"token renovado, vale mais {days} dias. troque o valor de {TOKEN_VAR} nas configurações "
              "do ambiente pelo novo token (ele foi impresso só aqui, com os 8 primeiros caracteres):")
        print("  ", str(data.get("access_token", ""))[:8] + "…  (o token inteiro está no json abaixo)")
        print(json.dumps({"access_token": data.get("access_token"), "expires_in": data.get("expires_in")}))
        return

    try:
        profile = fetch_profile(base, token)
    except GraphError as e:
        sys.exit(f"token não funcionou: {e}")
    print(f"ok: @{profile['username']}  seguidores={profile['followers_count']}  posts={profile['media_count']}")
    if args.check:
        return

    os.makedirs(args.out_dir, exist_ok=True)

    def dump(name, rows, extra=None):
        path = os.path.join(args.out_dir, name)
        payload = {"result": rows}
        if extra:
            payload.update(extra)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=1)
        print(f"escrito {path}")

    dump("profile.json", [profile])

    print(f"posts dos últimos {args.days} dias:")
    posts, errs = fetch_posts(base, token, args.days, want_skip=not args.no_skip)
    dump("posts.json", posts, {"errors": errs} if errs else None)
    if errs:
        print(f"  {len(errs)} post(s) sem insights (ver 'errors' no json)")

    daily, errs = fetch_daily(base, token, min(args.daily, 30))
    dump("daily_reach.json", daily, {"errors": errs} if errs else None)

    totals, errs = fetch_engagement_totals(base, token, min(args.daily, 30))
    dump("daily_engagement.json", totals, {"errors": errs} if errs else None)

    audience, errs = fetch_audience(base, token)
    dump("audience.json", [audience], {"errors": errs} if errs else None)

    print("\nagora: python3 .claude/skills/ig-metrics/metrics.py instagram/data/posts.json "
          f"--followers {profile['followers_count']} --tsv instagram/data/posts.tsv --out instagram/audit.md")


if __name__ == "__main__":
    main()
