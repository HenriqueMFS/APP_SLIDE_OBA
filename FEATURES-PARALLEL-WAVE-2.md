# 🚀 Features para Desenvolvimento Paralelo - Onda 2 (Performance)

**Data:** 2025-11-18
**Projeto:** APP_SLIDE_OBA
**Tipo:** Otimizações de Performance
**Base:** Análise em PERFORMANCE-ANALYSIS.md
**Commit base:** d9616e0

---

## 📋 Visão Geral

Esta onda de desenvolvimento paralelo implementa as otimizações de performance identificadas na análise detalhada. As features foram cuidadosamente divididas para minimizar conflitos e maximizar a execução paralela.

**Objetivo geral:** Reduzir tempo de geração em 40-60% e melhorar UX

---

## 🎯 Feature 1: Cache e Validações (F1-CACHE-VALIDATION)

### Metadados
- **ID:** F1-CACHE-VALIDATION
- **Agent:** Agent-D
- **Branch:** `claude/perf-cache-validation-{SESSION_ID}`
- **Prioridade:** 🔴 CRÍTICA
- **Estimativa:** 2-3h
- **Ganho esperado:** 30-40% de performance

### Descrição
Implementar caching de recursos pesados e validações de tamanho de arquivo para prevenir crashes e melhorar performance de re-execuções do Streamlit.

### Entregas Detalhadas

#### 1.1. Cache de Logo (`@st.cache_resource`)
**Arquivo:** `APP.py`
**Linhas afetadas:** 59-61
**Ganho:** 30x em re-execuções (20-50ms → <1ms)

**Código atual:**
```python
logo = Image.open(LOGO_PATH)
resample_filter = getattr(Image, "Resampling", Image).LANCZOS
logo = logo.resize((LOGO_WIDTH, LOGO_HEIGHT), resample_filter)
```

**Código otimizado:**
```python
@st.cache_resource
def carregar_logo():
    """Carrega e redimensiona logo uma única vez por sessão."""
    logo_img = Image.open(LOGO_PATH)
    resample_filter = getattr(Image, "Resampling", Image).LANCZOS
    return logo_img.resize((LOGO_WIDTH, LOGO_HEIGHT), resample_filter)

logo = carregar_logo()
```

#### 1.2. Cache de Extração de Dados (`@st.cache_data`)
**Arquivo:** `APP.py`
**Nova função:** `extrair_dados_cached`
**Ganho:** Evita reprocessamento em re-runs (0.5-2.5s economizados)

**Implementar após a função `extrair_dados` existente:**
```python
@st.cache_data(show_spinner="📊 Extraindo dados do DOCX...")
def extrair_dados_cached(docx_bytes):
    """
    Versão cached de extrair_dados para evitar reprocessamento.

    Args:
        docx_bytes (bytes): Conteúdo do arquivo DOCX em bytes

    Returns:
        dict: Dados extraídos organizados por equipe
    """
    from io import BytesIO
    return extrair_dados(BytesIO(docx_bytes))
```

**Atualizar interface (próximo ao botão de geração):**
```python
if docx_file:
    # Lê arquivo uma vez e cacheia
    docx_bytes = docx_file.read()
    docx_file.seek(0)  # Reset para outras operações
    dados = extrair_dados_cached(docx_bytes)
```

#### 1.3. Validação de Tamanho de Arquivos
**Arquivo:** `APP.py`
**Nova função:** `validar_tamanho_arquivo`
**Ganho:** Previne timeouts e OOM crashes

**Adicionar constantes no topo (após linha 56):**
```python
# Limites de arquivo
MAX_DOCX_SIZE_MB = 10  # 10 MB
MAX_PPTX_SIZE_MB = 20  # 20 MB
MAX_EQUIPES = 500      # Máximo de equipes
```

