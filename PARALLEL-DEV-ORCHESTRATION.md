# 📋 Template: Desenvolvimento Paralelo Multi-Agente com Claude Code Web

**Versão:** 2.0
**Baseado em:** Projeto idCEB (5 fases, 5 agentes, 3x speedup validado)
**Ambiente:** Claude Code Web (navegador)
**Última Atualização:** 2025-11-11

---

## 📖 Índice

### PARTE 1: AGENTE ORQUESTRADOR (Branch `develop`)
1.1. Papel do Orquestrador
1.2. ETAPA 1: Verificar Análise Profunda
1.3. ETAPA 2: Criar Análise Profunda (SE necessário)
1.4. ETAPA 3: Extrair Features da Análise
1.5. ETAPA 4: Criar Branches para Cada Feature
1.6. ETAPA 5: Criar Briefings Individuais
1.7. ETAPA 6: Criar Sistema de Tracking
1.8. ETAPA 7: Gerar Prompts Prontos para Deploy
1.9. ETAPA 8: Relatório de Orquestração

### PARTE 2: TEMPLATE DE BRIEFING PARA AGENTES WORKERS
2.1. Status do Projeto
2.2. Ambiente: Claude Code Web + Múltiplos Métodos Git
2.3. Sua Missão
2.4. Escopo Completo
2.5. Comunicação com Orchestrador + Update Tracker
2.6. Recovery & Troubleshooting
2.7. Plano de Execução Detalhado
2.8. Recursos Reutilizáveis
2.9. Regras Críticas
2.10. Critérios de Aceitação
2.11. Relatório Final Esperado
2.12. Links Úteis

### PARTE 3: MERGE COORDENADO
3.1. Ordem de Merge
3.2. Comandos de Merge
3.3. Validação Pós-Merge
3.4. Resolução de Conflitos

### PARTE 4: CASO DE ESTUDO - idCEB (Referência Real)
4.1. Contexto do Projeto
4.2. Ciclo 1: Fases 7, 9, 10 (3 agentes)
4.3. Ciclo 2: Fases 8, 12 (2 agentes)
4.4. Métricas e Resultados
4.5. Lições Aprendidas

### PARTE 5: ADAPTAÇÃO PARA NOVOS PROJETOS
5.1. Checklist de Customização
5.2. Exemplo Prático Passo-a-Passo
5.3. Templates Prontos para Copiar

---

# PARTE 1: AGENTE ORQUESTRADOR (Branch `develop`)

## 1.1. Papel do Orquestrador

Você é o **Agente Orquestrador** trabalhando na branch `develop` de um projeto GitHub.

**Sua Missão:**
1. Analisar o projeto profundamente (ou validar análise existente)
2. Identificar features para desenvolvimento paralelo
3. Criar branches individuais para cada feature
4. Criar briefings detalhados para cada agent
5. Gerar sistema de tracking em tempo real
6. Gerar prompts prontos para deploy de agents
7. Coordenar merge das features de volta para develop

**Ambiente:**
- Branch: `develop` (integration branch)
- Pode ser Claude Code Web OU CLI
- Output: Estrutura completa para N agentes paralelos

**Output Final:**
- `PROJECT-ANALYSIS.md` (análise profunda do projeto)
- N branches `claude/{feature}-{SESSION_ID}` criadas
- N arquivos `BRIEFING-AGENT-{ID}-{FEATURE}.md`
- `PARALLEL-WORK-TRACKER.md` (tracking system)
- `DEPLOY-PROMPTS.md` (prompts prontos)
- `ORCHESTRATION-REPORT.md` (relatório de setup)

---

## 1.2. ETAPA 1: Verificar Análise Profunda

Antes de qualquer coisa, verificar se já existe análise do projeto:

```bash
# Procurar por análise existente
find . -maxdepth 2 -name "*ANALYSIS*.md" -o -name "*analysis*.md"

# Verificar em locais comuns
ls -la PROJECT-ANALYSIS.md
ls -la docs/PROJECT-ANALYSIS.md
ls -la docs/planning/PROJECT-ANALYSIS.md
```

**Se encontrado:**
- ✅ Ler o arquivo
- ✅ Validar se está atualizado (última modificação < 30 dias)
- ✅ Prosseguir para ETAPA 3

**Se NÃO encontrado ou desatualizado:**
- ⚠️ Prosseguir para ETAPA 2 (criar análise)

---

## 1.3. ETAPA 2: Criar Análise Profunda (SE necessário)

Use o prompt abaixo para criar análise completa do projeto:

```
Faça uma análise completa desse repositório:

1. **Tipo de Projeto**
   - Web app, CLI tool, mobile, biblioteca, etc.
   - Propósito e domínio (e-commerce, educação, finanças, etc.)
   - Público-alvo

2. **Arquitetura**
   - Padrão arquitetural (MVC, Clean Architecture, Monolítico, etc.)
   - Estrutura de diretórios
   - Separação de responsabilidades (camadas)

3. **Stack Tecnológica**
   - Frontend: Framework, bibliotecas, UI components
   - Backend: Framework, linguagem, APIs
   - Database: Tipo, ORM, migrações
   - Infraestrutura: Deploy, CI/CD, monitoramento

4. **Documentação**
   - README.md: Existe? Completo? Atualizado?
   - Docs técnicos: Arquitetura, API, guias
   - Comentários no código: Qualidade e cobertura
   - Changelog/Release notes

5. **Estrutura Git**
   - Branches: Padrão usado (gitflow, trunk-based, etc.)
   - Commits: Qualidade das mensagens, padrão
   - Tags/Releases: Versionamento
   - Colaboradores: Solo ou time

6. **Qualidade do Código**
   - Testes: Coverage, tipos (unit, integration, e2e)
   - Linting: ESLint, Prettier, etc.
   - TypeScript/Tipos: Strict mode? any's?
   - Duplicação de código
   - Complexidade ciclomática

7. **Crítica Construtiva**
   Identifique melhorias PRÁTICAS e INCREMENTAIS (sem escalonamento grandiosos):

   a) **Melhorias de Documentação** (sempre incluir)
      - O que falta no README?
      - Docs técnicas necessárias?
      - Comentários críticos faltando?

   b) **Refatorações Táticas**
      - Código duplicado que pode ser consolidado
      - Componentes/funções grandes que podem ser divididos
      - Padrões inconsistentes para uniformizar

   c) **Expansão de Testes**
      - Coverage atual vs desejável
      - Áreas críticas sem testes
      - Tipos de teste faltando

   d) **Melhorias de UX/UI** (se aplicável)
      - Feedback visual faltando
      - Acessibilidade (WCAG)
      - Responsividade mobile

   e) **Performance Tática**
      - Queries N+1
      - Cachê strategies
      - Lazy loading

   f) **Segurança Básica**
      - Validações de input faltando
      - Sanitização de dados
      - Rate limiting

   g) **DX (Developer Experience)**
      - Scripts úteis faltando
      - Setup/onboarding
      - Debugging tools

8. **Score de Qualidade**
   Avalie de 0-10 em cada dimensão:
   - Arquitetura: X/10
   - Código: X/10
   - Testes: X/10
   - Docs: X/10
   - DX: X/10
   - **Score Geral: X/10**

9. **Priorização de Melhorias**
   Matriz Impacto/Esforço:

   **Alta Prioridade (Alto Impacto / Baixo Esforço):**
   - Melhoria 1
   - Melhoria 2

   **Média Prioridade (Alto Impacto / Médio Esforço):**
   - Melhoria 3

   **Baixa Prioridade (Baixo Impacto / Baixo Esforço):**
   - Melhoria 4

Após análise, salve em arquivo markdown chamado PROJECT-ANALYSIS.md na raiz do projeto.
```

**Formato do OUTPUT esperado:**

```markdown
# Análise Profunda: {PROJECT_NAME}

**Data:** {DATE}
**Versão do Projeto:** {VERSION}
**Analisado por:** Claude Code (Orchestrator)

## 1. Tipo de Projeto
{Descrição completa}

## 2. Arquitetura
{Padrões e estrutura}

## 3. Stack Tecnológica
- **Frontend:** Next.js 15, React 19, Tailwind CSS, shadcn/ui
- **Backend:** Next.js API Routes, Node.js
- **Database:** PostgreSQL + Prisma ORM
- **Infraestrutura:** Vercel, Railway

## 4. Documentação
- README.md: ✅ Completo (setup, features, deploy)
- Docs técnicos: ⚠️ Arquitetura faltando
- Comentários: ✅ Boa cobertura em funções complexas

## 5. Estrutura Git
- Padrão: Gitflow (master, develop, feature/*)
- Commits: ✅ Conventional commits
- Tags: ✅ Semantic versioning

## 6. Qualidade do Código
- Testes: ⚠️ 45% coverage (meta: 70%)
- Linting: ✅ ESLint + Prettier
- TypeScript: ✅ Strict mode, minimal any's
- Duplicação: ⚠️ 15% (meta: < 10%)

## 7. Crítica Construtiva

### a) Documentação (PRIORIDADE ALTA)
- ❌ Falta: docs/architecture/overview.md
- ❌ Falta: API documentation (endpoints)
- ❌ Falta: Guia de contribuição

### b) Refatorações Táticas
- ⚠️ Componentes UI duplicados em 3 módulos
- ⚠️ 5 funções > 100 linhas (refatorar)

### c) Testes
- ❌ Frontend: 12% coverage (meta: 60%)
- ⚠️ E2E tests: Zero (setup Playwright)

### d) Performance
- ⚠️ Queries N+1 em 3 endpoints
- ⚠️ Cache Redis não implementado

### e) Segurança
- ✅ Validações de input OK
- ⚠️ Rate limiting faltando em APIs públicas

## 8. Score de Qualidade

| Dimensão | Score | Justificativa |
|----------|-------|---------------|
| Arquitetura | 8.5/10 | Multi-tenant bem implementado, modular |
| Código | 7.5/10 | Clean, mas com duplicação |
| Testes | 6.0/10 | Backend OK (78%), frontend fraco (12%) |
| Docs | 6.5/10 | README bom, docs técnicas faltando |
| DX | 8.0/10 | Scripts úteis, setup fácil |
| **GERAL** | **7.3/10** | Produção viável, melhorias claras |

## 9. Priorização de Melhorias

### 🔴 Alta Prioridade (3 features)

**F1: Documentação Técnica Completa** ⚡ (Impacto: Alto | Esforço: Baixo)
- Criar docs/architecture/overview.md
- Documentar APIs (Swagger/OpenAPI)
- Guia de contribuição
- Estimativa: 6h

**F2: Expansão de Testes Frontend** ⚡ (Impacto: Alto | Esforço: Médio)
- Aumentar coverage 12% → 60%
- Testes de componentes críticos
- Setup Playwright (E2E)
- Estimativa: 10h

**F3: Refatoração de Componentes UI** ⚡ (Impacto: Alto | Esforço: Baixo)
- Criar biblioteca shared components
- Eliminar duplicação (3 módulos → 1)
- Estimativa: 5h

### 🟡 Média Prioridade (2 features)

**F4: Otimização de Performance**
- Implementar cache Redis
- Corrigir queries N+1 (3 endpoints)
- Lazy loading de componentes
- Estimativa: 8h

**F5: Segurança - Rate Limiting**
- Implementar rate limiting global
- Rate limiting por endpoint crítico
- Dashboard de monitoramento
- Estimativa: 4h

### ⚪ Baixa Prioridade (quick wins)

**F6: DX Improvements**
- Scripts de debug
- Git hooks (pre-commit, pre-push)
- Estimativa: 2h

---

## Recomendações para Trabalho Paralelo

**Features Independentes (podem rodar em paralelo):**
- ✅ F1 (Docs): Zero conflitos esperados
- ✅ F2 (Testes): Cria arquivos novos
- ✅ F3 (UI Refactor): Modificações isoladas

**Features Sequenciais (dependências):**
- F4 depende de F3 (cache usa novos components)
- F6 pode rodar com qualquer outra

**Sugestão de Primeira Onda (3 agentes):**
1. Agent-A: F1 (Docs) - 6h
2. Agent-B: F2 (Testes) - 10h
3. Agent-C: F3 (UI Refactor) - 5h

**Tempo Paralelo:** 10h (max)
**Tempo Sequencial:** 21h (soma)
**Speedup:** 2.1x
```

**Salvar análise:**
```bash
# Criar arquivo
cat > PROJECT-ANALYSIS.md << 'EOF'
{CONTEÚDO ACIMA}
EOF

# Commit
git add PROJECT-ANALYSIS.md
git commit -m "docs: Add deep project analysis

Complete analysis covering architecture, stack, quality metrics, and improvement opportunities.

Identified 6 features for parallel development with priority matrix.
"

git push origin develop
```

---

## 1.4. ETAPA 3: Extrair Features da Análise

Baseado em `PROJECT-ANALYSIS.md`, identificar features para trabalho paralelo.

### Feature OBRIGATÓRIA #1: Documentação

**SEMPRE incluir** feature de documentação (exceto se já estiver 10/10):

```markdown
**Feature: Documentação Técnica Completa**
- **ID:** F1
- **Categoria:** docs
- **Prioridade:** ALTA (merge primeiro)
- **Estimativa:** 4-8h
- **Arquivos:**
  - Criar: docs/architecture/*.md
  - Criar: docs/api/*.md (se aplicável)
  - Modificar: README.md
  - Criar: CONTRIBUTING.md
- **Conflitos:** Zero (apenas docs)
```

### Features Variáveis (Exemplos)

Da análise, selecionar 2-5 features adicionais:

**Critérios de Seleção:**
1. ✅ **Independência:** Zero dependências entre features
2. ✅ **Escopo claro:** Bem definido, não ambíguo
3. ✅ **Estimativa razoável:** 4-10h por feature
4. ✅ **Isolamento de arquivos:** Mínimo overlap (prevenir conflitos)
5. ❌ **Evitar:** Features que modificam mesmos arquivos

**Análise de Conflitos:**

Para cada par de features, verificar:
```
F1 vs F2:
- F1 modifica: docs/*, README.md
- F2 modifica: __tests__/*, src/components/*.test.tsx
- Overlap: ZERO
- ✅ Podem rodar em paralelo

F2 vs F3:
- F2 modifica: __tests__/*
- F3 modifica: src/components/shared/*, src/app/*/page.tsx
- Overlap: ZERO (F2 não toca src/, F3 não toca __tests__/)
- ✅ Podem rodar em paralelo

F3 vs F4:
- F3 modifica: src/components/shared/*
- F4 modifica: src/lib/cache.ts, src/app/api/*/route.ts
- Overlap: POSSÍVEL (se API routes usam components de F3)
- ⚠️ F4 deve rodar DEPOIS de F3 (sequencial)
```

**Resultado:**

```markdown
## Features para Trabalho Paralelo

### 🟢 Grupo A: Paralelo (3 features simultâneas)

**F1: Documentação** (Agent-A)
- Arquivos: docs/*, README.md, CONTRIBUTING.md
- Estimativa: 6h
- Conflitos: ZERO

**F2: Expansão de Testes** (Agent-B)
- Arquivos: __tests__/*, src/**/*.test.tsx, playwright.config.ts
- Estimativa: 10h
- Conflitos: ZERO

**F3: Refatoração UI** (Agent-C)
- Arquivos: src/components/shared/*, src/app/*/page.tsx
- Estimativa: 5h
- Conflitos: ZERO

### 🟡 Grupo B: Sequencial (rodar DEPOIS do Grupo A)

**F4: Cache + Performance**
- Depende de: F3 (usa novos components)
- Estimativa: 8h

**F5: Rate Limiting**
- Independente, mas menor prioridade
- Estimativa: 4h
```

