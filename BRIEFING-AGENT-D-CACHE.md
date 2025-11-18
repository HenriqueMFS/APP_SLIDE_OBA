# 🎯 BRIEFING: Agent-D - Cache e Validações (Performance)

**Data:** 2025-11-18
**Projeto:** APP_SLIDE_OBA
**Feature:** F1-CACHE-VALIDATION
**Prioridade:** 🔴 CRÍTICA
**Estimativa:** 2-3 horas
**Ganho esperado:** 30-40% de performance

---

## 📋 CONTEXTO DO PROJETO

Você é o **Agent-D**, responsável por implementar otimizações de cache e validações de arquivo no projeto APP_SLIDE_OBA. Este é um projeto Streamlit que gera apresentações PowerPoint automatizadas.

### Problema Identificado
A análise de performance (PERFORMANCE-ANALYSIS.md) identificou 3 problemas CRÍTICOS que você resolverá:

1. **Logo carregado sem cache:** 20-50ms desperdiçados a cada interação (30x mais lento que deveria)
2. **Dados extraídos sem cache:** Reprocessamento completo em cada re-run do Streamlit (0.5-2.5s desperdiçados)
3. **Sem validação de tamanho:** Risco de crashes por OOM com arquivos grandes

### Sua Missão
Implementar caching inteligente e validações preventivas para:
- ✅ Reduzir tempo de re-execução em 30x (logo)
- ✅ Evitar reprocessamento desnecessário (dados)
- ✅ Prevenir crashes e timeouts (validações)

---

## 🎯 ENTREGAS OBRIGATÓRIAS

### Entrega 1: Cache de Logo
**Arquivo:** `APP.py`
**Linhas:** ~59-61
**Tempo:** 15-20 minutos

#### Código Atual (PROBLEMA)
```python
# APP.py linha 59-61
logo = Image.open(LOGO_PATH)
resample_filter = getattr(Image, "Resampling", Image).LANCZOS
logo = logo.resize((LOGO_WIDTH, LOGO_HEIGHT), resample_filter)
```

**Por que é um problema:**
- Streamlit re-executa o script inteiro a cada interação (click, input, etc.)
- Logo é carregado do disco, decodificado e redimensionado 50-100 vezes em uma sessão típica
- Operação de resize com LANCZOS é computacionalmente cara
- **Tempo desperdiçado:** 20-50ms por interação → 2-5 segundos acumulados

#### Solução Esperada

**1. Criar função com cache ANTES da linha 58:**
```python
# -------------------- FUNÇÕES DE CACHE --------------------
@st.cache_resource
def carregar_logo():
    """
    Carrega e redimensiona logo uma única vez por sessão.

    Usa @st.cache_resource para cachear o objeto Image na memória,
    evitando recarregamento em cada re-run do Streamlit.

    Returns:
        PIL.Image: Logo redimensionada para dimensões configuradas

    Note:
        - Cache persiste durante toda a sessão Streamlit
        - Logo é carregada apenas 1 vez mesmo com múltiplas interações
        - Economiza 20-50ms por re-execução
    """
    logo_img = Image.open(LOGO_PATH)
    resample_filter = getattr(Image, "Resampling", Image).LANCZOS
    return logo_img.resize((LOGO_WIDTH, LOGO_HEIGHT), resample_filter)
```

**2. Atualizar linha 59-61 para:**
```python
# -------------------- CONFIGURAÇÃO INICIAL --------------------
st.set_page_config(layout=PAGE_LAYOUT)
logo = carregar_logo()  # ✅ Agora cached!
_, col_logo, _ = st.columns(COLUMN_PROPORTIONS)
```

**Validação:**
- [ ] Função `carregar_logo()` criada com decorador `@st.cache_resource`
- [ ] Docstring completa explicando o cache
- [ ] Linhas 59-61 atualizadas para usar `carregar_logo()`
- [ ] Teste: Logo carrega 1 vez por sessão (verificar console Streamlit)

---

