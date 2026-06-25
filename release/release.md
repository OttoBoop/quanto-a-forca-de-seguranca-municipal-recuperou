# Release — Patrimônio recuperado pela Força Municipal (100 dias)

> Derivado do paper `paper/recuperacoes.tex` (balanço de 100 dias; valoração de **celulares e cordões**). Motocicletas, armas e resultados operacionais entram como contexto, não valorados. Decisão de manchete (revenda vs reposição) é sua.

---

## ⬚ Manchete — VARIANTE A (revenda, conservador)
**Força Municipal recuperou cerca de R$ 168 mil em celulares e cordões nos primeiros 100 dias no Rio**

## ⬚ Manchete — VARIANTE B (reposição, maior impacto)
**Itens recuperados pela Força Municipal somam cerca de R$ 275 mil em 100 dias no Rio — o custo de repô-los por novos**

---

## Corpo

Nos primeiros 100 dias de atuação (15 de março a 23 de junho de 2026), a Força Municipal (SEGUR, Prefeitura do Rio) recuperou ou apreendeu 133 celulares e 15 cordões. A preços de mercado, esse patrimônio vale, em valor esperado, entre R$ 168 mil (revenda dos usados) e R$ 275 mil (custo de repor por novos) — podendo ir de R$ 12 mil a R$ 1,14 milhão nos extremos.

O grosso do valor está nos celulares: as 133 unidades respondem por cerca de 96% do total, valendo entre R$ 161 mil (revenda) e R$ 261 mil (reposição) — de ~R$ 350 o aparelho de entrada usado a milhares de reais o flagship novo, com média de R$ 1.212 a R$ 1.964 por aparelho. A conta segue a distribuição das marcas mais roubadas no país (Samsung, Apple, Motorola, Xiaomi) e os preços de mercado de cada modelo, do usado ao zero-quilômetro. Os 15 cordões respondem pelos demais ~4%.

A atuação se deu em 10 áreas, com implantação escalonada — da Rodoviária do Rio (desde 15 de março) ao Méier-Cachambi (desde 7 de junho). No mesmo período, o balanço oficial registra queda de roubos e furtos nas três primeiras áreas (Rodoviária e entorno −41,7%; Jardim de Alah −8,5%; Presidente Vargas e entorno −11,4%), mais de 6 mil abordagens, 771 conduções a delegacias, 133 motocicletas recuperadas e a retirada de 1 arma de fogo, 5 réplicas e 42 armas brancas das ruas — itens não incluídos na valoração acima.

**Ressalva.** A composição exata dos bens recuperados não foi divulgada: o mix vem da frequência de roubo e venda na cidade, e os preços são amostras de mercado (não um censo) — os valores podem oscilar conforme os modelos efetivamente apreendidos. Como as 10 áreas entraram em datas diferentes, o total acumulado não corresponde a 100 dias uniformes em toda a cidade.

Os valores são estimativas a preços de mercado, calculadas a partir de fontes públicas (anúncios de usados, varejo e cotação do ouro) e um modelo probabilístico com 215 preços coletados por modelo. A metodologia completa está no estudo técnico que acompanha este material.

No método, o valor de cada bem recuperado é uma variável aleatória: sorteia-se primeiro o modelo, segundo a frequência com que é roubado na cidade, e depois o preço, a partir de uma amostra real de valores daquele modelo — em duas bases, revenda (usado) e reposição (novo). Somando os bens por simulação de Monte Carlo (50 mil repetições), obtém-se não apenas o valor esperado, mas toda a distribuição de resultados possíveis e uma faixa de 90% de confiança. Nenhum desconto arbitrário é aplicado: o preço de usado já reflete o desgaste e o de novo é o custo de repor o bem.

---
*PDF 1 página: `../../scripts/gerar_pdf_curto.py`.*
