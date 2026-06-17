// ===================================================================
// TEMPLATE de Workflow para agentic-study-latex (FASE 3) — V2.
// Lição V2 (caso Forca Municipal, 2026-06): NAO use preco unico x fator de
// depreciacao (duplo desconto). Modele a DISTRIBUICAO REAL de modelos (peso de
// FONTE DE FREQUENCIA) e DOIS precos por modelo: usado (revenda) e novo (reposicao).
// Invoque via Workflow com args = { studyContext, items:[{key,label,prompt}] }.
// ===================================================================
export const meta = {
  name: 'agentic-study-research-v2',
  description: 'Distribuicao real de modelos por item (peso por frequencia) x dois precos (usado/revenda, novo/reposicao), com validacao adversarial do range completo',
  phases: [
    { title: 'Distribuicao', detail: 'matriz modelo x peso x usado x novo por item' },
    { title: 'Validacao', detail: 'verificador valida distribuicao + piso/teto reais + fontes' },
  ],
}

const { studyContext, items } = args

const DIST_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    item: { type: 'string' },
    distribution_basis: { type: 'string', description: 'fonte(s) de FREQUENCIA dos pesos + nota Rio-ouro vs proxy' },
    models: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          name: { type: 'string' },
          weight: { type: 'number', description: '0-1; pesos somam ~1' },
          price_used: { type: 'number', description: 'R$ usado/revenda' },
          price_new: { type: 'number', description: 'R$ novo/reposicao' },
          sources: {
            type: 'array',
            items: {
              type: 'object', additionalProperties: false,
              properties: {
                org: { type: 'string' }, year: { type: 'string' }, title: { type: 'string' },
                url: { type: 'string' }, value_seen: { type: 'string' }, date_accessed: { type: 'string' },
              },
              required: ['org', 'year', 'title', 'url', 'value_seen', 'date_accessed'],
            },
          },
        },
        required: ['name', 'weight', 'price_used', 'price_new', 'sources'],
      },
    },
    floor_used: { type: 'object', additionalProperties: false, properties: { model: { type: 'string' }, price: { type: 'number' }, url: { type: 'string' } }, required: ['model', 'price', 'url'] },
    ceiling_new: { type: 'object', additionalProperties: false, properties: { model: { type: 'string' }, price: { type: 'number' }, url: { type: 'string' } }, required: ['model', 'price', 'url'] },
    haircuts: { type: 'string', description: 'haircuts factuais nomeados (so na base revenda), nunca um delta generico' },
    caveats: { type: 'string' },
  },
  required: ['item', 'distribution_basis', 'models', 'floor_used', 'ceiling_new', 'haircuts', 'caveats'],
}

const VERDICT_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    item: { type: 'string' },
    distribution_ok: { type: 'boolean' }, floor_ok: { type: 'boolean' }, ceiling_ok: { type: 'boolean' }, sourcing_ok: { type: 'boolean' },
    corrections: { type: 'string', description: 'ajustes com fonte (org+url+valor) ou "nenhum"; pode apontar para CIMA' },
    overall: { type: 'string' },
  },
  required: ['item', 'distribution_ok', 'floor_ok', 'ceiling_ok', 'sourcing_ok', 'corrections', 'overall'],
}

phase('Distribuicao')
const results = await pipeline(
  items,
  (it) => agent(it.prompt + '\nRetorne SOMENTE o objeto estruturado.', { label: `dist:${it.key}`, phase: 'Distribuicao', schema: DIST_SCHEMA }),
  (research, it) => {
    if (!research) return { item: it.label, research: null, verdict: null }
    const vp = `Voce e VERIFICADOR do RANGE COMPLETO (NAO "puxe para o piso"). Item "${it.label}".
DISTRIBUICAO E PRECOS (JSON):
${JSON.stringify({ distribution_basis: research.distribution_basis, models: research.models, floor_used: research.floor_used, ceiling_new: research.ceiling_new, haircuts: research.haircuts }, null, 2)}
Verifique com 2a fonte independente (WebSearch/WebFetch):
1. distribution_ok: pesos de fonte de FREQUENCIA real (share/vendas/roubo), somam ~1, plausiveis?
2. floor_ok: piso e SKU usado real e dos mais baratos? ceiling_ok: teto e SKU novo real e dos mais caros do nucleo?
3. sourcing_ok: cada modelo tem price_used E price_new com fonte? Spot-check 2-3 precos load-bearing.
4. corrections: ajustes com fonte, ou "nenhum". Se algo esta SUBestimado, aponte para CIMA. NAO comprima o range.
Retorne SOMENTE o objeto estruturado.`
    return agent(vp, { label: `valida:${it.key}`, phase: 'Validacao', schema: VERDICT_SCHEMA }).then((v) => ({ item: it.label, research, verdict: v }))
  }
)
log(`Distribuicao+validacao: ${results.filter(Boolean).length}/${items.length} itens`)
return results.filter(Boolean)
