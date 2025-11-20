# Análise de Naming - Semana 2 (TEAM 1)

**Data:** 2025-11-20
**Responsável:** Agent-CLEAN-01, 02, 03, 04
**Branch:** `claude/analyze-repository-structure-011CV26eM3noi2SbsiDZJGqW`

---

## 📋 Problemas Identificados

### 1. Variáveis Não Descritivas (Agent-CLEAN-01)

#### ❌ Problema: Nomes de 1-2 caracteres

| Atual | Deveria Ser | Localização | Motivo |
|-------|-------------|-------------|---------|
| `r` | `registro` | `_organizar_dados_equipes()` | Nome genérico, não indica que é um registro de equipe |
| `m` | `membro` | `_organizar_dados_equipes()` | Nome genérico, não indica que é um membro da equipe |
| `p` | `paragrafo` | `replace_placeholders_in_shape()` | Nome genérico, não indica que é um parágrafo do PowerPoint |
| `tf` | `caixa_texto` | `replace_placeholders_in_shape()` | Abreviação não óbvia (text_frame) |
| `idx` | `indice_coluna` | `_processar_linhas_tabela()` | Abreviação, deveria ser mais específico |
| `prs` | `apresentacao` | `gerar_apresentacao()`, `duplicate_slide_with_media()` | Abreviação de "presentation", não descritivo |
| `doc` | `documento` | `extrair_dados()` | Abreviação genérica |
| `cab` | `cabecalho` | Várias funções | Abreviação, deveria ser completo |

#### ❌ Problema: Nomes vagos/genéricos

| Atual | Deveria Ser | Localização | Motivo |
|-------|-------------|-------------|---------|
| `info` | `dados_equipe` | `_organizar_dados_equipes()` | "info" é vago, não indica que são dados da equipe |
| `novo_el` | `elemento_shape_copiado` | `duplicate_slide_with_media()` | "novo_el" é vago |
| `new_el_xml` | `elemento_xml_shape` | `duplicate_slide_with_media()` | Mixing PT/EN |
| `blips` | `elementos_imagem_blip` | `duplicate_slide_with_media()` | Termo técnico não óbvio |
| `img_blob` | `dados_binarios_imagem` | `duplicate_slide_with_media()` | "blob" não é descritivo |

### 2. Funções Internas Mal Nomeadas (Agent-CLEAN-02)

#### ❌ Problema: Nomes genéricos de funções internas

| Atual | Deveria Ser | Localização | Motivo |
|-------|-------------|-------------|---------|
| `registrar()` | `_registrar_mapeamento_coluna()` | `_identificar_colunas_tabela()` | Nome vago, não indica o que registra |
| `combina()` | `_verifica_combinacao_fuzzy()` | `_identificar_colunas_tabela()` | Nome vago, não indica que é fuzzy matching |
| `obter_valor()` | `_extrair_valor_celula()` | `_processar_linhas_tabela()` | "obter" é genérico |
| `chave_ord()` | `_extrair_chave_ordenacao_alcance()` | `_organizar_dados_equipes()` | Abreviação, não descritivo |

### 3. Constantes com Nomes Inadequados (Agent-CLEAN-03)

#### ✅ Já bem nomeadas (não mudar):
- `LOGO_PATH`, `GIF_PATH` - claros e descritivos
- `FONT_NAME`, `FONT_SIZE_*` - bem organizados
- `COLOR_WHITE`, `COLOR_BLUE` - descritivos
- `PLACEHOLDER_*` - todos bem nomeados
- `MSG_*` - padronização boa

#### ⚠️ Poderiam ser melhorados (opcional):
- `SHAPE_TYPE_PICTURE = 13` → Poderia ter comentário explicando que 13 é MSO_SHAPE_TYPE

### 4. Mixing Português/Inglês (Agent-CLEAN-04)

#### ❌ Problema: Variáveis em inglês em código português

| Atual (EN) | Deveria Ser (PT) | Localização | Motivo |
|------------|------------------|-------------|---------|
| `shape` | `forma` | `replace_placeholders_in_shape()` | Parâmetro em inglês |
| `team_data` | `dados_equipe` | `replace_placeholders_in_shape()` | Parâmetro em inglês |
| `dados`, `template_stream` | OK (misturados mas aceitável) | `gerar_apresentacao()` | Contexto claro |
| `header_norm` | `cabecalhos_normalizados` | `_identificar_colunas_tabela()` | Variável interna em inglês |
| `aliases_norm` | `aliases_normalizados` | `_identificar_colunas_tabela()` | Variável interna em inglês |
| `tokens_por_coluna` | OK | `_identificar_colunas_tabela()` | Bom nome em PT |
| `full_text` | `texto_completo` | `replace_placeholders_in_shape()` | Variável interna em inglês |
| `selected_key` | `chave_selecionada` | `replace_placeholders_in_shape()` | Variável interna em inglês |
| `new_text` | `texto_novo` | `replace_placeholders_in_shape()` | Variável interna em inglês |
| `match` | `correspondencia` | `replace_placeholders_in_shape()` | Variável em inglês |