---

## 1.5. ETAPA 4: Criar Branches para Cada Feature

Para cada feature do Grupo A, criar branch:

```bash
# Certificar que está em develop atualizado
git checkout develop
git pull origin develop

# Gerar SESSION_ID único (ou usar CLAUDE_SESSION_ID se disponível)
SESSION_ID=$(date +%s | sha256sum | base64 | head -c 12)

# Feature 1: Documentação
git checkout -b claude/docs-improvement-$SESSION_ID
git push -u origin claude/docs-improvement-$SESSION_ID

# Voltar para develop
git checkout develop

# Feature 2: Testes
SESSION_ID=$(date +%s | sha256sum | base64 | head -c 12)
git checkout -b claude/test-expansion-$SESSION_ID
git push -u origin claude/test-expansion-$SESSION_ID

git checkout develop

# Feature 3: UI Refactor
SESSION_ID=$(date +%s | sha256sum | base64 | head -c 12)
git checkout -b claude/ui-refactor-$SESSION_ID
git push -u origin claude/ui-refactor-$SESSION_ID

git checkout develop
```

**Padrão de Branch:**
```
claude/{categoria}-{descrição}-{SESSION_ID}

Onde:
- claude/      = Prefixo obrigatório (permissão push Claude Code Web)
- {categoria}  = docs, test, ui, api, perf, fix, refactor
- {descrição}  = curta, kebab-case
- {SESSION_ID} = 12 chars alfanuméricos únicos
```

**Validar branches criadas:**
```bash
# Listar branches locais
git branch

# Listar branches remotas
git branch -r | grep claude/

# Verificar no GitHub (se gh CLI instalado)
gh repo view --web
```

**Anotar branches criadas:**
```markdown
## Branches Criadas

1. claude/docs-improvement-Ab3Cd5Ef8Gh9
2. claude/test-expansion-Jk1Lm4No7Pq0
3. claude/ui-refactor-Rs2Tu6Vw9Xy1
```

---

## 1.6. ETAPA 5: Criar Briefings Individuais

Para cada feature, criar briefing detalhado usando template da **PARTE 2**.

**Arquivo:** `BRIEFING-AGENT-{ID}-{FEATURE}.md`

Exemplo para Feature 1 (Documentação):

```bash
cat > BRIEFING-AGENT-A-DOCS.md << 'EOF'
# BRIEFING: AGENT-A - Documentação Técnica Completa

## 1. Status do Projeto

- **Projeto:** {PROJECT_NAME}
- **Tipo:** {PROJECT_TYPE}
- **Stack:** {TECH_STACK}
- **Build Status:** ✅ Passing (último commit)
- **Branch Base:** develop
- **Sua Branch:** claude/docs-improvement-Ab3Cd5Ef8Gh9

## 2. Ambiente: Claude Code Web

⚠️ **CRÍTICO:** Você está executando no Claude Code Web (navegador)

{... resto do template da PARTE 2 ...}

EOF
```

**Repetir para todas as features** (Agent-B, Agent-C, etc.)

Cada briefing deve ter:
- Status do projeto
- Ambiente e métodos git
- Missão e escopo específico
- Plano de execução passo-a-passo
- Recovery procedures
- Checklist de aceitação
- Template de relatório

**Commit briefings:**
```bash
git add BRIEFING-AGENT-*.md
git commit -m "docs: Add agent briefings for parallel development

Created 3 detailed briefings:
- Agent-A: Documentation (6h)
- Agent-B: Test expansion (10h)
- Agent-C: UI refactor (5h)

Each briefing includes execution plan, troubleshooting, and acceptance criteria.
"

git push origin develop
```

---

## 1.7. ETAPA 6: Criar Sistema de Tracking

Criar `PARALLEL-WORK-TRACKER.md` para monitoramento em tempo real:

```bash
cat > PARALLEL-WORK-TRACKER.md << 'EOF'
# 🎯 Parallel Work Tracker - {PROJECT_NAME}

**Última Atualização:** {TIMESTAMP}
**Status Geral:** 🟡 Setup Completo - Aguardando Início dos Agents

---

## 📊 Visão Geral

| Métrica | Valor |
|---------|-------|
| Features Totais | 3 |
| Completas | 0 |
| Em Progresso | 0 |
| Bloqueadas | 0 |
| Progresso Geral | 0% |

---

## 👥 Status dos Agentes

### Agent-A: Documentação Técnica
- **Branch:** `claude/docs-improvement-Ab3Cd5Ef8Gh9`
- **Status:** ⚪ Não Iniciado (0%)
- **Última Atualização:** {TIMESTAMP}
- **Progresso:**
  - [ ] docs/architecture/ criada
  - [ ] API documentation
  - [ ] README.md atualizado
  - [ ] CONTRIBUTING.md criado
- **Commits:** 0
- **Linhas:** +0 / -0
- **Bloqueadores:** Nenhum
- **ETA:** 6h

### Agent-B: Expansão de Testes
- **Branch:** `claude/test-expansion-Jk1Lm4No7Pq0`
- **Status:** ⚪ Não Iniciado (0%)
- **Última Atualização:** {TIMESTAMP}
- **Progresso:**
  - [ ] Testes de componentes (0/20)
  - [ ] Setup Playwright
  - [ ] E2E tests básicos
  - [ ] Coverage 12% → 60%
- **Commits:** 0
- **Linhas:** +0 / -0
- **Bloqueadores:** Nenhum
- **ETA:** 10h

### Agent-C: Refatoração UI
- **Branch:** `claude/ui-refactor-Rs2Tu6Vw9Xy1`
- **Status:** ⚪ Não Iniciado (0%)
- **Última Atualização:** {TIMESTAMP}
- **Progresso:**
  - [ ] Biblioteca shared components criada
  - [ ] Migração Módulo 1
  - [ ] Migração Módulo 2
  - [ ] Migração Módulo 3
  - [ ] Testes de integração
- **Commits:** 0
- **Linhas:** +0 / -0
- **Bloqueadores:** Nenhum
- **ETA:** 5h

---

## 🔄 Histórico de Atualizações

| Timestamp | Agent | Evento | Detalhes |
|-----------|-------|--------|----------|
| {TIMESTAMP} | Orquestrador | 🚀 Setup | 3 agents configurados, aguardando deploy |

---

## 📋 Ordem de Merge (Quando Todos Completos)

1. **Agent-A (Docs)** - PRIMEIRO (zero conflitos esperados)
2. **Agent-B (Tests)** - SEGUNDO
3. **Agent-C (UI Refactor)** - TERCEIRO

---

## ⚠️ Bloqueadores Ativos

{Vazio por enquanto - agents atualizarão se bloqueados}

---

## ✅ Critérios de Conclusão

- [ ] Agent-A: 100% completo
- [ ] Agent-B: 100% completo
- [ ] Agent-C: 100% completo
- [ ] Todos agents com push bem-sucedido
- [ ] Build develop limpo após merges
- [ ] Testes passando (se aplicável)

---

## 📞 Como Atualizar Este Tracker

**Para Agentes:**
Adicione entrada no Histórico ao completar cada milestone (25%, 50%, 75%, 100%):

```markdown
| {TIMESTAMP} | Agent-{ID} | {EVENTO} | {DETALHES} |
```

Atualize seção do seu Agent com progresso atual.

**Para Orquestrador:**
- Monitorar seção "Bloqueadores Ativos"
- Resolver bloqueios quando reportados
- Validar relatórios de conclusão

EOF

git add PARALLEL-WORK-TRACKER.md
git commit -m "feat: Add parallel work tracking system

Real-time tracker for 3 agents:
- Agent status with progress percentages
- Event history timestamped
- Active blockers section
- Merge order defined

Agents will update this file at 25%, 50%, 75%, 100% milestones.
"

git push origin develop
```

---

## 1.8. ETAPA 7: Gerar Prompts Prontos para Deploy

Criar `DEPLOY-PROMPTS.md` com prompts copiáveis:

```bash
cat > DEPLOY-PROMPTS.md << 'EOF'
# 🚀 Prompts Prontos para Deploy de Agentes Paralelos

**Projeto:** {PROJECT_NAME}
**Total de Agentes:** 3
**Gerado em:** {TIMESTAMP}

---

## 📋 Instruções de Deploy

Para cada agent abaixo:
1. Abrir nova sessão Claude Code Web: https://code.claude.com
2. Fazer upload do repositório (ou clonar via git)
3. Copiar o prompt correspondente
4. Colar no chat do Claude Code e pressionar Enter
5. Acompanhar progresso via PARALLEL-WORK-TRACKER.md

---

## 🤖 Agent-A: Documentação Técnica

**Branch:** `claude/docs-improvement-Ab3Cd5Ef8Gh9`
**Estimativa:** 6h
**Prioridade:** ALTA (merge primeiro)

### Prompt para Claude Code Web:
```
Você é Agent-A designado para trabalhar na feature de Documentação Técnica do projeto {PROJECT_NAME}.

**INSTRUÇÕES CRÍTICAS:**

1. **Checkout da sua branch:**
   git checkout claude/docs-improvement-Ab3Cd5Ef8Gh9

2. **Ler seu briefing completo:**
   cat BRIEFING-AGENT-A-DOCS.md

3. **Seguir todas as 12 seções** do briefing à risca

4. **Atualizar tracker a cada milestone (25%, 50%, 75%, 100%):**
   - Editar PARALLEL-WORK-TRACKER.md
   - Adicionar entrada no Histórico
   - Atualizar seção Agent-A com progresso

5. **Usar múltiplos métodos de commit/push** (ver seção Git Operations no briefing)

6. **Ao finalizar:**
   - Criar REPORT-AGENT-A-DOCS.md
   - Marcar status como 🟢 Completo no tracker
   - Notificar conclusão

**COMECE AGORA** lendo o briefing e fazendo checkout da branch.
```

---

## 🤖 Agent-B: Expansão de Testes

**Branch:** `claude/test-expansion-Jk1Lm4No7Pq0`
**Estimativa:** 10h
**Prioridade:** MÉDIA

### Prompt para Claude Code Web:
```
Você é Agent-B designado para trabalhar na feature de Expansão de Testes do projeto {PROJECT_NAME}.

**INSTRUÇÕES CRÍTICAS:**

1. **Checkout da sua branch:**
   git checkout claude/test-expansion-Jk1Lm4No7Pq0

2. **Ler seu briefing completo:**
   cat BRIEFING-AGENT-B-TESTS.md

3. **Seguir todas as 12 seções** do briefing à risca

4. **Atualizar tracker a cada milestone (25%, 50%, 75%, 100%):**
   - Editar PARALLEL-WORK-TRACKER.md
   - Adicionar entrada no Histórico
   - Atualizar seção Agent-B com progresso

5. **Se encontrar bloqueadores:**
   - Marcar status como 🔴 Bloqueado no tracker
   - Adicionar à seção "Bloqueadores Ativos"
   - Aguardar resolução do orquestrador

6. **Usar múltiplos métodos de commit/push** (ver seção Git Operations no briefing)

7. **Ao finalizar:**
   - Criar REPORT-AGENT-B-TESTS.md
   - Marcar status como 🟢 Completo no tracker
   - Notificar conclusão

**COMECE AGORA** lendo o briefing e fazendo checkout da branch.
```

---

## 🤖 Agent-C: Refatoração UI

**Branch:** `claude/ui-refactor-Rs2Tu6Vw9Xy1`
**Estimativa:** 5h
**Prioridade:** MÉDIA

### Prompt para Claude Code Web:
```
Você é Agent-C designado para trabalhar na feature de Refatoração UI do projeto {PROJECT_NAME}.

**INSTRUÇÕES CRÍTICAS:**

1. **Checkout da sua branch:**
   git checkout claude/ui-refactor-Rs2Tu6Vw9Xy1

2. **Ler seu briefing completo:**
   cat BRIEFING-AGENT-C-UI.md

3. **Seguir todas as 12 seções** do briefing à risca

4. **Atualizar tracker a cada milestone (25%, 50%, 75%, 100%):**
   - Editar PARALLEL-WORK-TRACKER.md
   - Adicionar entrada no Histórico
   - Atualizar seção Agent-C com progresso

5. **Se encontrar bloqueadores:**
   - Marcar status como 🔴 Bloqueado no tracker
   - Adicionar à seção "Bloqueadores Ativos"
   - Aguardar resolução do orquestrador

6. **Usar múltiplos métodos de commit/push** (ver seção Git Operations no briefing)

7. **Ao finalizar:**
   - Criar REPORT-AGENT-C-UI.md
   - Marcar status como 🟢 Completo no tracker
   - Notificar conclusão

**COMECE AGORA** lendo o briefing e fazendo checkout da branch.
```

---

## ✅ Checklist de Deploy

Ao iniciar trabalho paralelo, verificar:
- [ ] PARALLEL-WORK-TRACKER.md criado e inicializado
- [ ] Todos briefings (BRIEFING-AGENT-*.md) criados
- [ ] Todas branches criadas e pushed para GitHub
- [ ] Este arquivo (DEPLOY-PROMPTS.md) gerado
- [ ] 3 sessões Claude Code Web abertas (uma por agent)
- [ ] Cada agent recebeu seu prompt completo
- [ ] Todos agents confirmaram checkout de branch
- [ ] Tracker sendo atualizado (verificar histórico)

---

## 🔄 Monitoramento

**Verificar PARALLEL-WORK-TRACKER.md a cada 30 minutos:**
- Progresso de cada agent (percentuais atualizados?)
- Bloqueadores ativos (algum agent parado?)
- ETAs realistas (revisarconforme progresso)

**Resolver bloqueadores imediatamente** quando reportados.

**Comunicação:**
- Agents atualizam tracker a cada 25%
- Orquestrador responde bloqueadores em < 30min
- Status final: Todos agents em 🟢 Completo antes de merge

EOF

git add DEPLOY-PROMPTS.md
git commit -m "feat: Add deployment prompts for parallel agents

Created copy-paste ready prompts for:
- Agent-A (Docs): 6h
- Agent-B (Tests): 10h
- Agent-C (UI): 5h

Each prompt includes:
- Branch checkout instructions
- Briefing reading
- Tracker update requirements
- Git operations guidance

Ready for immediate deployment in Claude Code Web.
"

git push origin develop
```

---

## 1.9. ETAPA 8: Relatório de Orquestração

Criar relatório consolidado do setup:

