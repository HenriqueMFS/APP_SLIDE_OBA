# 🎯 BRIEFING: Agent-E - Constantes e Regex (Performance)

**Data:** 2025-11-18
**Projeto:** APP_SLIDE_OBA
**Feature:** F2-CONSTANTS-REGEX
**Prioridade:** 🟡 ALTA
**Estimativa:** 1-2 horas
**Ganho esperado:** 1.5x em extração de dados

---

## 📋 CONTEXTO DO PROJETO

Você é o **Agent-E**, responsável por refatorar aliases e regex para constantes globais pré-compiladas no projeto APP_SLIDE_OBA.

### Problema Identificado
A análise de performance (PERFORMANCE-ANALYSIS.md) identificou 2 problemas de ALTA prioridade:

1. **Aliases recalculados:** Dicionário com 50+ aliases é criado e normalizado para CADA tabela processada (5-10ms desperdiçados por tabela)
2. **Regex não compiladas:** Regex patterns recompilados a cada chamada de função (20-30% mais lento que deveria)

### Sua Missão
Refatorar código para usar constantes globais pré-processadas:
- ✅ Mover aliases para constantes globais (calculadas 1 vez)
- ✅ Normalizar aliases no carregamento do módulo
- ✅ Compilar regex patterns como constantes
- ✅ Atualizar funções para usar constantes

**Ganho esperado:** 1.5x mais rápido em extração de dados

---

## 🎯 ENTREGAS OBRIGATÓRIAS

### Entrega 1: Aliases como Constantes Globais
**Arquivo:** `APP.py`
**Linhas afetadas:** Topo do arquivo + `_identificar_colunas_tabela` (~176-336)
**Tempo:** 45-60 minutos

#### Problema Atual

Localizar função `_identificar_colunas_tabela` (linha ~176):

```python
def _identificar_colunas_tabela(cabecalho):
    """..."""
    # ... linhas 194-249 ...

    # ❌ PROBLEMA: Este dicionário é criado DENTRO da função
    # Recalculado para CADA tabela processada (5-10ms desperdiçados)
    aliases = {
        "Valido": [
            "valido", "alcance", "lancamentos validos", ...
        ],
        "Equipe": [
            "equipe", "nome equipe", "nome da equipe", ...
        ],
        # ... ~40 linhas de aliases ...
    }

    # ❌ PROBLEMA: Normalização feita para cada tabela
    aliases_norm = {
        campo: [normalizar_texto_base(alias) for alias in lista]
        for campo, lista in aliases.items()
    }

    # ❌ PROBLEMA: Lista criada dentro da função
    prioridade_campos = ["Valido", "Equipe", "Escola", ...]
```

**Por que é um problema:**
- Se documento tem 5 tabelas → aliases é criado e normalizado 5 vezes
- Normalização é operação cara: Unicode normalize + regex + lowercase
- Resultado é sempre idêntico (desperdício puro)

#### Solução Esperada

**PASSO 1: Adicionar constantes globais (APÓS linha 56, ANTES de "CONFIGURAÇÃO INICIAL"):**

```python
# -------------------- ALIASES DE CAMPOS --------------------
# Aliases para identificação de colunas em tabelas DOCX
# Cada campo pode ser identificado por múltiplos nomes/variações

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

def _normalizar_aliases():
    """
    Normaliza aliases uma única vez no carregamento do módulo.

    Percorre todos os aliases definidos em ALIASES_CAMPOS e aplica
    normalização de texto (remoção de acentos, lowercase, etc.) para
    criar versão pré-processada usada em matching.

    Returns:
        dict: Dicionário com aliases normalizados
              Estrutura: {campo: [alias_norm1, alias_norm2, ...]}

    Note:
        - Executada apenas 1 vez quando módulo é importado
        - Evita recalcular normalização para cada tabela
        - Ganho: 5-10ms por tabela processada
    """
    return {
        campo: [normalizar_texto_base(alias) for alias in lista]
        for campo, lista in ALIASES_CAMPOS.items()
    }

# Aliases normalizados (calculados uma vez no import do módulo)
ALIASES_NORMALIZADOS = _normalizar_aliases()

# Prioridade de campos para matching (ordem de tentativa)
PRIORIDADE_CAMPOS = [
    "Valido", "Equipe", "Escola", "Cidade", "Estado",
    "Aluno1", "Aluno2", "Aluno3", "Aluno4", "Aluno5"
]
```