### Entrega 2: Cache de Extração de Dados
**Arquivo:** `APP.py`
**Localização:** Após função `extrair_dados` (linha ~550)
**Tempo:** 30-40 minutos

#### Código Atual (PROBLEMA)
```python
# Interface Streamlit (linha ~870)
if st.button("✨ Gerar Apresentação"):
    if not docx_file or not pptx_file:
        st.warning(MSG_SEND_BOTH_FILES)
    else:
        dados = extrair_dados(docx_file)  # ❌ Reprocessa sempre
```

**Por que é um problema:**
- `extrair_dados` processa DOCX completo: parse XML, extrai tabelas, normaliza textos
- Usuário pode alterar nome do arquivo ou ajustar template → Streamlit re-executa
- **Tempo desperdiçado:** 0.5-2.5s em cada re-run mesmo sem alterar DOCX

#### Solução Esperada

**1. Criar função cached APÓS `extrair_dados` (linha ~550):**
```python
@st.cache_data(show_spinner="📊 Extraindo dados do DOCX...")
def extrair_dados_cached(docx_bytes):
    """
    Versão cached de extrair_dados para evitar reprocessamento.

    Cacheia o resultado da extração baseado no conteúdo (bytes) do arquivo.
    Se o mesmo arquivo for enviado novamente, retorna resultado do cache
    sem reprocessar.

    Args:
        docx_bytes (bytes): Conteúdo completo do arquivo DOCX em bytes

    Returns:
        dict: Dados extraídos organizados por equipe
              Estrutura: {nome_equipe: {Valido, Equipe, Escola, ...}}

    Note:
        - @st.cache_data usa hash dos bytes como chave de cache
        - Alteração no arquivo = novo hash = reprocessamento
        - Mesmo arquivo = mesmo hash = cache hit
        - show_spinner mostra mensagem durante processamento
    """
    from io import BytesIO
    return extrair_dados(BytesIO(docx_bytes))
```

**2. Localizar a interface (linha ~865-885) e atualizar:**

ENCONTRE este código:
```python
docx_file = st.file_uploader(
    "📄 Tabela de Dados (.docx)",
    type="docx",
    help="Arquivo contendo os dados das equipes."
)
pptx_file = st.file_uploader(
    "🎨 Template de Slide (.pptx)",
    type="pptx",
    help="Modelo do slide que será duplicado."
)
```

ADICIONE logo APÓS os uploaders:
```python
# Pré-processar DOCX para cache (se arquivo foi enviado)
dados = None
if docx_file is not None:
    # Lê arquivo uma vez e converte para bytes
    docx_bytes = docx_file.read()
    docx_file.seek(0)  # Reset pointer para outras operações

    # Extrai dados usando versão cached
    dados = extrair_dados_cached(docx_bytes)

    # Feedback ao usuário
    if dados:
        st.success(f"✅ {len(dados)} equipes encontradas no DOCX")
    else:
        st.error(MSG_NO_DATA_FOUND)
```

**3. Atualizar botão de geração (linha ~870-885):**

ENCONTRE:
```python
if st.button("✨ Gerar Apresentação"):
    if not docx_file or not pptx_file:
        st.warning(MSG_SEND_BOTH_FILES)
    else:
        dados = extrair_dados(docx_file)  # ❌ REMOVER esta linha
```

SUBSTITUA por:
```python
if st.button("✨ Gerar Apresentação"):
    if not docx_file or not pptx_file:
        st.warning(MSG_SEND_BOTH_FILES)
    elif not dados:  # ✅ Usa dados já extraídos
        st.error(MSG_NO_DATA_FOUND)
    else:
        # dados já foi extraído e cacheado acima
```

**Validação:**
- [ ] Função `extrair_dados_cached(docx_bytes)` criada
- [ ] Decorador `@st.cache_data(show_spinner="...")` aplicado
- [ ] Interface atualizada para ler bytes e usar cache
- [ ] Mensagem de sucesso mostra número de equipes
- [ ] Teste: Upload mesmo arquivo 2x → 2ª vez instantâneo

---

