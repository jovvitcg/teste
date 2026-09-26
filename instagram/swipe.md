# swipe file gringo (/ig-viral), 26/09/2026

```
SWIPE  ·  280 shorts  ·  7 canais  ·  baseline: mediana de cada canal (últimos 40 shorts)
```

**de onde veio e o que vale:** o instagram não mostra views sem login, e eu não
navego com a sua conta. o `/ig-viral` manda usar o youtube shorts como segundo
corpus, porque a gramática de gancho é a mesma e as views são públicas. puxei
os últimos 40 shorts de 7 canais de pokémon tcg com o `yt-dlp` e ranqueei pelo
múltiplo sobre a mediana de cada canal. o gancho aqui é o **título**, não a
fala (as legendas automáticas não vieram). o classificador do pacote é em
inglês e abstém em 232 de 280, então eu li os outliers na mão, que é o que o
skill manda fazer de qualquer jeito.

**o aviso que importa:** cinco dos sete canais têm 2 a 3 milhões de inscritos,
100 a 180 vezes o seu tamanho. dois são mais perto (pokichloe, 136 mil;
dannyphantump, 242 mil). o que se copia é a **forma** do gancho e a estrutura,
nunca a cadência, o tom ou a escala. formato que funciona a 3 milhões às
vezes funciona porque está a 3 milhões.

## os canais

| canal | inscritos | mediana (40 shorts) | maior múltiplo |
| --- | --- | --- | --- |
| @DeepPocketMonster | 2,39 M | 405 mil | 10x |
| @PokeRev | 3,31 M | 288 mil | 15x |
| @Leonhart | 2,03 M | 87 mil | 439x |
| @UnlistedLeaf | 2,74 M | 102 mil | 74x |
| @RealBreakingNate | 2,05 M | 329 mil | 25x |
| @dannyphantump | 242 mil | 5,5 mil | 18x |
| @pokichloe | 136 mil | 4,5 mil | 4,4x |

## outliers (acima de 3x), lidos na mão

```
 439x  @Leonhart           "A day in the life of a Pokémon master"                POV / dia na vida
  74x  @UnlistedLeaf       "SHEET OF POKÉMON CARDS GOES INTO A SLEEVE!"          visual satisfatório / coisa nunca vista
  54x  @Leonhart           "Why Pokemon cards were banned"                       curiosidade com afirmação forte
  51x  @Leonhart           "POV: You're trying to find a good place to rip packs" POV humor
  36x  @UnlistedLeaf       "THE SECRET POKÉMON CENTER"                            lugar/coisa secreta
  27x  @UnlistedLeaf       "HE OPENS A $1000 POKÉMON PACK"                       dinheiro em jogo no título
  25x  @RealBreakingNate   "Only 5 Seconds to Find The GOLD Frog Pokemon Card!"  desafio de 5 segundos (jogo com o espectador)
  24x  @UnlistedLeaf       "EATING ALL MCDONALDS X POKÉMON CARDS"                 absurdo visual
  18x  @dannyphantump      "26 Years Ago Today... TEAM ROCKET RELEASED!"          efeméride com data (canal de 242 mil!)
  16x  @RealBreakingNate   "Only 5 Seconds To Find The CAT Pokemon Card!"        desafio de 5 segundos (repetiu e andou de novo)
  15x  @PokeRev            "He Sent Me a Charizard God Pack..."                   god pack, resultado prometido
  12x  @PokeRev            "IMPOSSIBLE $5,000 God Pack FOUND"                     god pack + dinheiro
  12x  @RealBreakingNate   "Repacked Pokémon Cards in Target = CRAZY!"           vigilante do consumidor (repack, golpe)
  11x  @UnlistedLeaf       "I PULL A POKÉMON GOD PACK!!!!"                       god pack
  10x  @Leonhart           "I Opened an ERROR Pokemon pack!"                      pacote com erro (raridade do processo)
  10x  @DeepPocketMonster  "LOST OVER $1,000! PSA Base Set Charizard (Don't Do This)"  confissão de custo (#1) + grading
   9x  @Leonhart           "I ordered a 'chair' from Pokémon..."                  objeto absurdo
   8x  @RealBreakingNate   "She's Mad, I Lied About Buying Pokemon Cards!"        humor de casal (adjacente, não é o seu)
   6x  @DeepPocketMonster  "Every Water-Type Pokemon I Pull I Donate to #TeamSeas" mecânica de doação (aposta pública)
   6x  @Leonhart           "I Opened a $15,000 Pokémon Pack"                      dinheiro em jogo
   6x  @Leonhart           "The First Pack of Pokemon Cards EVER MADE"            história / superlativo (#26)
   5x  @UnlistedLeaf       "Take a Pokémon Card or DOUBLE IT??"                   escolha com aposta
   4x  @pokichloe          "THE BEST 151 GOD PACK?!"                              god pack (canal de 136 mil)
   4x  @Leonhart           "I collected EVERY Pokémon pack... in one binder"      quest completa / coleção inteira
   3x  @dannyphantump      "Day 272 of Collecting EVERY Pokemon Card Master Set!" série com contador de dias
   3x  @UnlistedLeaf       "World Record Pokémon Card Binder"                     superlativo (#26)
```

## o que está over-indexando (contagens no terço de cima, 93 shorts)

