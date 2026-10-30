# Caminho 1: skill `instagram-carousel` (29/10/2026)

Fonte de cada pauta: `<pauta>/carrossel.html` (base.css por caminho absoluto). PNGs 1080×1350 em `<pauta>/01.png…`; folha de aprovação em `<pauta>/out/folha.png`. Texto dos roteiros sem mudança de palavra. Os únicos acréscimos são o `.folio` (título corrido, sem número) nas pautas A e B e os `<br>` de quebra de linha.

## Ambiente: um tropeço antes do 1º render

`render.mjs` não abriu: o `@playwright/test` 1.59.1 do repo pede o chromium headless shell **1217**, e a máquina só tem o **1243** em `ms-playwright`. Não baixei nada nem editei o `render.mjs`. Rodei com um preload em `--import` (fora do repo, no scratchpad) que só passa `executablePath` do 1243 para o `chromium.launch`. O lint e a exportação são os do script original. Quem for rodar de novo nesta máquina vai bater no mesmo problema, e `npx playwright install chromium-headless-shell` resolve.

## Rodadas por pauta

| Pauta | Slides | Rodadas de correção (depois do 1º render) | O que o olho pegou |
|---|---|---|---|
| A releitura (nível A) | 8 | 3 | capa com miolo vazio, o "." do "Sim." escondido atrás das lombadas e a nota à mão quebrada em 3 linhas; slides 4, 5 e 7 com a metade de baixo vazia; h1 da capa a 168px quebrou feio ("conta na / meta."), então voltou a 150; **slide 3 com o texto encostado no `.folio`**; nota à mão do slide 8 quebrando em 3 linhas |
| B suspense (nível B) | 8 | 2 | capas do leque cortadas demais pela borda de baixo; o X vermelho do "tijolo" aparecia também nos livros finos (CSS pegava todos os `.brick`); fichas dos livros com o terço de baixo vazio (capa e sinopse cresceram); carimbo do Jabuti com caixa larga e vazia, e vermelho apagado no fundo escuro |
| C red flags (nível C) | 9 | 4 | slides 1, 4, 8 e 9 com metade da tela vazia (texto subiu de tamanho e o 4 ganhou rabisco); **"São 3h." quebrou em 2 linhas por cima da barra de ícones**; **rabisco da lombada encostado no texto**; "?" desenhado no slide 7 lia como texto e saiu; "Ela sabe quem / é." com o "é." órfão; "anota" sozinho numa linha no slide 6 |

## Decisões de nível

- **A (completo):** paleta ink/paper/brand/marker, as 3 fontes, grão, `.mark`/`.strike`/nota à mão, logo "Fita em L" (`-escuro`) no último slide. Capa em paper com o "Sim." gigante em Fraunces e duas lombadas iguais ("o mesmo livro duas vezes"). Não usa o molde ink + bilhete no topo.
- **B (leve):** o toque do Livra são só as fontes (Bricolage + Fraunces + letra de mão). A paleta é do post: noite fria, papel pardo de dossiê e carimbo vermelho. A assinatura (logo de 44px) entra só no último slide. Capa escura com o "4" gigante e as 4 capas reais em leque saindo por baixo. Os slides de livro levam a capa real presa com fita, o número de páginas grande e a sinopse.
- **C (sem marca):** print do app de notas do celular (Inter, checklist amarelo, marca-texto, tachado, rabisco de caneta, modo escuro no "São 3h."). Não tem grão, paleta nem fonte do Livra. As barras de cima e de baixo têm só ícones, sem nenhuma palavra fora do roteiro. "@livraapp" em cinza, 34px, só no slide 9.
- As três capas variam fundo (paper / noite / branco de app), herói (palavra gigante / capas em leque / título de nota) e composição.

## O que a skill ajudou

- Deu o vocabulário visual pronto, então a pauta A saiu "Livra" sem inventar nada: tokens, `.mark`, `.strike`, `.hand`, `.folio`, grão e o caminho do logo.
- Trouxe as regras que evitam retrabalho: sem seta, sem numeração, nada atravessa a divisa, margem ≥ 80, texto ≥ 32, capa fora do molde dos posts anteriores, linguagem neutra.
- O "abrir a folha e corrigir o que o olho pega" é o passo que fez diferença: todas as correções acima vieram dele.
- O `render.mjs` dá uma folha de aprovação e garante que a fonte carregou (sem Times New Roman).

## O que a skill atrapalhou ou não cobriu

- O lint deu "sem avisos" em **todas** as rodadas, inclusive nas que tinham colisão real: texto em cima do `.folio` (A3), "São 3h." em cima da barra de ícones (C5) e rabisco em cima do texto (C6). Ele só vê elemento saindo da caixa do slide, não elemento em cima de elemento nem texto invadindo o padding reservado. "Sem avisos" quer dizer só que nada saiu da borda.
- Ela é feita para o nível A. Para B e C não diz nada: o base.css injeta o grão e as 3 fontes em tudo, e tive de desligar o grão no C (`.slide.note::after { display: none }`). O lint também exige que a fonte usada esteja carregada, então no C a Inter precisou entrar por `@import` no `<style>`.
- Ela supõe a pasta em `marketing/instagram/<slug>/`, com caminho relativo e saída em `out/`. Aqui a pasta é outra, então foi preciso caminho absoluto e copiar os PNGs de `out/` para a pasta da pauta.
- A dependência do chromium do repo quebrou nesta máquina (seção Ambiente).
- Diz "nota à mão por cima", mas a Reenie Beanie em 80–130px quebra linha de forma imprevisível. Em 2 das 3 pautas a nota foi a última coisa a acertar.

## Avisos finais do lint

Os três: `sem avisos (caixa, vícios de IA, travessões, tamanho)`, com as ressalvas de cobertura acima. As colisões que o lint não vê foram corrigidas olhando os PNGs.
