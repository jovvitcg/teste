# teste (jovvi tcg)

este repositório guarda o pacote instagram-agent-skill (13 skills `ig-*`, de
jake schincariol, licença MIT), mais o `ig-metrics` que lê as métricas pelo
conector windsor.ai, adaptado pro jovvi, criador de conteúdo de
pokémon tcg no brasil (@jovvi.tcg).

## regras pra qualquer skill `ig-*` rodando aqui

- idioma: português brasileiro, sempre. lowercase por padrão, sem travessão,
  concordância masculina. o detalhe todo está em `instagram/voice.md`. leia
  esse arquivo antes de escrever qualquer roteiro, legenda, comentário ou dm.
- onde um SKILL.md fala em `~/.claude/instagram/<arquivo>` (voice.md, swipe.md,
  log.md, plan.md), use `instagram/<arquivo>` deste repositório quando o
  caminho da home não existir. neste repo a pasta `instagram/` é a fonte da
  verdade.
- as ferramentas python de cada skill rodam a partir da pasta da skill, por
  exemplo `python3 .claude/skills/ig-reel/hookscore.py hooks.txt`. python 3.8+
  sem dependências, nada sobe pra internet.
- nada é publicado no instagram. toda skill termina num bloco pronto pra
  copiar, e quem posta é o jovvi.
- preço de carta, cotação, set novo ou lançamento: pesquisar antes de escrever.
  nunca inventar número, nome de cliente ou resultado.

## instagram e métricas

- qualquer prompt sobre instagram (roteiro, legenda, o que postar, o que
  andou, métricas, insights, seguidores, alcance) usa as skills `ig-*` sem
  esperar o jovvi chamar pelo nome. `/ig-human` passa em tudo antes de mostrar.
- pra ler métricas, use `ig-metrics`. primeiro caminho: `graph.py`, direto
  da api da meta, com a variável de ambiente `IG_ACCESS_TOKEN` (se ela existir
  na sessão). segundo: o conector windsor.ai (`instagram`, conta
  `17841480042928495`, mais o `instagram_public` como reserva), se as
  ferramentas `mcp__Windsor_ai__*` estiverem na sessão. em nenhum caso peça pra
  colar insights, e nunca peça token no chat.
- se o conector devolver "not your real numbers" ou só zeros, as leituras
  estão pausadas pelo plano do windsor (o free inclui 1 fonte). avise,
  aponte o que resolve e não use os zeros.
- `instagram/data/` e `instagram/audit.md` ficam fora do git: são métricas
  pessoais.

## o que foi mudado em relação ao upstream

só as listas de palavras das ferramentas python e o `slop.json`, pra elas
funcionarem em português (o README.md lista cada mudança). os `SKILL.md`, o
`hooks.json` e o `rubric.json` são idênticos ao upstream, então dá pra
atualizar por cima quando o repositório original mudar.