**IMPORTANTE:** Você deve copiar EXATAMENTE todos os aliases que estão na função original. Use Read tool para ler a função `_identificar_colunas_tabela` e copiar os aliases completos.

**PASSO 2: Atualizar função `_identificar_colunas_tabela`:**

Localizar as linhas ~194-261 e **REMOVER COMPLETAMENTE** este bloco:

```python
# ❌ REMOVER TODO ESTE BLOCO (linhas ~194-261)
    aliases = {
        "Valido": ["valido", ...],
        # ... todo o dicionário ...
    }

    aliases_norm = {
        campo: [normalizar_texto_base(alias) for alias in lista]
        for campo, lista in aliases.items()
    }

    prioridade_campos = ["Valido", ...]
```

**SUBSTITUIR por apenas 2 linhas:**

```python
    # ✅ Usar constantes globais pré-normalizadas
    aliases_norm = ALIASES_NORMALIZADOS
    prioridade_campos = PRIORIDADE_CAMPOS
```

**Resultado:** Função `_identificar_colunas_tabela` fica ~60 linhas mais curta e 1.5x mais rápida!

**Validação:**
- [ ] ALIASES_CAMPOS criado no topo do arquivo
- [ ] Função `_normalizar_aliases()` criada
- [ ] ALIASES_NORMALIZADOS calculado no topo
- [ ] PRIORIDADE_CAMPOS definida no topo
- [ ] Linhas ~194-261 em `_identificar_colunas_tabela` removidas
- [ ] Função usa `ALIASES_NORMALIZADOS` e `PRIORIDADE_CAMPOS`

---

### Entrega 2: Compilação de Regex
**Arquivo:** `APP.py`
**Linhas afetadas:** Topo + `normalizar_texto_base` + outras funções com regex
**Tempo:** 30-40 minutos

#### Problema Atual

```python
# Em normalizar_texto_base (linha ~120)
def normalizar_texto_base(texto):
    # ...
    texto = re.sub(r"\s+", " ", texto).strip()  # ❌ Regex compilada a cada chamada
    return texto.lower()

# Em outras funções (se houver)
# re.sub(...), re.match(...), etc. com patterns literais
```

**Por que é um problema:**
- Python compila regex pattern a cada chamada de `re.sub`
- Compilação tem custo (parsing do pattern)
- Pattern é sempre idêntico (desperdício)
- **Ganho potencial:** 20-30% em operações de regex

#### Solução Esperada

**PASSO 1: Adicionar regex compiladas (APÓS PRIORIDADE_CAMPOS, ANTES de CONFIGURAÇÃO INICIAL):**

```python
# -------------------- REGEX COMPILADAS --------------------
# Compilar regex patterns uma vez para melhor performance

import re  # ✅ Mover import para cá se não estiver no topo

# Regex para normalização de texto
REGEX_WHITESPACE = re.compile(r"\s+")
REGEX_NON_ALPHANUMERIC = re.compile(r"[^a-z0-9]+")

# Regex para formatação de nomes de arquivo
REGEX_INVALID_FILENAME_CHARS = re.compile(r'[\\/:*?"<>|]')

# Regex para extração de alcance (se existir no código)
REGEX_ALCANCE = re.compile(r"(ALCANCE:\s*)([\d,.]+ m)", re.IGNORECASE)
```

**PASSO 2: Atualizar função `normalizar_texto_base` (linha ~120):**

Localizar:
```python
def normalizar_texto_base(texto):
    """..."""
    if not texto:
        return ""
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(ch for ch in texto if not unicodedata.combining(ch))
    texto = re.sub(r"\s+", " ", texto).strip()  # ❌ LINHA A MODIFICAR
    return texto.lower()
```

