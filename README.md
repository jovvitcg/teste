# instagram-agent pro jovvi tcg

as 13 skills `ig-*` do pacote [instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill)
(jake schincariol, licença MIT), instaladas neste repositório e ajustadas pra
escrever em português brasileiro com a voz do jovvi (@jovvi.tcg).

o pacote não posta nada. cada skill termina num bloco pronto pra copiar, e
quem aperta o botão é você.

## instalar no seu pc

precisa do claude code e, pra parte que dá nota, de python 3. sem chave de api,
sem conectar o instagram.

**macOS / linux**

```bash
git clone https://github.com/jovvitcg/teste.git
cd teste
./install.sh
```

**windows (powershell)**

```powershell
git clone https://github.com/jovvitcg/teste.git
cd teste
.\install.ps1
```

o script copia as 13 pastas soltas pra `~/.claude/skills/` (o caminho final tem
que ser `~/.claude/skills/ig-reel/SKILL.md`, sem `skills` duas vezes) e o
`voice.md` pra `~/.claude/instagram/voice.md`. se já existir um `voice.md` seu
lá, ele não sobrescreve. pra trocar, `./install.sh --force` ou
`.\install.ps1 -Force`.

depois: **reinicia o claude code** e digita `/ig-`. a lista aparece sozinha.

se preferir sem script, é só copiar `.claude/skills/ig-*` pra
`~/.claude/skills/` e `instagram/voice.md` pra `~/.claude/instagram/voice.md`.

dentro deste repositório nem precisa instalar: o claude code lê
`.claude/skills/` direto, e o `CLAUDE.md` avisa pra usar `instagram/voice.md`.

no windows, se `python3` não existir, fala pro claude usar `python` ou `py`.

## o voice.md

`instagram/voice.md` já vem preenchido com o que dá pra saber dos seus reels:
quem é você, pra quem fala, como soa, o que nunca fala, as posições, o setup de
gravação e a estrutura que funciona. o que está entre `{{chaves}}` só você
sabe (xinga ou não, ritmo em palavras por minuto, provas com número, link da
bio, palavra-chave). as skills nunca inventam isso. enquanto estiver vazio, o
rascunho volta com `{{seu número}}` no lugar.

se quiser refazer do zero: manda três legendas suas pro claude e pede
"escreve o meu voice.md a partir dessas".

## como usar

```
/ig-viral      o que está andando no nicho de pokémon tcg (uma vez por semana)
/ig-plan       a semana montada em cima disso
/ig-reel       o roteiro do reel, com três ganchos pontuados e o mapa de tempo
/ig-human      passa o texto e tira o cheiro de robô
/ig-caption    a legenda, testada no corte dos 125 caracteres
/ig-comment    os comentários do dia nos posts que o /ig-plan apontou
/ig-reply      as respostas de quem comentou em você
/ig-audit      sexta: o que andou e por quê
```

pra só experimentar, roda `/ig-profile`. ele dá nota ao perfil numa régua de
12 pontos e reescreve na ordem do que mais muda resultado.

| comando | o que faz |
| --- | --- |
| `/ig-reel` | um reel a partir de uma ideia. três ganchos de 26 fórmulas, pontuados, roteiro, texto de tela e beat sheet com tempo |
| `/ig-viral` | lê o que está funcionando no nicho, ranqueia por múltiplo sobre a mediana de cada conta, escreve o swipe file |
| `/ig-caption` | a legenda, com a caixa do que o feed mostra antes do "... mais" |
| `/ig-carousel` | carrossel: capa, slides e os arquivos 1080x1350 |
| `/ig-story` | a sequência de stories do dia e o caminho pro dm |
| `/ig-profile` | nota de 0 a 100 no perfil e reescrita por prioridade |
| `/ig-plan` | a semana: o que postar, formato, horário, com quem interagir |
| `/ig-human` | o humanizador. dois scripts que rodam de verdade |
| `/ig-comment` | comentários em post dos outros, nove tipos |
| `/ig-reply` | as respostas embaixo do seu post, ordenadas por intenção |
| `/ig-dm` | entrega da palavra-chave, primeira mensagem, proposta e dois follow-ups |
| `/ig-repurpose` | um vídeo longo ou podcast vira uma semana de reels e carrosséis |
| `/ig-audit` | post-mortem do que você já publicou |

## ler as métricas do instagram (`ig-metrics`)

o pacote original não se conecta ao instagram. o skill extra `ig-metrics`
resolve isso pelo conector windsor.ai que já está vinculado à sua conta do
claude, com o instagram @jovvi.tcg conectado. quando você falar de métricas,
insights, "o que andou" ou pedir um audit, ele puxa os posts com alcance,
views, envios, salvamentos, seguidores ganhos e retenção aos 3s, e monta a
tabela que o `/ig-audit` usa.

```bash
python3 .claude/skills/ig-metrics/metrics.py instagram/data/posts.json \
    --followers 3200 --tsv instagram/data/posts.tsv --out instagram/audit.md
```

**caminho principal, grátis:** o `graph.py` puxa direto da api da meta com um
token do seu app no meta for developers, guardado na variável de ambiente
`IG_ACCESS_TOKEN` (nas configurações do ambiente do claude, ou no `.env` do
seu shell no pc, nunca no repositório).

