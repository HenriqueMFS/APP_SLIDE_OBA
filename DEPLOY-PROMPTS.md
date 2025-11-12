# 🚀 Prompts Prontos para Deploy de Agentes Paralelos

**Projeto:** APP_SLIDE_OBA
**Total de Agentes:** 3
**Gerado em:** 2025-11-12 11:54 UTC
**Speedup Esperado:** 2.25x (18h → 8h)

---

## 📋 Instruções de Deploy

Para cada agent abaixo:

### Opção 1: Deploy em Claude Code Web (Recomendado)
1. Abrir nova sessão Claude Code Web: https://code.claude.com
2. Clonar repositório: `https://github.com/HenriqueMFS/APP_SLIDE_OBA.git`
3. Copiar o prompt correspondente abaixo
4. Colar no chat do Claude Code e pressionar Enter
5. Acompanhar progresso via `PARALLEL-WORK-TRACKER.md`

### Opção 2: Deploy via CLI (Se disponível)
1. Abrir nova sessão Claude CLI
2. Navegar até o repositório
3. Executar prompt via comandofile

---

## 🤖 Agent-A: Documentação Completa

**Branch:** `claude/docs-improvement-Y2JiYWRiNjI5`
**Estimativa:** 4-6h
**Prioridade:** 🔴 CRÍTICA (merge primeiro)

### ✨ Prompt para Claude Code Web:

```
Você é Agent-A designado para trabalhar na feature de Documentação Completa do projeto APP_SLIDE_OBA.

**INSTRUÇÕES CRÍTICAS:**

1. **Ler seu briefing completo:**
   cat BRIEFING-AGENT-A-DOCS.md

2. **Checkout da sua branch (criar se não existir):**
   git checkout -b claude/docs-improvement-Y2JiYWRiNjI5
   git push -u origin claude/docs-improvement-Y2JiYWRiNjI9

3. **Seguir todas as 7 fases** do briefing à risca:
   - Fase 1: Setup (5 min)
   - Fase 2: README.md (30-45 min)
   - Fase 3: docs/USAGE.md (45-60 min)
   - Fase 4: docs/INPUT_FORMAT.md (45-60 min)
   - Fase 5: docs/EXAMPLES.md (60-75 min)
   - Fase 6: Docstrings em APP.py (45-60 min)
   - Fase 7: Validação Final (15-20 min)

4. **Atualizar PARALLEL-WORK-TRACKER.md a cada milestone (25%, 50%, 75%, 100%):**
   - Checkout claude/analyze-repository-structure-011CV26eM3noi2SbsiDZJGqW
   - Editar seção Agent-A
   - Adicionar entrada no Histórico
   - Commit e push
   - Voltar para sua branch

5. **Ao finalizar:**
   - Criar REPORT-AGENT-A-DOCS.md (template no briefing)
   - Marcar status como 🟢 Completo no tracker
   - Confirmar que todos critérios de aceitação foram atendidos

**DELIVERABLES ESPERADOS:**
- README.md expandido (1 → 100+ linhas)
- docs/USAGE.md (~80 linhas)
- docs/INPUT_FORMAT.md (~100 linhas)
- docs/EXAMPLES.md (~120 linhas)
- Docstrings em 7 funções de APP.py
- REPORT-AGENT-A-DOCS.md

**COMECE AGORA** lendo o briefing completo e fazendo checkout da branch.
```

---

## 🤖 Agent-B: Setup e Infraestrutura

**Branch:** `claude/infra-setup-OWU5NzY3NDRj`
**Estimativa:** 3-4h
**Prioridade:** 🔴 CRÍTICA

### ✨ Prompt para Claude Code Web:

