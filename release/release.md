# Release — Patrimônio recuperado pela Força Municipal (V3)

> Derivado do paper V3 `paper/recuperacoes.tex` (auditado). As **motocicletas são sempre citadas à parte**, como componente adicional, separadas dos bens pessoais (celulares, bicicletas, cordões). Decisão de manchete (revenda vs reposição) é sua.

---

## ⬚ Manchete — VARIANTE A (revenda, conservador)
**Força Municipal recuperou cerca de R$ 1,96 milhão em bens em menos de três meses no Rio — R$ 185 mil em itens pessoais e R$ 1,8 milhão em motocicletas**

## ⬚ Manchete — VARIANTE B (reposição, maior impacto)
**Recuperações da Força Municipal somam cerca de R$ 2,48 milhões no Rio — R$ 312 mil em itens pessoais e R$ 2,2 milhões em motocicletas**

---

## Corpo

Entre 15 de março e 8 de junho de 2026, a Força Municipal (SEGUR, Prefeitura do Rio) recuperou ou apreendeu 118 celulares, 19 bicicletas e 15 cordões — além de 113 motocicletas, contabilizadas à parte. A preços de mercado, os itens pessoais (celulares, bicicletas e cordões) valem, em valor esperado, entre R$ 185 mil (revenda dos usados) e R$ 312 mil (custo de repor por novos). As 113 motocicletas adicionam, separadamente, entre R$ 1,77 e R$ 2,17 milhões — elevando o conjunto a um total de R$ 1,96 a R$ 2,48 milhões (de R$ 0,7 milhão a R$ 5 milhões nos extremos).

Entre os itens pessoais, o grosso está nos celulares: as 118 unidades respondem por cerca de 77%, valendo de R$ 143 mil a R$ 232 mil — de ~R$ 350 o aparelho usado mais barato a ~R$ 9.490 o flagship novo, com média de R$ 1.212 a R$ 1.964 por aparelho. A conta segue a distribuição das marcas mais roubadas no país (Samsung, Apple, Motorola, Xiaomi).

As motocicletas, tratadas à parte, são o maior componente isolado de todo o patrimônio recuperado. A conta parte da distribuição real do que mais se rouba no Rio (Honda CG 160 à frente, ranking da Polícia Civil-RJ) e da Tabela FIPE de cada modelo, do usado ao zero-quilômetro, com valor esperado de R$ 15,7 mil (revenda) a R$ 19,2 mil (reposição) por moto.

Os valores são estimativas a preços de mercado, calculadas a partir de fontes públicas (FIPE, anúncios de usados, varejo, cotação do ouro) e um modelo probabilístico com 470 preços coletados. A metodologia completa está no estudo técnico que acompanha este material.

Metodologicamente, o valor de cada bem recuperado é tratado como uma variável aleatória: sorteia-se primeiro o modelo, segundo a frequência com que é roubado na cidade, e depois o preço, a partir de uma amostra real de valores daquele modelo — em duas bases, revenda (usado) e reposição (novo). Somando os bens por simulação de Monte Carlo (50 mil repetições), obtém-se não apenas o valor esperado, mas toda a distribuição de resultados possíveis e uma faixa de 90% de confiança. Nenhum desconto arbitrário é aplicado: o preço de usado já reflete o desgaste e o de novo é o custo de repor o bem.

---
*PDF 1 página: `../../scripts/gerar_pdf_curto.py`.*
