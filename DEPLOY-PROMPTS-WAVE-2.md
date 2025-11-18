# 🚀 Deployment Prompts - Wave 2 (Performance)

**Onda:** Wave-2 (Otimizações de Performance)
**Data de criação:** 2025-11-18
**Uso:** Copiar e colar em novas sessões Claude Code Web

---

## 📋 Instruções Gerais

### Para o Usuário (Orquestrador)

1. **Abra 3 sessões separadas do Claude Code Web** (uma para cada agent)
2. **Conecte cada sessão ao repositório** `HenriqueMFS/APP_SLIDE_OBA`
3. **Copie o prompt correspondente** e cole em cada sessão
4. **Aguarde conclusão** de cada agent (2-3 horas por agent, paralelo)
5. **Execute merges** conforme ordem definida em PARALLEL-WORK-TRACKER-WAVE-2.md

### Notas Importantes

- ✅ Agents trabalham **simultaneamente** (não esperar um terminar para começar outro)
- ✅ Cada agent tem **branch isolada** (zero conflitos esperados)
- ✅ Agents devem **atualizar PARALLEL-WORK-TRACKER-WAVE-2.md** em milestones
- ✅ Agents devem **criar REPORT-AGENT-X.md** ao concluir
- ⚠️ **Não iniciar merges** até todos os 3 agents concluírem

---

## 🎯 PROMPT PARA AGENT-D (Cache e Validações)

```markdown
Você é o Agent-D, responsável por implementar otimizações de cache e validações no projeto APP_SLIDE_OBA.

## SUA MISSÃO

Implementar 3 otimizações CRÍTICAS de performance:
1. Cache de logo com @st.cache_resource (ganho: 30x)
2. Cache de extração de dados com @st.cache_data (ganho: 100-250x em re-runs)
3. Validações de tamanho de arquivo (previne crashes)

## INSTRUÇÕES

1. **Leia seu briefing completo:**
   - Arquivo: `BRIEFING-AGENT-D-CACHE.md`
   - Contém: Código exato, linhas específicas, testes obrigatórios

2. **Leia o contexto:**
   - `FEATURES-PARALLEL-WAVE-2.md` - Sua feature F1-CACHE-VALIDATION
   - `PERFORMANCE-ANALYSIS.md` - Problemas que você vai resolver

3. **Execute o briefing passo a passo:**
   - Siga EXATAMENTE as instruções do briefing
   - Faça commits incrementais (não um único commit)
   - Teste cada entrega antes de commitar

4. **Atualize o tracker em milestones:**
   - 25% (cache logo), 50% (cache dados), 75% (validações), 100% (push)
   - Arquivo: `PARALLEL-WORK-TRACKER-WAVE-2.md`

5. **Crie seu report final:**
   - Arquivo: `REPORT-AGENT-D.md`
   - Template está no briefing

## ENTREGAS OBRIGATÓRIAS

- [x] Cache de logo (função carregar_logo com @st.cache_resource)
- [x] Cache de extração (função extrair_dados_cached com @st.cache_data)
- [x] Validações de tamanho (validar_tamanho_arquivo)
- [x] Testes de validação executados
- [x] 4 commits (cache logo, cache dados, validações, report)
- [x] Push para `claude/perf-cache-validation-{SESSION_ID}`
- [x] REPORT-AGENT-D.md criado

## CRITÉRIOS DE SUCESSO

- ✅ Logo carrega 1 vez por sessão (não a cada interação)
- ✅ DOCX processa 1 vez (re-runs instantâneos)
- ✅ Arquivos >10MB DOCX e >20MB PPTX são rejeitados
- ✅ Performance: 30-40% mais rápido
- ✅ Funcionalidade preservada (sem quebrar código existente)

## AVISOS CRÍTICOS

- ❌ NÃO modificar função _identificar_colunas_tabela (é do Agent-E)
- ❌ NÃO modificar função gerar_apresentacao internamente (é do Agent-F)
- ❌ NÃO fazer refatorações além do escopo
- ✅ FOQUE apenas em cache e validações

## INÍCIO

Execute:
```bash
git status
git checkout -b claude/perf-cache-validation-{SESSION_ID}
```

Depois leia `BRIEFING-AGENT-D-CACHE.md` e comece a implementação.

Boa sorte! Sua missão é CRÍTICA para o sucesso da Wave-2! 🚀
```

---

## 🎯 PROMPT PARA AGENT-E (Constantes e Regex)

