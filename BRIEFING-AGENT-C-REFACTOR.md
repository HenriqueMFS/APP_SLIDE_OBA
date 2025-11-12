# BRIEFING: AGENT-C - Refatoração de Código

## 2.1. Status do Projeto

- **Projeto:** APP_SLIDE_OBA
- **Tipo:** Web App (Streamlit) - Gerador de Slides PowerPoint
- **Stack:** Python 3.11, Streamlit, python-docx, python-pptx, lxml, Pillow
- **Build Status:** ✅ Passing
- **Branch Base:** claude/analyze-repository-structure-011CV26eM3noi2SbsiDZJGqW
- **Sua Branch:** claude/refactor-code-OWJmZWU1Yjhi
- **Dependências:** Python 3.11+

**Fases/Features em Progresso (paralelo a você):**
- Agent-A: Documentação Completa (F1-DOCS) - pode ter adicionado docstrings
- Agent-B: Setup e Infraestrutura (F2-SETUP)

---

## 2.2. Ambiente: Claude Code Web

⚠️ **CRÍTICO:** Você está no Claude Code Web

**Sua Branch:** `claude/refactor-code-OWJmZWU1Yjhi`

---

## 2.3. Sua Missão

**Objetivo:** Refatorar APP.py para melhor manutenibilidade sem quebrar funcionalidades

**Estimativa:** 6-8h

**Prioridade:** 🟡 ALTA

**Arquivos Esperados:**
- **Modificar:** APP.py (refatoração significativa)

**Conflitos Potenciais:**
- **MÍNIMO com Agent-A:** Ele pode ter adicionado docstrings
  - Resolução: Ele será merged primeiro, você ajusta docstrings se necessário

**⚠️ CUIDADO EXTREMO:** Não quebrar funcionalidade existente!

---

## 2.4. Escopo Completo

### Features Principais

- [ ] **F3.1:** Extrair constantes de estilo para o topo do arquivo
- [ ] **F3.2:** Modularizar função `extrair_dados` em 3-4 funções menores
- [ ] **F3.3:** Adicionar validações robustas de entrada
- [ ] **F3.4:** Melhorar tratamento de erros com mensagens claras
- [ ] **F3.5:** Validar que aplicação funciona EXATAMENTE igual após refatoração

### Refatorações Específicas

#### F3.1: Extrair Constantes (estimativa: 1h)

**Localização:** Adicionar após imports (linha ~14)

```python
# -------------------- CONSTANTES DE CONFIGURAÇÃO --------------------
# Assets
LOGO_PATH = "logo_jornada.png"
GIF_PATH = "tiapamela.gif"
LOGO_WIDTH = 1235
LOGO_HEIGHT = 426

# -------------------- CONSTANTES DE ESTILO --------------------
# Fontes
FONT_NAME = "Lexend"

# Cores
FONT_COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT_COLOR_BLUE = RGBColor(0x00, 0x6F, 0xC0)

# Tamanhos de Fonte
FONT_SIZE_NAMES = Pt(26.5)
FONT_SIZE_TEAM = Pt(20)
FONT_SIZE_SCHOOL = Pt(20)
FONT_SIZE_ALCANCE_LABEL = Pt(28)
FONT_SIZE_ALCANCE_VALUE = Pt(35)
```

**Magic numbers a substituir:**
- Linha 19: `(1235, 426)` → `(LOGO_WIDTH, LOGO_HEIGHT)`
- Linha 22: `width=1235` → `width=LOGO_WIDTH`
- Linha 17: `"logo_jornada.png"` → `LOGO_PATH`
- Linha 450: `"tiapamela.gif"` → `GIF_PATH`
- Linha 301, 303, 340, 348, 361, 371, 385: Tamanhos de fonte → Constantes

---

#### F3.2: Modularizar `extrair_dados` (estimativa: 3-4h)

**Objetivo:** Quebrar função de 212 linhas em funções menores e testáveis

**Função 1: `_identificar_colunas_tabela`**
```python
def _identificar_colunas_tabela(cabecalho):
    """Identifica índices das colunas baseado em aliases e palavras-chave.

    Args:
        cabecalho (list): Lista de strings com nomes das colunas

    Returns:
        dict: Mapeamento {campo: índice_coluna}

    Raises:
        ValueError: Se colunas obrigatórias não forem encontradas
    """
    # Mover lógica das linhas 51-188 para cá
    # Retornar coluna_por_campo
    pass
```

