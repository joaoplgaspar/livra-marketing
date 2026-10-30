# Novidades da 1.13

Post de sex 30/10/2026 (pedido do fundador: "carrossel para hoje"). Skill instagram-carousel, nível A (identidade completa, post de produto).

## Estado medido
- App Store BR: 1.13 publicada em 30/10/2026 13:45:55Z (lookup iTunes, `currentVersionReleaseDate`).
- Play: 1.13 desde 26/10 (STATUS da main, medido 26/10); a página do Play hoje mostra as notas "Novidades da 1.13".
- Binário: main `13bf0216` (build 5: iOS 148, AAB versionCode 21).

## Prints = código da versão da loja
- Worktree `E:/Projetos/lura-a1c` em `d2a66a02` (filho de docs de `13bf0216`; `git diff 13bf0216 d2a66a02 -- src functions/src` vazio; só um `vitest.main.local.ts` não rastreado).
- Harnesses da própria versão (componentes reais, rede em stub, dados fictícios): `autores-harness` (busca, página do autor, livro), `conquistas-harness.garimpo` (cartão de desbloqueio), `store-harness` (`?page=1&tab=season`, `?tab=season`). 390×844, dpr 3, em `prints/`.
- Mascote: o harness da 1.13 não desenha o bicho (stub sem mascote) → mascote só em texto, no "e mais".

## Texto (fonte: notas da loja 1.13, marketing/lojas/1-13/ios.txt, publicadas)
- Livra Autores: página de cada autor com obras e lançamentos; vitrine na Busca e na Início (quem está sendo lido, lançamentos, Garimpo independente); seguir editora e receber às sextas o que ela vai lançar.
- Sou autor: Ajustes › Sou autor, ligar livros ao perfil, pedir verificação; com o selo: cuidar da página, trocar capa dos próprios livros, ver quantas pessoas têm as obras na estante, card "Estou no Livra".
- Garimpo: Primeiro Garimpo, Faro de Garimpo, Garimpo de Ouro.
- Mascotes: 7, ao lado da foto e na Início; dorme quando não lê; Loja, para quem é PRO (na 1.13; a web já vende sem PRO desde 24/10, `61afdb39`, que NÃO está no binário).
- Halloween grátis até 2/11 (segunda), conquista "Gostosuras ou Leituras".
- Logo e ícone novos · Loja com aba Temporada (Eclipse) · clube com pote animado e até 10 livros por pessoa · meta do ano opcional · remover seguidor sem bloquear · esconder sugestão de leitor parecido · a Lura não sugere o que já está na estante.

## Slides
1. a 1.13 chegou · O Livra agora tem lugar pra quem escreve. · ícone novo
2. Na Busca, uma vitrine de autores. (celular: busca)
3. Cada autor ganha uma página. (recorte: autor) + seguir editora
4. Livro independente agora conta. (recorte: Garimpo de Ouro)
5. Você escreve? Peça o selo. (passos, sem tela)
6. Halloween de graça até segunda. (recorte: banner da Loja)
7. A Loja ganhou a aba Temporada. (recorte: Eclipse)
8. E mais (lista)
9. Qual você testa primeiro? · atualiza na loja

## Correção de 30/10 (fundador: "pegou prints antigas, a seção de autores não está mais assim")
- Os frames `hoje-*` do `autores-harness` são a 1ª versão (mock de 07/10). Trocados pelos frames "-real", que montam os componentes atuais:
  `vit-real-busca` (slide 2), `real-a1b-autor&bib=grande` (3), `ed-real-hub-lancamentos` (4, novo), `real-perfil-visitante` (6). Em `prints/real/`.
- `card-real-*` usam a foto real do Raphael Montes: fora do post.
- A vitrine (`vit-real-busca`) usa capas e fotos de autores do catálogo de verdade (manifest em `harness/autores-vitrine-assets`), não dado de usuário.
- Agora são 10 slides.