```bash
python3 .claude/skills/ig-metrics/graph.py --check    # o token funciona?
python3 .claude/skills/ig-metrics/graph.py            # escreve instagram/data/*.json
python3 .claude/skills/ig-metrics/graph.py --refresh  # a cada 60 dias
```

**reserva:** a conta do windsor é a `jovvitcg@gmail.com`, com dois conectores: `instagram`
(insights) e `instagram_public` (o que o perfil mostra, usado pra completar
curtidas e comentários). o plano free do windsor inclui 1 fonte; se as
leituras pausarem, o conector devolve zeros com um aviso e o script se
recusa a auditar. aí é manter só o `instagram` ou fazer upgrade.

`instagram/data/` e `instagram/audit.md` ficam fora do git porque são
métricas pessoais.

## as ferramentas que rodam

sem dependência, sem internet, nada sobe. rodam no seu texto, no seu pc.

```bash
python3 .claude/skills/ig-reel/hookscore.py ganchos.txt          # ranqueia os ganchos
python3 .claude/skills/ig-reel/beats.py roteiro.txt --target 30  # tempo antes de gravar
python3 .claude/skills/ig-caption/caption.py legenda.txt --keywords "pokemon tcg,booster box"
python3 .claude/skills/ig-human/humanize.py rascunho.txt --report
python3 .claude/skills/ig-human/detect.py rascunho.txt
python3 .claude/skills/ig-viral/swipe.py coletado.tsv --out instagram/swipe.md
python3 .claude/skills/ig-metrics/metrics.py instagram/data/posts.json --tsv instagram/data/posts.tsv
```

os arquivos de trabalho (`swipe.md`, `log.md`, `plan.md`) ficam em
`instagram/` neste repositório, ou em `~/.claude/instagram/` no pc.

## o que mudou em relação ao upstream

os `SKILL.md`, o `hooks.json` e o `rubric.json` são idênticos ao original.
só as listas de palavras das ferramentas e o `slop.json` ganharam um bloco em
português, sempre somando ao inglês, nunca trocando. os quatro ganchos de
exemplo do README original continuam com a mesma nota (85.6, 81.4, 54.4, 9.6).

- `hookscore.py`: números falados, dinheiro, palavras de tensão, aberturas
  fracas e imperativos em pt-br. `R$400` conta como preço. "fala galera" e
  "no vídeo de hoje" viram dealbreaker. "você", "te", "seu" contam como falar
  com o espectador.
- `detect.py`: a checagem VOICE tinha régua só de inglês (contração com
  apóstrofo e "you/I"), então todo texto em português saía FLAGGED. agora, se
  o texto é em português, ela conta marcador oral (tá, pra, né) e pronome em
  pt-br com uma régua própria, porque a língua deixa o pronome cair.
- `humanize.py` e `slop.json`: "crucial" e "vital" também são palavras em
  português e viravam "important". agora viram "importante". entrou um bloco
  de vocabulário de robô em pt-br (mergulhar, alavancar, além disso, vale
  ressaltar) e a isca de instagram em pt-br (fala galera, não esquece de
  seguir, ativa o sininho, o algoritmo ama). estruturas flagadas, não
  trocadas: "não é só X, é Y", preâmbulo de vídeo, cumprimento, "em suma".
- `caption.py`: "comenta PALAVRA", "me chama", "salva esse", "link na bio",
  "arrasta pro lado" contam como pedido. hashtag com acento é lida inteira.
  `#viralizar`, `#explorar`, `#curtidas` entram como genéricas.
- `beats.py`: stopwords em pt-br, senão o loop do final contava "e" e "de"
  como palavra repetida do gancho.
- regex de palavra de todos os scripts aceita letra acentuada.

## limites que valem a pena saber

- não publica, não agenda, não conecta na conta. o `/ig-dm` diz onde fica a
  linha das respostas automáticas.
- não gera imagem nem vídeo. o `/ig-carousel` monta os arquivos de slide, a
  foto e o vídeo são seus.
- o `/ig-viral` é você navegando nas contas, em velocidade humana. sem você
  abrir as contas, ela não tem o que ler.
- a régua SPECIFICITY conta dígito e Nome Com Maiúscula. no seu lowercase,
  nome de carta não conta, então ela lê baixo. usa como lembrete de botar um
  número ou um nome, não como veredito.
- o classificador de fórmula de gancho (`hooks.json`) usa regex em inglês. em
  português ele se abstém e marca "unclassified". a fórmula você escolhe
  lendo o arquivo, que vale a leitura.
- limite de hashtag é 5 por post. se o instagram mudar, o instagram manda.

## atualizar do upstream

```bash
git clone --depth 1 https://github.com/Jakeschincariol/instagram-agent-skill.git /tmp/iga
diff -r /tmp/iga/skills .claude/skills
```

o que mudar em `SKILL.md`, `hooks.json` ou `rubric.json` dá pra copiar por
cima direto. nos `.py` e no `slop.json` compara antes, pra não perder o bloco
em português.

## créditos

pacote original de jake schincariol, [opusjake.ai](https://opusjake.ai), MIT.
a licença está em `LICENSE`. o passo a passo em português que motivou isso é
o guia "instagram-agent: 13 skills de claude que escrevem o seu instagram".
