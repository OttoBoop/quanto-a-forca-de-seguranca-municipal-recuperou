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
2. **O modelo do estudo**: uma equação que liga os parâmetros à grandeza de interesse (ex.: $V=\sum_i N_i\,v_i$, mas pode ser qualquer modelo) e como cada termo se decompõe.
3. **Lista de alvos a estimar** (preços, taxas, shares, quantidades, elasticidades…), cada um com faixa [baixo/central/alto] e, se distribucional, uma amostra.
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
- `pipeline(targets, pesquisar, verificar)`: 1 agente por **alvo do modelo** (preço, taxa, share, quantidade, elasticidade — o que seu modelo pedir) estima uma **faixa [baixo/central/alto]** e, se o estudo for distribucional, uma **amostra `samples`** de valores observados — tudo **com fontes** (org/url/valor/data). Um **verificador adversarial** confere plausibilidade/faixa/fontes (pode apontar **para cima**; nunca comprime o range).
- Saídas: a tabela de estimativas (vira `modelo_valores.md`) e o `inventario_fontes.md` (F-T.N).

### FASE 4 — Agregação, figuras e paper acadêmico
- **Agregação:** propague as faixas pelo **seu modelo** → intervalo total. Para estudo **distribucional**, monte `agg_input.json` (componentes do seu modelo: `{label, count, samples:{base:[...]}}`) e rode `templates/monte_carlo_dist.py` → `figuras/dist_itens.png` + `dist_total.png` + `dist_stats.md` (E, p5–p95, banda de 90% por **Monte Carlo, seed fixa**). *A combinação componente↔contagem é específica do seu modelo — você monta o `agg_input.json` a partir da saída da FASE 3.*
- **Paper:** preencha `templates/paper_skeleton.tex` (acadêmico) — **troque a equação de exemplo pela do seu modelo**; cada `\tbd{}` ← estimativas + F-T.N (valor + citação). Gere as figuras **antes** de compilar; `latexmk -pdf`.
- **Honestidade:** banda 90% = incerteza de **amostragem** (estreita por agregar N unidades); incerteza **estrutural** mora no envelope/sensibilidade. Declarar amostra ≠ censo.

### FASE 5 — Auditoria (obrigatória)
Audite (estilo `audit_sources`): toda cifra do paper tem entrada no inventário? As contas batem? As fontes load-bearing resolvem? **Monte Carlo reprodutível (re-rodar com a seed → mesmos números)? $\mathbb{E}[V]$ bate com o somatório?** Gere `auditoria_fontes.md`. Leve ⚠️/❓ ao humano; aplique correções conservadoras autonomamente.

## Verificação (definição de pronto)

```bash
latexmk -pdf paper/<nome>.tex            # compila sem erro
grep -c "A PESQUISAR\|\\tbd{" paper/<nome>.tex   # => 0 (nenhuma pendência)
python3 -c "import fitz; print(fitz.open('paper/<nome>.pdf').page_count)"  # PDF existe
```
+ toda cifra ∈ inventário; a **tabela de contribuição mostra o item dominante** (sanidade: se o item que deveria dominar não domina, há erro de ordem de grandeza).

## Lições destiladas (do exemplo trabalhado — valem em geral)

- **MODELO (a lição-mãe):** capture a **heterogeneidade real** — modele a distribuição dos tipos por uma **fonte de frequência** (não um ponto único) e escolha a **base de valor** certa. No exemplo de bens: distribuição de modelos × dois preços — usado (revenda) e novo (reposição) —, do usado mais barato ao novo mais caro. **NUNCA** preço já usado × fator de depreciação (duplo desconto: o mercado de usado já precifica o desgaste). Condição/estado entra só como **haircut factual nomeado**; a maior incerteza vira **eixo de sensibilidade**, não número cravado.
- **Não pule para a conclusão/manchete.** A manchete/release é resultado *downstream*; o estudo entrega **todos os ranges**, não um número conservador único. Release é skill separada ([[study-to-release]]), depois.
- **`siunitx` pode não existir** — defina `\newcommand{\reais}[1]{R\$\,#1}`.
- **Verificação adversarial valida o range inteiro** (pode apontar para cima); não enviesa para o piso.
- **"preço de sistema" vs "preço unitário"**: ex. "bike do Itaú"/Tembici (~R$16k/unidade) é custo de sistema — baliza/teto, **nunca** na soma.
- **Reporte em tempo real** ao humano durante a FASE 3 (regra dura do `agentic_research`).
- **No entregável humano**, não documente bastidores da IA; atribua achados à IA, não ao usuário.

## Arquivos da skill (genéricos — adapte ao seu modelo)
- `templates/research_workflow.js` — Workflow **genérico**: 1 agente por alvo → faixa [baixo/central/alto] + amostra opcional + fontes; verificação adversarial. Domínio-agnóstico.
- `templates/monte_carlo_dist.py` — agregação distribucional **genérica**, config-driven por `agg_input.json` (componentes/contagem/bases) → KDE por componente + total com banda 90% (seed fixa).
- `templates/paper_skeleton.tex` — esqueleto de paper acadêmico (equação do modelo + figuras + `\tbd{}`); troque a equação de exemplo pela do seu estudo.

## Exemplo trabalhado (referência concreta)
Caso **"valor de bens recuperados pela Força Municipal"** (pasta do caso / repo público `quanto-a-forca-de-seguranca-municipal-recuperou`): alvos = valor por categoria de item; `samples` = preços de mercado coletados; `agg_input.json` = itens × quantidade $N_i$ × amostras (revenda/reposição). Use-o para ver os templates preenchidos ponta a ponta.
