// ===================================================================
// TEMPLATE GENÉRICO de Workflow para agentic-study-latex (FASE 3).
// Estima, COM FONTES, cada "alvo" de pesquisa do seu modelo — seja ele um preço,
// uma taxa, um share, uma elasticidade, uma quantidade, o que for. Domínio-agnóstico.
//
// Cada alvo retorna: faixa [low/central/alto] + (opcional) `samples` (amostra de
// valores observados, p/ estudos distribucionais/Monte Carlo) + rationale + fontes.
// Um verificador adversarial confere plausibilidade, faixa e fontes (pode apontar
// para CIMA; nunca comprime o range).
//
// Invoque: Workflow com args = { studyContext, targets:[{key,label,prompt}] }
//   - studyContext: contexto + REGRAS DURAS (toda cifra com fonte; sem inventar).
//   - targets[].prompt: o que estimar e onde buscar (específico do seu modelo).
// Salve o resultado (objeto do tool result) p/ alimentar a agregação (FASE 4).
//
// EXEMPLO TRABALHADO (caso "valor de bens recuperados"): cada alvo = um parâmetro
// de valor (ex.: "valor de um celular recuperado"); `samples` = preços de mercado
// coletados; unit = "R$". O agregador combina por Σ N_i × amostra (ver monte_carlo_dist.py).
// ===================================================================
export const meta = {
  name: 'agentic-study-research',
  description: 'Estimativa fundamentada (faixa + amostra opcional + fontes) de cada alvo do modelo, com verificação adversarial',
  phases: [
    { title: 'Pesquisa', detail: '1 agente por alvo: faixa/amostra + fontes' },
    { title: 'Verificacao', detail: 'verificador adversarial: plausibilidade, faixa, fontes' },
  ],
}

const { studyContext, targets } = args

const CORE = `${studyContext || ''}

Estime o ALVO abaixo COM FONTES. Regras duras: toda cifra tem fonte real (org/url/valor visto/data); nada inventado; se não houver dado, diga. WebSearch + WebFetch, várias buscas.
Retorne: faixa [low, central, high] na unidade pedida; se o estudo for distribucional (Monte Carlo), inclua também \`samples\` — uma amostra de valores OBSERVADOS (não inventados) que represente a dispersão real do alvo. Retorne SOMENTE o objeto estruturado.`

const ESTIMATE_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    key: { type: 'string' },
    label: { type: 'string' },
    unit: { type: 'string', description: 'ex.: R$, %, fração, anos...' },
    low: { type: 'number' }, central: { type: 'number' }, high: { type: 'number' },
    samples: { type: 'array', items: { type: 'number' }, description: 'amostra de valores observados (opcional; p/ Monte Carlo)' },
    rationale: { type: 'string' },
    sources: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: { org: { type: 'string' }, year: { type: 'string' }, title: { type: 'string' }, url: { type: 'string' }, value_seen: { type: 'string' }, date_accessed: { type: 'string' } },
        required: ['org', 'title', 'url', 'value_seen', 'date_accessed'],
      },
    },
  },
  required: ['key', 'label', 'unit', 'low', 'central', 'high', 'rationale', 'sources'],
}

const VERDICT_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    key: { type: 'string' },
    plausible: { type: 'boolean' }, range_ok: { type: 'boolean' }, sourcing_ok: { type: 'boolean' },
    corrections: { type: 'string', description: 'ajustes com fonte (org+url+valor) ou "nenhum"; pode apontar para CIMA' },
  },
  required: ['key', 'plausible', 'range_ok', 'sourcing_ok', 'corrections'],
}

phase('Pesquisa')
const results = await pipeline(
  targets,
  (t) => agent(`${CORE}\n\nALVO (${t.key}): ${t.prompt}`, { label: `pesquisa:${t.key}`, phase: 'Pesquisa', schema: ESTIMATE_SCHEMA }),
  (est, t) => {
    if (!est) return { key: t.key, estimate: null, verdict: null }
    const vp = `VERIFICADOR ADVERSARIAL (2ª fonte independente). Alvo "${t.label}" (${est.unit}). Estimativa:
${JSON.stringify({ low: est.low, central: est.central, high: est.high, n_samples: (est.samples || []).length, rationale: est.rationale }, null, 2)}
1. plausible: a faixa bate com a realidade (sem absurdo/invenção)? Spot-check 1-2 valores numa 2ª fonte.
2. range_ok: low/central/high cobrem o leque real (não comprimido para o piso)? Se subestimado, aponte para CIMA.
3. sourcing_ok: há fontes reais?
corrections: ajustes com fonte, ou "nenhum". Retorne SOMENTE o objeto.`
    return agent(vp, { label: `verifica:${t.key}`, phase: 'Verificacao', schema: VERDICT_SCHEMA }).then((v) => ({ key: t.key, estimate: est, verdict: v }))
  }
)
log(`Pesquisa+verificação: ${results.filter(Boolean).length}/${targets.length} alvos`)
return results.filter(Boolean)