**Função 2: `_processar_linhas_tabela`**
```python
def _processar_linhas_tabela(tabela, coluna_por_campo, aliases):
    """Processa linhas da tabela e extrai registros.

    Args:
        tabela: Objeto Table do python-docx
        coluna_por_campo (dict): Mapeamento campo → índice
        aliases (dict): Aliases de campos

    Returns:
        list: Lista de dicionários com dados extraídos
    """
    # Mover lógica das linhas 195-213 para cá
    pass
```

**Função 3: `_organizar_dados_equipes`**
```python
def _organizar_dados_equipes(registros):
    """Organiza registros por equipe e formata para slides.

    Args:
        registros (list): Lista de registros extraídos

    Returns:
        list: Dados organizados e formatados para geração de slides
    """
    # Mover lógica das linhas 215-256 para cá
    pass
```

**Função Principal Refatorada:**
```python
def extrair_dados(uploaded_file):
    """Extrai e organiza dados do arquivo DOCX.

    Processa tabelas do documento Word contendo informações de equipes
    e retorna dados formatados prontos para geração de slides.

    Args:
        uploaded_file: Arquivo DOCX carregado via Streamlit

    Returns:
        list: Lista de dicionários com dados formatados para cada equipe

    Raises:
        ValueError: Se arquivo é inválido ou não contém dados
    """
    # Validar entrada
    if not uploaded_file:
        raise ValueError("Arquivo não fornecido")

    try:
        doc = Document(uploaded_file)
    except Exception as e:
        raise ValueError(f"Arquivo DOCX inválido: {e}")

    if not doc.tables:
        raise ValueError("Nenhuma tabela encontrada no documento")

    # Processar tabelas
    registros = []
    for tabela in doc.tables:
        if not tabela.rows:
            continue

        cabecalho = [c.text.strip() for c in tabela.rows[0].cells]

        try:
            coluna_por_campo = _identificar_colunas_tabela(cabecalho)
        except ValueError as e:
            st.warning(f"Tabela ignorada: {e}")
            continue

        aliases = {...}  # Manter definição de aliases aqui
        registros_tabela = _processar_linhas_tabela(tabela, coluna_por_campo, aliases)
        registros.extend(registros_tabela)

    if not registros:
        raise ValueError("Nenhum registro válido encontrado nas tabelas")

    # Organizar por equipes
    dados_finais = _organizar_dados_equipes(registros)

    return dados_finais
```

---

#### F3.3: Adicionar Validações (estimativa: 1-1.5h)

**Locais para adicionar validações:**

1. **Início de `extrair_dados`** (linha 44)
```python
if not uploaded_file:
    raise ValueError("Arquivo não fornecido")

try:
    doc = Document(uploaded_file)
except Exception as e:
    raise ValueError(f"Arquivo DOCX inválido: {e}")

if not doc.tables:
    raise ValueError("Nenhuma tabela encontrada no documento")
```

2. **Em `_identificar_colunas_tabela`**
```python
colunas_obrigatorias = ["Nome", "Equipe", "Valido"]
colunas_encontradas = list(coluna_por_campo.keys())

for col in colunas_obrigatorias:
    if col not in colunas_encontradas:
        raise ValueError(f"Coluna obrigatória '{col}' não encontrada")
```

3. **Em `gerar_apresentacao`** (linha 401)
```python
def gerar_apresentacao(dados, template_stream):
    if not dados:
        raise ValueError("Nenhum dado fornecido para geração")

    if not template_stream:
        raise ValueError("Template PPTX não fornecido")

    try:
        prs = Presentation(template_stream)
    except Exception as e:
        raise ValueError(f"Template PPTX inválido: {e}")

    if not prs.slides:
        raise ValueError("Template não contém slides")

    # ... resto do código
```

4. **Na interface Streamlit** (linha 435)
```python
if st.button("✨ Gerar Apresentação"):
    if not docx_file or not pptx_file:
        st.error("⚠️ Por favor, envie ambos os arquivos (DOCX e PPTX)")
    else:
        try:
            dados = extrair_dados(docx_file)
            prs_final = gerar_apresentacao(dados, pptx_file)
            # ... resto
        except ValueError as e:
            st.error(f"❌ Erro de validação: {e}")
        except Exception as e:
            st.error(f"❌ Erro ao gerar apresentação: {e}")
```

---

## 2.5. Plano de Execução Detalhado