```
Você é Agent-B designado para trabalhar na feature de Setup e Infraestrutura do projeto APP_SLIDE_OBA.

**INSTRUÇÕES CRÍTICAS:**

1. **Ler seu briefing completo:**
   cat BRIEFING-AGENT-B-SETUP.md

2. **Checkout da sua branch (criar se não existir):**
   git checkout -b claude/infra-setup-OWU5NzY3NDRj
   git push -u origin claude/infra-setup-OWU5NzY3NDRj

3. **Seguir todas as 7 fases** do briefing à risca:
   - Fase 1: Setup (5 min)
   - Fase 2: Criar .gitignore (15 min)
   - Fase 3: Remover __pycache__/ (10 min)
   - Fase 4: Fixar versões em requirements.txt (20 min)
   - Fase 5: Criar .env.example (15 min)
   - Fase 6: Otimizar imagens (60-90 min) ⚠️ CRÍTICO: preservar qualidade
   - Fase 7: Validação Final (15 min)

4. **Atualizar PARALLEL-WORK-TRACKER.md em milestones (15%, 30%, 50%, 65%, 90%, 100%):**
   - Checkout claude/analyze-repository-structure-011CV26eM3noi2SbsiDZJGqW
   - Editar seção Agent-B
   - Adicionar entrada no Histórico
   - Commit e push
   - Voltar para sua branch

5. **Ao finalizar:**
   - Criar REPORT-AGENT-B-SETUP.md (template no briefing)
   - Marcar status como 🟢 Completo no tracker
   - Validar que aplicação roda normalmente: streamlit run APP.py

**DELIVERABLES ESPERADOS:**
- .gitignore (~30 linhas)
- __pycache__/ removido do git
- requirements.txt com versões fixas
- .env.example criado
- logo_jornada.png otimizado (6.2 MB → <1 MB)
- tiapamela.gif otimizado (3.4 MB → <1.5 MB)
- REPORT-AGENT-B-SETUP.md

**ATENÇÃO:** Otimização de imagens deve preservar qualidade visual!

**COMECE AGORA** lendo o briefing completo e fazendo checkout da branch.
```

---

## 🤖 Agent-C: Refatoração de Código

**Branch:** `claude/refactor-code-OWJmZWU1Yjhi`
**Estimativa:** 6-8h
**Prioridade:** 🟡 ALTA

### ✨ Prompt para Claude Code Web:

```
Você é Agent-C designado para trabalhar na feature de Refatoração de Código do projeto APP_SLIDE_OBA.

**⚠️ MISSÃO CRÍTICA: NÃO QUEBRAR FUNCIONALIDADE EXISTENTE!**

**INSTRUÇÕES CRÍTICAS:**

1. **Ler seu briefing completo:**
   cat BRIEFING-AGENT-C-REFACTOR.md

2. **Checkout da sua branch (criar se não existir):**
   git checkout -b claude/refactor-code-OWJmZWU1Yjhi
   git push -u origin claude/refactor-code-OWJmZWU1Yjhi

3. **CRIAR BACKUP ANTES:**
   cp APP.py APP.py.backup

4. **Seguir todas as 6 fases** do briefing à risca:
   - Fase 1: Setup e Backup (10 min)
   - Fase 2: Extrair Constantes (60 min)
   - Fase 3: Modularizar extrair_dados - Parte 1 (90 min)
   - Fase 4: Modularizar extrair_dados - Parte 2 (90 min)
   - Fase 5: Adicionar Validações (75 min)
   - Fase 6: Validação Final e Testes (90 min) ⚠️ CRÍTICO

5. **TESTAR APÓS CADA FASE:**
   - Validar que aplicação roda: python -c "import APP"
   - Testar manualmente via Streamlit quando possível

6. **Atualizar PARALLEL-WORK-TRACKER.md em milestones (12%, 35%, 60%, 80%, 100%):**
   - Checkout claude/analyze-repository-structure-011CV26eM3noi2SbsiDZJGqW
   - Editar seção Agent-C
   - Adicionar entrada no Histórico
   - Commit e push
   - Voltar para sua branch

7. **Ao finalizar:**
   - Validação COMPLETA: Gerar slides e comparar com versão original
   - Criar REPORT-AGENT-C-REFACTOR.md (template no briefing)
   - Marcar status como 🟢 Completo no tracker

**DELIVERABLES ESPERADOS:**
- 15+ constantes extraídas no topo de APP.py
- Função extrair_dados modularizada (212 → 30 linhas + 3 helpers)
- 3 funções auxiliares:
  - _identificar_colunas_tabela (~50 linhas)
  - _processar_linhas_tabela (~40 linhas)
  - _organizar_dados_equipes (~60 linhas)
- 8+ validações adicionadas
- Funcionalidade 100% preservada
- REPORT-AGENT-C-REFACTOR.md

**REGRAS DE OURO:**
1. ⚠️ Testar frequentemente
2. ⚠️ Commits incrementais
3. ⚠️ Manter backup até finalizar
4. ⚠️ Se quebrar, restaurar: cp APP.py.backup APP.py

**COMECE AGORA** lendo o briefing completo e fazendo checkout + backup.
```

