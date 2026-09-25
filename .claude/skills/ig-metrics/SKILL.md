---
name: ig-metrics
description: >-
  Lê as métricas reais do Instagram do jovvi (@jovvi.tcg) pelo conector
  windsor.ai que já está vinculado à conta do Claude, e entrega a tabela que o
  /ig-audit pede: múltiplo sobre a mediana, envios por alcance, retenção aos
  3 segundos, seguidores ganhos por post. Use sempre que o jovvi falar de
  métricas, insights, alcance, views, seguidores, "o que andou", "como foi o
  reel", "quantas views deu", "puxa os dados do instagram", "relatório da
  semana", "audit", ou antes de qualquer /ig-audit, /ig-plan ou /ig-viral que
  precise de evidência da própria conta. Também quando ele perguntar como
  vincular o instagram.
---

# ig-metrics

o pacote original não fala com o instagram. este skill é a ponte: o conector
windsor.ai da conta do claude já tem o instagram do jovvi vinculado, e é por
ele que as métricas entram. nada é postado, só lido.

## o que já está vinculado

- conector: `instagram` (windsor.ai, ferramentas `mcp__Windsor_ai__*`)
- conta: `17841480042928495`, "Joao Vitor (jovvi.tcg)"
- também conectados na mesma conta windsor: meta ads (2 contas) e tiktok
  orgânico ("Jovvi"). isso importa por causa do plano, veja abaixo.

se o jovvi perguntar "como vinculo meu insta", a resposta é: já está. se um
dia precisar reconectar, `get_connector_connect_info("instagram")` devolve o
link de autorização. nunca peça senha nem token no chat.

se as ferramentas `mcp__Windsor_ai__*` não estiverem na sessão, o conector não
está disponível ali. nesse caso caia no que o `/ig-audit` já faz: peça print
ou export dos insights.

## a trava do plano free

o plano Free do windsor inclui **1 conta conectada**. com 4 conectadas, as
leituras ficam pausadas e o conector devolve **zeros com um aviso em texto**
("These are not your real numbers: reads are paused"). isso parece dado e não
é. o `metrics.py` detecta e sai com código 3. regras:

- **nunca** apresente esses zeros como métrica.
- diga o que resolve: desconectar as outras contas em
  https://onboard.windsor.ai/app/ (mantendo só o instagram) ou fazer upgrade
  em https://onboard.windsor.ai/app/pricing. a escolha é dele.
- depois de ele mexer, rode de novo. `get_connectors()` mostra o que ficou.

## as três consultas

todas com `connector: "instagram"` e `accounts: ["17841480042928495"]`. salve
o `result` de cada uma em json, no repositório em `instagram/data/` (ou em
`~/.claude/instagram/data/` no pc).

**1. posts com insights** (`instagram/data/posts.json`), `date_preset: "last_90dT"`
(use `last_30dT` pra semana, `last_180dT` pra histórico):

```
timestamp, media_type, media_product_type, media_permalink, media_caption,
media_reach, media_views, media_total_like_count, media_total_comments_count,
media_saved, media_shares, media_reel_avg_watch_time, media_reel_skip_rate,
media_follows
```

**2. perfil** (`instagram/data/profile.json`), `date_preset: "last_7dT"`:

```
username, followers_count, follows_count, media_count, biography, website
```

**3. diário da conta** (`instagram/data/daily.json`), `date_preset: "last_30d"`,
em duas chamadas porque são tabelas diferentes:

```
date, reach, follower_count
date, views, accounts_engaged, likes, comments, saves, shares, total_interactions
```

os campos vêm de `get_fields("instagram")`. não invente nome de campo.

## depois de puxar

```bash
python3 metrics.py instagram/data/posts.json --followers {followers_count} \
    --tsv instagram/data/posts.tsv --out instagram/audit.md
python3 ../ig-viral/swipe.py instagram/data/posts.tsv      # fórmula e nota de gancho por post
```

o `metrics.py` imprime a tabela do `/ig-audit` já calculada: múltiplo sobre a
mediana da própria conta, envios por alcance, salvamentos por alcance,
seguidores por alcance, retenção aos 3s (1 menos a taxa de pulo do reel) e
tempo médio assistido. e compara o terço de cima com o de baixo.

com a tabela na mão, siga o `/ig-audit` a partir de "Then find the pattern".
o que ele chama de "non-follower reach" a api não devolve por post; diga isso
em vez de estimar.

## regras

- número que não veio do conector ou do jovvi não existe. `{{seu número}}` e
  flag, como no resto do pacote.
- `media_follows`, `media_profile_visits` e `media_profile_activity` não vêm
  pra reels. célula vazia, não zero.
- `media_reel_skip_rate` pode chegar como 0-100 ou 0-1. o script normaliza.
- métricas de post são acumuladas desde a publicação, não do período. o
  `date_preset` filtra quais posts entram, não quanto de cada post.
- `follower_count_1d` só cobre os últimos 30 dias e conta com menos de 100
  seguidores não recebe.
- a régua de "o que está funcionando" é a do `/ig-audit`: múltiplo e envios
  por alcance, nunca views cru.

## rotina

pra isso rodar sozinho (por exemplo toda sexta, antes do `/ig-audit`), o jovvi
pede e uma Routine é criada com este skill como prompt. não crie a rotina sem
ele pedir: ela guarda a permissão do conector.
