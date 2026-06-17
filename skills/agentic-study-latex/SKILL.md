---
name: agentic-study-latex
description: Produz um paper acadêmico em LaTeX (PDF, com equações) a partir de uma fonte + um conjunto de itens/quantidades + um modelo paramétrico, rodando pesquisa agêntica por parâmetro (com fontes verificáveis) e verificação adversarial de cada cifra. Use para estudos quantitativos onde cada número precisa de fonte citável e o resultado é um intervalo [baixo/central/alto].
---

# Agentic Study → LaTeX

Transforma uma pergunta quantitativa ("quanto vale X?", "qual o impacto econômico de Y?") em um **paper LaTeX** fundamentado: abre com uma equação do modelo, pesquisa a faixa de cada parâmetro com fontes, e fecha com um intervalo total. Destilada do caso `generic-nb-lm-agentic-search/cases/Valor monetário de recuperações da força de segurança municipal/` (2026-06).

Complementa a pipeline V5 (NotebookLM + `agentic_research` + `audit_sources`), mas o entregável final é um **paper multi-página com equações** — não a manifestação `.md` + PDF de 1 página. Para gerar o release de imprensa depois, use a skill [[study-to-release]].

## Quando usar

- O usuário quer um estudo com modelo formal (equação) e números fundamentados, não só prosa.
- Cada cifra precisa de fonte citável (`(SOBRENOME/ÓRGÃO. "Título", Veículo, Ano)`) e inventário F-T.N.
- O resultado natural é uma faixa **[baixo, central, alto]**, não um número único.

## Inputs (peça ao usuário / defina no plano)

1. **Fonte** com as quantidades $N_i$ (slide, PDF, planilha). Transcreva áudios com `scripts/transcrever_audio.py` (faster-whisper).
2. **Modelo paramétrico**: a equação $V=\sum_i N_i\,v_i$ e como $v_i$ se decompõe em parâmetros (preços, fatores, shares).
3. **Lista de parâmetros a estimar**, cada um com faixa [baixo/central/alto].
4. **Decisões travadas** (escopo, conservadorismo, o que entra no total).

## Fluxo (FASES, ancorado no V5)

### FASE 0 — Plano de longo prazo
Escreva `LONG_TERM_GOALS.md` + `LOGS.md` (append-only) na pasta do caso. Trave: objetivo, fontes, decisões (Dn), modelo, padrões de qualidade, checkpoints. Uma instância fresca retoma lendo esses dois. **Peça aprovação do plano antes de gastar agentes.**

### FASE 1 — Base de conhecimento (NotebookLM) — *condicional*
Para claims **acadêmicos/institucionais estáveis**, crie um NB dedicado (`scripts/nb_create_notebook.py`) e suba ≥6 fontes curadas; pesquisa NB-first (≥3 queries).
**LIÇÃO (preço/dado de mercado ao vivo):** NB-RAG é ruim para garimpar OLX/FIPE/cotações. Inverta para **NB-after-capture** — a web descobre o valor, e a *evidência de coleta* (busca filtrada + data, ou print/PDF da consulta) é depositada no NB depois, como substrato de auditoria. Se a criação do NB travar (W-5: fica em `/notebook/creating`), não bloqueie: documente as fontes por URL+data e siga (a auditoria verifica via web). Use `scripts/nb_list_notebooks.py` para recuperar URLs.

### FASE 2 — Decomposição
Um **tópico por item/parâmetro** (ex.: 1 pesquisador por item recuperado). Liste as sub-perguntas de cada um (preços, share, depreciação).

### FASE 3 — Pesquisa + verificação (Workflow determinístico)
**Não use a skill `agentic_research` crua aqui** (histórico de crash, EC-5). Rode um **Workflow** (template `templates/research_workflow.js`):
- `pipeline(items, pesquisar, verificar)`: 1 agente monta a **distribuição de modelos** do item (peso $w_m$ de fonte de FREQUÊNCIA + `price_used` + `price_new` por modelo, com fontes URL+valor+data), e um **verificador adversarial** valida o **range completo** (pesos somam 1, piso=SKU usado mais barato real, teto=SKU novo mais caro real) — **não** "puxa para o piso". Schema estruturado força JSON.
- Aplique as correções do verificador (que podem apontar **para cima**).
- Saídas: `modelo_valores.md` (matrizes + propagação nas 2 bases + contribuição) e `inventario_fontes.md` (F-T.N).

### FASE 4 — Montagem do paper
Use `templates/paper_skeleton.tex`. Para cada `\tbd{}`: preencha com `valor + citação + 1 linha de "por que essa fonte"` a partir do F-T.N. Propagação nas duas bases: $\bar v_i^{b}=\sum_m w_{i,m}p_{i,m}^{b}$ para $b\in\{\text{rev,rep}\}$; piso/teto absolutos = SKU usado mais barato / novo mais caro. Tabela de contribuição por item; sensibilidade para a incerteza dominante. Compile com `latexmk -pdf`.

