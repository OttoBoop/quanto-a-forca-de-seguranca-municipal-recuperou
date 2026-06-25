# Proveniência dos dados — como cada cifra foi obtida

> **Escopo do estudo final (balanço de 100 dias, 15/03–23/06/2026):** valoração de **celulares (133)** e **cordões (15)**. As motocicletas (133 no balanço) ficam **fora da valoração** (contexto); as bicicletas foram **retiradas pelo órgão**. As seções de moto e bicicleta abaixo são mantidas como documentação dos dados (preservados em `dados_distribuicao.json`, fora da agregação) — incluindo a pesquisa de e-bikes feita para a versão anterior. Fonte dos itens e das áreas de atuação: slide oficial do balanço de 100 dias (SEGUR/Prefeitura do Rio).

Por item recuperado: os **modelos** da mistura, o **peso** de cada um e sua **fonte de frequência**, o **método e as fontes de preço** (usado e novo), o tamanho da amostra e a **forma** da distribuição. As citações completas (org, URL, valor, data) estão em [inventario_fontes.md](inventario_fontes.md) (formato F-T.N). Coleta de preços: 16/06/2026; pesquisa de e-bikes: 17/06/2026. Amostras de preço brutas por modelo em [dados_distribuicao.json](dados_distribuicao.json).

Princípio comum a todos os itens: o item recuperado é o que se **rouba na rua**, então o peso de cada modelo vem de uma **fonte de frequência** (ranking de roubo, participação de mercado, mix de anúncios) — não de uma escolha. O preço de cada modelo é uma **amostra observada** (cada anúncio/listagem = um preço), em duas bases: **revenda** (usado) e **reposição** (novo). Não se aplica fator de depreciação sobre o usado (o mercado de usado já precifica o desgaste).

---

## Celular (133 unidades) — E[V]: revenda R$ 1.212 · reposição R$ 1.964

**Pesos (frequência de roubo).** Participação por marca no roubo (Anuário do Fórum Brasileiro de Segurança Pública: Samsung 37%, Apple 25%, Motorola 23%, Xiaomi 10% — F-CEL.1/F-CEL.2), com cross-check na participação de mercado (StatCounter — F-CEL.3) e ajuste pelo perfil socioeconômico (TIC Domicílios — F-CEL.4) em direção a aparelhos de entrada/intermediários, que são a maioria do parque.

**Preços (método).** A dispersão de **usado** mais confiável veio de páginas **fetchadas** com sucesso da Trocafy e Trocafone (varejo de seminovos), em que **cada listagem = um preço** (A14: 13+ listagens; iPhone 11/13: 36 cada; S23: 30+; Moto G54; iPhone 13 Pro Max). Modelos legados (Galaxy A0x, Android genérico) entraram por trechos de busca (WebSearch). O **novo** veio do varejo (Magazine Luiza, Samsung, Apple). Total ~130 observações.

| Modelo | peso | usado (n; R$) | novo (n; R$) |
|---|--:|---|---|
| Galaxy A0x (A03/04/05) entrada | 0,14 | 12; 540–722 | 5; 549–799 |
| Galaxy A14/A15/A16 | 0,18 | 16; 530–1.124 | 6; 719–1.089 |
| Galaxy S (S23/24/25, Ultra) | 0,05 | 22; 1.403–3.698 | 6; 2.299–6.000 |
| Moto G (G24/G15/G54/G84) | 0,20 | 12; 602–962 | 6; 793–1.999 |
| iPhone 11 | 0,10 | 14; 998–2.000 | 4; 2.900–3.500 |
| iPhone 13 | 0,10 | 13; 1.700–3.113 | 4; 2.889–3.729 |
| iPhone Pro/Pro Max | 0,05 | 12; 3.300–5.300 | 4; 6.500–8.000 |
| Xiaomi Redmi Note 13 | 0,10 | 12; 500–1.200 | 5; 1.039–2.500 |
| Android legado/outros | 0,08 | 14; 90–1.029 | 5; 529–1.029 |

**Forma.** Fortemente assimétrica à direita: massa nos aparelhos de entrada, cauda nos *flagships*.

---

## Motocicleta — E[V]: revenda R$ 15.698 · reposição R$ 19.161  *(FORA do estudo final — contexto; balanço mostra 133 motos, não valoradas)*

**Pesos (frequência de roubo).** Ranking de roubo do Rio (Polícia Civil-RJ/ISP-RJ — F-MOT.1/F-MOT.2), com a Honda CG 160 na liderança isolada, corroborado pelos emplacamentos (Abraciclo — F-MOT.3).

**Preços (método).** Usado pela **Tabela FIPE por ano-modelo** (Mobiauto/tabelafipebrasil), em que cada ano-modelo gera um preço — daí a dispersão (F-MOT.4/F-MOT.6/F-MOT.7/F-MOT.9). Novo pelos preços 0km de concessionária/PPS das marcas (F-MOT.5/F-MOT.8). 10 modelos, da YBR 125 à XRE 300.

**Forma.** Concentrada entre R$ 10 mil e R$ 25 mil. *Haircut* factual de 25% na revenda para a fração com restrição (chassi remarcado — F-MOT.10), tratado como sensibilidade ρ.

---