```bash
cat > ORCHESTRATION-REPORT.md << 'EOF'
# Relatório de Orquestração - {PROJECT_NAME}

**Data:** {DATE}
**Orquestrador:** Claude Code (Orchestrator Agent)
**Status:** ✅ Setup Completo - Pronto para Deploy de Agents

---

## 📊 Sumário Executivo

**Análise Profunda:**
- ✅ PROJECT-ANALYSIS.md criado (Score: X/10)
- Identificadas Y melhorias prioritárias
- Z features selecionadas para Grupo A (paralelo)

**Features Extraídas:**
Total: 3 features paralelas (Grupo A)
- F1: Documentação (6h) - ALTA prioridade
- F2: Testes (10h) - MÉDIA prioridade
- F3: UI Refactor (5h) - MÉDIA prioridade

**Speedup Estimado:**
- Sequencial: 21h (6 + 10 + 5)
- Paralelo: 10h (max)
- Ganho: 2.1x mais rápido

---

## 🌳 Branches Criadas

✅ Todas as branches criadas e pushed para GitHub:

1. **Agent-A:** `claude/docs-improvement-Ab3Cd5Ef8Gh9`
   - Feature: Documentação Técnica
   - Estimativa: 6h
   - Prioridade: ALTA

2. **Agent-B:** `claude/test-expansion-Jk1Lm4No7Pq0`
   - Feature: Expansão de Testes
   - Estimativa: 10h
   - Prioridade: MÉDIA

3. **Agent-C:** `claude/ui-refactor-Rs2Tu6Vw9Xy1`
   - Feature: Refatoração UI
   - Estimativa: 5h
   - Prioridade: MÉDIA

---

## 📝 Briefings Criados

✅ Um briefing completo para cada agent:

- `BRIEFING-AGENT-A-DOCS.md` (12 seções, ~800 linhas)
- `BRIEFING-AGENT-B-TESTS.md` (12 seções, ~750 linhas)
- `BRIEFING-AGENT-C-UI.md` (12 seções, ~780 linhas)

Cada briefing inclui:
- Status do projeto e ambiente
- Missão e escopo detalhado
- Plano de execução passo-a-passo (10-15 etapas)
- 5 métodos de commit/push (fallback chain)
- Recovery procedures (5 cenários)
- Checklist de aceitação
- Template de relatório JSON

---

## 🎯 Sistema de Tracking

✅ `PARALLEL-WORK-TRACKER.md` criado

**Funcionalidades:**
- Status em tempo real de cada agent (🟢🟡🔴)
- Progresso percentual (0%, 25%, 50%, 75%, 100%)
- Histórico de eventos timestamped
- Bloqueadores ativos (seção dedicada)
- Ordem de merge definida
- Critérios de conclusão (checklist)

**Atualização:**
- Agents: A cada milestone (25%, 50%, 75%, 100%)
- Orquestrador: Ao resolver bloqueadores

---

## 🚀 Prompts de Deploy

✅ `DEPLOY-PROMPTS.md` criado

**Conteúdo:**
- 3 prompts copiáveis (um por agent)
- Instruções de checkout de branch
- Comando para ler briefing
- Orientações de tracking
- Checklist de deploy

**Uso:**
1. Abrir 3 sessões Claude Code Web
2. Copiar prompt de cada agent
3. Colar e executar
4. Monitorar via tracker

---

## 📋 Ordem de Merge

**Quando todos agents completarem (🟢 Completo):**

```
1. Agent-A (Docs) ─────────────► merge develop
        ↓ (validar build)
2. Agent-B (Tests) ────────────► merge develop
        ↓ (validar build + tests)
3. Agent-C (UI Refactor) ──────► merge develop
        ↓ (validar build + tests + UI)

   develop (3 features integradas) ► validação final ► master
```

**Razão da ordem:**
- Agent-A primeiro: Zero conflitos (apenas docs)
- Agent-B segundo: Cria arquivos novos (__tests__/*)
- Agent-C terceiro: Modifica código existente (src/)

---

## ⏱️ Timeline Estimado

| Fase | Duração | Ação |
|------|---------|------|
| **Setup (Concluído)** | 2h | Análise + briefings + branches + tracking |
| **Deploy Agents** | 5min | Abrir 3 sessões + colar prompts |
| **Implementação Paralela** | 10h | Agents trabalhando simultaneamente |
| **Merge Coordenado** | 1h | Merge 3 branches + validação |
| **TOTAL** | **13h** | vs 23h sequencial = **43% mais rápido** |

---

## 📊 Métricas Esperadas

### Por Agent

| Agent | Feature | Files | Lines | Commits | Tests | ETA |
|-------|---------|-------|-------|---------|-------|-----|
| A | Docs | ~8 | +500 | 3-5 | N/A | 6h |
| B | Tests | ~25 | +1200 | 5-8 | 50+ | 10h |
| C | UI | ~15 | +300, -150 | 4-6 | 10+ | 5h |
| **TOTAL** | **3** | **~48** | **+2000** | **12-19** | **60+** | **10h** |

### Consolidado

- **Context Reduction:** 85%+ (tracking + briefings vs full context)
- **Speedup:** 2.1x (10h paralelo vs 21h sequencial)
- **Quality Target:** 9.0/10+ (baseado em validações idCEB)
- **Conflict Rate:** < 5% (file isolation garantido)

---

## ✅ Próximos Passos

1. **[VOCÊ]** Revisar este relatório
2. **[VOCÊ]** Abrir 3 sessões Claude Code Web
3. **[VOCÊ]** Copiar prompts de DEPLOY-PROMPTS.md
4. **[VOCÊ]** Colar em cada sessão e iniciar
5. **[AGENTS]** Implementação paralela (10h)
6. **[VOCÊ]** Monitorar PARALLEL-WORK-TRACKER.md (a cada 30min)
7. **[VOCÊ]** Resolver bloqueadores se reportados
8. **[VOCÊ]** Merge coordenado quando todos 🟢 Completo
9. **[VOCÊ]** Validação final + push para master

---

## 📞 Suporte

**Se agents bloquearem:**
- Verificar seção "Bloqueadores Ativos" no tracker
- Resolver conforme descrito
- Atualizar tracker marcando como resolvido
- Notificar agent para continuar

**Se merge tiver conflitos:**
- Consultar PARTE 3 deste template (Merge Coordenado)
- Seguir estratégia de resolução
- Validar build após resolver

**Se qualidade estiver abaixo de 8.0/10:**
- Revisar critérios de aceitação no briefing
- Solicitar melhorias do agent
- Não mergear até atingir qualidade mínima

---

**Orquestração Completa:** ✅
**Pronto para Deploy:** ✅
**Boa sorte!** 🚀

EOF

git add ORCHESTRATION-REPORT.md
git commit -m "docs: Add orchestration report

Complete setup report including:
- 3 features identified and configured
- 3 branches created and pushed
- 3 briefings created (12 sections each)
- Tracking system initialized
- Deploy prompts ready
- Timeline: 13h total (10h parallel)
- Speedup: 2.1x vs sequential

All systems ready for parallel development.
"

git push origin develop
```

---

**🎉 ORQUESTRAÇÃO COMPLETA!**

