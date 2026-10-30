# Caminho 3: frontend-design (29/10/2026)

Skill `frontend-design:frontend-design` + HTML/CSS + render com o `@playwright/test` do repositório lura (`_trabalho/render.cjs`).
Saída: `a-releitura/` 8 PNG · `b-suspense-nacional/` 8 PNG · `c-red-flags/` 9 PNG, todos 1080×1350.

## Direção por pauta

**A, Releitura (nível A, Livra completo).** "O livro lido duas vezes": a primeira leitura fala em Bricolage seco, a segunda chega em Fraunces itálico. A caneta do Livra (Reenie + traço) só aparece onde existe gesto de leitor: riscar "reler é trapacear a meta", sublinhar "a frase que você não sublinhou", seta da nota à mão. Paleta: ink/paper/brand/marker do base.css, fundos alternados.

**B, Suspense nacional (nível B, toque = fontes do Livra).** "A espessura do livro": um trilho tracejado de 600 páginas (o tijolo do slide 2) atravessa a série, e cada livro preenche só a fração que tem (133/262/273/274). Cada slide de livro usa a cor da própria capa (lima, vinho, preto com lilás, cinza tempestade com rosa). Os slides de abertura e fechamento ficam em cinza "concreto molhado". Assinatura `-claro` pequena no último.

**C, Red flags (nível C, sem marca).** O trocadilho vira objeto: red flag = o marcador adesivo vermelho que leitor cola na página. Cada slide é uma página, a cada red flag uma aba nova é colada mais abaixo e as anteriores ficam na borda, então o carrossel vai enchendo de marcadores. Usa Archivo estreito (voz de post) e Newsreader itálico (a fala de quem lê), e só "@livraapp" a 55% no último slide.

## Rodadas de correção (depois do 1º render)

- **A: 2 rodadas.** (1) A nota à mão quebrava "nos" sozinho e a seta não apontava para o "Sim."; o sublinhado do slide 5 era um SVG com a largura da caixa e passava por baixo de uma linha inteira vazia, troquei por traço por linha (`box-decoration-break`); o slide 8 tinha "novo”." órfão; aspas retas viraram curvas. (2) O slide 5 ficou com o miolo vazio, então subi o corpo do texto; `text-wrap: balance` na ponte para não sobrar "termina." sozinho.
- **B: 1 rodada.** O "133 páginas" ficava acima do trilho e saía a 85 px da borda (passava raspando na margem); levei o rótulo para dentro do trilho, logo depois do preenchimento. A nota à mão quebrava "páginas" sozinha. Capa maior para fechar o vão entre a sinopse e o trilho. As capas do slide 8 foram centralizadas no espaço livre.
- **C: 3 rodadas.** (1) As abas pareciam barras de gráfico. Ganharam inclinação pequena e diferente em cada uma, sombra curta e borda na película, e o corpo do texto cresceu. (2) Órfãos: "4." sozinho no slide 8, "(Julga" / "sim.)" no 9. Também repeti o leque de abas do slide 1 no slide 9, que estava com meia página vazia. (3) "o" no fim de linha no slide 2 (resolvido com nbsp).

## Desvios de texto (todos tipográficos, nenhuma palavra mudou)
- Aspas retas do roteiro viraram aspas curvas (A8, C3, C4, C5).
- **B: acrescentei os numerais 1–4** nos slides de livro e sob as capas do slide 8. Não estão no roteiro, mas o CTA "Responde com o número" não funciona sem eles. O fundador decide se valem como "palavra a mais".
- B: os separadores "·" do roteiro (título · autor · páginas) viraram linhas/blocos separados.
- Quebras manuais (`<br>`, nbsp) em A8, C2, C8, C9.

## Problemas de ambiente
- O `@playwright/test` 1.59.1 do lura procura o `chromium_headless_shell-1217`, que não está instalado (a máquina tem o 1243). O `chrome.exe` completo do 1243 falhou com `spawn UNKNOWN`. Resolvi apontando `executablePath` para o `chrome-headless-shell.exe` do 1243 (default no script, sobrescrevível por `PW_CHROME`). Não baixei browser.
- O script também roda um verificador: texto a menos de 80 px da borda lateral ou com fonte abaixo de 32 px. Ele não acusou nada nas três pautas, então injetei um texto de 20 px colado na borda como controle positivo, e esse texto ele pegou. O vazamento visual (órfãos, vãos) só apareceu lendo os PNG.
- Fontes conferidas carregadas em cada render (Bricolage, Fraunces, Reenie; Archivo, Newsreader).

## A skill: ajudou e atrapalhou
**Ajudou:** obriga a ancorar cada pauta num objeto do assunto em vez de molde (trilho de páginas, aba adesiva, as duas leituras). Também fez as três pautas saírem diferentes entre si. A lista de "tells" evitou vícios comuns: eyebrow em caixa-alta, meta com "·", numeração decorativa (só usei número em B, onde a lista é referenciada) e seta "→". O "gaste a ousadia num lugar só" segurou os slides de texto puro bem limpos.
**Atrapalhou:** foi escrita para página web. Metade do texto (hero, responsivo, foco de teclado, motion) não serve para slide estático. Não diz nada sobre a mecânica de carrossel (slide autônomo, recorte 3:4 do grid, texto ≥ 32 px), e isso saiu das regras do teste e do meu verificador. O tell nº 1 da skill (fundo creme, serifa de contraste e acento terracota) é praticamente a identidade do Livra, então no nível A a skill empurra contra a marca. Segui o brief, que prevalece. A regra "não destacar uma palavra só" bate de frente com o marca-texto típico de BookTok, e por isso só usei ênfase onde ela é um gesto com sentido (riscar, sublinhar).
