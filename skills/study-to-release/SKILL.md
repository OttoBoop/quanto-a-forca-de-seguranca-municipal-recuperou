---
name: study-to-release
description: Gera um release curto de imprensa (~300 palavras, 1 página) a partir de um estudo/paper já pronto e auditado, com manchete parametrizável (piso conservador vs estimativa central) e checagem de fidelidade ao paper. Use DEPOIS que o estudo está fechado — a manchete é resultado do estudo, não input.
---

# Study → Release

Converte um estudo/paper técnico fechado em um **release de imprensa curto e fiel**. Destilada do caso `generic-nb-lm-agentic-search/cases/Valor monetário de recuperações da força de segurança municipal/` (2026-06). Par natural da skill [[agentic-study-latex]].

## Regra de ouro

**A manchete é o RESULTADO do paper, não um input.** Só rode esta skill quando o estudo estiver **completo e auditado** (`audit_sources` fechado). Nunca desenhe o estudo em torno da manchete; nunca rode esta skill com o paper ainda em aberto.

## Quando usar

- Existe um paper/estudo pronto (`.tex`/`.md`) + `inventario_fontes.md`, e o usuário quer um release/nota para imprensa.

## Inputs

1. Caminho do paper pronto e do `inventario_fontes.md`.
2. **Framing** (parametrizável): `piso` (lidera com o limite inferior defensável — à prova de contestação) ou `central` (lidera com a estimativa central — mais impacto). **Default: gerar AS DUAS variantes** e deixar o humano escolher (é uma decisão dele, geralmente adiada até ver a confiabilidade dos números).
3. Janela temporal / quem fez (ex.: SEGUR/Força Municipal, 15/03–08/06).

## Como montar (template `templates/release_template.md`)

1. **Manchete** — em 2 variantes (piso e central), claramente marcadas para o humano escolher.
2. **Lead** (1 parágrafo): o quê, quem, quando, o número-cabeça com a ressalva de que é estimativa de mercado.
3. **Corpo** (1–2 parágrafos): abre pelo item dominante; cada cifra com a fonte resumida (FIPE, mercado de usados, cotação etc.).
4. **Ressalva** (1 frase): a maior incerteza do estudo, em linguagem leiga.
5. **Nota de método** (1 frase): cita as fontes de dados (não os bastidores da IA).

## Regras duras

- **Fidelidade:** toda cifra do release tem que existir no paper/inventário. Rode a checagem: nenhum número novo, nenhum superlativo sem número por trás.
- **Sem bastidores de IA** no texto público (workaround de pipeline, falha de fetch, retry de agente). Atribua achados à análise/IA, **não** ao porta-voz humano. Cite a fonte do dado (ex.: FIPE, Anuário FBSP), não "uma IA descobriu".
- **Não afirme mais do que o paper sustenta.** O release é recorte fiel, não amplificação.
- **Conservadorismo no piso:** para público adversarial, a variante `piso` ("pelo menos R$ X") é a mais defensável.

## Verificação

```bash
# toda cifra do release aparece no paper/inventario (fidelidade):
# (revisar manualmente ou com check_release_fidelity.py)
python3 scripts/gerar_pdf_curto.py --input release.md   # opcional: PDF 1 página (Times 12, 1.5, A4)
```
+ checklist: manchete nas 2 variantes? cada cifra rastreável? sem superlativo sem número? nota de método cita fontes (não a IA)? sem bastidores de pipeline?

## Arquivos da skill
- `templates/release_template.md` — estrutura do release com 2 manchetes.