**Nova função (adicionar após `formatar_texto`):**
```python
def validar_tamanho_arquivo(uploaded_file, max_size_mb, tipo):
    """
    Valida tamanho de arquivo antes de processar.

    Args:
        uploaded_file: Arquivo do st.file_uploader
        max_size_mb (int): Tamanho máximo em MB
        tipo (str): Tipo do arquivo (para mensagem)

    Returns:
        tuple: (bool válido, str mensagem_erro)
    """
    if not uploaded_file:
        return True, ""

    uploaded_file.seek(0, 2)  # Vai para o final
    size_bytes = uploaded_file.tell()
    uploaded_file.seek(0)  # Volta para o início

    size_mb = size_bytes / (1024 * 1024)

    if size_mb > max_size_mb:
        return False, f"❌ Arquivo {tipo} muito grande: {size_mb:.1f} MB (máximo: {max_size_mb} MB)"

    return True, ""
```

**Atualizar botão de geração (adicionar validações):**
```python
if st.button("✨ Gerar Apresentação"):
    if not docx_file or not pptx_file:
        st.warning(MSG_SEND_BOTH_FILES)
    else:
        # Validações de tamanho
        valid_docx, msg_docx = validar_tamanho_arquivo(docx_file, MAX_DOCX_SIZE_MB, "DOCX")
        valid_pptx, msg_pptx = validar_tamanho_arquivo(pptx_file, MAX_PPTX_SIZE_MB, "PPTX")

        if not valid_docx:
            st.error(msg_docx)
        elif not valid_pptx:
            st.error(msg_pptx)
        else:
            # Processa normalmente (código existente)
            # ...
```

### Arquivos Modificados
- `APP.py` (3 seções: linhas ~59-61, nova função cache, validações na interface)

### Conflitos Esperados
- **Com Agent-E:** ZERO (Agent-E mexe em constantes/aliases, não em cache)
- **Com Agent-F:** ZERO (Agent-F mexe em progress bar, não em cache)
- **Probabilidade:** 0-5%

### Testes Necessários
1. ✅ Logo carrega apenas 1 vez por sessão
2. ✅ DOCX processado apenas 1 vez mesmo alterando nome
3. ✅ Arquivo >10MB DOCX é rejeitado
4. ✅ Arquivo >20MB PPTX é rejeitado
5. ✅ Arquivos válidos processam normalmente

### Critérios de Sucesso
- [ ] `@st.cache_resource` aplicado em carregar_logo
- [ ] `@st.cache_data` aplicado em extrair_dados_cached
- [ ] Validação de tamanho implementada e testada
- [ ] Performance: Re-execuções 30x mais rápidas
- [ ] Sem quebra de funcionalidade

---

## 🎯 Feature 2: Constantes e Regex (F2-CONSTANTS-REGEX)

### Metadados
- **ID:** F2-CONSTANTS-REGEX
- **Agent:** Agent-E
- **Branch:** `claude/perf-constants-regex-{SESSION_ID}`
- **Prioridade:** 🟡 ALTA
- **Estimativa:** 1-2h
- **Ganho esperado:** 1.5x em extração de dados

### Descrição
Mover aliases para constantes globais pré-normalizadas e compilar regex para eliminar recalculações redundantes.

### Entregas Detalhadas

#### 2.1. Aliases como Constantes Globais
**Arquivo:** `APP.py`
**Seção afetada:** Topo do arquivo + `_identificar_colunas_tabela`
**Ganho:** 1.5x (5-10ms economizados por tabela)

