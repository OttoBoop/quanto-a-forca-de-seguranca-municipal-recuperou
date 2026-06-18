# Quanto a Força de Segurança Municipal Recuperou

**Valor monetário do patrimônio recuperado pela Força Municipal** (SEGUR / Prefeitura do Rio de Janeiro) entre **15 de março e 8 de junho de 2026**.

Estudo quantitativo: **Prefeitura do Rio — Secretaria Municipal de Desenvolvimento Econômico & COMPSTAT RIO.**

## A pergunta

No período, a Força Municipal recuperou/apreendeu **118 celulares, 113 motocicletas, 19 bicicletas e 15 cordões**. Quanto vale, em reais, esse patrimônio? A resposta não é um número único: estima-se a **distribuição** de valores plausíveis de cada item.

## Duas versões (mesmo modelo, conjuntos de itens diferentes)

| PDF | Itens | Valor esperado | Envelope | Item dominante |
|---|---|---|---|---|
| [`paper/recuperacoes.pdf`](paper/recuperacoes.pdf) | celular, **moto**, bicicleta, cordão | **R$ 1,94 mi** (revenda) → **R$ 2,44 mi** (reposição) | R$ 0,9 – 5,0 mi | motocicletas (~90%) |
| [`paper/recuperacoes_sem_motos.pdf`](paper/recuperacoes_sem_motos.pdf) | celular, bicicleta, cordão | **R$ 169 mil** (revenda) → **R$ 275 mil** (reposição) | R$ 12 mil – 1,36 mi | celulares (~85%) |

A **metodologia é idêntica** nas duas; a única diferença é o conjunto de itens.

## Metodologia (resumo)

O valor de uma unidade recuperada é uma **variável aleatória de mistura**: sorteia-se o modelo segundo a **frequência** com que é roubado na cidade, e o preço a partir de uma **amostra de preços de mercado** daquele modelo — em duas bases: **revenda** (usado) e **reposição** (novo). O total é agregado por **Monte Carlo** (50 mil iterações, semente fixa) → valor esperado + **banda de 90%**.

- **Distribuição de modelos:** marca mais roubada (Anuário FBSP) + perfil socioeconômico (TIC); motos pelo ranking de roubo do Rio (Polícia Civil-RJ); bicicletas **de uso pessoal**, incluindo as **elétricas** (share estimado por proxies — Aliança Bike/Abraciclo — pois o ISP-RJ não separa o tipo); cordões pela prevalência folheado vs. ouro.
- **Formas de cauda pesada:** bicicleta (convencionais + e-bikes) e cordão (folheado + ouro) têm distribuição **fortemente assimétrica à direita** — massa no baixo valor, cauda fina no caro; por isso seus painéis usam escala logarítmica. A média fica bem acima da mediana nesses dois itens.
- **Preços:** 469 observações de mercado coletadas por modelo (usado e novo), em 16/06/2026.
- **Fontes:** toda cifra é referenciada — ver [`dados/proveniencia_dados.md`](dados/proveniencia_dados.md) (como cada dado foi obtido, por item), [`dados/inventario_fontes.md`](dados/inventario_fontes.md) e [`dados/dados_distribuicao.json`](dados/dados_distribuicao.json).

## Estrutura do repositório

```
paper/     papers LaTeX (com e sem motos) + PDFs + figuras (distribuições)
dados/     proveniência por item, amostras de preço (json), inventário de fontes, estatísticas
release/   textos curtos para imprensa (com e sem motos)
scripts/   coleta/transcrição, Monte Carlo + gráficos, geração de PDF
fonte/     foto do slide oficial da SEGUR (dado de origem)
skills/    método reutilizável (pesquisa→paper, paper→release)
```

## Reproduzir

```bash
python scripts/gerar_distribuicoes.py                       # versão com motos
python scripts/gerar_distribuicoes.py --exclude moto \
       --figdir figuras_sem_motos --stats dist_stats_sem_motos.md   # sem motos
latexmk -pdf paper/recuperacoes.tex
latexmk -pdf paper/recuperacoes_sem_motos.tex
```

## Caveats

Estimativas **a preços de mercado**. A composição dos itens é *proxy* (frequência de roubo/vendas; nacional onde não há recorte do Rio). As amostras de preço são aproximações, não censo. Nas motocicletas, "recuperada" (restituída) difere de "apreendida" (retida por irregularidade) — ver o paper.

---
*Período: 15/03–08/06/2026 (painel SEGUR/Força Municipal). Coleta de preços: 16/06/2026.*