### Entrega 3: Validação de Tamanho de Arquivos
**Arquivo:** `APP.py`
**Localização:** Constantes + nova função + interface
**Tempo:** 30-40 minutos

#### Problema
- Usuário pode enviar arquivo DOCX de 100 MB ou PPTX de 500 MB
- Streamlit tenta processar sem limites → timeout ou OOM crash
- Feedback vem tarde demais (após timeout)

#### Solução Esperada

**1. Adicionar constantes (APÓS linha 56, antes de XML_NAMESPACE):**
```python
# -------------------- LIMITES DE ARQUIVO --------------------
MAX_DOCX_SIZE_MB = 10  # Máximo 10 MB para DOCX
MAX_PPTX_SIZE_MB = 20  # Máximo 20 MB para PPTX
MAX_EQUIPES = 500      # Máximo de equipes suportadas
```

**2. Criar função de validação (APÓS `formatar_texto`, linha ~115):**
```python
def validar_tamanho_arquivo(uploaded_file, max_size_mb, tipo):
    """
    Valida tamanho de arquivo antes de processar.

    Verifica se arquivo enviado está dentro do limite permitido para
    prevenir timeouts e crashes por falta de memória.

    Args:
        uploaded_file: Objeto UploadedFile do Streamlit (ou None)
        max_size_mb (int): Tamanho máximo permitido em megabytes
        tipo (str): Tipo do arquivo para mensagem de erro (ex: "DOCX", "PPTX")

    Returns:
        tuple: (bool válido, str mensagem_erro)
               - (True, "") se válido ou arquivo None
               - (False, "mensagem") se excede tamanho

    Examples:
        >>> valid, msg = validar_tamanho_arquivo(docx_file, 10, "DOCX")
        >>> if not valid:
        >>>     st.error(msg)
    """
    if not uploaded_file:
        return True, ""

    # Obtém tamanho do arquivo
    uploaded_file.seek(0, 2)  # Seek to end
    size_bytes = uploaded_file.tell()
    uploaded_file.seek(0)  # Reset to beginning

    size_mb = size_bytes / (1024 * 1024)

    if size_mb > max_size_mb:
        return False, (
            f"❌ Arquivo {tipo} muito grande: {size_mb:.1f} MB\n"
            f"Tamanho máximo permitido: {max_size_mb} MB\n"
            f"💡 Dica: Reduza o número de linhas ou remova imagens pesadas do arquivo."
        )

    return True, ""
```

**3. Atualizar interface - adicionar validações DENTRO do botão:**

ENCONTRE o botão (linha ~870):
```python
if st.button("✨ Gerar Apresentação"):
    if not docx_file or not pptx_file:
        st.warning(MSG_SEND_BOTH_FILES)
    elif not dados:
        st.error(MSG_NO_DATA_FOUND)
    else:
        # Código de geração aqui...
```

SUBSTITUA por:
```python
if st.button("✨ Gerar Apresentação"):
    if not docx_file or not pptx_file:
        st.warning(MSG_SEND_BOTH_FILES)
    else:
        # ✅ VALIDAÇÕES DE TAMANHO (adicionar ANTES de processar)
        valid_docx, msg_docx = validar_tamanho_arquivo(
            docx_file, MAX_DOCX_SIZE_MB, "DOCX"
        )
        valid_pptx, msg_pptx = validar_tamanho_arquivo(
            pptx_file, MAX_PPTX_SIZE_MB, "PPTX"
        )

        # Validação de número de equipes
        valid_num_equipes = True
        msg_num_equipes = ""
        if dados and len(dados) > MAX_EQUIPES:
            valid_num_equipes = False
            msg_num_equipes = (
                f"❌ Muitas equipes: {len(dados)}\n"
                f"Máximo suportado: {MAX_EQUIPES} equipes\n"
                f"💡 Dica: Divida o arquivo em lotes menores."
            )

        # Exibe erros de validação
        if not valid_docx:
            st.error(msg_docx)
        elif not valid_pptx:
            st.error(msg_pptx)
        elif not dados:
            st.error(MSG_NO_DATA_FOUND)
        elif not valid_num_equipes:
            st.error(msg_num_equipes)
        else:
            # ✅ Todas validações passaram, prossegue com geração
            # (código de geração existente continua aqui)
```