---

## 📊 Estatísticas

| Categoria | Quantidade | Prioridade |
|-----------|------------|------------|
| Variáveis não descritivas (1-2 chars) | 8 | 🔴 Alta |
| Variáveis vagas/genéricas | 5 | 🟡 Média |
| Funções internas mal nomeadas | 4 | 🟡 Média |
| Mixing PT/EN | 10 | 🟢 Baixa |
| **TOTAL** | **27** | - |

---

## 🎯 Plano de Refatoração

### Fase 1: Variáveis de 1-2 caracteres (Prioridade Alta)
**Impacto:** Alto - Dificulta leitura
**Risco:** Baixo - Renomeação simples
**Ordem:**
1. `r` → `registro` (5 ocorrências em `_organizar_dados_equipes`)
2. `m` → `membro` (10+ ocorrências em list comprehensions)
3. `p` → `paragrafo` (5 ocorrências em `replace_placeholders_in_shape`)
4. `tf` → `caixa_texto` (15+ ocorrências)
5. `idx` → `indice_coluna` (3 ocorrências)
6. `prs` → `apresentacao` (10+ ocorrências)
7. `doc` → `documento` (5 ocorrências)
8. `cab` → `cabecalho` (variável temporária, 2 ocorrências)

### Fase 2: Funções Internas (Prioridade Média)
**Impacto:** Médio - Melhora clareza
**Risco:** Baixo - Funções privadas
**Ordem:**
1. `registrar()` → `_registrar_mapeamento_coluna()`
2. `combina()` → `_verifica_combinacao_fuzzy()`
3. `obter_valor()` → `_extrair_valor_celula()`
4. `chave_ord()` → `_extrair_chave_ordenacao_alcance()`

### Fase 3: Variáveis Genéricas (Prioridade Média)
**Impacto:** Médio
**Risco:** Baixo
**Ordem:**
1. `info` → `dados_equipe`
2. `novo_el` → `elemento_shape_copiado`
3. `img_blob` → `dados_binarios_imagem`

### Fase 4: Mixing PT/EN (Prioridade Baixa)
**Impacto:** Baixo - Estético
**Risco:** Baixo
**Ordem:**
1. `shape` → `forma` (parâmetro de função - requer cuidado)
2. `team_data` → `dados_equipe` (parâmetro)
3. Variáveis internas: `header_norm`, `full_text`, `new_text`, etc.

---

## ⚠️ Cuidados Especiais

### Não Renomear (Mantém em Inglês):
1. **Objetos de bibliotecas externas:**
   - `shape` (python-pptx) - objeto da biblioteca
   - `text_frame`, `paragraph`, `run` - termos técnicos do python-pptx
   - `Document`, `Presentation` - classes das bibliotecas

2. **Termos técnicos universais:**
   - `regex`, `tokens` - termos técnicos consolidados
   - `blob` (em contexto de imagens) - termo técnico

3. **Convenções estabelecidas:**
   - Nomes de parâmetros de callbacks/helpers podem manter inglês se for mais claro

### Renomeações que Exigem Atenção:
1. `prs` → `apresentacao`: 10+ ocorrências, verificar todas
2. `tf` → `caixa_texto`: Usado em múltiplos contextos, verificar todos
3. `m` em list comprehensions: Cuidado com escopo

---

## 📝 Convenções Adotadas

### Para Nomes em Português:
1. **Variáveis:** `snake_case` (ex: `dados_equipe`, `indice_coluna`)
2. **Funções privadas:** `_snake_case_descritivo` (ex: `_extrair_valor_celula`)
3. **Constantes:** `UPPER_SNAKE_CASE` (ex: `LOGO_PATH`)
4. **Preferir nomes completos:** `cabecalho` > `cab`, `indice` > `idx`

### Quando Usar Inglês:
1. **Objetos de bibliotecas:** Manter nomes originais
2. **Termos técnicos consolidados:** regex, tokens, blob (quando apropriado)
3. **Callbacks genéricos:** `key=lambda x: ...` (aceitável)

---

## ✅ Validação

Após cada renomeação, executar:
```bash
# Verificar se código ainda funciona
python -m py_compile APP.py

# Verificar linters
flake8 APP.py
pylint APP.py --disable=C0111,C0103,C0330

# Buscar possíveis nomes esquecidos
grep -n '\br\b\s*=' APP.py  # Verificar se 'r' ainda existe
```

---

**Status:** Análise completa ✅
**Próximo:** Iniciar Fase 1 - Renomear variáveis de 1-2 caracteres