Substituir por:
```python
def normalizar_texto_base(texto):
    """
    Normaliza texto removendo acentos e caracteres especiais.

    Converte texto para forma normalizada Unicode (NFKD), remove
    caracteres de combinação (acentos), normaliza espaços em branco
    e converte para lowercase.

    Args:
        texto: Texto a ser normalizado (pode ser str, int, etc.)

    Returns:
        str: Texto normalizado (lowercase, sem acentos, espaços únicos)

    Examples:
        >>> normalizar_texto_base("São Paulo")
        'sao paulo'
        >>> normalizar_texto_base("  múltiplos   espaços  ")
        'multiplos espacos'

    Note:
        - Usa REGEX_WHITESPACE pré-compilada para performance
        - 20-30% mais rápido que re.sub com pattern literal
    """
    if not texto:
        return ""
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(ch for ch in texto if not unicodedata.combining(ch))
    texto = REGEX_WHITESPACE.sub(" ", texto).strip()  # ✅ Usa regex compilada
    return texto.lower()
```

**PASSO 3: Buscar outras funções que usam regex:**

Usar Grep tool para encontrar todas as ocorrências de `re.sub`, `re.match`, `re.search`:

```bash
# Buscar funções que usam regex
grep -n "re\\.sub\\|re\\.match\\|re\\.search" APP.py
```

**Funções candidatas para otimização:**
1. `formatar_nome_arquivo` - se usar regex para remover caracteres inválidos
2. `replace_placeholders_in_shape` - se usar regex para detectar placeholders
3. Qualquer outra função que use patterns literais

**Atualizar cada função encontrada:**

Exemplo (se `formatar_nome_arquivo` existir):
```python
# ❌ ANTES
def formatar_nome_arquivo(nome):
    return re.sub(r'[\\/:*?"<>|]', '_', nome)

# ✅ DEPOIS
def formatar_nome_arquivo(nome):
    """
    Remove caracteres inválidos de nome de arquivo.

    Args:
        nome (str): Nome do arquivo original

    Returns:
        str: Nome sanitizado (caracteres inválidos substituídos por '_')
    """
    return REGEX_INVALID_FILENAME_CHARS.sub('_', nome)
```

**Validação:**
- [ ] Regex compiladas adicionadas no topo (REGEX_WHITESPACE, etc.)
- [ ] `normalizar_texto_base` usa `REGEX_WHITESPACE.sub`
- [ ] Outras funções atualizadas para usar regex compiladas
- [ ] Docstrings atualizadas mencionando performance
- [ ] Teste: Funcionamento idêntico ao anterior

---

## 🔧 PROCEDIMENTOS OBRIGATÓRIOS

### 1. Preparação Inicial (10 min)

```bash
# 1. Verificar branch atual
git status
git branch --show-current

# 2. Criar e trocar para sua branch
SESSION_ID="SUBSTITUA_PELO_SEU_SESSION_ID"
git checkout -b claude/perf-constants-regex-${SESSION_ID}

# 3. Verificar que está na branch correta
git branch --show-current
# Deve mostrar: claude/perf-constants-regex-XXXXX

# 4. Ler função _identificar_colunas_tabela COMPLETA
# IMPORTANTE: Você DEVE copiar os aliases exatos da função original
```

### 2. Implementação (60-90 min)

**ORDEM DE IMPLEMENTAÇÃO:**

#### Passo 1: Ler aliases originais (10 min)
```bash
# Use Read tool para ler linhas 176-336 de APP.py
# Copie EXATAMENTE todos os aliases
```

#### Passo 2: Criar constantes globais (20-25 min)
1. Adicionar seção de ALIASES (após linha 56)
2. Copiar aliases da função original para ALIASES_CAMPOS
3. Criar função `_normalizar_aliases()`
4. Definir ALIASES_NORMALIZADOS e PRIORIDADE_CAMPOS
5. Testar: Executar Python e importar APP.py (deve importar sem erros)

#### Passo 3: Atualizar _identificar_colunas_tabela (10-15 min)
1. Localizar linhas ~194-261 (bloco de aliases)
2. Deletar bloco completo
3. Adicionar 2 linhas usando constantes globais
4. Verificar indentação
5. Testar: Função deve executar normalmente

#### Passo 4: Adicionar regex compiladas (10-15 min)
1. Criar seção de REGEX (após PRIORIDADE_CAMPOS)
2. Definir todas as regex compiladas
3. Testar: Importar APP.py sem erros