**Validação:**
- [ ] Constantes MAX_DOCX_SIZE_MB, MAX_PPTX_SIZE_MB, MAX_EQUIPES adicionadas
- [ ] Função `validar_tamanho_arquivo` criada com docstring
- [ ] Validações aplicadas ANTES de processar
- [ ] Mensagens de erro claras e com dicas
- [ ] Teste: Arquivo >10MB DOCX é rejeitado com mensagem clara
- [ ] Teste: Arquivo >20MB PPTX é rejeitado com mensagem clara

---

## 🔧 PROCEDIMENTOS OBRIGATÓRIOS

### 1. Preparação Inicial (10 min)

```bash
# 1. Verificar branch atual
git status
git branch --show-current

# 2. Criar e trocar para sua branch
SESSION_ID="SUBSTITUA_PELO_SEU_SESSION_ID"
git checkout -b claude/perf-cache-validation-${SESSION_ID}

# 3. Verificar que está na branch correta
git branch --show-current
# Deve mostrar: claude/perf-cache-validation-XXXXX

# 4. Ler os arquivos necessários
# - APP.py (para entender estrutura)
# - FEATURES-PARALLEL-WAVE-2.md (suas entregas detalhadas)
# - PERFORMANCE-ANALYSIS.md (contexto do problema)
```

### 2. Implementação (90-120 min)

**ORDEM DE IMPLEMENTAÇÃO (importante para evitar quebrar código):**

#### Passo 1: Cache de Logo (15-20 min)
1. Localizar linha 58-61 (configuração inicial)
2. Criar seção de funções de cache ANTES da linha 58
3. Criar função `carregar_logo()` com `@st.cache_resource`
4. Atualizar linha 59 para usar `carregar_logo()`
5. Testar: Executar Streamlit e verificar que logo aparece
6. Verificar console: "Cache miss" na 1ª vez, "Cache hit" nas próximas

#### Passo 2: Cache de Extração (30-40 min)
1. Localizar função `extrair_dados` (linha ~494-550)
2. Criar função `extrair_dados_cached` APÓS ela
3. Localizar file uploaders na interface (linha ~865)
4. Adicionar pré-processamento após uploaders
5. Atualizar botão de geração para usar `dados` já extraídos
6. Testar: Upload DOCX 2x → 2ª vez deve ser instantâneo

#### Passo 3: Validações (30-40 min)
1. Adicionar constantes MAX_* (linha ~56)
2. Criar função `validar_tamanho_arquivo` (após `formatar_texto`)
3. Atualizar botão de geração com validações
4. Testar validações com arquivo pequeno (deve passar)
5. Testar com mensagem de erro clara

### 3. Testes de Validação (20-30 min)

**Checklist de Testes Obrigatórios:**

```bash
# Teste 1: Cache de Logo
# - Executar: streamlit run APP.py
# - Ação: Clicar em algum botão/input várias vezes
# - Verificar console: Logo NÃO é recarregado
# ✅ Esperado: "carregar_logo() - Cache hit" no console

# Teste 2: Cache de Extração
# - Upload DOCX
# - Ver mensagem "✅ X equipes encontradas"
# - Alterar campo de texto (nome arquivo)
# - Verificar que DOCX NÃO é reprocessado
# ✅ Esperado: Instantâneo, sem spinner de extração

# Teste 3: Validação DOCX Grande
# - Criar DOCX fake >10MB ou usar arquivo grande
# - Fazer upload
# - Clicar "Gerar Apresentação"
# ✅ Esperado: Erro "Arquivo DOCX muito grande: X MB"

# Teste 4: Validação PPTX Grande
# - Criar PPTX fake >20MB
# - Fazer upload
# - Clicar "Gerar Apresentação"
# ✅ Esperado: Erro "Arquivo PPTX muito grande: X MB"

# Teste 5: Fluxo Completo Normal
# - Upload DOCX pequeno (<10MB)
# - Upload PPTX pequeno (<20MB)
# - Gerar apresentação
# ✅ Esperado: Funciona normalmente, mais rápido
```

