# fichário: link fixo por fichário e página pública completa

plano pra corrigir o compartilhamento do fichário em jovvitcg.com.br. o código
do site não está neste repositório. este arquivo existe pra ser entregue a quem
for implementar (ou colado numa sessão do claude aberta no repositório do site).

escrito em 26/09/2026 a partir de três mensagens de um usuário do fichário.

## o que o usuário relatou

1. **o link muda a cada alteração.** o link de compartilhar sai como
   `https://jovvitcg.com.br/fichario/s/jpr-pokedex-only-foil-04`. toda vez que
   ele mexe no fichário o número do fim sobe, e o link que ele já mandou pras
   pessoas fica preso na versão antiga.
2. **"público" só funciona pra um fichário.** a opção mais abaixo no diálogo
   deixa o link permanente, mas marcar um fichário como público tira o outro.
3. **a página do link não mostra o estado das cartas.** abre só a ilustração.
   não dá pra ver o que ele tem e o que falta, e as etiquetas (holo, reverse,
   master ball, personalizada) não aparecem.
4. **o pdf já mostra tudo certo.** o export em pdf traz a sobreposição
   "não tenho ainda" nas cartas que faltam e a etiqueta personalizada (no
   exemplo, "clara") em cima da carta. ele pediu que o link funcione igual.

## o que dá pra afirmar do lado de fora

verificado no bundle público do site (vite + react, spa):

- rota `/fichario/s/:slug`, renderizada pelo chunk `binder-public`.
- o builder é o chunk `fixario-builder`; existe um chunk `pokedex-etiquetas`,
  o que bate com a existência de etiquetas personalizadas.
- a api mora em `https://jovvi.jovvitcg.com.br`.

inferido do padrão do link e do relato, a confirmar no código:

- o slug é `<prefixo do dono>-<nome do fichário>-<contador>`. cada salvamento
  gera um retrato imutável com contador novo. o retrato antigo continua no ar.
- "público" é um campo único na conta (um fichário público por usuário), não
  um campo do fichário.
- o retrato ou a página pública descarta os campos `tenho` e `etiquetas` que o
  pdf usa. o dado existe no fichário, porque o pdf o renderiza.

## a correção

### 1. público passa a ser do fichário, não da conta

- `binder.is_public: boolean`, padrão `false`. sem limite de quantos fichários
  públicos por conta.
- `binder.slug: string`, único, gerado uma vez na criação a partir do nome
  (`jpr-pokedex-only-foil`). renomear o fichário não troca o slug. se um dia
  for permitido trocar, guardar o slug antigo como alias que redireciona.
- migração: o fichário que hoje está marcado como público na conta recebe
  `is_public = true`. o campo antigo na conta some depois que a migração rodar.

### 2. dois tipos de link, os dois continuam valendo

| link | exemplo | o que abre |
|---|---|---|
| fixo | `/fichario/s/jpr-pokedex-only-foil` | a versão atual, enquanto `is_public` for `true` |
| desta versão | `/fichario/s/jpr-pokedex-only-foil-04` | o retrato daquele salvamento, nunca muda |

resolução da rota `/fichario/s/:slug`, nesta ordem:

1. bate com `binder.slug` de um fichário com `is_public = true`: renderiza a
   versão atual.
2. bate com o slug de um retrato: renderiza o retrato. no topo, aviso "versão
   de dd/mm/aaaa" e, se o fichário de origem estiver público, um link "ver a
   versão atual" apontando pro link fixo.
3. nada bate, ou o fichário foi despublicado: 404 com texto amigável.

nenhum link antigo com número quebra.

### 3. o diálogo "compartilhar fichário"

- mostra os dois links, cada um com um nome curto:
  - **link fixo, atualiza sozinho.** só aparece se o fichário estiver
    público; se não estiver, mostra o toggle "deixar público" ali mesmo.
  - **link desta versão, não muda.** o comportamento de hoje.
- "copiar link" e "whatsapp" usam o link fixo por padrão quando o fichário
  está público. o link da versão fica um clique abaixo.
- o toggle "público" fica dentro do diálogo do fichário e mexe só nesse
  fichário.

### 4. a página pública mostra o mesmo que o pdf

- a página `binder-public` passa a usar o mesmo componente de card do export
  em pdf, ou o pdf passa a usar o da página, tanto faz, desde que seja um só.
- em cada carta: sobreposição "não tenho ainda" quando `tenho = false`, e as
  etiquetas (holo, reverse, master ball, poké ball e as personalizadas) como
  aparecem no pdf.
- no topo: "x de y" cartas, mais o nome do fichário e do dono.
- o retrato (link com número) precisa guardar `tenho` e `etiquetas` por carta.
  se hoje o retrato salva só a lista de cartas, é aqui que o dado se perde.
- toggle do dono, no diálogo de compartilhar: "mostrar as que faltam". padrão
  ligado. desligado, a página esconde as cartas com `tenho = false` e o
  contador some, porque nem todo mundo quer expor o que não tem.

## como saber que ficou pronto

- editar um fichário público e abrir o link fixo numa aba anônima: a mudança
  aparece sem trocar a url.
- marcar dois fichários como públicos: os dois links fixos abrem ao mesmo
  tempo.
- abrir um link antigo com `-04`: continua abrindo o retrato daquela versão,
  com o aviso de data.
- abrir qualquer link público: as cartas que faltam aparecem escurecidas com
  "não tenho ainda" e as etiquetas aparecem em cima da carta, igual ao pdf.
- desligar "mostrar as que faltam": as cartas que faltam somem da página e o
  pdf continua igual.

## resposta pro usuário (whatsapp)

passou pelo `ig-human`. sem emoji, sem travessão, lowercase.

```
valeu por mandar, isso ajuda demais. esse 04 no fim do link é o número da versão: cada vez que você mexe no pokedex only foil o site gera um retrato novo, e o link antigo fica preso na versão anterior. vou fazer um link fixo por fichário, que atualiza sozinho e funciona pra mais de um ao mesmo tempo. e no link vai aparecer o que você tem, o que falta e as etiquetas: holo, reverse, master ball e as personalizadas. te aviso quando subir.
```