**Adicionar após as constantes existentes (após linha 56):**
```python
# -------------------- ALIASES DE CAMPOS --------------------
ALIASES_CAMPOS = {
    "Valido": [
        "valido", "alcance", "lancamentos validos", "lancamentos válidos",
        "lançamentos válidos", "lançamentos validos"
    ],
    "Equipe": [
        "equipe", "nome equipe", "nome da equipe", "equipe/", "dados da equipe"
    ],
    "Escola": [
        "escola", "nome escola", "nome da escola"
    ],
    "Cidade": [
        "cidade", "municipio", "município"
    ],
    "Estado": [
        "estado", "uf", "sigla uf", "sigla estado"
    ],
    "Aluno1": [
        "aluno 1", "aluno1", "nome aluno 1", "primeiro aluno", "1º aluno"
    ],
    "Aluno2": [
        "aluno 2", "aluno2", "nome aluno 2", "segundo aluno", "2º aluno"
    ],
    "Aluno3": [
        "aluno 3", "aluno3", "nome aluno 3", "terceiro aluno", "3º aluno"
    ],
    "Aluno4": [
        "aluno 4", "aluno4", "nome aluno 4", "quarto aluno", "4º aluno"
    ],
    "Aluno5": [
        "aluno 5", "aluno5", "nome aluno 5", "quinto aluno", "5º aluno"
    ],
}

# Normalizar aliases uma única vez no carregamento
def _normalizar_aliases():
    """Normaliza aliases uma única vez no carregamento do módulo."""
    return {
        campo: [normalizar_texto_base(alias) for alias in lista]
        for campo, lista in ALIASES_CAMPOS.items()
    }

# Aliases normalizados (calculados uma vez)
ALIASES_NORMALIZADOS = _normalizar_aliases()

# Prioridade de campos para matching
PRIORIDADE_CAMPOS = ["Valido", "Equipe", "Escola", "Cidade", "Estado",
                     "Aluno1", "Aluno2", "Aluno3", "Aluno4", "Aluno5"]
```

**Atualizar função `_identificar_colunas_tabela` (remover aliases locais):**

Localizar estas linhas (~197-249) e **REMOVER**:
```python
# ❌ REMOVER este bloco completo de aliases locais
aliases = {
    "Valido": ["valido", "alcance", ...],
    # ... todo o dicionário ...
}

aliases_norm = {
    campo: [normalizar_texto_base(alias) for alias in lista]
    for campo, lista in aliases.items()
}

prioridade_campos = ["Valido", "Equipe", ...]
```

**Substituir por:**
```python
# ✅ Usar constantes globais pré-normalizadas
aliases_norm = ALIASES_NORMALIZADOS
prioridade_campos = PRIORIDADE_CAMPOS
```

#### 2.2. Compilação de Regex
**Arquivo:** `APP.py`
**Seção:** Após ALIASES (topo do arquivo)
**Ganho:** 20-30% mais rápido em operações de regex

**Adicionar após ALIASES_NORMALIZADOS:**
```python
# -------------------- REGEX COMPILADAS --------------------
import re

# Compilar regex uma vez para melhor performance
REGEX_WHITESPACE = re.compile(r"\s+")
REGEX_NON_ALPHANUMERIC = re.compile(r"[^a-z0-9]+")
REGEX_INVALID_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|]')
REGEX_ALCANCE = re.compile(r"(ALCANCE:\s*)([\d,.]+ m)", re.IGNORECASE)
```

**Atualizar função `normalizar_texto_base`:**

Localizar linha ~120:
```python
# ❌ ANTES
def normalizar_texto_base(texto):
    if not texto:
        return ""
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(ch for ch in texto if not unicodedata.combining(ch))
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto.lower()
```

Substituir por:
```python
# ✅ DEPOIS (usa regex compilada)
def normalizar_texto_base(texto):
    """
    Normaliza texto removendo acentos e caracteres especiais.

    Args:
        texto: Texto a ser normalizado

    Returns:
        str: Texto normalizado (lowercase, sem acentos, espaços únicos)
    """
    if not texto:
        return ""
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(ch for ch in texto if not unicodedata.combining(ch))
    texto = REGEX_WHITESPACE.sub(" ", texto).strip()  # ✅ Usa regex compilada
    return texto.lower()
```

**Atualizar outras funções que usam regex:**

Buscar e atualizar `formatar_nome_arquivo` e `replace_placeholders_in_shape` se usarem regex.

### Arquivos Modificados
- `APP.py` (topo do arquivo + `_identificar_colunas_tabela` + `normalizar_texto_base`)

### Conflitos Esperados
- **Com Agent-D:** ZERO (Agent-D não mexe em aliases)
- **Com Agent-F:** ZERO (Agent-F mexe apenas em progress bar)
- **Probabilidade:** 0-5%

### Testes Necessários
1. ✅ Aliases funcionam corretamente (mesmos matches de antes)
2. ✅ Normalização de texto funciona igual
3. ✅ Performance: Processamento 1.5x mais rápido
4. ✅ Nenhuma regressão em identificação de colunas