1. **resultado prometido no título** (god pack, error pack, "pulled best card
   first pack"): 11 vezes no terço de cima, 2 no de baixo. é o seu god pack
   (2,0x) e é o oposto do seu "bora abrir e ver" (0,9x).
2. **dinheiro em jogo no título** ($1.000, $5.000, $15.000, "lost over
   $1,000"): 9 vezes em cima, 1 embaixo. fórmula #1 do hooks.json. o seu
   "pedido de R$30.000" (1,0x) tinha isso na fala e não na legenda nem no
   título fixo.
3. **jogo com o espectador com relógio** ("only 5 seconds to find"): 3 vezes
   em cima, 0 embaixo, e o mesmo canal repetiu três vezes sem decair. é o
   substituto natural do seu "se eu acertar", que decaiu em sete episódios:
   aqui o espectador joga, em vez de assistir você jogar.
4. **curiosidade com afirmação ou data** ("why cards were banned", "first
   pack ever made", "26 years ago today"): 5 vezes em cima. o do
   dannyphantump fez 18x num canal do seu tamanho.
5. **vigilante do consumidor** (repack no Target): 2 vezes em cima. é a sua
   bandeira (acessibilidade, anti-scalper) em formato de denúncia.
6. **aposta pública / quest com contador** (doar o que puxar, dia 272, coleção
   inteira num fichário): 4 vezes em cima. é o formato do Deep Pocket Monster
   ("montar o set em 48h ou perde tudo").

o que está no fundo: pet abrindo pacote (4 vezes, todas abaixo de 0,3x),
"last pack magic" e "pack battle" repetidos (série desgastada, igual à sua),
lugar exótico sem payoff (Coliseu, vending na Itália), troca de carta com
estranho. gimmick sem aposta e sem resultado prometido.

comprimento do gancho: 7 palavras em cima e 7 embaixo. não separa nada nesse
corpus. o que separa é se o título promete um resultado, um valor ou um jogo.

## os não classificados (232 de 280)

o classificador não pegou porque os títulos são em caixa alta com emoji e as
regex são de fala. lendo na mão, três formas que não estão no `hooks.json` e
valem entrar:

- **POV: {situação que todo colecionador viveu}.** o 439x e o 51x do Leonhart
  são isso. você já fez uma vez (donuts, 1,0x). a diferença: a situação tem
  que ser universal do hobby, não uma piada de uma nota.
- **{coisa} entrando em {lugar}, sem fala.** o "sheet of cards goes into a
  sleeve" (74x) é puro visual satisfatório. você vende sleeve.
- **"só 5 segundos pra achar X."** um jogo em que quem joga é quem assiste.
  gera comentário, gera rewatch (loop), e não desgasta porque a página muda
  toda vez.

## a sua versão (pra mandar pro /ig-reel com a fórmula já escolhida)

**#18 cold open + jogo de 5 segundos (o substituto do "se eu acertar")**
"você tem 5 segundos pra achar o {{Pokémon}} nessa página."
na tela: `5 SEGUNDOS`. a página do fichário ocupa o quadro inteiro, relógio
no canto, e no fim você mostra onde estava. a página muda toda semana, então
não desgasta. comentário: "achei / não achei". é o seu fichário sendo visto
por quem nunca viu.

**#1 confissão de custo + resultado prometido**
"R$30.000 em cartas na mesa. o maior pedido da loja, embalado em um minuto."
título fixo `PEDIDO DE R$30.000` no quadro 1. você já gravou isso (26/08,
1,0x) com o número só na fala e a legenda em outro assunto. regravado curto,
com o título e a legenda dizendo o número, é outro post.

**#23 efeméride com data (o "26 years ago today")**
"há 30 anos saía o primeiro pacotinho de pokémon do mundo." pra 20/10/2026, o
aniversário exato do primeiro set no japão (confirmar a data antes de gravar:
está no relatório). liga com a coleção de 30 anos, que é o seu tema mais
forte, e o canal do seu tamanho fez 18x com essa forma.

**#7 vigilante (repack no Target, versão brasil)**
"tem gente vendendo pacotinho repack como lacrado no {{marketplace}}. esse é o
sinal." só se você tiver um caso real, com print. sem caso real, não existe
vídeo. mas é a sua bandeira em formato de denúncia, e protege quem tá
começando.

**#6 aposta pública (Deep Pocket Monster, tamanho jovvi)**
"vou montar a página dos três iniciais de kanto por menos de R$50 em 7 dias.
se não conseguir, as cartas vão pra comunidade." contador de dias nos
stories, resultado em reel. é o "vou doar todas as cartas do meu binder" (13,
62% de retenção) com uma aposta e um prazo.

**visual satisfatório, sem fala**
"cem cartas entrando no sleeve." mão, mesa, som. 20 segundos. você vende o
sleeve e o vídeo não pede nada.

## confiança

280 shorts em 7 canais sustenta as formas acima. o que ele não sustenta é
"vai funcionar no seu tamanho": os canais são de 7 a 180 vezes maiores, e só
dois estão perto. as três formas mais seguras pra testar primeiro são as que
o canal pequeno provou (efeméride com data, 18x em 242 mil) e as que o seu
próprio histórico já provou de lado (resultado prometido no título, god pack
2,0x; humor de colecionador, meme 4,5x).

o que eu não coletei: instagram de verdade (10 contas, 12 reels cada, na sua
mão). se quiser esse corpus, abre as contas no seu navegador e me passa
handle, seguidores, mediana, views e a primeira frase de cada reel; o
`swipe.py` faz o resto.

arquivos: `instagram/data/swipe_gringa.tsv` (as 280 linhas) e
`instagram/data/swipe_gringa_raw.md` (a saída crua do swipe.py).