---

## 📊 Monitoramento de Progresso

### Como Verificar Status dos Agents

**Via Tracker:**
```bash
# Ver tracker atualizado
git checkout claude/analyze-repository-structure-011CV26eM3noi2SbsiDZJGqW
git pull origin claude/analyze-repository-structure-011CV26eM3noi2SbsiDZJGqW
cat PARALLEL-WORK-TRACKER.md | grep -A 15 "Agent-A\|Agent-B\|Agent-C"
```

**Via GitHub (se branches forem pushed):**
```bash
# Listar branches remotas
git ls-remote --heads origin | grep claude/

# Ver commits de cada branch
git log origin/claude/docs-improvement-Y2JiYWRiNjI5 --oneline -5
git log origin/claude/infra-setup-OWU5NzY3NDRj --oneline -5
git log origin/claude/refactor-code-OWJmZWU1Yjhi --oneline -5
```

**Via Reports:**
Quando agents completarem, buscar:
- `REPORT-AGENT-A-DOCS.md`
- `REPORT-AGENT-B-SETUP.md`
- `REPORT-AGENT-C-REFACTOR.md`

---

## 🔧 Troubleshooting de Deploy

### Problema: Agent não consegue criar branch

**Solução:**
O orquestrador pode criar manualmente:
```bash
git checkout claude/analyze-repository-structure-011CV26eM3noi2SbsiDZJGqW
git checkout -b claude/docs-improvement-Y2JiYWRiNjI5
git push -u origin claude/docs-improvement-Y2JiYWRiNjI5
```

### Problema: Agent reporta push falhando (erro 403)

**Solução:**
Ver "Múltiplos Métodos de Commit/Push" nos briefings.
- Tentar Método 2: Criar branch remota primeiro
- Último recurso: Criar patches

### Problema: Conflito ao atualizar tracker

**Solução:**
```bash
git pull origin claude/analyze-repository-structure-011CV26eM3noi2SbsiDZJGqW --rebase
# Resolver conflitos mantendo ambas as atualizações
git add PARALLEL-WORK-TRACKER.md
git rebase --continue
```

---

## ✅ Checklist de Deploy

Antes de fazer deploy dos agents, confirmar:

- [ ] ANALISE_REPOSITORIO.md existe e está completo
- [ ] FEATURES-PARALLEL-WAVE-1.md criado
- [ ] BRIEFING-AGENT-A-DOCS.md criado (completo)
- [ ] BRIEFING-AGENT-B-SETUP.md criado (completo)
- [ ] BRIEFING-AGENT-C-REFACTOR.md criado (completo)
- [ ] PARALLEL-WORK-TRACKER.md criado
- [ ] Branches locais criadas (ou agents criarão)
- [ ] DEPLOY-PROMPTS.md criado (este arquivo)
- [ ] ORCHESTRATION-REPORT.md criado (próximo)

---

## 🎯 Próximos Passos (Orquestrador)

1. ✅ Criar ORCHESTRATION-REPORT.md
2. ✅ Commit todos arquivos de orquestração
3. ✅ Push para branch base
4. 🚀 **DEPLOY:** Abrir 3 sessões Claude Code e colar prompts
5. 👁️ **MONITOR:** Acompanhar PARALLEL-WORK-TRACKER.md
6. 🔀 **MERGE:** Quando todos completos, merge em ordem (A → B → C)
7. ✅ **VALIDATE:** Testar develop após todos merges

---

**Prompts criados por:** Orquestrador
**Data:** 2025-11-12 11:54 UTC
**Prontos para deploy:** ✅ SIM