#### Passo 5: Atualizar funções com regex (15-20 min)
1. Buscar funções que usam `re.sub`, `re.match`, etc.
2. Atualizar `normalizar_texto_base` primeiro
3. Atualizar outras funções encontradas
4. Atualizar docstrings
5. Testar cada função modificada

### 3. Testes de Validação (15-20 min)

**Checklist de Testes:**

```python
# Teste 1: Importação do módulo
import importlib
import APP
importlib.reload(APP)
# ✅ Deve importar sem erros

# Teste 2: Constantes definidas
print(APP.ALIASES_CAMPOS)
print(APP.ALIASES_NORMALIZADOS)
print(APP.PRIORIDADE_CAMPOS)
# ✅ Devem existir e estar corretas

# Teste 3: Normalização funciona
from APP import normalizar_texto_base
result = normalizar_texto_base("São Paulo")
assert result == "sao paulo"
# ✅ Deve retornar "sao paulo"

# Teste 4: Regex compiladas
print(type(APP.REGEX_WHITESPACE))
# ✅ Deve ser <class 're.Pattern'>

# Teste 5: Extração completa (END-TO-END)
# - Upload DOCX de teste
# - Verificar que equipes são extraídas corretamente
# - Performance deve ser melhor
# ✅ Deve funcionar identicamente ao código original
```

### 4. Commits e Push (15 min)

```bash
# Commit 1: Aliases como constantes
git add APP.py
git commit -m "perf: Mover aliases para constantes globais

- Criar ALIASES_CAMPOS com todos os aliases de campos
- Implementar _normalizar_aliases() para pré-processar
- Definir ALIASES_NORMALIZADOS e PRIORIDADE_CAMPOS
- Remover aliases locais de _identificar_colunas_tabela
- Ganho: 1.5x mais rápido (5-10ms por tabela economizados)"

# Commit 2: Regex compiladas
git add APP.py
git commit -m "perf: Compilar regex patterns como constantes

- Criar REGEX_WHITESPACE, REGEX_NON_ALPHANUMERIC, etc.
- Atualizar normalizar_texto_base para usar regex compilada
- Atualizar outras funções que usam regex
- Ganho: 20-30% mais rápido em operações de regex"

# Commit 3: Report final
git add REPORT-AGENT-E.md
git commit -m "docs: Report final do Agent-E (Constantes e Regex)"

# Push para remote
git push -u origin claude/perf-constants-regex-${SESSION_ID}
```

---

## 📊 REPORT FINAL OBRIGATÓRIO

Criar arquivo `REPORT-AGENT-E.md`:

```markdown
# 📊 Report Final - Agent-E (Constantes e Regex)

**Data conclusão:** YYYY-MM-DD HH:MM
**Branch:** claude/perf-constants-regex-{SESSION_ID}
**Status:** ✅ CONCLUÍDO | ⚠️ PARCIAL | ❌ BLOQUEADO

---

## ✅ Entregas Concluídas

- [x] ALIASES_CAMPOS criado no topo do arquivo
- [x] Função _normalizar_aliases() implementada
- [x] ALIASES_NORMALIZADOS calculado
- [x] PRIORIDADE_CAMPOS definida
- [x] _identificar_colunas_tabela refatorada (aliases removidos)
- [x] REGEX_WHITESPACE e outras regex compiladas
- [x] normalizar_texto_base usa regex compilada
- [x] Outras funções atualizadas (listar quais)
- [x] Testes de validação executados
- [x] Commits e push realizados

## 📈 Resultados de Performance

### Aliases como Constantes
- **Antes:** Aliases criados e normalizados N vezes (N = num tabelas)
- **Depois:** Aliases criados 1 vez no import
- **Ganho:** 1.5x mais rápido em extração de dados

### Regex Compiladas
- **Antes:** Pattern compilado a cada chamada
- **Depois:** Pattern compilado 1 vez no import
- **Ganho:** 20-30% em operações de regex

## 🧪 Testes Executados

1. ✅ Importação do módulo sem erros
2. ✅ Constantes ALIASES_* definidas corretamente
3. ✅ normalizar_texto_base funciona igual
4. ✅ Regex compiladas funcionam corretamente
5. ✅ Extração END-TO-END funciona normalmente

## 📝 Commits Realizados

1. ✅ perf: Mover aliases para constantes globais
2. ✅ perf: Compilar regex patterns
3. ✅ docs: Report final Agent-E

**Total:** 3 commits
**Push status:** ✅ Sucesso

## 📊 Estatísticas de Refatoração

- **Linhas removidas:** ~60-70 (aliases duplicados)
- **Linhas adicionadas:** ~80-90 (constantes globais)
- **Funções otimizadas:** X (listar)
- **Regex compiladas:** 4 (WHITESPACE, NON_ALPHANUMERIC, INVALID_FILENAME, ALCANCE)

## ⚠️ Problemas Encontrados

(Liste qualquer problema ou decisão técnica)

## 💡 Observações

(Observações para o orquestrador)

---

**Assinatura:** Agent-E
**Commit final:** {HASH}
**Pronto para merge:** ✅ SIM | ❌ NÃO
```

