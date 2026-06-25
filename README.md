# Quanto a Força de Segurança Municipal Recuperou

**Valor monetário do patrimônio recuperado pela Força Municipal** (SEGUR / Prefeitura do Rio de Janeiro) nos **primeiros 100 dias** de atuação (**15 de março a 23 de junho de 2026**).

Estudo quantitativo: **Prefeitura do Rio — Secretaria Municipal de Desenvolvimento Econômico & COMPSTAT RIO.**

## A pergunta

No balanço de 100 dias, a Força Municipal recuperou/apreendeu **133 celulares e 15 cordões** (entre outros itens). Quanto vale, em reais, esse patrimônio? A resposta não é um número único: estima-se a **distribuição** de valores plausíveis de cada item.

## O estudo

| PDF | Itens valorados | Valor esperado | Envelope | Item dominante |
|---|---|---|---|---|
| [`paper/recuperacoes.pdf`](paper/recuperacoes.pdf) | celular (133), cordão (15) | **R$ 168 mil** (revenda) → **R$ 275 mil** (reposição) | R$ 12 mil – 1,14 mi | celulares (~96%) |

**Escopo.** O estudo valora **celulares e cordões**. As **133 motocicletas**, as armas e os demais resultados operacionais do balanço entram como **contexto, não valorados**. As **bicicletas foram retiradas** do balanço pelo órgão (a pesquisa anterior, com bicicletas elétricas, segue documentada nos dados e nas versões históricas).

## Contexto operacional (100 dias)

Atuação em **10 áreas**, com implantação escalonada (Rodoviária do Rio desde 15/03 … Méier-Cachambi desde 07/06). O balanço oficial registra queda de roubos/furtos nas três primeiras áreas (−41,7% / −8,5% / −11,4%), >6 mil abordagens, 771 conduções, 133 motocicletas recuperadas e a retirada de 1 arma de fogo, 5 réplicas e 42 armas brancas. Fonte: [`fonte/slide_100dias.jpeg`](fonte/slide_100dias.jpeg).

## Metodologia (resumo)

O valor de uma unidade recuperada é uma **variável aleatória de mistura**: sorteia-se o modelo segundo a **frequência** com que é roubado na cidade, e o preço a partir de uma **amostra de preços de mercado** daquele modelo — em duas bases: **revenda** (usado) e **reposição** (novo). O total é agregado por **Monte Carlo** (50 mil iterações, semente fixa) → valor esperado + **banda de 90%**.

- **Distribuição de modelos:** celulares pela marca mais roubada (Anuário FBSP) + perfil socioeconômico (TIC); cordões pela prevalência folheado vs. ouro.
- **Forma do cordão:** distribuição **fortemente assimétrica à direita** (folheado domina; ouro na cauda) — média bem acima da mediana; o painel usa escala logarítmica.
- **Preços:** 215 observações de mercado por modelo (usado e novo), coletadas em 16/06/2026.
- **Fontes:** toda cifra é referenciada — ver [`dados/proveniencia_dados.md`](dados/proveniencia_dados.md) (como cada dado foi obtido, por item), [`dados/inventario_fontes.md`](dados/inventario_fontes.md) e [`dados/dados_distribuicao.json`](dados/dados_distribuicao.json).

## Versões anteriores

As versões anteriores (janela de 85 dias, que **incluíam motocicletas** e **bicicletas/e-bikes**) estão preservadas em [`historico/`](historico/) — ver [`historico/README.md`](historico/README.md). Foram superadas pelo balanço de 100 dias (celulares 118→133; bicicletas retiradas pelo órgão; motos fora da valoração).

## Estrutura do repositório

```
paper/      estudo final (LaTeX + PDF) + figuras (distribuições)
dados/      proveniência por item, amostras de preço (json), inventário de fontes, estatísticas
release/    texto curto para imprensa (2 variantes de manchete)
historico/  versões anteriores (com motos / com bicicletas), congeladas
scripts/    coleta/transcrição, Monte Carlo + gráficos, geração de PDF
fonte/      slides oficiais da SEGUR (balanço de 100 dias e anterior)
skills/     método reutilizável (pesquisa→paper, paper→release)
```

## Reproduzir

```bash
python scripts/gerar_distribuicoes.py --exclude moto bicicleta   # estudo final (celular + cordão)
latexmk -pdf paper/recuperacoes.tex
```

## Caveats

Estimativas **a preços de mercado**. A composição dos itens é *proxy* (frequência de roubo/vendas; nacional onde não há recorte do Rio). As amostras de preço são aproximações, não censo. As 10 áreas entraram em datas diferentes, então o total acumulado não corresponde a 100 dias uniformes em toda a cidade.

---
*Balanço de 100 dias: 15/03–23/06/2026 (painel SEGUR/Força Municipal). Coleta de preços: 16/06/2026.*