### Fase 1: Setup e Backup (10 min)

```bash
# Checkout branch
git checkout -b claude/refactor-code-OWJmZWU1Yjhi
git push -u origin claude/refactor-code-OWJmZWU1Yjhi

# Criar backup do APP.py original
cp APP.py APP.py.backup

# Validar que aplicação roda antes da refatoração
streamlit run APP.py --server.headless=true --server.port=8501 &
sleep 5
curl -I http://localhost:8501
kill %1
```

---

### Fase 2: Extrair Constantes (60 min)

```bash
# 1. Adicionar constantes no topo (após imports, antes de st.set_page_config)
# Usar Edit tool para adicionar bloco de constantes

# 2. Substituir magic numbers por constantes em todo o arquivo
# Locais principais:
# - Linha 19: logo.resize
# - Linha 22: st.image width
# - Linha 17, 450: paths de imagens
# - Linhas 301, 303, 340, 348, 361, 371, 385, 395: tamanhos de fonte e cores

# 3. Testar que aplicação ainda roda
python -c "import APP; print('✅ Import OK')"

# 4. Commit
git add APP.py
git commit -m "refactor: extract style constants to top of file

Extracted 15+ magic numbers to named constants:
- Asset paths (LOGO_PATH, GIF_PATH)
- Logo dimensions (LOGO_WIDTH, LOGO_HEIGHT)
- Font configuration (FONT_NAME, sizes, colors)

Improves maintainability and consistency.

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

git push origin claude/refactor-code-OWJmZWU1Yjhi

# Atualizar tracker (12%)
```

---

### Fase 3: Modularizar `extrair_dados` - Parte 1 (90 min)

```bash
# 1. Criar função _identificar_colunas_tabela
# Mover lógica das linhas 51-188
# Adicionar docstring
# Adicionar validação de colunas obrigatórias

# 2. Testar isoladamente (se possível)
python -c "
from APP import _identificar_colunas_tabela
cabecalho = ['Nome', 'Equipe', 'Função', 'Escola', 'Cidade', 'Estado', 'Válido']
resultado = _identificar_colunas_tabela(cabecalho)
print('✅ _identificar_colunas_tabela OK:', resultado)
"

# 3. Commit incremental
git add APP.py
git commit -m "refactor: extract _identificar_colunas_tabela from extrair_dados

Moved column identification logic to separate function (50 lines).
Added validation for required columns.

Part 1/3 of extrair_dados modularization.

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

git push origin claude/refactor-code-OWJmZWU1Yjhi

# Atualizar tracker (35%)
```

---

### Fase 4: Modularizar `extrair_dados` - Parte 2 (90 min)

```bash
# 1. Criar função _processar_linhas_tabela
# Mover lógica das linhas 195-213

# 2. Criar função _organizar_dados_equipes
# Mover lógica das linhas 215-256

# 3. Refatorar extrair_dados para usar as 3 funções auxiliares
# Manter apenas orquestração + validações

# 4. Testar que funcionalidade não quebrou
python -c "
from docx import Document
from APP import extrair_dados
# Criar documento de teste simples...
# (se possível, ou validar manualmente via Streamlit)
"

# 5. Commit
git add APP.py
git commit -m "refactor: complete extrair_dados modularization

Created 3 helper functions:
- _processar_linhas_tabela: Process table rows (40 lines)
- _organizar_dados_equipes: Organize by teams (60 lines)
- extrair_dados: Now orchestrates helpers (30 lines, was 212)

Improved testability and readability.

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

git push origin claude/refactor-code-OWJmZWU1Yjhi

# Atualizar tracker (60%)
```

---

### Fase 5: Adicionar Validações (75 min)

```bash
# 1. Adicionar validações em extrair_dados
# 2. Adicionar validações em gerar_apresentacao
# 3. Melhorar tratamento de erros na interface Streamlit

# 4. Testar cenários de erro:
# - Upload sem arquivo
# - DOCX inválido
# - DOCX sem tabelas
# - PPTX inválido

# 5. Commit
git add APP.py
git commit -m "refactor: add robust input validation

Added validations in:
- extrair_dados: File, tables, required columns
- gerar_apresentacao: Data, template, slides
- Streamlit interface: Better error messages

Improves user experience with clear error feedback.

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

git push origin claude/refactor-code-OWJmZWU1Yjhi

# Atualizar tracker (80%)
```

---

### Fase 6: Validação Final e Testes (90 min)

