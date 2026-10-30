# Caminho 2 — canvas-design + theme-factory (29/10/2026)

Render: Python + PIL, desenhado em 2x e reduzido para 1080×1350, com grão de papel leve. Scripts em `_trabalho/` (`lib.py` = motor de composição com checagem automática de margem ≥ 80 px e colisão de caixas; `a_releitura.py`, `b_suspense.py`, `c_redflags.py`; `sheet.py` = folha de contato). Filosofias completas em `_trabalho/filosofia-*.md`.

## Filosofias visuais criadas

- **Segunda Margem** (A, releitura) — a página tem duas camadas de tempo: a tinta impressa e a mão que voltou depois. Tipografia monumental calma na primeira camada; marca-texto, risco de caneta, círculo e nota à mão como a "segunda leitura" que reorganiza o sentido.
- **Arquivo Noturno** (B, suspense nacional) — o mistério fotografado com frieza de perícia: cada livro é uma prova catalogada sobre azul-noite, com algarismo-etiqueta e uma régua de páginas (traço a cada 10, traço alto no limite de 280) que mede sem comentar.
- **Código de Sinais** (C, red flags) — a gramática das bandeiras de alerta: galhardetes geométricos em fileira funcionando como placar (cheio/vazio), diagramas de guia de campo (pilha de 47, mostrador 1h→3h, estante, lombada) e uma única inversão para vermelho, na red flag 4 ("a 4ª é você").

## Temas (theme-factory)

- A: sem tema da theme-factory. O nível A pede identidade completa do Livra (tokens do base.css: ink/paper/brand/marker, Bricolage + Fraunces itálico + Reenie Beanie).
- B: tema pronto **Ocean Depths** (navy #1a2332, teal #2d8b8b, seafoam #a8dadc, cream #f1faee) como paleta. O toque do Livra são as fontes (Bricolage, Fraunces itálico e Reenie Beanie na nota à mão), mais a assinatura pequena no último slide. As fontes do tema (DejaVu Sans) foram descartadas.
- C: tema próprio **"Sinal Vermelho"**, pelo "create your own" da skill: papel #f3eee5, preto #151313, vermelho de sinalização #e0281e. Fontes da pasta canvas-fonts: Instrument Sans Bold, Instrument Serif Italic e Big Shoulders Bold. Sem marca; só "@livraapp" em cinza, 34 px, no slide 9.
- O fluxo da theme-factory manda mostrar o showcase e esperar a escolha do usuário. Num teste cego feito por subagente isso não cabe, então eu escolhi e registro aqui.

## Rodadas de correção (render → abrir PNG → corrigir)

- **A — 4 rodadas.** (1) A nota à mão vazava a margem e colidia com o "Sim."; o tracking −0,05em deixava as letras do Bricolage encostadas (o PIL não aplica kerning GPOS). (2) O risco atravessava a quebra de linha ("trapacear / a meta"); o círculo do "capítulo 2" cortava o "no"; a opção entre aspas quebrava depois de "só". (3) Com a expressão riscada amarrada numa linha só, o texto passava da margem, e foi preciso reduzir o corpo. (4) Ajustes de respiro (slides 5 e 8) e uma viúva ("termina.") na ponte.
- **B — 4 rodadas.** (1) O "4" gigante colidia com o título e a nota vazava a margem. (2) Havia vazio entre a sinopse e a régua, e o número de páginas ficou junto da régua. (3) A nota precisou ser recentralizada e o "4" aumentado e subido. (4) Quebras: "fim de semana" ficou amarrado e "Qual você / começa na sexta?" passou a quebrar no lugar certo.
- **C — 4 rodadas.** (1) O balanceamento de linhas gerava primeira linha curta ("Se você"). Reescrevi o algoritmo para custo de irregularidade com penalidade de primeira e última linha curtas. (2) e (3) Quebras explícitas onde a frase pede ("Fala / “só mais um capítulo” / à 1h da manhã.", "Qual é a sua? / Comenta o número."). (4) Corpo do slide 9.
- O verificador automático terminou com 0 problemas nas três pautas. Inspeção visual feita em folha de contato e em tamanho real nos slides críticos.

## Liberdades tomadas (sem mudar palavra)

- Aspas retas viraram aspas tipográficas (“ ”).
- "Red flag N" aparece em caixa alta (transformação de caixa, não troca de texto).
- Algarismos 1–4 (B) e 1–5 (C) entram como etiquetas visuais. Sem eles, "Responde com o número" e "Comenta o número" não funcionam. Não é numeração de página.
- Quebras de linha manuais.
- Elementos gráficos sem texto: fita-marcador, lista de 12 linhas de caderno, régua de páginas, pilha, mostrador, estante, lombada, bandeiras.

## Problemas

- O PIL sem libraqm não faz kerning GPOS nem shaping. Compensei com tracking menos apertado, e o Bricolage fica um pouco mais "solto" do que no navegador.
- Fontes variáveis (Bricolage e Fraunces) precisaram ser instanciadas em estáticas com fontTools antes de o PIL usá-las.
- Tudo que o navegador dá de graça (quebra balanceada, decoração que acompanha a quebra, medir antes de desenhar) teve de ser escrito à mão: cerca de 300 linhas de motor de layout antes do primeiro slide.
- Alguns slides de afirmação (A2, B7) ficaram com muito campo vazio. É escolha deliberada da filosofia ("um ponto de tensão e muito ar"), mas pode parecer "vazio" no feed.

## O que as skills ajudaram e atrapalharam (carrossel com texto)

- **canvas-design ajudou.** A filosofia escrita antes deu coerência de sistema a cada pauta: um motivo gráfico recorrente por carrossel (marcação de segunda leitura, régua de perícia, placar de bandeiras). Também empurrou para diagramas sem texto, que carregam a piada ou o dado (pilha de 47, mostrador 1h→3h, régua 133/262/273/274 contra 600) em vez de enfeite.
- **canvas-design atrapalhou.** Foi escrita para pôster de arte com "texto mínimo", em uma página. Não diz nada sobre corpo mínimo, hierarquia de leitura, quebra de linha, legibilidade em celular ou sequência de slides. Insiste em "fonte fina" e "texto sussurrado", o oposto do que um carrossel de texto fixo pede. E manda tratar o tema como "referência sutil", quando aqui o texto é o produto. Usei a filosofia para o sistema visual e ignorei as instruções de tipografia.
- **theme-factory ajudou pouco.** É uma paleta de 4 cores pronta e rápida. Ocean Depths caiu bem para suspense noturno.
- **theme-factory atrapalhou.** As fontes dos temas (DejaVu, FreeSans) são genéricas e não servem para Instagram. O fluxo obrigatório de "mostrar showcase e esperar escolha" não se aplica a trabalho autônomo. A skill também não tem nada sobre contraste de texto sobre a cor.
- **Saldo:** para carrossel com texto congelado, as duas skills dão direção estética, mas zero ofício de layout de texto. O ganho real veio de construir o motor de composição com checagem de margem e colisão.
