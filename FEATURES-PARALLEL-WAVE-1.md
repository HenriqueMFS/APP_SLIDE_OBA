# 🚀 Features para Desenvolvimento Paralelo - Onda 1

**Projeto:** APP_SLIDE_OBA
**Data:** 2025-11-12
**Base Branch:** develop (local) / claude/analyze-repository-structure-011CV26eM3noi2SbsiDZJGqW (remote)

---

## 📊 Análise de Independência

### 🟢 Grupo A: Paralelo Completo (3 features simultâneas)

Estas 3 features NÃO compartilham arquivos e podem rodar 100% em paralelo:

---

## Feature 1: Documentação Completa

**ID:** F1-DOCS
**Categoria:** docs
**Prioridade:** 🔴 CRÍTICA (merge primeiro - zero conflitos)
**Estimativa:** 4-6h

### Escopo
- Atualizar README.md com descrição completa
- Adicionar instruções de instalação e uso
- Documentar formato esperado dos arquivos de entrada
- Criar exemplos de uso
- Adicionar docstrings nas funções principais de APP.py

### Arquivos Modificados
```
CRIAR:
- docs/USAGE.md (guia de uso detalhado)
- docs/INPUT_FORMAT.md (formato dos arquivos DOCX/PPTX)
- docs/EXAMPLES.md (exemplos práticos)

MODIFICAR:
- README.md (expandir significativamente)
- APP.py (adicionar docstrings nas funções)
```

### Arquivos NÃO Tocados
- requirements.txt
- .gitignore
- Imagens
- Estrutura de código (apenas docstrings)

### Conflitos Esperados
**ZERO** - Apenas documentação

### Critérios de Aceitação
- [ ] README.md >= 100 linhas com seções completas
- [ ] docs/USAGE.md criado com exemplos passo-a-passo
- [ ] docs/INPUT_FORMAT.md com especificação de colunas
- [ ] Todas as funções principais têm docstrings (formatar_texto, normalizar_texto_base, extrair_dados, duplicate_slide_with_media, replace_placeholders_in_shape, gerar_apresentacao)
- [ ] Pelo menos 2 exemplos práticos documentados

---

## Feature 2: Setup e Infraestrutura

**ID:** F2-SETUP
**Categoria:** infra
**Prioridade:** 🔴 CRÍTICA
**Estimativa:** 3-4h

### Escopo
- Criar .gitignore completo
- Remover __pycache__/ do versionamento
- Fixar versões em requirements.txt
- Criar .env.example
- Otimizar imagens (logo_jornada.png e tiapamela.gif)

### Arquivos Modificados
```
CRIAR:
- .gitignore (completo para Python/Streamlit)
- .env.example (template de variáveis de ambiente)

MODIFICAR:
- requirements.txt (adicionar versões específicas)
- logo_jornada.png (otimizar: 6.2 MB → ~500 KB)
- tiapamela.gif (otimizar: 3.4 MB → ~1 MB)

REMOVER DO GIT:
- __pycache__/ (via git rm --cached -r)
```

### Arquivos NÃO Tocados
- APP.py (código permanece intacto)
- README.md
- docs/

### Conflitos Esperados
**ZERO** - Arquivos de configuração independentes

### Critérios de Aceitação
- [ ] .gitignore criado com pelo menos 20 padrões Python
- [ ] __pycache__/ removido do histórico git
- [ ] requirements.txt com 5 dependências versionadas
- [ ] .env.example criado com LOGO_PATH, GIF_PATH
- [ ] logo_jornada.png < 1 MB (mantendo qualidade visual)
- [ ] tiapamela.gif < 1.5 MB
- [ ] Build/run do Streamlit funciona normalmente após mudanças

---

## Feature 3: Refatoração de Código

**ID:** F3-REFACTOR
**Categoria:** refactor
**Prioridade:** 🟡 ALTA
**Estimativa:** 6-8h

### Escopo
- Extrair constantes de estilo para o topo do arquivo
- Quebrar função `extrair_dados` em 3-4 funções menores
- Adicionar validações básicas de entrada
- Melhorar tratamento de erros

### Arquivos Modificados
```
MODIFICAR:
- APP.py (refatoração significativa, mas mantendo funcionalidade)
```

### Arquivos NÃO Tocados
- requirements.txt (F2 cuida)
- README.md (F1 cuida)
- docs/ (F1 cuida)
- .gitignore (F2 cuida)
- Imagens (F2 cuida)

### Refatorações Específicas

#### 1. Extrair Constantes (APP.py:1-25)
```python
# -------------------- CONSTANTES DE ESTILO --------------------
FONT_NAME = "Lexend"
FONT_COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT_COLOR_BLUE = RGBColor(0x00, 0x6F, 0xC0)

FONT_SIZE_NAMES = Pt(26.5)
FONT_SIZE_TEAM = Pt(20)
FONT_SIZE_SCHOOL = Pt(20)
FONT_SIZE_ALCANCE_LABEL = Pt(28)
FONT_SIZE_ALCANCE_VALUE = Pt(35)

LOGO_PATH = "logo_jornada.png"
GIF_PATH = "tiapamela.gif"
LOGO_WIDTH = 1235
LOGO_HEIGHT = 426
```