```bash
# 1. Teste completo end-to-end
streamlit run APP.py

# Testar manualmente:
# - Upload DOCX válido
# - Upload PPTX válido
# - Gerar apresentação
# - Validar slides gerados estão corretos
# - Testar com dados de múltiplas equipes
# - Testar cenários de erro (arquivos inválidos)

# 2. Comparar com backup
diff APP.py.backup APP.py | head -100

# 3. Validar métricas de código
wc -l APP.py
echo "Linhas antes: 461"
echo "Linhas depois: ~500 (com validações e funções auxiliares)"

# 4. Verificar se Agent-A adicionou docstrings
# Se sim, garantir que estão preservadas

# 5. Criar relatório final
cat > REPORT-AGENT-C-REFACTOR.md << 'EOF'
# Relatório Final - Agent-C: Refatoração de Código

## Status: ✅ COMPLETO

## Resumo de Entregas

### Refatorações Realizadas

1. **Constantes Extraídas (15+)**
   - Assets: LOGO_PATH, GIF_PATH, dimensões
   - Estilo: FONT_NAME, tamanhos, cores
   - Localização: Linhas 15-30 (novo)

2. **Função `extrair_dados` Modularizada**
   - Antes: 212 linhas monolíticas
   - Depois: 30 linhas + 3 funções auxiliares
   - Funções criadas:
     - `_identificar_colunas_tabela` (50 linhas)
     - `_processar_linhas_tabela` (40 linhas)
     - `_organizar_dados_equipes` (60 linhas)

3. **Validações Adicionadas (8+)**
   - extrair_dados: Arquivo, tabelas, colunas obrigatórias
   - gerar_apresentacao: Dados, template, slides
   - Interface: Mensagens de erro claras

### Estatísticas

- **Commits:** 5
- **Linhas antes:** 461
- **Linhas depois:** ~510 (+ ~50 linhas de validações/funções)
- **Complexidade reduzida:** Função principal 212 → 30 linhas
- **Funções auxiliares:** +3 (testáveis independentemente)
- **Constantes extraídas:** 15+
- **Tempo decorrido:** ~6.5h

## Validações

### Funcionais
- ✅ Aplicação roda sem erros
- ✅ Upload de DOCX funciona
- ✅ Upload de PPTX funciona
- ✅ Geração de slides funciona
- ✅ Slides gerados são idênticos à versão original
- ✅ Formatação preservada (fontes, cores, tamanhos)
- ✅ Ordenação de equipes correta
- ✅ Nomes formatados corretamente

### Erros e Validações
- ✅ Upload sem arquivo: Erro claro
- ✅ DOCX inválido: Erro claro
- ✅ DOCX sem tabelas: Erro claro
- ✅ Colunas obrigatórias faltando: Erro claro
- ✅ PPTX inválido: Erro claro

### Código
- ✅ Imports funcionam: `import APP` OK
- ✅ Constantes acessíveis
- ✅ Funções auxiliares com docstrings
- ✅ Código mais legível e manutenível

## Critérios de Aceitação

- [x] Pelo menos 10 constantes extraídas (15 entregues)
- [x] Função `extrair_dados` <= 50 linhas (30 linhas)
- [x] 3 funções auxiliares criadas
- [x] Validações adicionadas em >= 5 pontos (8 pontos)
- [x] Todas funções auxiliares têm docstrings
- [x] Testes manuais passando: upload DOCX + PPTX → gera slides
- [x] Funcionalidade idêntica à versão original

## Melhorias de Qualidade

### Antes da Refatoração
- 1 função monolítica (212 linhas)
- Magic numbers espalhados (15+)
- Validações mínimas
- Difícil de testar
- Difícil de manter

### Depois da Refatoração
- 4 funções modulares (30 + 50 + 40 + 60 linhas)
- Constantes centralizadas
- Validações robustas em 8 pontos
- Funções auxiliares testáveis
- Código autodocumentado

## Observações

- Funcionalidade 100% preservada
- Zero regressões detectadas
- Código significativamente mais manutenível
- Facilita futuras extensões
- Docstrings de Agent-A preservadas (se houver)

## Próximos Passos (Orquestrador)

1. Validar entregas deste agent
2. Fazer merge após Agent-A e Agent-B (terceiro da fila)
3. Validar build final de develop

---

**Agent-C: Refatoração de Código - ✅ 100% COMPLETO**
**Data de conclusão:** 2025-11-12
**Branch:** claude/refactor-code-OWJmZWU1Yjhi
EOF

git add REPORT-AGENT-C-REFACTOR.md
git commit -m "docs: relatório final Agent-C

Refatoração completa entregue:
- 15+ constantes extraídas
- extrair_dados modularizada (212 → 30 + 3 helpers)
- 8 validações adicionadas
- Funcionalidade 100% preservada

Status: ✅ 100% COMPLETO

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

git push origin claude/refactor-code-OWJmZWU1Yjhi

# Atualizar tracker (100%)

# Remover backup
rm APP.py.backup
```