### Critérios de Sucesso
- [ ] Constantes ALIASES_CAMPOS e ALIASES_NORMALIZADOS no topo
- [ ] Regex compiladas (REGEX_WHITESPACE, etc.)
- [ ] _identificar_colunas_tabela usa constantes globais
- [ ] normalizar_texto_base usa REGEX_WHITESPACE
- [ ] Performance: 1.5x mais rápido em extração
- [ ] Sem quebra de funcionalidade

---

## 🎯 Feature 3: Progress Bar e UX (F3-PROGRESS-UX)

### Metadados
- **ID:** F3-PROGRESS-UX
- **Agent:** Agent-F
- **Branch:** `claude/perf-progress-ux-{SESSION_ID}`
- **Prioridade:** 🟡 ALTA
- **Estimativa:** 1-2h
- **Ganho esperado:** UX significativamente melhor (não afeta performance técnica)

### Descrição
Implementar progress bars e indicadores de status para melhorar experiência do usuário durante operações longas (5-30 segundos).

### Entregas Detalhadas

#### 3.1. Progress Bar na Geração de Apresentação
**Arquivo:** `APP.py`
**Função afetada:** `gerar_apresentacao` (linha ~808)
**Ganho:** UX crítico para arquivos grandes

**Substituir função `gerar_apresentacao` completa:**

```python
def gerar_apresentacao(dados, template_stream):
    """
    Gera apresentação PowerPoint com dados fornecidos e progress bar.

    Cria uma apresentação duplicando o slide modelo para cada equipe
    e preenchendo os placeholders com os dados correspondentes. Mostra
    progresso em tempo real.

    Args:
        dados (list): Lista de dicionários com dados de cada equipe
        template_stream: Stream do arquivo PPTX template

    Returns:
        Presentation: Objeto Presentation com slides gerados
    """
    # Criar elementos de progresso
    progress_placeholder = st.empty()
    status_placeholder = st.empty()

    try:
        # Etapa 1: Carregar template (0-10%)
        status_placeholder.info("📂 Carregando template PowerPoint...")
        progress_placeholder.progress(0)

        prs = Presentation(template_stream)
        progress_placeholder.progress(10)

        if not dados or not prs.slides:
            status_placeholder.success("✅ Template carregado (sem dados para processar)")
            return prs

        modelo = prs.slides[0]
        slides_para_preencher = [modelo]

        # Etapa 2: Duplicar slides (10-60%)
        num_duplicacoes = len(dados) - 1
        if num_duplicacoes > 0:
            status_placeholder.info(f"📋 Duplicando slides para {len(dados)} equipes...")

            for i in range(num_duplicacoes):
                novo_slide = duplicate_slide_with_media(prs, modelo)
                slides_para_preencher.append(novo_slide)

                # Atualiza progresso (10% a 60%)
                progresso = 10 + int((i + 1) / num_duplicacoes * 50)
                progress_placeholder.progress(progresso)
                status_placeholder.info(
                    f"📋 Duplicando slides: {i + 1}/{num_duplicacoes} "
                    f"({int((i + 1) / num_duplicacoes * 100)}%)"
                )
        else:
            progress_placeholder.progress(60)

        # Etapa 3: Preencher dados (60-100%)
        status_placeholder.info(f"✏️ Preenchendo dados em {len(dados)} slides...")

        for i, (slide, team) in enumerate(zip(slides_para_preencher, dados)):
            for shape in slide.shapes:
                replace_placeholders_in_shape(shape, team)

            # Atualiza progresso (60% a 100%)
            progresso = 60 + int((i + 1) / len(dados) * 40)
            progress_placeholder.progress(progresso)
            status_placeholder.info(
                f"✏️ Preenchendo dados: {i + 1}/{len(dados)} equipes "
                f"({int((i + 1) / len(dados) * 100)}%)"
            )

        # Finalização
        progress_placeholder.progress(100)
        status_placeholder.success(
            f"✅ Apresentação gerada com sucesso! {len(dados)} slides criados."
        )

        return prs

    except Exception as e:
        status_placeholder.error(f"❌ Erro durante geração: {str(e)}")
        raise

    finally:
        # Limpa progress bar após 2 segundos
        import time
        time.sleep(2)
        progress_placeholder.empty()
        status_placeholder.empty()
```