### 4. Commits e Push (15-20 min)

```bash
# IMPORTANTE: Fazer commits incrementais, NÃO um único commit

# Commit 1: Cache de logo
git add APP.py
git commit -m "perf: Implementar cache de logo com @st.cache_resource

- Criar função carregar_logo() com cache
- Reduz tempo de re-execução em 30x (20-50ms → <1ms)
- Logo carregada apenas 1 vez por sessão Streamlit
- Ganho: 2-5 segundos economizados em sessão típica"

# Commit 2: Cache de extração
git add APP.py
git commit -m "perf: Implementar cache de extração de dados DOCX

- Criar extrair_dados_cached() com @st.cache_data
- Pré-processar DOCX após upload
- Evita reprocessamento em re-runs do Streamlit
- Ganho: 0.5-2.5s economizados por re-run"

# Commit 3: Validações
git add APP.py
git commit -m "perf: Adicionar validações de tamanho de arquivo

- Implementar validar_tamanho_arquivo()
- Limites: 10MB DOCX, 20MB PPTX, 500 equipes
- Previne timeouts e crashes por OOM
- Mensagens de erro claras com dicas ao usuário"

# Commit 4: Report final
git add REPORT-AGENT-D.md
git commit -m "docs: Report final do Agent-D (Cache e Validações)"

# Push para remote
git push -u origin claude/perf-cache-validation-${SESSION_ID}

# IMPORTANTE: Se push falhar com erro 403
# Tente novamente após 2 segundos (pode ser throttling)
# Se persistir após 4 tentativas, reporte no REPORT
```

---

## 📊 REPORT FINAL OBRIGATÓRIO

Ao concluir, criar arquivo `REPORT-AGENT-D.md`:

```markdown
# 📊 Report Final - Agent-D (Cache e Validações)

**Data conclusão:** YYYY-MM-DD HH:MM
**Branch:** claude/perf-cache-validation-{SESSION_ID}
**Status:** ✅ CONCLUÍDO | ⚠️ PARCIAL | ❌ BLOQUEADO

---

## ✅ Entregas Concluídas

- [x] Cache de logo com @st.cache_resource
- [x] Cache de extração de dados com @st.cache_data
- [x] Validação de tamanho DOCX (10MB)
- [x] Validação de tamanho PPTX (20MB)
- [x] Validação de número de equipes (500)
- [x] Mensagens de erro claras
- [x] Testes de validação executados
- [x] Commits e push realizados

## 📈 Resultados de Performance

### Cache de Logo
- **Antes:** 20-50ms por re-execução
- **Depois:** <1ms (cache hit)
- **Ganho:** 30x mais rápido

### Cache de Extração
- **Antes:** 0.5-2.5s por re-run
- **Depois:** <10ms (cache hit)
- **Ganho:** 100-250x mais rápido em re-runs

### Validações
- [x] DOCX >10MB rejeitado
- [x] PPTX >20MB rejeitado
- [x] >500 equipes rejeitado
- [x] Mensagens claras exibidas

## 🧪 Testes Executados

1. ✅ Cache de logo funcionando (verificado no console)
2. ✅ Cache de extração funcionando (re-run instantâneo)
3. ✅ Validação DOCX grande (erro exibido)
4. ✅ Validação PPTX grande (erro exibido)
5. ✅ Fluxo completo normal (geração funciona)

## 📝 Commits Realizados

1. ✅ perf: Implementar cache de logo
2. ✅ perf: Implementar cache de extração
3. ✅ perf: Adicionar validações de tamanho
4. ✅ docs: Report final Agent-D

**Total:** 4 commits
**Push status:** ✅ Sucesso

## ⚠️ Problemas Encontrados

(Liste qualquer problema, bloqueio ou decisão técnica tomada)

Exemplos:
- Nenhum problema encontrado
- [Se houver] Conflito em linha X resolvido com estratégia Y

## 💡 Observações

(Adicione qualquer observação relevante para o orquestrador)

Exemplos:
- Cache funciona perfeitamente em desenvolvimento
- Validações podem ser ajustadas conforme necessidade
- Performance medida: 40% mais rápido em testes

---

**Assinatura:** Agent-D
**Commit final:** {HASH DO ÚLTIMO COMMIT}
**Pronto para merge:** ✅ SIM | ❌ NÃO (explicar por quê)
```