#### 2. Modularizar extrair_dados (APP.py:44-256)
Quebrar em:
- `identificar_colunas_tabela(header_norm, aliases_norm, palavras_chave)` - 50 linhas
- `processar_linhas_tabela(tabela, coluna_por_campo, aliases)` - 40 linhas
- `organizar_dados_equipes(registros)` - 60 linhas
- `extrair_dados(uploaded_file)` - 30 linhas (orquestra as 3 acima)

#### 3. Adicionar Validações
- Validar `uploaded_file` não é None
- Validar arquivo DOCX é válido
- Validar existência de tabelas
- Validar colunas obrigatórias encontradas
- Mensagens de erro claras para usuário

### Conflitos Esperados
**ZERO** - Único agente modificando APP.py

### Critérios de Aceitação
- [ ] Pelo menos 10 constantes extraídas no topo
- [ ] Função `extrair_dados` <= 50 linhas (orquestra outras)
- [ ] 3 funções auxiliares criadas: `identificar_colunas_tabela`, `processar_linhas_tabela`, `organizar_dados_equipes`
- [ ] Validações adicionadas em pelo menos 5 pontos críticos
- [ ] Todas as funções têm docstrings (incluídas pelo próprio agente)
- [ ] Testes manuais passando: upload DOCX + PPTX → gera slides corretamente
- [ ] Código formatado (considerar black/autopep8)

---

## 🔍 Análise de Conflitos - Matriz de Overlap

| Feature | Arquivos Principais | Overlap com F1 | Overlap com F2 | Overlap com F3 |
|---------|---------------------|----------------|----------------|----------------|
| F1-DOCS | README.md, docs/, APP.py (docstrings) | - | ❌ ZERO | ⚠️ Mínimo (docstrings) |
| F2-SETUP | .gitignore, requirements.txt, imagens | ❌ ZERO | - | ❌ ZERO |
| F3-REFACTOR | APP.py (código) | ⚠️ Mínimo (docstrings) | ❌ ZERO | - |

**Análise:**
- F1 vs F2: ✅ **100% Independentes** (zero overlap)
- F1 vs F3: ⚠️ **95% Independentes** (overlap mínimo: docstrings em APP.py)
  - Resolução: F1 adiciona docstrings, F3 também adiciona. Merge F1 primeiro, F3 depois valida/ajusta se necessário
- F2 vs F3: ✅ **100% Independentes** (zero overlap)

**Conclusão:** ✅ As 3 features podem rodar em paralelo com risco mínimo de conflitos

---

## 📋 Ordem de Merge (Quando Completas)

1. **F1-DOCS** (merge primeiro)
   - Zero código funcional tocado
   - Apenas documentação e docstrings
   - Validação: verificar se build roda

2. **F2-SETUP** (merge segundo)
   - Arquivos de config independentes
   - Validação: verificar se .gitignore funciona, imagens carregam, requirements instalam

3. **F3-REFACTOR** (merge terceiro)
   - Pode haver docstrings de F1 para ajustar
   - Validação: rodar testes manuais completos, verificar nenhuma funcionalidade quebrou

---

## ⏱️ Estimativas de Tempo

| Métrica | Sequencial | Paralelo | Speedup |
|---------|-----------|----------|---------|
| F1-DOCS | 6h | 6h | - |
| F2-SETUP | 4h | 4h | - |
| F3-REFACTOR | 8h | 8h | - |
| **TOTAL** | **18h** | **8h** (max) | **2.25x** |

---

## 🚨 Bloqueadores Potenciais

### F1-DOCS
- Risco Baixo
- Pode precisar de clarificações sobre formato esperado de entrada (consultar código ou usuário)

### F2-SETUP
- Risco Médio
- Otimização de imagens pode degradar qualidade (precisa validação visual)
- Versões de requirements podem ter incompatibilidades (testar após fixar)

### F3-REFACTOR
- Risco Alto
- Refatoração pode introduzir bugs sutis
- Testes manuais críticos ao final
- Recomendar criar backup/tag antes do merge

---

## 🎯 Próximos Passos (Orquestrador)

- [x] Criar este documento de features
- [ ] Criar branches remotas para cada feature (ETAPA 4)
- [ ] Criar briefings individuais (ETAPA 5)
- [ ] Criar PARALLEL-WORK-TRACKER.md (ETAPA 6)
- [ ] Criar DEPLOY-PROMPTS.md (ETAPA 7)
- [ ] Criar ORCHESTRATION-REPORT.md (ETAPA 8)

---

**Documento criado pelo Agente Orquestrador**
**Revisão:** v1.0
