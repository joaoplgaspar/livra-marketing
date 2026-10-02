# Reel · "o app errou a cor desse livro" (ter 06/10, 20h)

Formato: devlog narrado pelo fundador (voz por cima, telas + motion, sem rosto e sem nome) · Revelação
Duração: ~30 s · 9:16 · legenda queimada (a maioria assiste sem som) · pensado para turbinar

## Verdade (medido 01/10 com o código da 1.11, `lura-1-11-wt` em 10e37192)
Mesmo caminho do app: capa desenhada inteira num quadrado 32×32 → `pickDominantPaletteFromPixels` (6 cores) → `deriveReadingTheme` modo automático. Saída em `material/medicao-motor-1.11.json`.
Regra dos botões (`buildThemeSeedFromPaletteV3`): fundo = 1ª cor com saturação mínima; botões = a cor de **maior saturação relativa** entre as outras.
- **Capa clássica (azul, 9786555653311):** fundo `#d9ebf1` + botões `#187190`. **Acertou** (azul). O rosa do título não entra nas 6 cores.
- **Edição "Novo capítulo extra" (lilás e rosa, apple:6745801622):** fundo lilás `#ebe5f3` + botões **marrons `#864833`**, a cor do cabelo dela. **Errou.**
- ⚠️ O BACKLOG dizia "azul-escuro + marrom" para a clássica; isso **não se reproduz** no código da 1.11 com a capa da Apple. O erro real está na edição lilás. O vídeo conta essa.
- Tema da leitura atual = PRO, na 1.11 (Ajustes › Aparência). O erro segue aberto, por isso o vídeo termina em "tô consertando".

## Roteiro

| Tempo | Tela | Texto na tela | Voz |
|---|---|---|---|
| 0–2 s | **Sua gravação ②**: app com botões marrons, capa lilás ao lado | **o app errou a cor desse livro** | — |
| 2–6 s | **Sua gravação ①**: a capa azul e o app ficando azul ("Seu tema agora é de…") | o app pega a cor da capa | "Eu fiz o Livra pintar o app com a cor do livro que você tá lendo." |
| 6–10 s | `B-capa-classica.mp4` (só o começo: capa → quadradinhos) | 32 × 32 pixels | "Ele espreme a capa num quadrado de 32 por 32 pixels e fica com as seis cores que mais aparecem." |
| 10–12 s | `B-capa-classica-4-tema.png` | na capa azul: acertou | "Na capa azul, acertou." |
| 12–22 s | `A-novo-capitulo-extra.mp4` inteiro (capa lilás → pixels → 6 cores → o marrom destacado → o tema) | lilás e rosa → **marrom** | "Aí eu testei a edição lilás. A capa é lilás e rosa. E o app pintou os botões de marrom. É o cabelo dela. Pros botões, o app escolhe a cor mais intensa da capa, e aqui a mais intensa é o marrom." |
| 22–27 s | Você mexendo no código (borrado) | tô consertando | "Tô ensinando ele a escolher a cor que a capa quer mostrar, e não só a mais intensa." |
| 27–30 s | Volta pra gravação ② (loop) | qual capa eu testo? | "Qual capa você quer que eu teste?" |

**Legenda do post**
Ensinei o app a pegar a cor da capa do livro que você tá lendo. Na capa azul da Hipótese do Amor, acertou. Na lilás, pintou tudo de marrom.
Qual capa você quer que eu teste?
#booktokbrasil #bookstagrambrasil #livros #bookstagram

## Material pronto (`material\`)
| Arquivo | O que é |
|---|---|
| `A-novo-capitulo-extra.mp4` · 10,6 s | capa lilás → quadrado → pixela até 32×32 → 6 cores saem → o marrom ganha contorno amarelo → fundo + botões do tema |
| `B-capa-classica.mp4` · 10,6 s | o mesmo com a capa azul (termina no tema azul) |
| `A-…-1-capa` · `-2-32x32` · `-3-seis-cores` · `-4-tema` (.png) | os quadros-chave parados, para segurar mais tempo onde quiser |
| `B-…` (.png) | idem, capa clássica |
| `capa-*.png` | as duas capas em 835×1200 |
| `medicao-motor-1.11.json` | as cores e os tokens que o código devolveu (prova) |

Os clipes não têm texto (só os códigos de cor): o texto entra no editor, do roteiro acima.

## O que só você grava (celular, conta @livraapp, PRO)
Antes: Ajustes › Aparência › Tema da leitura atual ligado, modo **Automático**.
1. **Gravação ①:** põe *A hipótese do amor* (capa azul, Arqueiro) em Lendo como leitura mais recente → abre o Início e grava até o aviso "Seu tema agora é de…" e o app azul.
2. **Gravação ②:** troca para *A hipótese do amor: Novo capítulo extra* (capa lilás) → grava o app mudando.
   **Confere se os botões saíram marrons.** O app lê a capa por um proxy, e a amostra pode variar um pouco da que eu medi. Se não sair marrom, me avisa antes de gravar a voz: a história muda.
3. Tela de código: qualquer trecho de `src/config/readingTheme.ts`, borrado.
Nada de outra pessoa na tela (seguidores, liga, notificações): corta ou borra.