---

## ⚠️ AVISOS CRÍTICOS

### ❌ NÃO FAÇA ISSO:
- ❌ NÃO modificar função `carregar_logo` ou `extrair_dados_cached` (são do Agent-D)
- ❌ NÃO modificar função `gerar_apresentacao` internamente (é do Agent-F)
- ❌ NÃO alterar lógica de matching de colunas (apenas refatorar constantes)
- ❌ NÃO adicionar novos aliases ou remover aliases existentes
- ❌ NÃO modificar ordem de PRIORIDADE_CAMPOS

### ✅ FAÇA ISSO:
- ✅ Copie EXATAMENTE todos os aliases da função original
- ✅ Mantenha indentação e formatação consistentes
- ✅ Teste que matching de colunas funciona igual
- ✅ Adicione docstrings completas
- ✅ Reporte qualquer divergência no REPORT

---

## 🆘 TROUBLESHOOTING

### Problema: Aliases não são encontrados (erro de identificação de colunas)
**Solução:**
1. Verificar que TODOS os aliases foram copiados da função original
2. Verificar que normalização está sendo aplicada corretamente
3. Adicionar print debug: `print(ALIASES_NORMALIZADOS)`
4. Comparar com aliases originais

### Problema: Erro "name 'REGEX_WHITESPACE' is not defined"
**Solução:**
1. Verificar que regex foi definida ANTES de ser usada
2. Verificar que está no escopo global (não dentro de função)
3. Verificar indentação (deve estar no nível mais externo)

### Problema: Performance não melhorou
**Solução:**
1. Verificar que função realmente usa constantes (não recria aliases)
2. Verificar que regex compilada está sendo usada
3. Medir com `time.time()` antes/depois
4. Reportar medições no REPORT

---

## 📚 RECURSOS DE REFERÊNCIA

- **FEATURES-PARALLEL-WAVE-2.md:** Suas entregas detalhadas
- **PERFORMANCE-ANALYSIS.md:** Problema 2.1 (aliases) e 4.2 (regex)
- **APP.py linhas 176-336:** Função `_identificar_colunas_tabela` original
- **Python re docs:** https://docs.python.org/3/library/re.html#re.compile

---

## ✅ CHECKLIST FINAL

- [ ] ALIASES_CAMPOS com TODOS os aliases originais
- [ ] ALIASES_NORMALIZADOS calculado corretamente
- [ ] PRIORIDADE_CAMPOS definida
- [ ] _identificar_colunas_tabela usa constantes (aliases removidos)
- [ ] Regex compiladas (WHITESPACE, NON_ALPHANUMERIC, etc.)
- [ ] normalizar_texto_base usa REGEX_WHITESPACE.sub
- [ ] Outras funções atualizadas para usar regex compiladas
- [ ] Todos os testes passaram
- [ ] 3 commits realizados
- [ ] Push realizado
- [ ] REPORT-AGENT-E.md criado

---

**Boa sorte, Agent-E! Sua refatoração vai eliminar recalculações desperdiçadas! 🚀**

**Em caso de dúvidas:** Leia função original completa antes de começar
**Em caso de bloqueio:** Documente no REPORT