```markdown
Você é o Agent-E, responsável por refatorar aliases e regex para constantes globais no projeto APP_SLIDE_OBA.

## SUA MISSÃO

Implementar 2 refatorações de ALTA prioridade:
1. Mover aliases para constantes globais pré-normalizadas (ganho: 1.5x)
2. Compilar regex patterns como constantes (ganho: 20-30%)

## INSTRUÇÕES

1. **Leia seu briefing completo:**
   - Arquivo: `BRIEFING-AGENT-E-CONSTANTS.md`
   - Contém: Código exato, aliases completos, regex a compilar

2. **Leia o contexto:**
   - `FEATURES-PARALLEL-WAVE-2.md` - Sua feature F2-CONSTANTS-REGEX
   - `PERFORMANCE-ANALYSIS.md` - Problemas 2.1 (aliases) e 4.2 (regex)

3. **IMPORTANTE - Copie aliases originais:**
   - Leia função `_identificar_colunas_tabela` (linhas ~176-336)
   - Copie EXATAMENTE todos os aliases para ALIASES_CAMPOS
   - NÃO invente novos aliases, NÃO remova aliases existentes

4. **Execute o briefing passo a passo:**
   - Criar constantes globais no topo do arquivo
   - Remover ~60 linhas de aliases locais
   - Compilar regex patterns
   - Atualizar funções para usar constantes

5. **Atualize o tracker em milestones:**
   - 25%, 50%, 75%, 100%
   - Arquivo: `PARALLEL-WORK-TRACKER-WAVE-2.md`

6. **Crie seu report final:**
   - Arquivo: `REPORT-AGENT-E.md`
   - Template está no briefing

## ENTREGAS OBRIGATÓRIAS

- [x] ALIASES_CAMPOS criado (todos os aliases originais)
- [x] ALIASES_NORMALIZADOS calculado
- [x] PRIORIDADE_CAMPOS definida
- [x] _identificar_colunas_tabela refatorada (aliases removidos)
- [x] REGEX_WHITESPACE e outras regex compiladas
- [x] normalizar_texto_base usa regex compilada
- [x] Testes de validação executados
- [x] 3 commits (aliases, regex, report)
- [x] Push para `claude/perf-constants-regex-{SESSION_ID}`
- [x] REPORT-AGENT-E.md criado

## CRITÉRIOS DE SUCESSO

- ✅ Aliases são constantes globais (não recriados por tabela)
- ✅ Normalização executada 1 vez no import (não N vezes)
- ✅ Regex compiladas (não recompiladas a cada chamada)
- ✅ Matching de colunas funciona EXATAMENTE igual ao original
- ✅ Performance: 1.5x mais rápido em extração de dados

## AVISOS CRÍTICOS

- ❌ NÃO modificar funções de cache (são do Agent-D)
- ❌ NÃO modificar função gerar_apresentacao (é do Agent-F)
- ❌ NÃO alterar lógica de matching (apenas refatorar constantes)
- ❌ NÃO adicionar/remover aliases (copiar EXATAMENTE do original)
- ✅ FOQUE em mover para constantes e compilar regex

## INÍCIO

Execute:
```bash
git status
git checkout -b claude/perf-constants-regex-{SESSION_ID}
```

Depois leia `BRIEFING-AGENT-E-CONSTANTS.md` e a função `_identificar_colunas_tabela` completa.

Boa sorte! Sua refatoração vai eliminar recalculações desperdiçadas! 🚀
```

---

## 🎯 PROMPT PARA AGENT-F (Progress Bar e UX)

```markdown
Você é o Agent-F, responsável por implementar progress bars e melhorias de UX no projeto APP_SLIDE_OBA.

## SUA MISSÃO

Implementar sistema completo de progress bar:
1. Progress bar 0-100% com 3 etapas (template, duplicação, preenchimento)
2. Mensagens de status descritivas em tempo real
3. Auto-limpeza após 2 segundos
4. Ganho: UX profissional para operações longas (5-30s)

## INSTRUÇÕES

1. **Leia seu briefing completo:**
   - Arquivo: `BRIEFING-AGENT-F-PROGRESS.md`
   - Contém: Implementação COMPLETA da função gerar_apresentacao

2. **Leia o contexto:**
   - `FEATURES-PARALLEL-WAVE-2.md` - Sua feature F3-PROGRESS-UX
   - `PERFORMANCE-ANALYSIS.md` - Problema 4.3 (falta de indicadores)

3. **Execute o briefing:**
   - Substituir função `gerar_apresentacao` COMPLETA
   - Implementar 3 etapas de progresso
   - Adicionar placeholders com st.empty()
   - Calcular porcentagens corretamente

4. **Atualize o tracker em milestones:**
   - 25%, 50%, 75%, 100%
   - Arquivo: `PARALLEL-WORK-TRACKER-WAVE-2.md`

5. **Crie seu report final:**
   - Arquivo: `REPORT-AGENT-F.md`
   - Template está no briefing

## ENTREGAS OBRIGATÓRIAS

- [x] Progress bar implementada em gerar_apresentacao
- [x] Etapa 1 (0-10%): Carregamento de template
- [x] Etapa 2 (10-60%): Duplicação de slides
- [x] Etapa 3 (60-100%): Preenchimento de dados
- [x] Mensagens de status com emojis e percentuais
- [x] Auto-limpeza após 2s (finally block)
- [x] Tratamento de exceções
- [x] Testes com 5, 50, 200 equipes
- [x] 2-3 commits (progress, report)
- [x] Push para `claude/perf-progress-ux-{SESSION_ID}`
- [x] REPORT-AGENT-F.md criado

## CRITÉRIOS DE SUCESSO

- ✅ Progress bar aparece e atualiza em tempo real
- ✅ 3 etapas claramente visíveis
- ✅ Porcentagens corretas (ex: "47/50 (94%)")
- ✅ Auto-limpeza após 2 segundos
- ✅ Funcionalidade preservada (PPTX gerado corretamente)
- ✅ UX: Usuário confiante de que aplicação está processando

## AVISOS CRÍTICOS

- ❌ NÃO modificar funções de cache (são do Agent-D)
- ❌ NÃO modificar constantes ALIASES_* ou REGEX_* (são do Agent-E)
- ❌ NÃO alterar LÓGICA de duplicação/preenchimento (apenas adicionar UI)
- ✅ Use st.empty() para placeholders reutilizáveis
- ✅ Calcule porcentagens com int() (não float)
- ✅ FOQUE em adicionar progress bar sem quebrar funcionalidade

## INÍCIO

Execute:
```bash
git status
git checkout -b claude/perf-progress-ux-{SESSION_ID}
```

Depois leia `BRIEFING-AGENT-F-PROGRESS.md` e localize a função `gerar_apresentacao` (linha ~808).

Boa sorte! Sua UX vai transformar a experiência do usuário! 🚀
```