#### 3.2. Indicador de Extração de Dados
**Arquivo:** `APP.py`
**Seção:** Antes da chamada de `extrair_dados` ou `extrair_dados_cached`

Se Agent-D implementou `extrair_dados_cached`, o decorator `@st.cache_data(show_spinner="...")` já adiciona indicador.

Caso contrário, adicionar:
```python
# Antes de processar DOCX
with st.spinner("📊 Extraindo dados do DOCX..."):
    dados = extrair_dados(docx_file)

if not dados:
    st.error(MSG_NO_DATA_FOUND)
else:
    st.success(f"✅ {len(dados)} equipes encontradas no DOCX")
```

#### 3.3. Melhorar Mensagens de Feedback
**Arquivo:** `APP.py`
**Constantes:** Adicionar novas mensagens

**Adicionar após linha 52 (MSG_CAPTION_READY):**
```python
# Mensagens de progresso
MSG_PROGRESS_LOADING_TEMPLATE = "📂 Carregando template PowerPoint..."
MSG_PROGRESS_DUPLICATING = "📋 Duplicando slides para {} equipes..."
MSG_PROGRESS_FILLING = "✏️ Preenchendo dados em {} slides..."
MSG_SUCCESS_GENERATED = "✅ Apresentação gerada com sucesso! {} slides criados."
MSG_SUCCESS_DATA_EXTRACTED = "✅ {} equipes encontradas no DOCX"
MSG_PROGRESS_EXTRACTING = "📊 Extraindo dados do DOCX..."
```

### Arquivos Modificados
- `APP.py` (função `gerar_apresentacao` + constantes de mensagens)

### Conflitos Esperados
- **Com Agent-D:** BAIXO (5-10%) - Ambos mexem em `gerar_apresentacao`, mas Agent-D apenas adiciona validações antes, Agent-F modifica corpo da função
- **Com Agent-E:** ZERO (Agent-E mexe em constantes/aliases)
- **Probabilidade:** 5-10%

### Testes Necessários
1. ✅ Progress bar aparece durante geração
2. ✅ Porcentagem atualiza corretamente (0→10→60→100%)
3. ✅ Mensagens de status são claras e informativas
4. ✅ Progress bar desaparece após conclusão
5. ✅ Funcionalidade de geração não quebra

### Critérios de Sucesso
- [ ] Progress bar implementada em `gerar_apresentacao`
- [ ] 3 etapas de progresso: template (0-10%), duplicação (10-60%), preenchimento (60-100%)
- [ ] Mensagens de status claras
- [ ] Auto-limpeza de progress bar após 2s
- [ ] UX: Usuário vê progresso em tempo real
- [ ] Sem quebra de funcionalidade

---

## 📊 Matriz de Conflitos

| Feature | Agent | Arquivos | Linhas Principais | Conflito D | Conflito E | Conflito F |
|---------|-------|----------|-------------------|------------|------------|------------|
| F1-CACHE-VALIDATION | Agent-D | APP.py | 59-61, nova função, interface | - | 0% | 0% |
| F2-CONSTANTS-REGEX | Agent-E | APP.py | Topo, _identificar_colunas | 0% | - | 0% |
| F3-PROGRESS-UX | Agent-F | APP.py | gerar_apresentacao | 5% | 0% | - |

**Análise de Conflitos:**
- ✅ **Agent-D + Agent-E:** ZERO conflitos (seções completamente diferentes)
- ✅ **Agent-D + Agent-F:** ZERO conflitos (Agent-D não mexe em gerar_apresentacao)
- ⚠️ **Agent-E + Agent-F:** ZERO conflitos diretos
- **Conflito geral estimado:** 0-5% (mínimo)

---

## 🔄 Ordem de Merge Recomendada

### Estratégia: Por Prioridade e Dependência