---

## ⚠️ AVISOS CRÍTICOS

### ❌ NÃO FAÇA ISSO:
- ❌ NÃO mexer em funções que não foram mencionadas neste briefing
- ❌ NÃO alterar constantes de fontes, cores, placeholders
- ❌ NÃO modificar função `_identificar_colunas_tabela` (é do Agent-E)
- ❌ NÃO modificar função `gerar_apresentacao` internamente (é do Agent-F)
- ❌ NÃO remover docstrings ou comentários existentes
- ❌ NÃO fazer refatorações além do escopo

### ✅ FAÇA ISSO:
- ✅ Siga exatamente as linhas indicadas neste briefing
- ✅ Adicione docstrings completas em todas as novas funções
- ✅ Teste cada entrega antes de commitar
- ✅ Faça commits incrementais (não um único commit gigante)
- ✅ Relate qualquer problema no REPORT-AGENT-D.md
- ✅ Peça ajuda se encontrar bloqueio

---

## 🆘 TROUBLESHOOTING

### Problema: Streamlit não encontra @st.cache_resource
**Solução:** Verificar versão Streamlit >= 1.18
```bash
pip show streamlit
# Se < 1.18, atualizar: pip install streamlit>=1.51.0
```

### Problema: Cache não funciona (sempre recarrega)
**Solução:**
1. Verificar decorador está acima da função (não abaixo)
2. Verificar indentação correta
3. Limpar cache Streamlit: Clicar "Clear cache" na interface

### Problema: Push falha com 403
**Solução:**
1. Verificar que branch começa com `claude/`
2. Verificar que branch termina com session ID correto
3. Tentar novamente após 2 segundos
4. Se persistir, reportar no REPORT

### Problema: Validação não funciona (arquivo grande passa)
**Solução:**
1. Verificar que `uploaded_file.seek(0, 2)` está sendo executado
2. Verificar cálculo: `size_bytes / (1024 * 1024)`
3. Adicionar print debug: `print(f"Tamanho: {size_mb:.2f} MB")`

---

## 📚 RECURSOS DE REFERÊNCIA

- **FEATURES-PARALLEL-WAVE-2.md:** Suas entregas detalhadas
- **PERFORMANCE-ANALYSIS.md:** Contexto e análise completa
- **APP.py atual:** Código base para modificação
- **Streamlit Cache Docs:** https://docs.streamlit.io/library/advanced-features/caching

---

## ✅ CHECKLIST FINAL

Antes de marcar como concluído, verificar:

- [ ] Função `carregar_logo()` criada com `@st.cache_resource`
- [ ] Função `extrair_dados_cached()` criada com `@st.cache_data`
- [ ] Função `validar_tamanho_arquivo()` criada com docstring
- [ ] Constantes MAX_DOCX_SIZE_MB, MAX_PPTX_SIZE_MB, MAX_EQUIPES adicionadas
- [ ] Interface atualizada para usar cache e validações
- [ ] Todos os 5 testes executados e passaram
- [ ] 4 commits realizados (cache logo, cache dados, validações, report)
- [ ] Push realizado com sucesso
- [ ] REPORT-AGENT-D.md criado e commitado
- [ ] Branch pronta para merge

---

**Boa sorte, Agent-D! Sua missão é crítica para o sucesso da Wave-2! 🚀**

**Em caso de dúvidas:** Consulte FEATURES-PARALLEL-WAVE-2.md ou PERFORMANCE-ANALYSIS.md
**Em caso de bloqueio:** Documente no REPORT e siga até onde conseguir