### FASE 4* — Tratamento probabilístico + gráficos (opcional, recomendado)
Quando o usuário quer **distribuição de probabilidade de valor** (histograma de "qual a prob.\ de um item valer $y$"), suba um nível:
- **Colete preços brutos** por modelo (arrays `prices_used`/`prices_new`, ~8–15 obs/modelo; FIPE por ano-modelo dá dispersão natural; Trocafy/varejo fetcháveis; OLX/ML só por snippet). Salve em `dados_distribuicao.json`.
- **Modelo = v.a. de mistura:** $V_i^b\sim\sum_m w_{i,m}\hat F_{i,m}^b$ (sorteia modelo por peso → preço da amostra). $\mathbb{E},\mathrm{Var}$ fechadas; total $V^b=\sum_i\sum_{k}^{N_i}V_{i,k}^b$ por **Monte Carlo (seed fixa)** → média + **banda 90%**.
- **Gráficos** com `templates/monte_carlo_dist.py` (venv com matplotlib/numpy/scipy; estilo dpi 200, KDE): por item (`dist_itens.png`) + total com banda (`dist_total.png`) + `dist_stats.md`.
- **Paper acadêmico:** Abstract · Introdução · Metodologia (modelo probabilístico + distribuição + coleta + Monte Carlo) · Resultados (figuras + tabelas) · Conclusões · Limitações · Fontes. Preâmbulo ganha `\usepackage{graphicx,float}` + `\graphicspath{{figuras/}}`; figuras via `\includegraphics[width=\linewidth]{...}`.
- Honestidade: banda 90% = incerteza de **amostragem** (estreita por agregação de N unidades); incerteza **estrutural** mora no envelope [piso, teto] e na sensibilidade. Declarar amostra ≠ censo.

### FASE 5 — Auditoria (obrigatória)
Audite (estilo `audit_sources`): toda cifra do paper tem entrada no inventário? As contas batem? As fontes load-bearing resolvem? **Monte Carlo reprodutível (re-rodar com a seed → mesmos números)? $\mathbb{E}[V]$ bate com o somatório?** Gere `auditoria_fontes.md`. Leve ⚠️/❓ ao humano; aplique correções conservadoras autonomamente.

## Verificação (definição de pronto)

```bash
latexmk -pdf paper/<nome>.tex            # compila sem erro
grep -c "A PESQUISAR\|\\tbd{" paper/<nome>.tex   # => 0 (nenhuma pendência)
python3 -c "import fitz; print(fitz.open('paper/<nome>.pdf').page_count)"  # PDF existe
```
+ toda cifra ∈ inventário; a **tabela de contribuição mostra o item dominante** (sanidade: se o item que deveria dominar não domina, há erro de ordem de grandeza).

## Lições destiladas (V1 errada → V2 correta)

- **MODELO DE VALOR (a lição-mãe):** valor de bens recuperados = **distribuição real de modelos** (peso por fonte de FREQUÊNCIA: roubo/vendas/frota) **× dois preços por modelo: usado (revenda) e novo (reposição)**. O range vai do **modelo usado mais barato ao novo mais caro** (bracket de 4: $V^{\min}, V^{\text{rev}}, V^{\text{rep}}, V^{\max}$). **NUNCA** preço único × fator de depreciação $\delta$ — isso é duplo desconto (o mercado de usado já precifica o desgaste) e foi o erro da V1. Estado físico entra só como **haircut factual nomeado** na revenda (ex.: celular bloqueado = só peças; moto com restrição = −25%); incerteza dominante vira **eixo de sensibilidade**, não número cravado.
- **Não pule para a conclusão/manchete.** A manchete/release é resultado *downstream*; o estudo entrega **todos os ranges**, não um número conservador único. Release é skill separada ([[study-to-release]]), depois.
- **`siunitx` pode não existir** — defina `\newcommand{\reais}[1]{R\$\,#1}`.
- **Verificação adversarial valida o range inteiro** (pode apontar para cima); não enviesa para o piso.
- **"preço de sistema" vs "preço unitário"**: ex. "bike do Itaú"/Tembici (~R$16k/unidade) é custo de sistema — baliza/teto, **nunca** na soma.
- **Reporte em tempo real** ao humano durante a FASE 3 (regra dura do `agentic_research`).
- **No entregável humano**, não documente bastidores da IA; atribua achados à IA, não ao usuário.

## Arquivos da skill
- `templates/paper_skeleton.tex` — esqueleto LaTeX com equações + `\tbd{}`.
- `templates/research_workflow.js` — Workflow de pesquisa+verificação adversarial por item (schema com `prices_used`/`prices_new` arrays para a variante probabilística).
- `templates/monte_carlo_dist.py` — distribuições de mistura + Monte Carlo do total + gráficos (KDE por item, total com banda 90%, seed fixa). Lê `dados_distribuicao.json`.