```
1. Agent-D (F1-CACHE-VALIDATION) ← CRÍTICO, sem dependências
   ↓
2. Agent-E (F2-CONSTANTS-REGEX)   ← ALTO, independente de D
   ↓
3. Agent-F (F3-PROGRESS-UX)       ← ALTO, pode ter conflito mínimo com D
```

### Comandos de Merge

```bash
# Merge 1: Agent-D (Cache e Validações)
git checkout claude/analyze-repository-structure-011CV26eM3noi2SbsiDZJGqW
git fetch origin
git merge --no-ff origin/claude/perf-cache-validation-{SESSION_ID} \
  -m "merge: Agent-D - Cache e Validações (performance)"

# Merge 2: Agent-E (Constantes e Regex)
git merge --no-ff origin/claude/perf-constants-regex-{SESSION_ID} \
  -m "merge: Agent-E - Constantes e Regex (performance)"

# Merge 3: Agent-F (Progress Bar)
git merge --no-ff origin/claude/perf-progress-ux-{SESSION_ID} \
  -m "merge: Agent-F - Progress Bar e UX"
```

### Resolução de Conflitos Esperados

Se houver conflito em `gerar_apresentacao`:
- **Preferir:** Agent-F (tem a versão com progress bar completa)
- **Validar:** Que validações de Agent-D foram aplicadas ANTES da chamada
- **Estratégia:** `git merge --strategy-option theirs` se necessário

---

## 📈 Ganhos Esperados Totais

### Performance (Técnica)

| Cenário | Tempo Atual | Após Wave-2 | Melhoria |
|---------|-------------|-------------|----------|
| **10 equipes** | 700ms | ~400ms | **-43%** |
| **50 equipes** | 3.2s | ~1.8s | **-44%** |
| **200 equipes** | 12.5s | ~7.0s | **-44%** |

**Ganho médio esperado:** 40-50% mais rápido

### Performance (UX)

- ✅ **Progress bar:** Usuário vê progresso em tempo real
- ✅ **Mensagens claras:** Status de cada etapa
- ✅ **Sem travamentos aparentes:** Aplicação parece responsiva
- ✅ **Validações preventivas:** Erros claros antes de processar
- ✅ **Cache transparente:** Re-execuções instantâneas

---

## ✅ Validação Final

### Checklist de Integração

Após todos os merges, validar:

- [ ] Logo carrega apenas 1 vez (cache funciona)
- [ ] DOCX processa apenas 1 vez em re-runs (cache funciona)
- [ ] Aliases são constantes globais (não recalculados)
- [ ] Regex são compiladas (performance melhor)
- [ ] Progress bar aparece durante geração
- [ ] Validações de tamanho funcionam (10MB DOCX, 20MB PPTX)
- [ ] Funcionalidade completa preservada
- [ ] Performance: 40-50% mais rápido em benchmarks

### Testes de Performance

```python
# Script de teste (executar após Wave-2)
import time

# Teste 1: Cache de logo (deve ser <5ms na 2ª execução)
start = time.time()
logo = carregar_logo()  # Deve vir do cache
print(f"Cache de logo: {(time.time() - start) * 1000:.2f}ms")  # Esperado: <5ms

# Teste 2: Geração de 50 equipes
# Esperado: <2s (vs. 3.2s antes)

# Teste 3: Re-run após alterar nome
# Esperado: Não reprocessar DOCX (instantâneo)
```

---

## 🎯 Métricas de Sucesso

### Técnicas
- ✅ Redução de 40-50% no tempo de geração
- ✅ Re-execuções 30x mais rápidas (cache)
- ✅ Zero OOM errors (validações)
- ✅ Zero timeouts (validações)

### Qualitativas
- ✅ Código mais limpo (constantes globais)
- ✅ UX profissional (progress bars)
- ✅ Mensagens claras (feedback ao usuário)
- ✅ Robustez aumentada (validações)

---

**Documento preparado por:** Claude Code (Orquestrador)
**Status:** ✅ Pronto para deployment de agentes
**Próximos passos:** Criar briefings detalhados para cada agente