## Bicicleta — E[V]: revenda R$ 973 · reposição R$ 1.508  *(FORA do estudo final — retirada pelo órgão; inclui a pesquisa de e-bikes, preservada como referência)*

**Pesos (frequência).** As bicicletas **convencionais** seguem o mix de usados do Rio (OLX-RJ via Diário do Rio: Caloi 70,1%, Oggi 8,3%, GTS 5,4% — F-BIK.1/F-BIK.2), avaliadas como bens de **uso pessoal** (compradas por pessoa física). A **bicicleta elétrica (e-bike)** entra com peso **7%** — a fração estimada de e-bikes de consumidor entre as bicicletas furtadas/em circulação. Não há recorte oficial do roubo por tipo (a série do ISP-RJ registra furto/roubo de bicicleta sem separar elétrica de convencional — F-BIK.7); o peso é estimado por proxies: e-bikes são ~5,4% da produção nacional de bicicletas em 2024 (Abraciclo — F-BIK.8) e ~2% das vendas (Aliança Bike — F-BIK.9), com sobre-representação no roubo por alto valor (alta de +59% no furto de bicicleta no RJ em 2025; o app 190RJ da PM cadastra o chassi "especialmente em modelos elétricos" — F-BIK.10). A faixa plausível vai de 3% a 14% (eixo de sensibilidade no paper).

**Preços (método).** Convencionais: usado por anúncios OLX-RJ (snippets) e páginas fetchadas de seminovos (Las Magrelas, Decathlon — F-BIK.4); novo pelo varejo (Magazine Luiza, Mormaii, Caloi — F-BIK.3/F-BIK.5). E-bike: novo do varejo (Caloi, Oggi, Decathlon, Sense, Two Dogs, Magazine — F-BIK.11), cobrindo entrada (R$ 1.400–3.500), urbana (~R$ 5.900) e E-MTB (~R$ 15.600); usado de lojas de seminovos (Flash Bike, Pedalla, Buxa — F-BIK.12), com venda particular ~15–30% abaixo.

| Modelo | peso | usado (n; R$) | novo (n; R$) |
|---|--:|---|---|
| Caloi entrada aro 26 (Andes/Ventura) | 0,465 | 12; 284–1.100 | 6; 783–1.559 |
| Outras nacionais entrada (Oggi/GTS/Mormaii) | 0,167 | 10; 600–2.000 | 6; 593–2.000 |
| Genérica passeio aro 26 | 0,140 | 10; 80–350 | 4; 389–699 |
| MTB aro 29 alumínio entrada | 0,093 | 9; 800–2.000 | 4; 864–4.490 |
| Infantil | 0,065 | 9; 80–300 | 4; 410–690 |
| **Bicicleta elétrica (e-bike)** | **0,070** | 16; 1.500–12.799 | 18; 1.400–17.990 |

E-bike isolada: média usado ≈ R$ 5.126, novo ≈ R$ 6.706. Convencional isolada: média usado ≈ R$ 668, novo ≈ R$ 1.115.

**Forma.** Assimétrica à direita: corpo nas convencionais (R$ 80–2.000) e cauda longa nas e-bikes (até ~R$ 18 mil). A bicicleta de **sistema compartilhado** (Tembici/Bike Itaú, ~R$ 16 mil/unidade — F-BIK.6) é custo de sistema, **fora da soma**.

---

## Cordão (15 unidades) — E[V]: revenda R$ 462 · reposição R$ 934

**Pesos / composição.** Modelo único cuja amostra de preço embute a forma: folheado/semijoia dominando em número de peças, ouro como minoria que concentra o valor. Cerca de 30% das faixas amostradas são de ouro (as acima de R$ 250). A forma assimétrica à direita é fundamentada academicamente (Home Office RR81: valor de bens roubados com média ≫ mediana, 2% dos furtos = 46% do valor — F-COR.1; literatura atuarial de *loss distributions* — F-COR.2); a composição segue a distribuição de mercado (folheado lidera o volume — Euromonitor, Limeira/IBGM — F-COR.5/F-COR.9) com proxies de comportamento (IBGE PNAD 2021; FBSP/Datafolha — F-COR.10/F-COR.11).

**Preços (método).** Folheado pelo varejo de semijoias (Shekinah, Prata Pura — F-COR.7); ouro por gramatura × cotação do ouro 18k (~R$ 530/g em 16/06).

**Forma.** Fortemente assimétrica à direita (folheado R$ 15–250; ouro 18k de R$ 280 a R$ 3.000 usado). A fração de ouro entra como eixo de sensibilidade.

---

## Total recuperado — estudo final (Monte Carlo, seed 20260616, 50 mil iterações)

Escopo: **celular (133) + cordão (15)**, balanço de 100 dias.

| base | E[V] | banda 90% |
|---|--:|--:|
| revenda | R$ 168 mil | R$ 150–187 mil |
| reposição | R$ 275 mil | R$ 244–309 mil |

Celulares ≈ 96% do valor; cordões ≈ 4%. Envelope extremo (cada item no modelo usado mais barato → no novo mais caro): ≈ **R$ 12 mil – 1,14 milhão**.

As motocicletas (133) e bicicletas seguem em `dados_distribuicao.json`, mas **fora desta agregação** (ver o banner no topo). As versões anteriores (com motos / com bicicletas) estão em `historico/`.