---

## 📊 Checklist de Deployment

### Antes de Deployar

- [ ] Todos os briefings criados e commitados
- [ ] FEATURES-PARALLEL-WAVE-2.md criado
- [ ] PARALLEL-WORK-TRACKER-WAVE-2.md criado
- [ ] Este arquivo (DEPLOY-PROMPTS-WAVE-2.md) criado
- [ ] ORCHESTRATION-REPORT-WAVE-2.md criado
- [ ] Commit e push de toda documentação

### Durante Deployment

- [ ] Abrir 3 sessões Claude Code Web separadas
- [ ] Conectar cada sessão ao repositório
- [ ] Copiar prompt Agent-D e colar na sessão 1
- [ ] Copiar prompt Agent-E e colar na sessão 2
- [ ] Copiar prompt Agent-F e colar na sessão 3
- [ ] Aguardar conclusão dos 3 agents

### Após Deployment

- [ ] Verificar que 3 branches foram criadas no GitHub
- [ ] Ler REPORT-AGENT-D.md
- [ ] Ler REPORT-AGENT-E.md
- [ ] Ler REPORT-AGENT-F.md
- [ ] Executar merges na ordem: D → E → F
- [ ] Validar performance final
- [ ] Atualizar ORCHESTRATION-REPORT-WAVE-2.md

---

## 🔍 Verificação de Branches

Após deployment, verificar que branches existem:

```bash
git fetch origin
git branch -r | grep perf-

# Esperado:
# origin/claude/perf-cache-validation-XXXXX
# origin/claude/perf-constants-regex-XXXXX
# origin/claude/perf-progress-ux-XXXXX
```

---

## 📞 Suporte

### Se Agent Ficar Bloqueado

1. Verificar se leu o briefing completo
2. Verificar se leu arquivos de contexto (FEATURES, PERFORMANCE-ANALYSIS)
3. Pedir para consultar briefing novamente
4. Pedir para documentar blocker em REPORT

### Se Agent Desviar do Escopo

1. Lembrar de seguir EXATAMENTE o briefing
2. Reforçar avisos críticos (NÃO modificar X, Y, Z)
3. Pedir para reverter mudanças fora do escopo
4. Focar apenas nas entregas obrigatórias

### Se Houver Conflito no Merge

1. Identificar qual agent modificou a seção
2. Consultar FEATURES-PARALLEL-WAVE-2.md seção "Matriz de Conflitos"
3. Aplicar estratégia de resolução recomendada
4. Validar que funcionalidade está preservada

---

## 🎯 Expectativas de Tempo

| Agent | Estimativa | Tempo Real (Preencher após) |
|-------|------------|----------------------------|
| Agent-D | 2-3h | ___ |
| Agent-E | 1-2h | ___ |
| Agent-F | 1-2h | ___ |
| **Paralelo** | **2-3h** | ___ |
| **Merges** | **30-45min** | ___ |
| **Total Wave-2** | **3-4h** | ___ |

---

## 📈 Métricas de Sucesso Final

Após Wave-2 completa, validar:

### Performance
- [ ] Geração 10 equipes: 700ms → ~400ms (-43%)
- [ ] Geração 50 equipes: 3.2s → ~1.8s (-44%)
- [ ] Geração 200 equipes: 12.5s → ~7.0s (-44%)
- [ ] Re-run logo: 30ms → <1ms (30x)
- [ ] Re-run dados: 1.5s → <10ms (150x)

### UX
- [ ] Progress bar aparece durante geração
- [ ] Mensagens claras e descritivas
- [ ] Validações rejeitam arquivos grandes
- [ ] Feedback imediato ao usuário

### Código
- [ ] Aliases são constantes globais
- [ ] Regex são compiladas
- [ ] Cache implementado corretamente
- [ ] Funcionalidade 100% preservada

---

**Preparado por:** Orchestrator (Claude Code)
**Data:** 2025-11-18
**Status:** ✅ Pronto para deployment
**Próximo passo:** Copiar prompts e deployar agents