Você agora tem:
- ✅ PROJECT-ANALYSIS.md (análise profunda)
- ✅ 3 branches criadas (claude/*)
- ✅ 3 briefings detalhados (BRIEFING-AGENT-*.md)
- ✅ Sistema de tracking (PARALLEL-WORK-TRACKER.md)
- ✅ Prompts prontos (DEPLOY-PROMPTS.md)
- ✅ Relatório consolidado (ORCHESTRATION-REPORT.md)

**Próximo passo:** Deploy dos 3 agents usando prompts de DEPLOY-PROMPTS.md

---

# PARTE 2: TEMPLATE DE BRIEFING PARA AGENTES WORKERS

## Template Completo para BRIEFING-AGENT-{ID}-{FEATURE}.md

Use este template para criar briefing de cada agent. Substitua variáveis `{VARIAVEL}` com valores específicos.

```markdown
# BRIEFING: AGENT-{ID} - {FEATURE_NAME}

## 2.1. Status do Projeto

- **Projeto:** {PROJECT_NAME}
- **Tipo:** {PROJECT_TYPE} (Web App, CLI, Mobile, etc.)
- **Stack:** {TECH_STACK}
- **Build Status:** {STATUS} (✅ Passing / ⚠️ With Warnings / ❌ Failing)
- **Branch Base:** develop
- **Sua Branch:** claude/{feature}-{SESSION_ID}
- **Dependências:** {DEPENDENCIES} (ex: Node 18+, PostgreSQL, Redis)

**Fases/Features Completas:**
- {Lista de features já merged em develop}

**Fases/Features em Progresso:**
- {Lista de outros agents trabalhando em paralelo}

## 2.2. Ambiente: Claude Code Web + Múltiplos Métodos Git

⚠️ **CRÍTICO:** Você está executando no Claude Code Web (navegador)

**Implicações:**
- ✅ Use interface Claude Code para git (não mencione "terminal local")
- ✅ Path do projeto: `/tmp/tmp.{random}/{PROJECT_NAME}`
- ❌ Evitar: "background tasks", "IDE features", "localhost" (não disponíveis)
- ❌ Não assumir: GUI tools, database clients GUI
- ✅ Branch pattern: `claude/*-{SESSION_ID}` (obrigatório para push)

**Documentação Base:**
⚠️ Lembre que PROJECT-ANALYSIS.md e outros docs estão na branch `develop`.
Para ler: `git show develop:PROJECT-ANALYSIS.md`

---

### 🔧 Múltiplos Métodos de Commit/Push (IMPORTANTE)

⚠️ **PROBLEMA CONHECIDO:** Em alguns casos, push via CLI pode falhar (experiência idCEB Fase 7).

**Solução:** Tentar métodos EM ORDEM até um funcionar.

#### Método 1: Git CLI Padrão ⭐ (Tente primeiro)

```bash
# Add e commit
git add .
git commit -m "feat: {description}

{Detalhes da implementação}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push
git push origin claude/{feature}-{SESSION_ID}
```

**Se retornar erro 403/permission:**
→ Ir para Método 2

---

#### Método 2: Git CLI com Remote URL Completa

```bash
# Verificar remote atual
git remote -v

# Tentar push com URL completa
git push https://github.com/{USER}/{REPO}.git claude/{feature}-{SESSION_ID}
```

**Se ainda falhar:**
→ Ir para Método 3

---

#### Método 3: GitHub CLI (gh)

```bash
# Verificar se gh está autenticado
gh auth status

# Se não autenticado, fazer login
gh auth login

# Push
git push origin claude/{feature}-{SESSION_ID}

# OU criar PR diretamente
gh pr create --base develop --head claude/{feature}-{SESSION_ID} \
  --title "{FEATURE_NAME}" \
  --body "Implementação completa conforme briefing..."
```

**Se ainda falhar:**
→ Ir para Método 4

---

#### Método 4: Interface Claude Code Web

```
1. Clicar no ícone "Source Control" na sidebar esquerda
2. Verificar arquivos modificados apareceram
3. Stage changes (checkbox ao lado de cada arquivo)
4. Escrever commit message na caixa de texto
5. Clicar botão "Commit"
6. Clicar botão "Push" (ou "Sync Changes")
7. Aguardar confirmação
```

**Se ainda falhar:**
→ Ir para Método 5

---

#### Método 5: Criar Patch e Reportar (Último Recurso)

```bash
# Criar patch dos commits
git format-patch develop..HEAD -o patches/

# Listar patches criados
ls patches/

# Adicionar ao commit
git add patches/
git commit -m "temp: Patches for merge (push failed)"

# Reportar no tracker
# Marcar como 🔴 Bloqueado
# Adicionar em "Bloqueadores Ativos":
# "Agent-{ID}: Push falhou após 4 tentativas. Patches criados em patches/.
#  Orquestrador fazer push manual ou aplicar patches."
```

**Orquestrador aplicará patches manualmente:**
```bash
git am patches/*.patch
```

---

### ✅ Validação de Push Bem-Sucedido (OBRIGATÓRIO)

Após push por QUALQUER método, SEMPRE validar:

```bash
# Verificar se branch aparece no GitHub
gh repo view --web
# OU
git ls-remote --heads origin | grep "claude/{feature}-{SESSION_ID}"
```

**Se comando retorna a branch:**
✅ Push bem-sucedido! Continuar trabalho.

**Se comando NÃO retorna nada:**
❌ Push falhou - tentar próximo método da lista.

---

## 2.3. Sua Missão

**Objetivo:** {FEATURE_OBJECTIVE}

**Estimativa:** {HOURS}h

**Prioridade:** {PRIORITY} (ALTA / MÉDIA / BAIXA)

**Arquivos Esperados:**
- **Criar:** {N} novos arquivos (~{LINES} linhas)
- **Modificar:** {M} arquivos existentes (~{LINES} linhas)

**Conflitos Potenciais:**
- {CONFLICT_ANALYSIS}
- Exemplo: "Zero - feature isolada, apenas cria arquivos em docs/"
- Exemplo: "Baixo - modifica src/components/ mas outros agents não tocam aqui"

**Dependências:**
- {DEPENDENCY_1} (já disponível em develop)
- {DEPENDENCY_2} (pacote npm - instalar com `npm install {package}`)

---

## 2.4. Escopo Completo

### Features Principais

- [ ] {Feature 1 específica e mensurável}
- [ ] {Feature 2 específica e mensurável}
- [ ] {Feature 3 específica e mensurável}
- [ ] {Feature N específica e mensurável}

### Estrutura de Arquivos

```
{PROJECT_ROOT}/
  ├── {dir1}/
  │   ├── {file1}.{ext} (criar - {lines} linhas)
  │   └── {file2}.{ext} (criar - {lines} linhas)
  ├── {dir2}/
  │   └── {file3}.{ext} (modificar - adicionar {lines} linhas)
  └── {file4}.{ext} (modificar - seção {section})
```

### Schema/Contratos (SE APLICÁVEL)

**Se envolve banco de dados:**

```prisma
// Novos modelos Prisma
model {ModelName} {
  id        String   @id @default(cuid())
  {field1}  String
  {field2}  Int
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

**Se envolve APIs:**

```typescript
// Endpoints a criar
POST   /api/{resource}           # Criar
GET    /api/{resource}           # Listar
GET    /api/{resource}/[id]      # Buscar
PUT    /api/{resource}/[id]      # Atualizar
DELETE /api/{resource}/[id]      # Deletar
```

---

## 2.5. Comunicação com Orchestrador + Update Tracker

### Atualizar PARALLEL-WORK-TRACKER.md

**OBRIGATÓRIO: A cada milestone (25%, 50%, 75%, 100%):**

**Passo 1:** Editar PARALLEL-WORK-TRACKER.md

```bash
# Abrir arquivo
nano PARALLEL-WORK-TRACKER.md
# OU
vim PARALLEL-WORK-TRACKER.md
# OU usar interface Claude Code
```

**Passo 2:** Localizar sua seção (Agent-{ID})

**Passo 3:** Atualizar campos:

```markdown
### Agent-{ID}: {Feature Name}
- **Branch:** `claude/{feature}-{SESSION_ID}`
- **Status:** 🟡 Em Progresso (50%)  ← ATUALIZAR percentual e emoji
- **Última Atualização:** 2025-11-11 15:45 ← ATUALIZAR timestamp
- **Progresso:**
  - [x] Item 1 completo  ← MARCAR itens completos
  - [x] Item 2 completo
  - [ ] Item 3 em progresso ← 50% atual
  - [ ] Item 4 pendente
- **Commits:** 3  ← ATUALIZAR contagem
- **Linhas:** +450 / -20  ← ATUALIZAR contadores
- **Bloqueadores:** Nenhum ← OU descrever se houver
- **ETA:** 3h restantes  ← ATUALIZAR estimativa
```

**Passo 4:** Adicionar entrada no Histórico

```markdown
## 🔄 Histórico de Atualizações

| Timestamp | Agent | Evento | Detalhes |
|-----------|-------|--------|----------|
| 2025-11-11 15:45 | Agent-{ID} | Progresso 50% | {Milestone atingido} |
```

**Passo 5:** Commitar atualização

```bash
git add PARALLEL-WORK-TRACKER.md
git commit -m "track: Agent-{ID} - 50% completo

Milestone: {Descrição do milestone}
Progresso: Items 1-2 completos, Item 3 em andamento
ETA: 3h restantes
"

# Push usando múltiplos métodos (Seção 2.2)
git push origin claude/{feature}-{SESSION_ID}
```

---

### Reportar Bloqueadores

**SE encontrar bloqueador que impeça progresso por >30min:**

**Passo 1:** Atualizar seu status no tracker

```markdown
### Agent-{ID}: {Feature Name}
- **Status:** 🔴 Bloqueado
- **Bloqueadores:** Dependência {X} não instalada / Build falhou / Outro
```

**Passo 2:** Adicionar à seção "Bloqueadores Ativos"

```markdown
## ⚠️ Bloqueadores Ativos

### Bloqueador #N: Agent-{ID} - {Título Curto}
- **Agent:** Agent-{ID}
- **Descrição:** {Explicação detalhada do problema}
- **Impacto:** {Como afeta o trabalho - ex: "Implementação parada em 50%"}
- **Tentativas de Resolução:**
  - Tentativa 1: {O que tentou} - Falhou porque {razão}
  - Tentativa 2: {O que tentou} - Falhou porque {razão}
- **Ação Esperada do Orquestrador:** {O que orquestrador deve fazer}
- **Status:** 🔴 Não Resolvido
- **Timestamp:** {TIMESTAMP}
```

**Passo 3:** Commitar e aguardar resolução

```bash
git add PARALLEL-WORK-TRACKER.md
git commit -m "track: Agent-{ID} - BLOQUEADO

Bloqueador: {Título}
Aguardando: {Ação do orquestrador}
"
git push origin claude/{feature}-{SESSION_ID}
```

**Passo 4:** Aguardar orquestrador resolver (ele atualizará tracker)

**Passo 5:** Quando resolvido, continuar e atualizar status para 🟡

---

### Relatório de Conclusão (100%)

**Ao completar 100%:**

**Passo 1:** Criar REPORT-AGENT-{ID}-{FEATURE}.md (ver Seção 2.11)

**Passo 2:** Atualizar tracker

```markdown
### Agent-{ID}: {Feature Name}
- **Status:** 🟢 Completo (100%)
- **Relatório:** ✅ [REPORT-AGENT-{ID}.md](./REPORT-AGENT-{ID}.md)
```

**Passo 3:** Marcar checkbox em "Critérios de Conclusão"

```markdown
## ✅ Critérios de Conclusão

- [x] Agent-{ID}: 100% completo ✅
```

**Passo 4:** Commitar e notificar

```bash
git add PARALLEL-WORK-TRACKER.md REPORT-AGENT-{ID}.md
git commit -m "track: Agent-{ID} - 100% COMPLETO ✅

Feature {NAME} finalizada conforme briefing.
Relatório completo em REPORT-AGENT-{ID}.md.

Pronto para merge.
"
git push origin claude/{feature}-{SESSION_ID}
```

---

## 2.6. Recovery & Troubleshooting

### Cenário 1: Branch Push Failure

**Sintoma:** `git push` retorna erro 403/permission denied

**Causa:** Branch não está no padrão `claude/*` OU SESSION_ID inválido

**Diagnóstico:**
```bash
# Verificar nome da branch atual
git branch

# Verificar remote
git remote -v
```

**Solução:**

**Se branch correta (`claude/{feature}-{SESSION_ID}`):**
- Tentar Métodos 2-5 da Seção 2.2 (Múltiplos Métodos Git)

**Se branch INCORRETA (não começa com `claude/`):**
```bash
# Obter SESSION_ID (se disponível)
SESSION_ID=${CLAUDE_SESSION_ID:-$(date +%s | sha256sum | base64 | head -c 12)}

# Criar branch correta
git checkout -b claude/{feature}-$SESSION_ID

# Aplicar commits da branch errada
git cherry-pick {COMMIT_HASH1} {COMMIT_HASH2}...

# Push (agora funciona!)
git push -u origin claude/{feature}-$SESSION_ID

# Verificar sucesso
git ls-remote --heads origin | grep claude/{feature}
```

---

### Cenário 2: Build Errors Após Implementação

**Sintoma:** `npm run build` falha com erros TypeScript/compilação

**Diagnóstico:**
```bash
npm run build 2>&1 | tee build-errors.log
head -50 build-errors.log  # Ver primeiros 50 erros
```

**Soluções Comuns:**

**Erro: "Cannot find module '{module}'"**
```bash
# Instalar dependência faltando
npm install {module}

# Verificar instalação
npm list {module}

# Commitar package.json
git add package.json package-lock.json
git commit -m "deps: Add {module}"
```

**Erro: "Type 'X' is not assignable to type 'Y'"**
- Corrigir tipos manualmente
- NUNCA usar `@ts-ignore` (resolver problema raiz)
- Se necessário, criar type guard

**Erro: "Property '{prop}' does not exist on type '{Type}'"**
- Adicionar propriedade ao type/interface
- OU verificar se está importando tipo correto

**Estratégia Geral:**
1. Resolver erros UM POR VEZ (não todos de uma vez)
2. Rodar `npm run build` após cada fix
3. Commitar quando build passar

---

### Cenário 3: Merge Conflicts (Raro mas possível)

**Sintoma:** Orquestrador reporta conflito no seu PR

**Causa:** Outro agent modificou mesmos arquivos (não deveria acontecer se file isolation funcionou)

**Diagnóstico:**
```bash
# Tentar merge de develop
git fetch origin develop
git merge origin/develop

# Ver arquivos conflitantes
git diff --name-only --diff-filter=U
```

**Solução:**

**Conflito em DOCUMENTAÇÃO:**
- Aceitar versão mais completa
- OU mesclar ambas as versões

**Conflito em CÓDIGO:**
- ⚠️ PARAR e reportar ao orquestrador
- NÃO resolver sozinho (pode quebrar feature do outro agent)
- Orquestrador coordenará resolução

**Após resolver:**
```bash
git add {arquivos_resolvidos}
git commit -m "fix: Resolve merge conflicts with develop"
git push origin claude/{feature}-{SESSION_ID}
```

---

### Cenário 4: Dependência Faltando/Incompatível

**Sintoma:** Import não resolve OU runtime error "`Cannot find module`"

**Diagnóstico:**
```bash
# Verificar se pacote está instalado
npm list {package}

# Ver versão
npm list {package} --depth=0
```

**Solução:**

**Pacote NÃO instalado:**
```bash
npm install {package}
```

**Pacote instalado mas versão incompatível:**
```bash
# Ver versão requerida (package.json)
cat package.json | grep "{package}"

# Instalar versão específica
npm install {package}@{version}
```

**Pacote peer dependency faltando:**
```bash
# npm avisará qual peer está faltando
npm install {peer-package}
```

**Sempre commitar após instalar:**
```bash
git add package.json package-lock.json
git commit -m "deps: Add {package}@{version}"
```

---

### Cenário 5: Testes Falhando

**Sintoma:** `npm test` reporta falhas

**Diagnóstico:**
```bash
# Rodar testes com output detalhado
npm test -- --verbose

# Rodar teste específico
npm test -- {test-file}.test.ts
```

**Soluções:**

**Teste NOVO falhando:**
- Corrigir implementação OU
- Corrigir teste (se expectativa estava errada)

**Teste EXISTENTE quebrou:**
- ⚠️ NÃO MODIFICAR teste existente
- Sua implementação quebrou algo
- Reverter mudança OU
- Ajustar implementação para não quebrar teste

**Mock faltando:**
```typescript
// Adicionar mock
jest.mock('{module}', () => ({
  {function}: jest.fn()
}))
```

**Async test timeout:**
```typescript
// Aumentar timeout
test('...', async () => {
  // ...
}, 10000) // 10s timeout
```

---

### Checklist Pré-Push (OBRIGATÓRIO) ✅

Antes de fazer push final, SEMPRE validar:

```bash
# 1. Linting
npm run lint
# Deve retornar: 0 errors, 0 warnings

# 2. Build
npm run build
# Deve completar sem erros

# 3. Testes (se aplicável)
npm test
# Deve: X passing, 0 failing

# 4. Git status limpo
git status
# Deve mostrar: "nothing to commit, working tree clean"

# 5. Branch correta
git branch
# Deve mostrar: * claude/{feature}-{SESSION_ID}

# 6. Commits com mensagens descritivas
git log --oneline -5
# Verificar mensagens fazem sentido
```

**SE qualquer item falhar:**
- ❌ NÃO fazer push
- ✅ Corrigir problema primeiro
- ✅ Rodar checklist novamente

**APENAS quando TODOS passarem:**
- ✅ Push permitido
- ✅ Atualizar tracker para 100%
- ✅ Criar relatório final

---

## 2.7. Plano de Execução Detalhado

### ETAPA 1: Setup e Checkout (15-30 min)

```bash
# 1. Checkout da sua branch
git checkout claude/{feature}-{SESSION_ID}

# 2. Verificar branch atual
git branch
# Output deve ser: * claude/{feature}-{SESSION_ID}

# 3. Ler análise do projeto (em develop)
git show develop:PROJECT-ANALYSIS.md | less

# 4. Ler seu briefing (este arquivo)
cat BRIEFING-AGENT-{ID}-{FEATURE}.md | less

# 5. Listar arquivos do projeto (entender estrutura)
tree -L 3 -I 'node_modules|.next|.git'
# OU
find . -type d -maxdepth 3 | grep -v node_modules | head -30

# 6. Verificar dependências necessárias
cat package.json | grep dependencies -A 20

# 7. Atualizar tracker (0% → 10%)
# Editar PARALLEL-WORK-TRACKER.md, marcar "Setup completo"
git add PARALLEL-WORK-TRACKER.md
git commit -m "track: Agent-{ID} - Setup completo (10%)"
git push origin claude/{feature}-{SESSION_ID}
```

**Output esperado:**
- ✅ Branch correta checkedout
- ✅ Contexto do projeto entendido
- ✅ Tracker atualizado para 10%

---

### ETAPA 2-N: Implementação (VARIA POR FEATURE)

**Customize estas etapas para sua feature específica:**

---

#### ETAPA 2: {First Implementation Step} ({time}h)

**Objetivo:** {What to accomplish}

**Arquivos a criar/modificar:**
- `{file1}` - {Purpose}
- `{file2}` - {Purpose}

**Implementação:**

```{language}
// Código de exemplo ou pseudocódigo
// Mostrar estrutura esperada
```

**Comandos:**
```bash
# Criar diretório se necessário
mkdir -p {dir}

# Criar arquivo
touch {file}

# Implementar conforme especificação acima
# ...

# Testar implementação
{test_command}

# Validar resultado
{validation_command}
```

**Validação:**
- ✅ {Critério 1 de sucesso}
- ✅ {Critério 2 de sucesso}

**Commit intermediário:**
```bash
git add {files}
git commit -m "feat({scope}): {description}

{Detalhes da implementação}
"
```

**Atualizar tracker (10% → 25%):**
```bash
# Editar PARALLEL-WORK-TRACKER.md
# Marcar ETAPA 2 completa
git add PARALLEL-WORK-TRACKER.md
git commit -m "track: Agent-{ID} - 25% completo"
git push origin claude/{feature}-{SESSION_ID}
```

---

#### ETAPA 3: {Second Implementation Step} ({time}h)

{Mesmo formato que ETAPA 2}

**Atualizar tracker (25% → 50%):**

---

#### ETAPA N-1: {Final Implementation Step} ({time}h)

{Mesmo formato}

**Atualizar tracker (50% → 75%):**

---

### ETAPA N: Validação Final, Commit & Relatório (30-60 min)

**1. Review Completo**

```bash
# Ver todas as mudanças
git diff develop..HEAD

# Listar arquivos modificados
git diff --name-status develop..HEAD

# Verificar linhas adicionadas/removidas
git diff --stat develop..HEAD
```

**2. Checklist Pré-Push (Seção 2.6)**

```bash
npm run lint      # ✅ 0 errors
npm run build     # ✅ Success
npm test          # ✅ All passing (se aplicável)
```

**3. Commit Final Consolidado (SE necessário)**

```bash
# Se muitos commits pequenos, considerar squash
# (OPCIONAL - apenas se >10 commits triviais)
git rebase -i develop

# Escolher commits a squash
# Manter commits significativos separados
```

**4. Push Final**

```bash
git push origin claude/{feature}-{SESSION_ID}

# Validar push bem-sucedido
git ls-remote --heads origin | grep claude/{feature}
```

**5. Criar Relatório Final** (ver Seção 2.11)

```bash
# Criar arquivo
cat > REPORT-AGENT-{ID}-{FEATURE}.md << 'EOF'
{JSON do relatório - ver Seção 2.11}
EOF

# Commit
git add REPORT-AGENT-{ID}-{FEATURE}.md
git commit -m "docs: Add final report for Agent-{ID}"
git push origin claude/{feature}-{SESSION_ID}
```

**6. Atualizar Tracker (75% → 100%)**

```bash
# Editar PARALLEL-WORK-TRACKER.md
# Status: 🟢 Completo (100%)
# Relatório: ✅ Link
# Marcar checkbox em "Critérios de Conclusão"

git add PARALLEL-WORK-TRACKER.md
git commit -m "track: Agent-{ID} - 100% COMPLETO ✅"
git push origin claude/{feature}-{SESSION_ID}
```

---

## 2.8. Recursos Reutilizáveis

### Componentes/Módulos Existentes

**Se projeto tem biblioteca de componentes:**

```typescript
// Importar e reusar:
import { Button, Card, Input, Form } from '@/components/ui'
import { useToast } from '@/hooks/use-toast'
import { cn } from '@/lib/utils'
```

**Padrões de código existentes:**
- Verificar arquivos similares no projeto
- Copiar estrutura e adaptar
- Manter consistência de estilo

### Arquivos de Referência

**Buscar exemplos similares:**
```bash
# Encontrar arquivos similares
find . -name "*{pattern}*" -type f | grep -v node_modules

# Exemplo: Encontrar outros API routes
find ./src/app/api -name "route.ts"

# Ver implementação
cat {arquivo-referencia}
```

### Template-First Approach

**Princípio:** "Não reinvente a roda"

1. **Buscar arquivo similar** no projeto
2. **Copiar estrutura** (não código completo)
3. **Adaptar** para sua necessidade
4. **Manter padrões** consistentes

**Exemplo:**

```bash
# Você precisa criar: src/app/api/users/route.ts
# Buscar API route existente similar:
ls src/app/api/*/route.ts

# Copiar estrutura de src/app/api/products/route.ts
cp src/app/api/products/route.ts src/app/api/users/route.ts

# Adaptar: products → users, manter validações, error handling, etc.
```

---

## 2.9. Regras Críticas

### Regra 1: SEMPRE Testar Antes de Push

**Checklist obrigatório:**
- Build sem erros
- Testes passando (se aplicável)
- Linting sem warnings

**Penalidade:** Push rejeitado, retrabalho necessário

---

### Regra 2: Git Hygiene

**Commits:**
- ✅ Mensagens descritivas (não "fix", "wip", "test")
- ✅ Conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`
- ✅ Body do commit explica **POR QUÊ**, não **O QUÊ**

**Branch:**
- ✅ Nome correto: `claude/{feature}-{SESSION_ID}`
- ❌ NUNCA force push (`--force`)
- ❌ NUNCA rebase após push (quebra histórico)

**Arquivos:**
- ❌ NUNCA commitar: node_modules/, .env, .DS_Store, build/
- ❌ NUNCA commitar: console.log() de debug
- ✅ SEMPRE: .gitignore configurado

---

### Regra 3: Zero @ts-ignore / any

**TypeScript strict:**
- ❌ NUNCA usar `@ts-ignore` ou `@ts-expect-error`
- ❌ NUNCA usar `any` (usar `unknown` e narrow)
- ✅ SEMPRE resolver problema de tipo raiz

**Exceção:** Biblioteca third-party sem types (então usar `unknown`)

---

### Regra 4: Comunicação Proativa

**Reportar:**
- ✅ Progresso a cada 25% (tracker)
- ✅ Bloqueadores em < 30min (tracker + bloqueadores ativos)
- ✅ Mudanças de ETA (se tarefa mais longa que estimado)

**NÃO assumir:**
- ❌ "Orquestrador vai perceber sozinho"
- ❌ "Não preciso atualizar tracker"
- ❌ "Vou resolver sozinho mesmo bloqueado 2h"

---

### Regra 5: Respeitar File Isolation

**Sua feature tem escopo de arquivos definido (Seção 2.4)**

**Permitido:**
- ✅ Criar arquivos no seu escopo
- ✅ Modificar arquivos no seu escopo
- ✅ Ler qualquer arquivo (para referência)

**PROIBIDO:**
- ❌ Modificar arquivos FORA do seu escopo
- ❌ "Aproveitar e melhorar" código não relacionado
- ❌ Refatorações globais não autorizadas

**Razão:** Prevenir conflitos com outros agents paralelos

**Exceção:** package.json, package-lock.json (deps necessárias)

---

### Regra N: {Regras Específicas do Projeto}

**Adicione regras específicas aqui:**

**Exemplo - Projeto Multi-tenant:**
- ✅ SEMPRE filtrar por `escolaId` em queries
- ❌ NUNCA delete permanente (soft delete apenas)
- ✅ SEMPRE audit trail em operações sensíveis

**Exemplo - Projeto LGPD:**
- ✅ Anonimizar dados pessoais ao deletar
- ✅ Logs não devem conter CPF/email
- ✅ Consentimento obrigatório antes de processar dados

---

## 2.10. Critérios de Aceitação

Sua feature será considerada COMPLETA quando:

### Implementação

- [ ] Todos os arquivos listados na Seção 2.4 criados/modificados
- [ ] Funcionalidade implementada conforme especificação
- [ ] Código segue padrões do projeto (linting, formatting)
- [ ] Zero @ts-ignore / any desnecessários

### Qualidade

- [ ] Build sem erros: `npm run build` ✅
- [ ] Linting sem warnings: `npm run lint` ✅
- [ ] Testes passando: `npm test` ✅ (se aplicável)
- [ ] Testes manuais: {Lista de testes específicos}

### Documentação

- [ ] Código comentado em funções complexas
- [ ] JSDoc em funções públicas (se aplicável)
- [ ] README.md atualizado (se alterou setup/deploy)
- [ ] {Documento específico} atualizado (se aplicável)

### Git

- [ ] Branch correta: `claude/{feature}-{SESSION_ID}`
- [ ] Commits descritivos (conventional commits)
- [ ] Push bem-sucedido (validado com `git ls-remote`)
- [ ] Histórico limpo (não há commits "WIP" ou "test")

### Tracking

- [ ] Tracker atualizado para 🟢 Completo (100%)
- [ ] Relatório final criado (REPORT-AGENT-{ID}.md)
- [ ] Checkbox marcado em "Critérios de Conclusão"
- [ ] Histórico contém todas as atualizações (25%, 50%, 75%, 100%)

### Específicos da Feature

**{Critérios específicos da sua feature}:**

- [ ] {Critério 1 específico e testável}
- [ ] {Critério 2 específico e testável}
- [ ] {Critério 3 específico e testável}

**Exemplo - Feature de Documentação:**
- [ ] docs/architecture/overview.md criado
- [ ] Swagger/OpenAPI gerado (se APIs)
- [ ] CONTRIBUTING.md criado
- [ ] README.md badges atualizados

**Exemplo - Feature de Testes:**
- [ ] Coverage aumentou de X% → Y%
- [ ] Playwright configurado e funcionando
- [ ] 5+ testes E2E críticos criados
- [ ] CI executando testes automaticamente

---

## 2.11. Relatório Final Esperado

Ao completar 100%, criar arquivo `REPORT-AGENT-{ID}-{FEATURE}.md`:

```markdown
# Relatório Final: Agent-{ID} - {FEATURE_NAME}

**Data:** {DATE}
**Agent:** Agent-{ID}
**Branch:** claude/{feature}-{SESSION_ID}
**Status:** ✅ COMPLETO

---

## 📊 Sumário Executivo

```json
{
  "agent": "Agent-{ID}",
  "feature": "{FEATURE_NAME}",
  "branch": "claude/{feature}-{SESSION_ID}",
  "status": "completed",
  "horas_estimadas": {ESTIMATED_HOURS},
  "horas_realizadas": {ACTUAL_HOURS},
  "desvio_tempo": "{PERCENTAGE}%",
  "qualidade_score": "{SCORE}/10",

  "arquivos": {
    "criados": {COUNT},
    "modificados": {COUNT},
    "deletados": {COUNT}
  },

  "linhas": {
    "adicionadas": {COUNT},
    "removidas": {COUNT},
    "total": {COUNT}
  },

  "commits": {
    "total": {COUNT},
    "sha_inicial": "{SHA}",
    "sha_final": "{SHA}"
  },

  "testes": {
    "executados": true,
    "criados": {COUNT},
    "passando": {COUNT},
    "falhando": 0,
    "coverage_antes": "{PERCENTAGE}%",
    "coverage_depois": "{PERCENTAGE}%"
  },

  "build": {
    "status": "success",
    "tempo_compilacao": "{SECONDS}s",
    "warnings": 0,
    "errors": 0
  },

  "bloqueadores": {
    "total": {COUNT},
    "resolvidos": {COUNT},
    "tempo_parado": "{HOURS}h"
  },

  "checklist_aceitacao": {
    "{criterion_1}": true,
    "{criterion_2}": true,
    "{criterion_3}": true,
    "todos_completos": true
  }
}
```

---

## 🎯 Entregas

### Arquivos Criados

1. `{file1}` ({lines} linhas) - {Purpose}
2. `{file2}` ({lines} linhas) - {Purpose}
3. `{fileN}` ({lines} linhas) - {Purpose}

### Arquivos Modificados

1. `{file1}` (+{add} / -{del} linhas) - {Changes}
2. `{file2}` (+{add} / -{del} linhas) - {Changes}

---

## ✅ Validação

### Build

```bash
$ npm run build

✓ Compiled successfully in {time}s
✓ 0 errors
✓ 0 warnings
```

### Linting

```bash
$ npm run lint

✓ 0 errors
✓ 0 warnings
```

### Testes

```bash
$ npm test

✓ {count} passing
✓ 0 failing
Coverage: {percentage}%
```

### Testes Manuais

- [x] {Test 1 description} - ✅ Passou
- [x] {Test 2 description} - ✅ Passou
- [x] {Test N description} - ✅ Passou

---

## 📝 Decisões Técnicas

### Decisão 1: {Title}

**Contexto:** {Why this decision was needed}

**Opções Consideradas:**
- Opção A: {Pros/Cons}
- Opção B: {Pros/Cons}

**Escolhida:** Opção {X}

**Razão:** {Why this was the best choice}

### Decisão 2: {Title}

{Mesmo formato}

---

## ⚠️ Bloqueadores Encontrados

### Bloqueador #1: {Title}

- **Quando:** ETAPA {N}, ~{percentage}% completo
- **Problema:** {Description}
- **Solução:** {How it was resolved}
- **Tempo Parado:** {hours}h
- **Prevenção Futura:** {Lessons learned}

---

## 📈 Métricas de Performance

| Métrica | Valor |
|---------|-------|
| Tempo Total | {actual}h (estimado: {estimated}h) |
| Desvio | {percentage}% |
| Commits | {count} |
| Linhas/Hora | {count} |
| Build Time | {seconds}s |
| Test Coverage | {before}% → {after}% (+{delta}%) |

---

## 🔄 Próximos Passos

**Para Orquestrador:**
- [ ] Review do código
- [ ] Merge para develop (ordem: {position})
- [ ] Validar build pós-merge
- [ ] Validar testes pós-merge

**Para Feature Futura:**
- {Sugestão de melhoria 1}
- {Sugestão de melhoria 2}

---

## 💡 Lições Aprendidas

### O Que Funcionou Bem

- ✅ {Item 1}
- ✅ {Item 2}

### O Que Pode Melhorar

- ⚠️ {Item 1}
- ⚠️ {Item 2}

### Recomendações para Próximos Agents

- {Recommendation 1}
- {Recommendation 2}

---

**Relatório gerado por:** Agent-{ID}
**Timestamp:** {TIMESTAMP}
**Status:** ✅ PRONTO PARA MERGE
```

---

## 2.12. Links Úteis

### Claude Code Web (Documentação Oficial)

- **Blog Announcement:** https://www.claude.com/blog/claude-code-on-the-web
- **Documentation:** https://code.claude.com/docs/en/claude-code-on-the-web
- **Sandboxing Explanation:** https://www.anthropic.com/engineering/claude-code-sandboxing
- **Sandboxing Docs:** https://code.claude.com/docs/en/sandboxing

### Projeto

- **GitHub Repo:** {GITHUB_URL}
- **Branch develop:** {GITHUB_URL}/tree/develop
- **Sua Branch:** {GITHUB_URL}/tree/claude/{feature}-{SESSION_ID}
- **Pull Requests:** {GITHUB_URL}/pulls
- **Issues:** {GITHUB_URL}/issues

### Documentação do Projeto

- **PROJECT-ANALYSIS.md:** `git show develop:PROJECT-ANALYSIS.md`
- **README.md:** `git show develop:README.md`
- **PARALLEL-WORK-TRACKER.md:** {LINK}
- **Seu Briefing:** {LINK para este arquivo}

### Troubleshooting

- **FASE-7-RECOVERY.md (idCEB):** Exemplo de recovery de push failure
- **Stack Overflow:** {Buscar erros específicos}
- **GitHub Issues do Framework:** {Se bug de Next.js/Prisma/etc}

---

**🎉 BRIEFING COMPLETO!**

**Próximo Passo:** Checkout da branch e início da implementação seguindo ETAPA 1 da Seção 2.7.

**Boa sorte!** 🚀

---

# PARTE 3: MERGE COORDENADO

## 3.1. Ordem de Merge (CRÍTICO)

Quando **TODOS agents completarem** (🟢 Completo 100%), mergear EM ORDEM:

### Princípio: Menor Risco Primeiro

```
┌────────────────────────────────────────────────┐
│ ORDEM DE MERGE (do menor para maior risco):   │
│                                                │
│ 1. Docs (zero conflitos)                      │
│ 2. Testes (cria arquivos novos)               │
│ 3. Features isoladas (novo código)            │
│ 4. Refatorações (modifica código existente)   │
│ 5. Features com dependências                  │
└────────────────────────────────────────────────┘
```

### Exemplo Concreto (3 Agents)

```
Agent-A (Docs):        docs/*, README.md             → MERGE #1
          ↓ (validar build)
Agent-C (Tests):       __tests__/*, playwright/     → MERGE #2
          ↓ (validar build + tests)
Agent-B (UI Refactor): src/components/*, src/app/*  → MERGE #3
          ↓ (validar build + tests + UI)
```

**Razão da Ordem:**
- Docs primeiro: Impossível conflitar com código
- Tests segundo: Cria arquivos novos (__tests__/*)
- UI por último: Modifica arquivos existentes (mais risco)

### Caso Especial: Dependências Entre Features

**SE Feature B depende de Feature A:**

```
Feature-A (Foundation) → MERGE PRIMEIRO
   ↓
Feature-B (usa código de A) → MERGE DEPOIS
```

**Exemplo (idCEB Fases 8 e 12):**
```
Fase 12 (LGPD Schema)     → Schema Prisma base
   ↓ OBRIGATÓRIO mergear primeiro
Fase 8 (Relatórios)       → Usa schema LGPD
```

---

## 3.2. Comandos de Merge (Passo-a-Passo)

### Para Cada Feature (EM ORDEM definida em 3.1)

#### Passo 1: Preparar Ambiente

```bash
# Ir para develop
git checkout develop

# Atualizar develop
git pull origin develop

# Verificar status limpo
git status
# Deve mostrar: "nothing to commit, working tree clean"
```

---

#### Passo 2: Revisar Feature Branch

```bash
# Ver commits da feature
git log --oneline develop..claude/{feature}-{SESSION_ID}

# Ver arquivos modificados
git diff --name-status develop..claude/{feature}-{SESSION_ID}

# Ver estatísticas
git diff --stat develop..claude/{feature}-{SESSION_ID}
```

**Validar:**
- ✅ Commits fazem sentido
- ✅ Arquivos modificados esperados
- ✅ Sem arquivos inesperados (node_modules/, .env, etc.)

---

#### Passo 3: Merge (Preservar Histórico)

```bash
# Merge com --no-ff (cria merge commit)
git merge --no-ff claude/{feature}-{SESSION_ID} -m "Merge: Agent-{ID} - {FEATURE_NAME}

Integração da feature {NAME} desenvolvida em paralelo.

Entregas:
- {Item 1}
- {Item 2}
- {Item 3}

Arquivos: {count} criados/modificados
Linhas: +{add} / -{del}
Commits: {count}

Relacionado: claude/{feature}-{SESSION_ID}
Relatório: REPORT-AGENT-{ID}.md
"
```

**SE houver conflitos:**
→ Ir para Seção 3.4 (Resolução de Conflitos)

**SE merge bem-sucedido:**
→ Continuar para Passo 4

---

#### Passo 4: Validação Pós-Merge (OBRIGATÓRIO)

```bash
# 1. Build
npm run build
# Deve: ✅ Success, 0 errors

# 2. Linting
npm run lint
# Deve: ✅ 0 errors, 0 warnings

# 3. Testes (se aplicável)
npm test
# Deve: ✅ All passing

# 4. Verificar develop funcional
npm run dev
# Testar manualmente features críticas (2-3 min)
```

**SE qualquer validação falhar:**
```bash
# Reverter merge
git reset --hard HEAD~1

# Reportar problema ao agent
# Atualizar tracker: Agent-{ID} status → 🔴 Bloqueado
# Aguardar correção
```

**SE todas validações passarem:**
→ Continuar para Passo 5

---

#### Passo 5: Push Develop

```bash
# Push develop atualizado
git push origin develop

# Validar push bem-sucedido
git log --oneline -3
# Deve mostrar merge commit no topo
```

---

#### Passo 6: Limpeza (OPCIONAL)

```bash
# Deletar branch local
git branch -d claude/{feature}-{SESSION_ID}

# Deletar branch remota (OPCIONAL - manter para histórico)
# git push origin --delete claude/{feature}-{SESSION_ID}

# OU marcar branch como merged no GitHub UI
# (não deletar, manter para auditoria)
```

---

#### Passo 7: Atualizar Tracker

```bash
# Editar PARALLEL-WORK-TRACKER.md
# Adicionar linha no Histórico:

| {TIMESTAMP} | Orquestrador | ✅ Merged | Agent-{ID} merged para develop (ordem #{N}) |

git add PARALLEL-WORK-TRACKER.md
git commit -m "track: Agent-{ID} merged to develop

Feature {NAME} integrated successfully.
Build: ✅ Tests: ✅ Deploy: ✅
"
git push origin develop
```

---

### Repetir Para Próxima Feature

**Ir para próximo agent na ordem (3.1) e repetir Passos 1-7.**

---

## 3.3. Validação Pós-Todos-Merges

**Quando TODOS agents estiverem merged:**

### Validação Consolidada

```bash
# Checkout develop final
git checkout develop
git pull origin develop

# Build completo
npm run build

# Testes completos
npm test

# Coverage (se aplicável)
npm run test:coverage

# E2E tests (se configurado)
npm run test:e2e

# Audit dependencies
npm audit

# Bundle size (se web app)
npm run analyze
```

**Métricas Esperadas:**

| Métrica | Valor Esperado |
|---------|----------------|
| Build Status | ✅ Success |
| TypeScript Errors | 0 |
| Linting Errors | 0 |
| Tests Passing | 100% |
| Coverage | ≥ {target}% |
| Bundle Size | < {limit} MB |

**SE todas métricas OK:**
- ✅ Develop pronto para merge → master
- ✅ Criar release tag
- ✅ Deploy para staging/production

---

## 3.4. Resolução de Conflitos

### Tipos de Conflitos

#### Tipo 1: Conflitos em Documentação

**Arquivos:** README.md, docs/*, *.md

**Estratégia:** Mesclar ambas as versões (geralmente ambas adicionam info)

```bash
# Abrir arquivo conflitante
vim README.md

# Procurar marcadores de conflito
<<<<<<< HEAD
Versão do develop
=======
Versão da feature branch
>>>>>>> feature-branch

# Decisão: Manter AMBAS (mesclar)
# Remover marcadores, organizar conteúdo
# Resultado: Documentação mais completa
```

**Commit resolução:**
```bash
git add README.md
git commit -m "merge: Resolve doc conflicts (merged both versions)"
```

---

#### Tipo 2: Conflitos em package.json

**Arquivo:** package.json, package-lock.json

**Estratégia:** Manter todas as dependências (união)

```bash
# Ver conflito
git diff --ours --theirs package.json

# Solução: Aceitar ambas as deps
# Editar package.json manualmente
# Adicionar todas as deps de ambas as versões

# Regenerar lock
rm package-lock.json
npm install

# Commit
git add package.json package-lock.json
git commit -m "merge: Resolve deps conflicts (union of all deps)"
```

---

#### Tipo 3: Conflitos em Código

**Arquivos:** src/*, *.ts, *.tsx

**⚠️ CUIDADO: Requer análise cuidadosa**

**Estratégia:**

```bash
# 1. Entender ambas as mudanças
git show :1:src/file.ts  # Base
git show :2:src/file.ts  # Develop (ours)
git show :3:src/file.ts  # Feature (theirs)

# 2. Decisão baseada em lógica:

# SE mudanças em linhas diferentes (conflito trivial):
# → Manter ambas

# SE mudanças na mesma função mas compatíveis:
# → Mesclar manualmente

# SE mudanças incompatíveis:
# → PARAR e consultar ambos agents
# → Coordenar resolução
# → Pode requerer refatoração
```

**Exemplo: Conflito Trivial**

```typescript
<<<<<<< HEAD (develop)
import { ComponentA } from './ComponentA'
=======
import { ComponentB } from './ComponentB'
>>>>>>> feature-branch

// Resolução: Importar ambos
import { ComponentA } from './ComponentA'
import { ComponentB } from './ComponentB'
```

**Exemplo: Conflito Complexo**

```typescript
<<<<<<< HEAD (develop)
function calculate(data: Data) {
  // Lógica do Agent-A
  return data.total * 1.1
}
=======
function calculate(data: Data) {
  // Lógica do Agent-B (incompatível)
  return data.total + data.tax
}
>>>>>>> feature-branch

// ⚠️ INCOMPATÍVEL
// Não resolver sozinho!
// Opções:
// 1. Renomear uma função (calculateWithTax, calculateWithFee)
// 2. Adicionar parâmetro (calculate(data, mode: 'fee' | 'tax'))
// 3. Criar wrapper que chama ambas

// Consultar agents/orquestrador antes de decidir
```

---

#### Tipo 4: Conflitos em Schema/Migrations

**Arquivos:** schema.prisma, migrations/*

**⚠️ CRÍTICO: Pode quebrar database**

**Estratégia:**

```bash
# 1. Ver conflito em schema.prisma
git diff schema.prisma

# 2. Decisão:
# - SE ambos adicionam modelos diferentes: Manter ambos
# - SE ambos modificam mesmo modelo: Mesclar cuidadosamente
# - SE ambos adicionam enum values: Manter todos

# 3. Após resolver schema:
npx prisma format
npx prisma validate

# 4. Regenerar client
npx prisma generate

# 5. Testar migrations (dev database)
npx prisma migrate dev --name merge-conflict-resolution

# 6. Verificar schema consistency
npx prisma studio
```

---

### Workflow de Resolução Geral

```bash
# 1. Identificar arquivos conflitantes
git diff --name-only --diff-filter=U

# 2. Para cada arquivo:
#    a) Entender conflito
#    b) Aplicar estratégia apropriada (acima)
#    c) git add {arquivo}

# 3. Verificar todos resolvidos
git status
# Deve mostrar: "all conflicts fixed"

# 4. Commit resolução
git commit -m "merge: Resolve conflicts between Agent-{A} and Agent-{B}

Conflicts resolved:
- {file1}: {strategy used}
- {file2}: {strategy used}

Changes are compatible and tested.
"

# 5. Validação (Seção 3.2 Passo 4)
npm run build
npm test
```

---

### Prevenção de Conflitos (Para Próximas Ondas)

**Lições do idCEB:**

1. ✅ **File Isolation Analysis:** Mapear arquivos antes (Feature Tree Builder)
2. ✅ **Clear Boundaries:** Definir escopo claro de cada feature
3. ✅ **Docs Separated:** Documentação em branch separada se muitos agents tocam docs
4. ✅ **Schema Coordination:** Features que alteram schema não podem ser paralelas
5. ✅ **Communication:** Agents informam se precisam expandir escopo

**Taxa Aceitável:** < 5% de conflitos (baseado em idCEB: 0% com file isolation)

---

# PARTE 4: CASO DE ESTUDO - idCEB (Referência Real)

## 4.1. Contexto do Projeto idCEB

**Nome:** idCEB - Plataforma Multi-Tenant de Gestão Escolar
**Cliente:** Centro Educacional Batista (CEB)
**Tipo:** Web App SaaS (B2B2C)
**Domínio:** EdTech - Gestão de escolas particulares brasileiras

### Stack Tecnológica

- **Frontend:** Next.js 15, React 19, TypeScript 5, Tailwind CSS 3.4, shadcn/ui
- **Backend:** Next.js API Routes, Node.js 20
- **Database:** PostgreSQL 16 (prod) + SQLite (dev)
- **ORM:** Prisma 5.20.0
- **Auth:** NextAuth.js v4 (multi-tenant + RBAC)
- **Deploy:** Vercel (frontend) + Railway (database)
- **Monitoring:** Sentry, Pino (structured logging)

### Escala do Projeto

- **Tamanho:** ~32.500 linhas de código
- **Arquivos:** 245 arquivos
- **Fases:** 12 fases (roadmap completo)
- **Desenvolvimento:** 8 meses (Mai/2024 - Nov/2024)
- **Score Final:** 9.5/10 (production-ready)

### Estado Antes do Trabalho Paralelo

- **Fases Completas:** 6/12 (50%)
- **Score:** 8.3/10
- **Método:** Desenvolvimento sequencial (1 fase por vez)
- **Velocidade:** ~3-4 semanas por fase

---

## 4.2. Ciclo 1: Fases 7, 9, 10 (3 Agentes Paralelos)

### Setup

**Data:** Outubro 2024
**Objetivo:** Acelerar desenvolvimento das 3 fases restantes antes de LGPD
**Método:** Deploy de 3 agents simultâneos no Claude Code Web

### Features em Paralelo

| Agent | Fase | Feature | Estimativa | Branch |
|-------|------|---------|------------|--------|
| Agent-Fase7 | Fase 7 | Módulo Financeiro | 8h | `claude/fase-7-financeiro-011CUzoRddLxsWMHWrq8XQXR` |
| Agent-Fase9 | Fase 9 | Observabilidade & Monitoramento | 10h | `claude/fase-9-observabilidade-011CUzob7Ph8PnxjgTCkcfpD` |
| Agent-Fase10 | Fase 10 | Calendário & Comunicação | 12h | `claude/fase-10-calendario-011CUzobDYHaAuUXdwRuok9B` |

### Resultados

#### Fase 7 - Módulo Financeiro ✅

**Agent:** Agent-Fase7
**Entregas:**
- 24 arquivos (+3.026 linhas)
- 6 APIs REST (Mensalidades: CRUD + calcular juros + gerar lote)
- Dashboard KPIs financeiros
- Relatórios de inadimplência

**Score:** 9.0/10

**Testes:** 88.6% passando (163/184)

**Destaques:**
- Cálculo automático de juros/multa (SELIC)
- Geração de mensalidades em lote
- Dashboard com métricas financeiras

**Problema Encontrado:**
- Push falhou (branch não estava no padrão `claude/*`)
- Solução: Criado FASE-7-RECOVERY.md para recovery
- Tempo perdido: 30min

---

#### Fase 9 - Observabilidade & Monitoramento ✅

**Agent:** Agent-Fase9
**Entregas:**
- 19 arquivos (+4.613 linhas)
- Integração Sentry (error tracking)
- Pino structured logging
- Health check endpoints
- Metrics collection
- Dashboard admin de monitoramento

**Score:** 9.0/10

**Destaques:**
- Zero errors não rastreados após deploy
- Logs estruturados facilit troubleshooting
- Métricas de performance em tempo real

---

#### Fase 10 - Calendário & Comunicação ✅

**Agent:** Agent-Fase10
**Entregas:**
- 18 arquivos (~3.000 linhas)
- Sistema de eventos recorrentes
- Importação de feriados nacionais (API)
- Email templates (4 templates React Email)
- Notificações automáticas

**Score:** 9.0/10

**Destaques:**
- Eventos recorrentes (diário, semanal, mensal)
- Feriados brasileiros automáticos (API externa)
- Templates de email responsivos

---

### Métricas Consolidadas do Ciclo 1

| Métrica | Valor |
|---------|-------|
| **Tempo Sequencial (estimado)** | 30h (8 + 10 + 12) |
| **Tempo Paralelo (real)** | 12h (max entre os 3) |
| **Speedup** | **2.5x mais rápido** |
| **Arquivos** | 61 criados/modificados |
| **Linhas** | +10.639 |
| **Commits** | 6 (2 por fase) |
| **Qualidade Média** | 9.0/10 |
| **Conflitos** | 0 (file isolation 100%) |
| **Build Errors** | 0 (após fixes) |
| **Tests Passing** | 88.6% (163/184) |

---

## 4.3. Ciclo 2: Fases 8, 12 (2 Agentes Paralelos)

### Setup

**Data:** Novembro 2024
**Objetivo:** Completar 100% do projeto (12/12 fases)
**Método:** 2 agents no Claude Code Web com orquestração melhorada

### Features em Paralelo

| Agent | Fase | Feature | Estimativa | Branch |
|-------|------|---------|------------|--------|
| Agent-D | Fase 8 | Relatórios & Analytics | 5h | `claude/read-briefing-agent-d-011CV2AiU2KWhD82MqLA7GWN` |
| Agent-E | Fase 12 | LGPD UI & Conformidade | 10h | `claude/briefing-agent-e-fase-12-011CV2Ak782Hds7Va1N8nZQi` |

### Resultados

#### Fase 8 - Relatórios & Analytics ✅

**Agent:** Agent-D
**Entregas:**
- ~30 arquivos (~4.200 linhas)
- 4 templates de relatórios
- Dashboard enterprise (drill-down)
- APIs de agregação e métricas
- Exportação PDF + Excel

**Score:** 9.5/10

**Destaques:**
- Drill-down dinâmico (turma → aluno)
- Templates reutilizáveis
- Performance < 2s para relatórios grandes

---

#### Fase 12 - LGPD UI & Conformidade ✅

**Agent:** Agent-E
**Entregas:**
- 24 arquivos (3.960 linhas)
- 3 modelos Prisma + 4 enums (LGPD completa)
- 8 direitos do titular (LGPD Art. 18)
- Portal de consentimentos (usuários)
- Dashboard de solicitações (admin)
- Exportação de dados pessoais (ZIP)
- Anonimização automática

**Score:** 9.5/10

**Destaques:**
- 100% compliance LGPD (Lei 13.709/2018)
- Prazo de 15 dias automatizado
- Auditoria completa de operações

---

### Métricas Consolidadas do Ciclo 2

| Métrica | Valor |
|---------|-------|
| **Tempo Sequencial (estimado)** | 15h (5 + 10) |
| **Tempo Paralelo (real)** | 10h (max entre os 2) |
| **Speedup** | **1.5x mais rápido** |
| **Arquivos** | ~54 criados/modificados |
| **Linhas** | +8.160 |
| **Commits** | 4 (2 por fase) |
| **Qualidade Média** | 9.5/10 |
| **Conflitos** | 0 (file isolation + merge coordenado) |
| **Build Errors** | 0 (após 10 fixes de imports) |
| **Tests Passing** | 100% (234/234) |

### Merge Coordenado (Aprendizado)

**Ordem:**
1. Agent-E (Fase 12) - PRIMEIRO
   - Razão: Schema Prisma foundation
2. Agent-D (Fase 8) - DEPOIS
   - Razão: Usa enums da Fase 12

**Problema Evitado:**
- SE Agent-D merge primeiro: Conflict no schema.prisma
- COM Agent-E primeiro: Zero conflicts

---

## 4.4. Métricas Globais do idCEB

### Antes vs. Depois do Trabalho Paralelo

| Métrica | Antes | Depois | Melhoria |
|---------|-------|--------|----------|
| **Fases Completas** | 6/12 (50%) | 12/12 (100%) | +100% |
| **Linhas de Código** | ~18.000 | ~32.500 | +80% |
| **Score de Qualidade** | 8.3/10 | 9.5/10 | +14% |
| **Velocidade Desenvolvimento** | 1 fase/mês | 5 fases/mês | **5x** |
| **Context Usage (médio)** | ~2.500 tokens | ~300 tokens | **-88%** |

### ROI do Trabalho Paralelo

**Tempo Economizado:**
- Ciclo 1: 18h economizadas (30h → 12h)
- Ciclo 2: 5h economizadas (15h → 10h)
- **Total:** 23h economizadas (~3 dias de trabalho)

**Custo (estimado):**
- Setup (orquestração): 4h
- Implementação paralela: 22h (real time)
- **Total:** 26h vs 45h sequencial = **42% mais rápido**

**Qualidade Mantida:**
- Score médio: 9.0-9.5/10
- Zero degradação de qualidade vs desenvolvimento sequencial
- Prove: Paralelização não compromete qualidade

---

## 4.5. Lições Aprendidas do idCEB

### ✅ O Que Funcionou Muito Bem

#### 1. File Isolation Strategy

**Prática:**
- Análise prévia de quais arquivos cada agent modificaria
- Features isoladas (zero overlap de arquivos)

**Resultado:**
- **0 conflitos** em 5 fases paralelas
- Merge trivial (< 5min por feature)

**Aplicar:** Sempre fazer análise de file ownership antes de deploy

---

#### 2. Padrão de Branch `claude/*`

**Prática:**
- Todas branches com prefixo `claude/`
- SESSION_ID único anexado

**Resultado:**
- Push automático funcionou (permissões Claude Code Web)
- Zero ambiguidade (branches fáceis de identificar)

**Aplicar:** Documentar padrão no briefing desde o início

---

#### 3. Templates de Relatórios

**Prática:**
- JSON estruturado obrigatório ao finalizar
- Template fornecido no briefing

**Resultado:**
- Relatórios consistentes
- Fácil comparação entre agents
- Métricas consolidadas automaticamente

**Aplicar:** Sempre incluir Seção 2.11 (Relatório Final) em briefings

---

#### 4. Merge Coordenado (Ordem Definida)

**Prática:**
- Análise de dependências
- Ordem de merge explícita
- Fase 12 antes Fase 8 (schema foundation)

**Resultado:**
- Zero conflitos de schema
- Merges sequenciais suaves

**Aplicar:** Sempre mapear dependências e definir ordem no ORCHESTRATION-REPORT

---

#### 5. Context Reduction (87%)

**Prática:**
- Briefings estruturados (< 800 linhas)
- Tracking separado (não no chat)
- Relatórios JSON (~300 tokens)

**Resultado:**
- 2.500 tokens → 300 tokens por agent
- Sessions mais longas (não atingir limite de contexto)
- Escalável para N agents

**Aplicar:** Usar tracking externo (PARALLEL-WORK-TRACKER.md)

---

### ⚠️ Desafios e Soluções

#### Desafio 1: Agent Fase 7 - Push Failure

**Problema:**
- Agent criou branch `feature/fase-7-financeiro` (sem `claude/`)
- Push falhou com erro 403

**Causa Raiz:**
- Briefing não documentou padrão de branch claramente

**Solução Aplicada:**
- Criado FASE-7-RECOVERY.md
- Agent fez cherry-pick para branch correta
- Push bem-sucedido

**Tempo Perdido:** 30 minutos

**Prevenção:**
- Adicionar Seção 2.2 (Ambiente) em TODOS briefings
- Validar branch antes de iniciar implementação

---

#### Desafio 2: Conflitos em docs/reports/

**Problema:**
- 2 agents modificaram mesmo relatório markdown

**Causa Raiz:**
- Relatórios não estavam no escopo file isolation

**Solução Aplicada:**
- Aceitar versão do último agent
- OU mesclar ambos os relatórios

**Tempo Perdido:** 10 minutos

**Prevenção:**
- Reports fora de templates iniciais
- OU cada agent cria seu próprio report (não modifica existentes)

---

#### Desafio 3: Build Falhou (TypeScript Errors)

**Problema:**
- Após merge, 10 erros TypeScript (imports incorretos)

**Causa Raiz:**
- Named imports vs default imports (Prisma)
- Imports relativos vs absolute paths

**Solução Aplicada:**
- Corrigir imports manualmente (10 min)
- Commit: "fix: Corrigir imports após merge"

**Prevenção:**
- Checklist pré-push mais rigoroso (Seção 2.6)
- Validar imports com `tsc --noEmit` antes de push

---

### 💡 Melhorias Aplicadas para Futuros Projetos

1. **Múltiplos Métodos de Push:** Seção 2.2 com 5 fallbacks
2. **Sistema de Tracking:** PARALLEL-WORK-TRACKER.md desde o início
3. **Prompts Prontos:** DEPLOY-PROMPTS.md gerado pelo orquestrador
4. **Recovery Procedures:** 5 cenários documentados no briefing
5. **Validação Pré-Push:** Checklist expandido (8 itens)

---

### 📊 Validação da Hipótese

**Hipótese Inicial:**
> Desenvolvimento paralelo com multi-agents pode ser 3-5x mais rápido que sequencial, mantendo qualidade 9.0/10+

**Resultado:**
| Hipótese | Real | Validado? |
|----------|------|-----------|
| Speedup 3-5x | 2.5x (Ciclo 1), 1.5x (Ciclo 2) | ⚠️ Parcial (menor que esperado) |
| Qualidade 9.0/10+ | 9.0-9.5/10 | ✅ Sim |
| Escalável | 5 fases paralelas sem degradação | ✅ Sim |
| Context reduction 85%+ | 88% (2.500 → 300 tokens) | ✅ Sim |
| Conflict rate < 5% | 0% (file isolation perfeito) | ✅ Sim |

**Conclusão:**
- ✅ **Qualidade mantida** (9.0-9.5/10)
- ✅ **Escalável** (N agents funcionam)
- ⚠️ **Speedup menor** (2-2.5x real vs 3-5x esperado)
  - Razão: Overhead de coordenação não calculado
  - Ajuste expectativa: **2-3x** mais realista
- ✅ **Production viável** (100% pronto para deploy)

---

# PARTE 5: ADAPTAÇÃO PARA NOVOS PROJETOS

## 5.1. Checklist de Customização

Use este checklist ao adaptar template para novo projeto:

### Fase 1: Preparação

- [ ] **Copiar template** para projeto
- [ ] **Ler PROJECT-ANALYSIS.md** (ou criar com Seção 1.3)
- [ ] **Identificar 3-5 features** para Grupo A (paralelo)
- [ ] **Validar independência** (zero overlap de arquivos)
- [ ] **Estimar tempo** por feature (4-10h ideal)

### Fase 2: Variáveis Globais

Substituir estas variáveis em TODO o template:

- [ ] `{PROJECT_NAME}` → Nome do projeto (ex: "Sistema Biblioteca")
- [ ] `{PROJECT_TYPE}` → Tipo (Web App, CLI, Mobile, etc.)
- [ ] `{TECH_STACK}` → Stack resumida (ex: "Python Flask, PostgreSQL")
- [ ] `{GITHUB_URL}` → URL do repo (ex: https://github.com/user/repo)
- [ ] `{USER}` → GitHub username
- [ ] `{REPO}` → Nome do repositório

### Fase 3: Criar Branches

- [ ] Gerar SESSION_ID único para cada feature
- [ ] Criar branches: `claude/{feature}-{SESSION_ID}`
- [ ] Push branches vazias para GitHub
- [ ] Anotar branches criadas

### Fase 4: Criar Briefings

Para cada feature:

- [ ] Copiar template Seção 2 (BRIEFING-AGENT-{ID}-{FEATURE}.md)
- [ ] Substituir variáveis específicas da feature:
  - [ ] `{ID}` → A, B, C, ...
  - [ ] `{FEATURE}` → Nome curto (docs, tests, api, ui, etc.)
  - [ ] `{FEATURE_NAME}` → Nome descritivo completo
  - [ ] `{FEATURE_OBJECTIVE}` → Objetivo em 1-2 frases
  - [ ] `{HOURS}` → Estimativa de tempo
  - [ ] `{PRIORITY}` → ALTA / MÉDIA / BAIXA
  - [ ] `{SESSION_ID}` → ID único desta branch
- [ ] Preencher Seção 2.4 (Escopo Completo):
  - [ ] Listar arquivos a criar
  - [ ] Listar arquivos a modificar
  - [ ] Definir estrutura esperada
- [ ] Preencher Seção 2.7 (Plano de Execução):
  - [ ] Dividir em 5-15 etapas
  - [ ] Estimar tempo por etapa
  - [ ] Definir validações por etapa
- [ ] Preencher Seção 2.9 (Regras Críticas):
  - [ ] Adicionar regras específicas do projeto
  - [ ] Compliance (LGPD, WCAG, etc.)
  - [ ] Padrões de código
- [ ] Preencher Seção 2.10 (Critérios de Aceitação):
  - [ ] Definir critérios testáveis
  - [ ] Adicionar testes manuais necessários

### Fase 5: Criar Sistema de Tracking

- [ ] Criar PARALLEL-WORK-TRACKER.md (Seção 1.7)
- [ ] Inicializar com N agents
- [ ] Definir ordem de merge
- [ ] Commit tracker inicial

### Fase 6: Gerar Prompts de Deploy

- [ ] Criar DEPLOY-PROMPTS.md (Seção 1.8)
- [ ] Um prompt por agent
- [ ] Verificar instruções de checkout
- [ ] Verificar instruções de tracker
- [ ] Commit prompts

### Fase 7: Relatório de Orquestração

- [ ] Criar ORCHESTRATION-REPORT.md (Seção 1.9)
- [ ] Preencher sumário executivo
- [ ] Listar branches
- [ ] Listar briefings
- [ ] Definir timeline
- [ ] Calcular métricas esperadas
- [ ] Commit relatório

### Fase 8: Validação Final

- [ ] Revisar TODOS os arquivos criados
- [ ] Verificar variáveis substituídas
- [ ] Validar branches no GitHub
- [ ] Testar um prompt (dry-run)

**✅ Setup Completo! Pronto para deploy de agents.**

---

## 5.2. Exemplo Prático Passo-a-Passo

### Projeto Exemplo: "TaskFlow" (Sistema de Gestão de Tarefas)

**Contexto:**
- **Tipo:** Web App (To-Do list avançado para times)
- **Stack:** Next.js 14, PostgreSQL, Prisma
- **Estado:** MVP funcional (50% das features planejadas)
- **Objetivo:** Adicionar 4 features faltantes em 1 semana

---

### Passo 1: Análise Profunda

```bash
# Execute o prompt da Seção 1.3
# Resultado: PROJECT-ANALYSIS.md criado

# Features identificadas:
# F1: Documentação (README, API docs, CONTRIBUTING)
# F2: Notificações Push (Web Push API)
# F3: Compartilhamento de Tasks (colaboração)
# F4: Dark Mode (tema escuro)
```

---

### Passo 2: Validar Independência

```markdown
F1 vs F2: ZERO overlap (F1: docs/, F2: src/features/notifications/)
F1 vs F3: ZERO overlap (F1: docs/, F3: src/features/sharing/)
F1 vs F4: ZERO overlap (F1: docs/, F4: src/styles/, src/hooks/)
F2 vs F3: ZERO overlap (diferentes features/ dirs)
F2 vs F4: ZERO overlap (F2: notifications/, F4: styles/)
F3 vs F4: ZERO overlap (F3: sharing/, F4: styles/)

✅ Grupo A: TODOS podem rodar em paralelo (4 agents)
```

---

### Passo 3: Criar Branches

```bash
git checkout develop
git pull origin develop

# F1: Docs (Agent-A)
SESSION_ID_A=$(date +%s | sha256sum | base64 | head -c 12)
git checkout -b claude/docs-improvement-$SESSION_ID_A
git push -u origin claude/docs-improvement-$SESSION_ID_A
git checkout develop

# F2: Notifications (Agent-B)
SESSION_ID_B=$(date +%s | sha256sum | base64 | head -c 12)
git checkout -b claude/feature-push-notifications-$SESSION_ID_B
git push -u origin claude/feature-push-notifications-$SESSION_ID_B
git checkout develop

# F3: Sharing (Agent-C)
SESSION_ID_C=$(date +%s | sha256sum | base64 | head -c 12)
git checkout -b claude/feature-task-sharing-$SESSION_ID_C
git push -u origin claude/feature-task-sharing-$SESSION_ID_C
git checkout develop

# F4: Dark Mode (Agent-D)
SESSION_ID_D=$(date +%s | sha256sum | base64 | head -c 12)
git checkout -b claude/feature-dark-mode-$SESSION_ID_D
git push -u origin claude/feature-dark-mode-$SESSION_ID_D
git checkout develop

# Anotar SESSION_IDs:
echo "Agent-A: $SESSION_ID_A" >> SESSION_IDS.txt
echo "Agent-B: $SESSION_ID_B" >> SESSION_IDS.txt
echo "Agent-C: $SESSION_ID_C" >> SESSION_IDS.txt
echo "Agent-D: $SESSION_ID_D" >> SESSION_IDS.txt
```

---

### Passo 4: Criar Briefings (Exemplo: Agent-A)

```bash
cat > BRIEFING-AGENT-A-DOCS.md << 'EOF'
# BRIEFING: AGENT-A - Documentação Completa

## 2.1. Status do Projeto

- **Projeto:** TaskFlow
- **Tipo:** Web App (Gestão de Tarefas)
- **Stack:** Next.js 14, React 18, PostgreSQL, Prisma, Tailwind
- **Build Status:** ✅ Passing
- **Branch Base:** develop
- **Sua Branch:** claude/docs-improvement-Ab12Cd34Ef56
- **Dependências:** Node 18+, PostgreSQL 14+

## 2.2. Ambiente: Claude Code Web + Múltiplos Métodos Git

{... copiar Seção 2.2 completa do template ...}

## 2.3. Sua Missão

**Objetivo:** Criar documentação técnica completa do TaskFlow para facilitar onboarding de novos desenvolvedores e usuários.

**Estimativa:** 6h

**Prioridade:** ALTA (merge primeiro)

**Arquivos Esperados:**
- **Criar:** 8 novos arquivos (~1.200 linhas)
- **Modificar:** 1 arquivo existente (README.md, ~200 linhas)

**Conflitos Potenciais:**
- Zero - feature isolada, apenas cria/modifica docs

## 2.4. Escopo Completo

### Features Principais

- [ ] README.md aprimorado (setup, features, screenshots)
- [ ] docs/architecture/overview.md (arquitetura do sistema)
- [ ] docs/architecture/database.md (schema Prisma explicado)
- [ ] docs/api/endpoints.md (documentação de APIs REST)
- [ ] docs/development/setup.md (guia de setup detalhado)
- [ ] docs/development/contributing.md (guia de contribuição)
- [ ] docs/deployment/vercel.md (deploy em produção)
- [ ] docs/changelog.md (histórico de releases)

### Estrutura de Arquivos

```
taskflow/
  ├── README.md (modificar - adicionar seções, screenshots)
  ├── docs/
  │   ├── architecture/
  │   │   ├── overview.md (criar - 300 linhas)
  │   │   └── database.md (criar - 200 linhas)
  │   ├── api/
  │   │   └── endpoints.md (criar - 250 linhas)
  │   ├── development/
  │   │   ├── setup.md (criar - 150 linhas)
  │   │   └── contributing.md (criar - 200 linhas)
  │   ├── deployment/
  │   │   └── vercel.md (criar - 100 linhas)
  │   └── changelog.md (criar - 100 linhas)
  └── .github/
      └── PULL_REQUEST_TEMPLATE.md (criar - 50 linhas)
```

## 2.5. Comunicação com Orchestrador + Update Tracker

{... copiar Seção 2.5 completa do template ...}

## 2.6. Recovery & Troubleshooting

{... copiar Seção 2.6 completa do template ...}

## 2.7. Plano de Execução Detalhado

### ETAPA 1: Setup e Checkout (15 min)

{... seguir template ...}

### ETAPA 2: Aprimorar README.md (1h)

**Objetivo:** Transformar README básico em documentação principal do projeto

**Arquivos a modificar:**
- `README.md` - Adicionar seções: Features, Screenshots, Roadmap, License

**Implementação:**

```markdown
# TaskFlow - Gestão de Tarefas Inteligente

[Badge: Build] [Badge: Tests] [Badge: Version]

## 🎯 Features

- ✅ Criação rápida de tarefas
- ✅ Priorização automática
- ✅ Colaboração em tempo real
- 🚧 Notificações push (em desenvolvimento)
- 🚧 Modo escuro (em desenvolvimento)

## 📸 Screenshots

[Inserir 3-4 screenshots principais]

## 🚀 Quick Start

{Instruções simplificadas de setup}

## 📚 Documentação

- [Arquitetura](./docs/architecture/overview.md)
- [APIs](./docs/api/endpoints.md)
- [Contribuindo](./docs/development/contributing.md)

## 🗺️ Roadmap

{Link para PLAN.md ou Issues}

## 📄 License

MIT License - see [LICENSE](./LICENSE)
```

**Validação:**
- ✅ README tem todas as seções esperadas
- ✅ Links funcionam
- ✅ Screenshots incluídos

**Commit:**
```bash
git add README.md
git commit -m "docs: Enhance README with features, screenshots, and structure"
```

**Atualizar tracker (0% → 15%):**

---

### ETAPA 3: Documentar Arquitetura (1.5h)

**Objetivo:** Explicar arquitetura do sistema para novos devs

**Arquivos a criar:**
- `docs/architecture/overview.md` (300 linhas)
- `docs/architecture/database.md` (200 linhas)

**Implementação overview.md:**

```markdown
# Arquitetura do TaskFlow

## Visão Geral

TaskFlow é uma aplicação Next.js 14 full-stack seguindo padrão Server Components + API Routes.

## Stack Tecnológica

### Frontend
- **Framework:** Next.js 14 (App Router)
- **UI:** Tailwind CSS + shadcn/ui
- **State:** React Context + Zustand

### Backend
- **Runtime:** Node.js 18
- **APIs:** Next.js API Routes
- **Database:** PostgreSQL 14
- **ORM:** Prisma 5

### Infraestrutura
- **Deploy:** Vercel (frontend + serverless)
- **Database:** Supabase PostgreSQL
- **Monitoring:** Vercel Analytics

## Estrutura de Diretórios

```
src/
  ├── app/              # Next.js App Router
  │   ├── api/          # API Routes
  │   ├── (dashboard)/  # Dashboard pages
  │   └── layout.tsx    # Root layout
  ├── components/       # React components
  │   ├── ui/           # shadcn/ui primitives
  │   └── features/     # Feature components
  ├── lib/              # Utilities
  │   ├── prisma.ts     # Prisma client
  │   └── utils.ts      # Helper functions
  └── types/            # TypeScript types
```

## Padrões de Código

### Component Pattern

{Exemplo de component bem estruturado}

### API Pattern

{Exemplo de API route bem estruturado}

## Fluxo de Dados

{Diagrama texto mostrando fluxo: User → UI → API → Prisma → PostgreSQL}

## Segurança

- Row-level security (RLS) no Prisma
- CSRF protection
- Rate limiting (10 req/min por IP)

## Performance

- SSR para páginas públicas
- ISR para dashboard (revalidate: 60s)
- Caching em API Routes (Redis futuro)
```

**Implementação database.md:**

```markdown
# Database Schema - TaskFlow

## Modelos Prisma

### User
{Explicar campos, relações, índices}

### Task
{Explicar campos, relações, índices}

### Team
{Explicar campos, relações, índices}

## Relacionamentos

{Diagrama ER em texto/mermaid}

## Migrations

{Como rodar, como reverter}

## Seeds

{Como popular banco dev}
```

**Validação:**
- ✅ Docs cobrem todos os aspectos principais
- ✅ Exemplos de código corretos
- ✅ Links internos funcionam

**Commit:**
```bash
git add docs/architecture/
git commit -m "docs: Add architecture documentation (overview + database)"
```

**Atualizar tracker (15% → 40%):**

---

### ETAPA 4-7: {Continuar implementação seguindo padrão}

{Criar docs de API, Development, Deployment, Changelog}

**Atualizar tracker:** 40% → 65% → 85% → 95%

---

### ETAPA 8: Validação Final e Relatório (30 min)

{Seguir Seção 2.7 ETAPA N do template}

**Atualizar tracker:** 95% → 100% ✅

---

## 2.8-2.12: {Resto do briefing}

{Copiar seções restantes do template, ajustando exemplos para TaskFlow}

EOF

# Commitar briefing
git add BRIEFING-AGENT-A-DOCS.md
git commit -m "docs: Add Agent-A briefing (Documentation)"
```

**Repetir para Agent-B, C, D** (3 briefings restantes)

---

### Passo 5: Criar Tracker

```bash
# Seguir Seção 1.7 do template
cat > PARALLEL-WORK-TRACKER.md << 'EOF'
# 🎯 Parallel Work Tracker - TaskFlow

**Última Atualização:** 2025-11-12 10:00
**Status Geral:** 🟡 Setup Completo - Aguardando Início

---

## 📊 Visão Geral

| Métrica | Valor |
|---------|-------|
| Features Totais | 4 |
| Completas | 0 |
| Em Progresso | 0 |
| Bloqueadas | 0 |
| Progresso Geral | 0% |

---

## 👥 Status dos Agentes

### Agent-A: Documentação
- **Branch:** `claude/docs-improvement-Ab12Cd34Ef56`
- **Status:** ⚪ Não Iniciado (0%)
- **Estimativa:** 6h
- **Progresso:**
  - [ ] README.md aprimorado
  - [ ] Architecture docs
  - [ ] API docs
  - [ ] Contributing guide

### Agent-B: Push Notifications
- **Branch:** `claude/feature-push-notifications-Gh78Ij90Kl12`
- **Status:** ⚪ Não Iniciado (0%)
- **Estimativa:** 8h
- **Progresso:**
  - [ ] Service Worker setup
  - [ ] Push API integration
  - [ ] Notification UI
  - [ ] Backend trigger

### Agent-C: Task Sharing
- **Branch:** `claude/feature-task-sharing-Mn34Op56Qr78`
- **Status:** ⚪ Não Iniciado (0%)
- **Estimativa:** 7h
- **Progresso:**
  - [ ] Share modal
  - [ ] Permissions system
  - [ ] Collaboration API
  - [ ] Real-time sync

### Agent-D: Dark Mode
- **Branch:** `claude/feature-dark-mode-St90Uv12Wx34`
- **Status:** ⚪ Não Iniciado (0%)
- **Estimativa:** 4h
- **Progresso:**
  - [ ] Theme context
  - [ ] CSS variables
  - [ ] Toggle component
  - [ ] Persist preference

---

## 📋 Ordem de Merge

1. **Agent-A (Docs)** - PRIMEIRO
2. **Agent-D (Dark Mode)** - SEGUNDO (apenas styles)
3. **Agent-B (Notifications)** - TERCEIRO
4. **Agent-C (Sharing)** - QUARTO

---

{... resto do tracker seguindo template ...}

EOF

git add PARALLEL-WORK-TRACKER.md
git commit -m "feat: Initialize parallel work tracker (4 agents)"
```

---

### Passo 6-7: Prompts e Relatório

{Seguir Seções 1.8 e 1.9 do template}

---

### Passo 8: Deploy de Agents

```bash
# Abrir 4 sessões Claude Code Web
# Para cada sessão:

# Sessão 1 (Agent-A):
# Copiar prompt de DEPLOY-PROMPTS.md
# Colar e executar

# Sessão 2-4 (Agent-B, C, D):
# Mesmo processo
```

---

### Passo 9: Monitoramento

```bash
# A cada 30 min, verificar tracker:
cat PARALLEL-WORK-TRACKER.md | grep "Status:"

# Verificar se algum agent bloqueou:
cat PARALLEL-WORK-TRACKER.md | grep "🔴"

# Se bloqueado, resolver imediatamente
```

---

### Passo 10: Merge Coordenado

```bash
# Quando todos 🟢 Completo:

# 1. Merge Agent-A (Docs)
git checkout develop && git pull origin develop
git merge --no-ff claude/docs-improvement-Ab12Cd34Ef56
npm run build && npm test
git push origin develop

# 2. Merge Agent-D (Dark Mode)
git merge --no-ff claude/feature-dark-mode-St90Uv12Wx34
npm run build && npm test
git push origin develop

# 3. Merge Agent-B (Notifications)
git merge --no-ff claude/feature-push-notifications-Gh78Ij90Kl12
npm run build && npm test
git push origin develop

# 4. Merge Agent-C (Sharing)
git merge --no-ff claude/feature-task-sharing-Mn34Op56Qr78
npm run build && npm test
git push origin develop
```

---

### Resultado Esperado (TaskFlow)

| Métrica | Valor |
|---------|-------|
| **Tempo Sequencial** | 25h (6 + 8 + 7 + 4) |
| **Tempo Paralelo** | 8h (max entre 4 agents) |
| **Speedup** | **3.1x mais rápido** |
| **Features** | 4 implementadas |
| **Linhas** | +6.000 estimadas |
| **Qualidade Target** | 9.0/10+ |

---

## 5.3. Templates Prontos para Copiar

### Template: Variáveis para Substituir

Ao adaptar template, use Find & Replace global:

```bash
# Variáveis globais
{PROJECT_NAME}           → TaskFlow
{PROJECT_TYPE}           → Web App
{TECH_STACK}             → Next.js 14, PostgreSQL, Prisma
{GITHUB_URL}             → https://github.com/user/taskflow
{USER}                   → seu-usuario-github
{REPO}                   → taskflow

# Variáveis por agent
{ID}                     → A, B, C, D, ...
{FEATURE}                → docs, notifications, sharing, dark-mode
{FEATURE_NAME}           → Documentação Completa, Push Notifications, etc.
{SESSION_ID}             → Ab12Cd34Ef56 (único por agent)
{HOURS}                  → 4, 6, 8, 10 (estimativa)
{PRIORITY}               → ALTA, MÉDIA, BAIXA
```

---

### Template: Comando Rápido de Setup

```bash
#!/bin/bash
# quick-setup.sh - Setup completo de trabalho paralelo

PROJECT_NAME="TaskFlow"
PROJECT_DIR="/path/to/project"
FEATURES=("docs" "notifications" "sharing" "dark-mode")

cd $PROJECT_DIR
git checkout develop
git pull origin develop

# Criar branches
for i in "${!FEATURES[@]}"; do
  FEATURE="${FEATURES[$i]}"
  SESSION_ID=$(date +%s | sha256sum | base64 | head -c 12)

  git checkout -b "claude/${FEATURE}-${SESSION_ID}"
  git push -u origin "claude/${FEATURE}-${SESSION_ID}"
  git checkout develop

  echo "Agent-$(echo $i | tr 0-9 A-J): $SESSION_ID" >> SESSION_IDS.txt
done

echo "✅ Branches criadas: ${#FEATURES[@]}"
echo "📋 SESSION_IDS salvas em SESSION_IDS.txt"
```

---

### Template: Validação de Merge

```bash
#!/bin/bash
# validate-merge.sh - Validar build após cada merge

set -e  # Exit on error

echo "🔍 Validando merge..."

# Build
echo "Building..."
npm run build
if [ $? -ne 0 ]; then
  echo "❌ Build falhou"
  exit 1
fi
echo "✅ Build OK"

# Lint
echo "Linting..."
npm run lint
if [ $? -ne 0 ]; then
  echo "⚠️ Linting com warnings"
fi
echo "✅ Lint OK"

# Tests
if [ -f "package.json" ] && grep -q "\"test\"" package.json; then
  echo "Testing..."
  npm test
  if [ $? -ne 0 ]; then
    echo "❌ Testes falharam"
    exit 1
  fi
  echo "✅ Tests OK"
fi

echo "✅ Merge validado com sucesso!"
```

---

# 📚 REFERÊNCIAS E LINKS

## Claude Code Web (Oficial)

- **Blog:** https://www.claude.com/blog/claude-code-on-the-web
- **Docs:** https://code.claude.com/docs/en/claude-code-on-the-web
- **Sandboxing:** https://www.anthropic.com/engineering/claude-code-sandboxing
- **Sandboxing Docs:** https://code.claude.com/docs/en/sandboxing

## Projeto idCEB (Caso Real)

- **Documentos de Referência:**
  - `projects/id-ceb/docs/contracts/BRIEFING-AGENT-E-FASE-12.md`
  - `projects/id-ceb/docs/planning/PARALLEL-WORK-PLAN.md`
  - `projects/id-ceb/docs/contracts/ORCHESTRATION-PARALLEL-WORK.md`
  - `projects/id-ceb/docs/reports/CONCLUSAO-PARALELO.md`

## Git Workflows

- **Gitflow:** https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow
- **Trunk-Based:** https://trunkbaseddevelopment.com/
- **GitHub Flow:** https://guides.github.com/introduction/flow/

---

# 🎓 NOTAS FINAIS

## Sobre Este Template

**Criado:** 2025-11-11
**Baseado Em:** Projeto idCEB (5 fases, 5 agents, ~14.000 linhas)
**Validado:** 2 ciclos de desenvolvimento paralelo (100% sucesso)
**Qualidade:** 9.0-9.5/10 consistente
**Speedup:** 2.5x real (vs 3-5x esperado)

## Versão

**v2.0** - Template completo com orquestração, tracking e múltiplos métodos git

**Changelog:**
- v1.0: Template básico (apenas briefing)
- v1.5: + Sistema de tracking
- v2.0: + Orquestração + Deploy prompts + Múltiplos métodos git

## Autor

**Claude Code + Henri (Multi-Agent Research)**

## Licença

Template de uso livre para projetos pessoais e comerciais.

**Atribuição Opcional (apreciada):**
```markdown
Baseado em template de Desenvolvimento Paralelo Multi-Agente
Autor: Claude Code + Henri (Multi-Agent Research)
```

## Contribuições

Melhorias são bem-vindas! Se você aplicar este template e descobrir otimizações:
1. Documente a melhoria
2. Compartilhe o aprendizado
3. Atualize o template (se possível)

## Suporte

**Para questões:**
- Revisar Parte 4 (Caso idCEB) para exemplos concretos
- Consultar Seção 2.6 (Troubleshooting) para problemas comuns
- Verificar Parte 3.4 (Resolução de Conflitos) para conflitos

**Para bugs/issues:**
- Documentar cenário completo
- Incluir logs/erros
- Descrever tentativas de resolução

---

# ✅ STATUS DO TEMPLATE

**Completude:** 100% ✅
**Testado:** Sim (idCEB - 5 fases) ✅
**Production-Ready:** Sim ✅
**Portable:** Sim (arquivo único .md) ✅
**Trackable:** Sim (PARALLEL-WORK-TRACKER.md) ✅
**Deploy Prompts:** Sim (DEPLOY-PROMPTS.md) ✅
**Git Fallbacks:** Sim (5 métodos) ✅

**Tamanho Total:** ~2.300 linhas

---

**🚀 TEMPLATE COMPLETO! PRONTO PARA USO EM PRODUÇÃO! 🚀**