---

## 2.6. Critérios de Aceitação

- [ ] Pelo menos 10 constantes extraídas no topo
- [ ] Função `extrair_dados` <= 50 linhas (orquestra outras)
- [ ] 3 funções auxiliares criadas com nomes iniciando em `_`
- [ ] Cada função auxiliar tem docstring completa
- [ ] Validações adicionadas em >= 5 pontos críticos
- [ ] Testes manuais passando: upload DOCX + PPTX → gera slides corretamente
- [ ] Slides gerados são idênticos à versão original
- [ ] Formatação preservada (cores, fontes, tamanhos)
- [ ] Mensagens de erro claras em cenários de falha
- [ ] REPORT-AGENT-C-REFACTOR.md criado
- [ ] PARALLEL-WORK-TRACKER.md atualizado para 100%

---

## 2.7. Regras Críticas

1. ⚠️ **NÃO QUEBRAR FUNCIONALIDADE** - Prioridade máxima!
2. ⚠️ **TESTAR FREQUENTEMENTE** - Após cada refatoração, validar que ainda funciona
3. ⚠️ **COMMITS INCREMENTAIS** - Não acumular muitas mudanças
4. ⚠️ **BACKUP ANTES** - Manter `APP.py.backup` até finalizar
5. ✅ **FUNÇÕES PRIVADAS** - Prefixar funções auxiliares com `_`
6. ✅ **DOCSTRINGS OBRIGATÓRIAS** - Todas funções auxiliares
7. ✅ **VALIDAR ANTES E DEPOIS** - Comparar comportamento

---

## 2.8. Troubleshooting

### Problema: Aplicação Para de Funcionar Após Refatoração

**Solução:**
```bash
# Restaurar backup
cp APP.py.backup APP.py

# Refazer refatoração em passos menores
# Testar após cada mudança pequena

# Ou: Fazer git revert do commit problemático
git revert HEAD
```

### Problema: Conflito de Docstrings com Agent-A

**Solução:**
```bash
# Verificar se Agent-A já foi merged
git log develop | grep "Agent-A"

# Se sim, fazer merge de develop na sua branch
git merge develop

# Resolver conflitos mantendo:
# - Suas refatorações de código
# - Docstrings do Agent-A
```

### Problema: Testes Manuais Revelam Comportamento Diferente

**Identificar diferença:**
```bash
# Gerar slides com versão original
git checkout APP.py.backup
streamlit run APP.py
# Gerar apresentação, salvar como "original.pptx"

# Gerar slides com versão refatorada
git checkout APP.py
streamlit run APP.py
# Gerar apresentação, salvar como "refatorado.pptx"

# Comparar manualmente no PowerPoint
```

**Corrigir:**
- Identificar qual função auxiliar está causando diferença
- Adicionar prints/logs temporários
- Ajustar lógica para match exato com original

---

## 2.9. Links Úteis

- **Projeto no GitHub:** https://github.com/HenriqueMFS/APP_SLIDE_OBA
- **Branch Base:** claude/analyze-repository-structure-011CV26eM3noi2SbsiDZJGqW
- **Sua Branch:** claude/refactor-code-OWJmZWU1Yjhi
- **Análise de Complexidade:** ANALISE_REPOSITORIO.md (seção "Análise de Complexidade")

---

## Checklist Rápido Antes de Começar

- [ ] Li todo o briefing
- [ ] Entendi minha missão (refatoração sem quebrar funcionalidade)
- [ ] Sei que devo fazer backup primeiro
- [ ] Sei que devo testar após cada refatoração
- [ ] Sei os 5 deliverables principais
- [ ] Checkout na minha branch + backup criado

**COMECE AGORA pela Fase 1: Setup e Backup!**

**⚠️ LEMBRE-SE: TESTAR, TESTAR, TESTAR! Não quebrar funcionalidade é CRÍTICO!**
