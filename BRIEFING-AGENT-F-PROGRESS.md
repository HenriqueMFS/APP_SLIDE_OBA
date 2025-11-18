# 🎯 BRIEFING: Agent-F - Progress Bar e UX (Performance)

**Data:** 2025-11-18
**Projeto:** APP_SLIDE_OBA
**Feature:** F3-PROGRESS-UX
**Prioridade:** 🟡 ALTA
**Estimativa:** 1-2 horas
**Ganho esperado:** UX significativamente melhor

---

## 📋 CONTEXTO DO PROJETO

Você é o **Agent-F**, responsável por implementar progress bars e melhorias de UX no projeto APP_SLIDE_OBA.

### Problema Identificado
A análise de performance (PERFORMANCE-ANALYSIS.md) identificou problema crítico de UX:

1. **Operações longas sem feedback:** Geração de 200 slides pode levar 10-30 segundos sem NENHUM indicador de progresso
2. **Aplicação parece travada:** Usuário não sabe se está processando ou se crashou
3. **Sem estimativa:** Usuário não tem ideia de quanto tempo falta

### Sua Missão
Implementar sistema completo de progress bar para:
- ✅ Mostrar progresso em tempo real (0-100%)
- ✅ Exibir mensagens de status claras ("Duplicando slides 23/50...")
- ✅ Dividir geração em 3 etapas visíveis (template, duplicação, preenchimento)
- ✅ Auto-limpar progress bar após conclusão

**Ganho esperado:** UX profissional, usuário confiante de que aplicação está funcionando

---

## 🎯 ENTREGA OBRIGATÓRIA

### Entrega 1: Progress Bar na Geração de Apresentação
**Arquivo:** `APP.py`
**Função afetada:** `gerar_apresentacao` (linha ~808-880)
**Tempo:** 60-90 minutos

#### Código Atual (PROBLEMA)

Localizar função `gerar_apresentacao` (linha ~808):

```python
def gerar_apresentacao(dados, template_stream):
    """
    Gera apresentação PowerPoint com dados fornecidos.
    # ... docstring ...
    """
    prs = Presentation(template_stream)

    if not dados or not prs.slides:
        return prs

    modelo = prs.slides[0]
    slides_para_preencher = [modelo]

    # ❌ PROBLEMA: Loop longo SEM feedback
    for _ in range(len(dados) - 1):
        novo_slide = duplicate_slide_with_media(prs, modelo)
        slides_para_preencher.append(novo_slide)

    # ❌ PROBLEMA: Loop longo SEM feedback
    for slide, team in zip(slides_para_preencher, dados):
        for shape in slide.shapes:
            replace_placeholders_in_shape(shape, team)

    return prs
```

**Por que é um problema:**
- Processamento de 200 equipes = 10-30 segundos
- Usuário vê tela congelada (sem indicação de progresso)
- Não sabe se aplicação travou ou está processando
- Não pode estimar quanto tempo falta
- **UX inaceitável para produção**

#### Solução Esperada

**SUBSTITUIR função `gerar_apresentacao` COMPLETA por:**

```python
def gerar_apresentacao(dados, template_stream):
    """
    Gera apresentação PowerPoint com dados fornecidos e progress bar.

    Cria uma apresentação duplicando o slide modelo para cada equipe
    e preenchendo os placeholders com os dados correspondentes. Mostra
    progresso em tempo real dividido em 3 etapas:
    - Etapa 1 (0-10%): Carregamento do template
    - Etapa 2 (10-60%): Duplicação de slides
    - Etapa 3 (60-100%): Preenchimento de dados

    Args:
        dados (list): Lista de dicionários com dados de cada equipe
                      Estrutura: [{Valido, Equipe, Escola, ...}, ...]
        template_stream: Stream do arquivo PPTX template (BytesIO ou similar)

    Returns:
        Presentation: Objeto Presentation com slides gerados

    Note:
        - Progress bar é auto-limpado após 2 segundos
        - Mensagens de status mostram progresso detalhado
        - Usuário pode acompanhar cada etapa em tempo real
    """
    # Criar elementos de interface para progresso
    progress_placeholder = st.empty()
    status_placeholder = st.empty()

    try:
        # ==================== ETAPA 1: CARREGAR TEMPLATE (0-10%) ====================
        status_placeholder.info("📂 Carregando template PowerPoint...")
        progress_placeholder.progress(0)

        prs = Presentation(template_stream)
        progress_placeholder.progress(10)

        # Se não há dados ou slides, retorna template vazio
        if not dados or not prs.slides:
            status_placeholder.success("✅ Template carregado (sem dados para processar)")
            return prs

        modelo = prs.slides[0]
        slides_para_preencher = [modelo]

        # ==================== ETAPA 2: DUPLICAR SLIDES (10-60%) ====================
        num_duplicacoes = len(dados) - 1

        if num_duplicacoes > 0:
            status_placeholder.info(
                f"📋 Duplicando slides para {len(dados)} equipes..."
            )

            for i in range(num_duplicacoes):
                # Duplicar slide
                novo_slide = duplicate_slide_with_media(prs, modelo)
                slides_para_preencher.append(novo_slide)

                # Calcular progresso (10% a 60%)
                progresso_duplicacao = int((i + 1) / num_duplicacoes * 50)
                progresso_total = 10 + progresso_duplicacao
                progress_placeholder.progress(progresso_total)

                # Atualizar mensagem de status
                percentual = int((i + 1) / num_duplicacoes * 100)
                status_placeholder.info(
                    f"📋 Duplicando slides: {i + 1}/{num_duplicacoes} ({percentual}%)"
                )
        else:
            # Apenas 1 slide, pula direto para 60%
            progress_placeholder.progress(60)

        # ==================== ETAPA 3: PREENCHER DADOS (60-100%) ====================
        status_placeholder.info(f"✏️ Preenchendo dados em {len(dados)} slides...")

        for i, (slide, team) in enumerate(zip(slides_para_preencher, dados)):
            # Preencher todos os shapes do slide
            for shape in slide.shapes:
                replace_placeholders_in_shape(shape, team)

            # Calcular progresso (60% a 100%)
            progresso_preenchimento = int((i + 1) / len(dados) * 40)
            progresso_total = 60 + progresso_preenchimento
            progress_placeholder.progress(progresso_total)

            # Atualizar mensagem de status
            percentual = int((i + 1) / len(dados) * 100)
            status_placeholder.info(
                f"✏️ Preenchendo dados: {i + 1}/{len(dados)} equipes ({percentual}%)"
            )

        # ==================== FINALIZAÇÃO ====================
        progress_placeholder.progress(100)
        status_placeholder.success(
            f"✅ Apresentação gerada com sucesso! {len(dados)} slides criados."
        )

        return prs

    except Exception as e:
        # Em caso de erro, exibir mensagem clara
        status_placeholder.error(f"❌ Erro durante geração: {str(e)}")
        raise  # Re-lança exceção para tratamento superior

    finally:
        # Limpar progress bar após 2 segundos (auto-cleanup)
        import time
        time.sleep(2)
        progress_placeholder.empty()
        status_placeholder.empty()
```

**Detalhamento da Implementação:**

**1. Elementos de Interface:**
```python
progress_placeholder = st.empty()  # Container para barra de progresso
status_placeholder = st.empty()    # Container para mensagens de status
```

**2. Etapa 1 - Carregamento (0-10%):**
- Carrega template PPTX
- Exibe "📂 Carregando template..."
- Progresso fixo: 0% → 10%

**3. Etapa 2 - Duplicação (10-60%):**
- Duplica N-1 slides (primeiro já existe)
- Progresso dinâmico: 10% → 60%
- Mensagem: "📋 Duplicando slides: X/Y (Z%)"

**4. Etapa 3 - Preenchimento (60-100%):**
- Preenche placeholders em N slides
- Progresso dinâmico: 60% → 100%
- Mensagem: "✏️ Preenchendo dados: X/Y (Z%)"

**5. Auto-limpeza:**
- Após 2 segundos, limpa progress bar
- Usuário vê mensagem de sucesso antes de sumir

**Validação:**
- [ ] Função `gerar_apresentacao` completamente substituída
- [ ] Progress bar inicia em 0%
- [ ] 3 etapas claramente separadas (10%, 60%, 100%)
- [ ] Mensagens de status descritivas
- [ ] Progress bar atualiza durante processamento
- [ ] Auto-limpeza após 2 segundos
- [ ] Tratamento de exceção com mensagem clara

---

### Entrega 2 (OPCIONAL): Melhorar Mensagens de Interface
**Arquivo:** `APP.py`
**Seção:** Constantes de mensagens (linha ~46-52)
**Tempo:** 10-15 minutos

#### Adicionar novas constantes de mensagens (OPCIONAL)

Se quiser padronizar mensagens, adicionar após linha 52:

```python
# Mensagens de progresso (usadas em gerar_apresentacao)
MSG_PROGRESS_LOADING_TEMPLATE = "📂 Carregando template PowerPoint..."
MSG_PROGRESS_DUPLICATING = "📋 Duplicando slides para {} equipes..."
MSG_PROGRESS_DUPLICATING_DETAIL = "📋 Duplicando slides: {}/{} ({}%)"
MSG_PROGRESS_FILLING = "✏️ Preenchendo dados em {} slides..."
MSG_PROGRESS_FILLING_DETAIL = "✏️ Preenchendo dados: {}/{} equipes ({}%)"
MSG_SUCCESS_GENERATED = "✅ Apresentação gerada com sucesso! {} slides criados."
MSG_ERROR_GENERATION = "❌ Erro durante geração: {}"
```

E então usar em `gerar_apresentacao`:
```python
status_placeholder.info(MSG_PROGRESS_LOADING_TEMPLATE)
# ...
status_placeholder.info(MSG_PROGRESS_DUPLICATING.format(len(dados)))
```

**NOTA:** Esta entrega é OPCIONAL. Se preferir manter strings inline (hard-coded), está OK.

**Validação (se implementar):**
- [ ] Constantes MSG_PROGRESS_* adicionadas
- [ ] Função usa constantes ao invés de strings hard-coded
- [ ] Mensagens consistentes em toda a aplicação

---

## 🔧 PROCEDIMENTOS OBRIGATÓRIOS

### 1. Preparação Inicial (10 min)

```bash
# 1. Verificar branch atual
git status
git branch --show-current

# 2. Criar e trocar para sua branch
SESSION_ID="SUBSTITUA_PELO_SEU_SESSION_ID"
git checkout -b claude/perf-progress-ux-${SESSION_ID}

# 3. Verificar que está na branch correta
git branch --show-current
# Deve mostrar: claude/perf-progress-ux-XXXXX

# 4. Ler função gerar_apresentacao completa
# Localizar linha ~808-880
```

### 2. Implementação (60-90 min)

**ORDEM DE IMPLEMENTAÇÃO:**

#### Passo 1: Backup da função original (5 min)
```bash
# Copiar função original para referência
# Se algo der errado, você tem a versão original
```

#### Passo 2: Substituir função completa (30-40 min)
1. Localizar função `gerar_apresentacao` (linha ~808)
2. Selecionar função completa (do `def` até o `return prs`)
3. Deletar função completa
4. Copiar nova implementação com progress bar
5. Verificar indentação e formatação
6. Salvar arquivo

#### Passo 3: Testar localmente (20-30 min)
```bash
# Executar Streamlit
streamlit run APP.py

# Testar com arquivo pequeno (5-10 equipes)
# - Progress bar deve aparecer
# - 0% → 10% → 60% → 100%
# - Mensagens devem ser claras
# - Auto-limpeza após 2s

# Testar com arquivo médio (30-50 equipes)
# - Verificar que percentuais atualizam corretamente
# - Mensagens mostram progresso real

# Verificar que funcionalidade não quebrou
# - PPTX gerado corretamente
# - Todos os placeholders preenchidos
# - Número correto de slides
```

#### Passo 4 (OPCIONAL): Adicionar constantes de mensagens (10-15 min)
1. Adicionar constantes MSG_PROGRESS_* (linha ~52)
2. Atualizar função para usar constantes
3. Testar que mensagens aparecem corretamente

### 3. Testes de Validação (20-30 min)

**Checklist de Testes:**

```bash
# Teste 1: Progress Bar Aparece
# - Upload DOCX e PPTX
# - Clicar "Gerar Apresentação"
# - Verificar que barra de progresso aparece
# ✅ Esperado: Barra azul de 0 a 100%

# Teste 2: Etapas Corretas
# - Observar mensagens durante geração
# - Verificar: "Carregando..." → "Duplicando..." → "Preenchendo..."
# ✅ Esperado: 3 etapas distintas com emojis corretos

# Teste 3: Porcentagens Corretas
# - Gerar com 10 equipes
# - Verificar que "Duplicando 9/9 (100%)" aparece
# - Verificar que "Preenchendo 10/10 (100%)" aparece
# ✅ Esperado: Números corretos, sem erros de cálculo

# Teste 4: Auto-limpeza
# - Após geração completa
# - Verificar que progress bar desaparece após 2s
# ✅ Esperado: Mensagem "✅ Apresentação gerada..." some após 2s

# Teste 5: Tratamento de Erro
# - Forçar erro (ex: template inválido)
# - Verificar mensagem de erro
# ✅ Esperado: "❌ Erro durante geração: [mensagem]"

# Teste 6: Funcionalidade Preservada
# - Gerar apresentação completa
# - Baixar PPTX
# - Abrir no PowerPoint/LibreOffice
# - Verificar todos os slides
# ✅ Esperado: PPTX perfeito, todos os dados preenchidos
```

### 4. Commits e Push (10-15 min)

```bash
# Commit 1: Progress bar
git add APP.py
git commit -m "feat: Implementar progress bar em gerar_apresentacao

- Adicionar barra de progresso com 3 etapas (0-10-60-100%)
- Exibir mensagens de status em tempo real
- Mostrar progresso de duplicação de slides
- Mostrar progresso de preenchimento de dados
- Auto-limpeza de UI após 2 segundos
- Tratamento de exceções com mensagens claras
- UX: Usuário vê progresso em operações longas (5-30s)"

# Commit 2: Constantes de mensagens (SE implementou)
git add APP.py
git commit -m "refactor: Padronizar mensagens de progresso em constantes

- Adicionar MSG_PROGRESS_* no topo do arquivo
- Atualizar gerar_apresentacao para usar constantes
- Melhora manutenibilidade e i18n futuro"

# Commit 3: Report final
git add REPORT-AGENT-F.md
git commit -m "docs: Report final do Agent-F (Progress Bar e UX)"

# Push para remote
git push -u origin claude/perf-progress-ux-${SESSION_ID}
```

---

## 📊 REPORT FINAL OBRIGATÓRIO

Criar arquivo `REPORT-AGENT-F.md`:

```markdown
# 📊 Report Final - Agent-F (Progress Bar e UX)

**Data conclusão:** YYYY-MM-DD HH:MM
**Branch:** claude/perf-progress-ux-{SESSION_ID}
**Status:** ✅ CONCLUÍDO | ⚠️ PARCIAL | ❌ BLOQUEADO

---

## ✅ Entregas Concluídas

- [x] Progress bar implementada em gerar_apresentacao
- [x] 3 etapas de progresso (template, duplicação, preenchimento)
- [x] Mensagens de status descritivas
- [x] Porcentagens dinâmicas atualizando em tempo real
- [x] Auto-limpeza após 2 segundos
- [x] Tratamento de exceções com feedback claro
- [x] Constantes de mensagens (se implementado)
- [x] Testes de validação executados
- [x] Commits e push realizados

## 📈 Melhorias de UX

### Antes
- ❌ Tela congelada durante geração (5-30s)
- ❌ Sem feedback de progresso
- ❌ Usuário não sabe se travou ou está processando
- ❌ Sem estimativa de tempo

### Depois
- ✅ Progress bar 0-100% em tempo real
- ✅ Mensagens claras de cada etapa
- ✅ Percentual exato (ex: "Preenchendo 47/50 (94%)")
- ✅ Usuário confiante de que está processando
- ✅ Estimativa implícita pelo progresso

## 🧪 Testes Executados

1. ✅ Progress bar aparece e atualiza corretamente
2. ✅ 3 etapas executam em sequência correta
3. ✅ Porcentagens calculadas corretamente
4. ✅ Auto-limpeza funciona após 2s
5. ✅ Erro exibe mensagem clara
6. ✅ Funcionalidade preservada (PPTX gerado corretamente)

### Testes com Diferentes Tamanhos

- **5 equipes:** Progress bar completa em ~2s (rápido mas visível)
- **50 equipes:** Progress bar completa em ~10s (UX excelente)
- **200 equipes:** Progress bar completa em ~30s (usuário confiante)

## 📝 Commits Realizados

1. ✅ feat: Implementar progress bar em gerar_apresentacao
2. ✅ refactor: Padronizar mensagens (se implementado)
3. ✅ docs: Report final Agent-F

**Total:** 2-3 commits
**Push status:** ✅ Sucesso

## 📊 Detalhes de Implementação

### Etapas de Progresso

- **Etapa 1 (0-10%):** Carregamento de template
  - Tempo: ~100-500ms
  - Mensagem: "📂 Carregando template PowerPoint..."

- **Etapa 2 (10-60%):** Duplicação de slides
  - Tempo: ~40% do tempo total
  - Mensagem: "📋 Duplicando slides: X/Y (Z%)"

- **Etapa 3 (60-100%):** Preenchimento de dados
  - Tempo: ~60% do tempo total
  - Mensagem: "✏️ Preenchendo dados: X/Y (Z%)"

### Cálculos de Progresso

```python
# Duplicação: 10% base + (i/total * 50%)
progresso = 10 + int((i + 1) / num_duplicacoes * 50)

# Preenchimento: 60% base + (i/total * 40%)
progresso = 60 + int((i + 1) / len(dados) * 40)
```

## ⚠️ Problemas Encontrados

(Liste qualquer problema)

Exemplos:
- Nenhum problema encontrado
- [Se houver] Progress bar pisca muito rápido com <3 equipes (normal, operação rápida)

## 💡 Observações

(Observações para o orquestrador)

Exemplos:
- Progress bar melhora significativamente a confiança do usuário
- Para arquivos pequenos (<10 equipes), progresso é quase instantâneo
- Para arquivos grandes (>100 equipes), UX é crítica e funciona perfeitamente

## 🎯 Melhorias Futuras (Opcional)

- [ ] Adicionar botão de cancelamento
- [ ] Mostrar tempo estimado restante
- [ ] Adicionar som/notificação ao concluir
- [ ] Progress bar para extração de DOCX também

---

**Assinatura:** Agent-F
**Commit final:** {HASH}
**Pronto para merge:** ✅ SIM | ❌ NÃO
```

---

## ⚠️ AVISOS CRÍTICOS

### ❌ NÃO FAÇA ISSO:
- ❌ NÃO modificar funções `carregar_logo`, `extrair_dados_cached`, `validar_tamanho_arquivo` (são do Agent-D)
- ❌ NÃO modificar constantes ALIASES_* ou REGEX_* (são do Agent-E)
- ❌ NÃO alterar lógica de duplicação ou preenchimento (apenas adicionar UI)
- ❌ NÃO mudar ordem das etapas (template → duplicação → preenchimento)
- ❌ NÃO usar `st.progress()` direto (usar `progress_placeholder.progress()`)

### ✅ FAÇA ISSO:
- ✅ Use `st.empty()` para criar placeholders reutilizáveis
- ✅ Calcule porcentagens corretamente (int() para evitar floats)
- ✅ Teste com arquivos de diferentes tamanhos (5, 50, 200 equipes)
- ✅ Verifique que auto-limpeza funciona (finally block)
- ✅ Mantenha mensagens claras e com emojis
- ✅ Trate exceções e exiba mensagens de erro

---

## 🆘 TROUBLESHOOTING

### Problema: Progress bar não aparece
**Solução:**
1. Verificar que `progress_placeholder = st.empty()` está ANTES do try
2. Verificar que `progress_placeholder.progress(X)` está sendo chamado
3. Verificar que não há erros antes de chegar no progresso

### Problema: Progress bar não atualiza (fica em 0%)
**Solução:**
1. Verificar cálculos de progresso (print debug)
2. Verificar que loop está executando (`print(i)`)
3. Verificar que `progress_placeholder.progress()` é chamado dentro do loop

### Problema: Mensagens não somem após geração
**Solução:**
1. Verificar que `finally` block existe
2. Verificar que `time.sleep(2)` está executando
3. Verificar que `.empty()` é chamado nos placeholders

### Problema: Porcentagem errada (ex: "150%" ou "0%")
**Solução:**
1. Verificar divisão: `(i + 1) / total` (não `i / total`)
2. Verificar multiplicação: `* 100` para percentual
3. Verificar conversão: `int(...)` para evitar floats
4. Adicionar print: `print(f"i={i}, total={total}, %={percentual}")`

### Problema: Funcionalidade quebrou (PPTX não gera)
**Solução:**
1. Verificar que lógica de duplicação e preenchimento não foi alterada
2. Verificar que apenas UI foi adicionada
3. Comparar com função original (deve ter MESMA lógica + UI)
4. Remover progress bar temporariamente para testar

---

## 📚 RECURSOS DE REFERÊNCIA

- **FEATURES-PARALLEL-WAVE-2.md:** Sua entrega detalhada
- **PERFORMANCE-ANALYSIS.md:** Problema 4.3 (progress bars)
- **APP.py linhas 808-880:** Função `gerar_apresentacao` original
- **Streamlit Progress Docs:** https://docs.streamlit.io/library/api-reference/status/st.progress

---

## ✅ CHECKLIST FINAL

- [ ] Função `gerar_apresentacao` completamente reescrita
- [ ] Progress bar com 3 etapas (0→10→60→100%)
- [ ] Mensagens de status descritivas com emojis
- [ ] Porcentagens dinâmicas corretas
- [ ] Auto-limpeza após 2s (finally block)
- [ ] Tratamento de exceções
- [ ] Constantes de mensagens (se implementado)
- [ ] Testes com 5, 50 e 200 equipes
- [ ] Funcionalidade preservada (PPTX correto)
- [ ] 2-3 commits realizados
- [ ] Push realizado
- [ ] REPORT-AGENT-F.md criado

---

**Boa sorte, Agent-F! Sua UX vai transformar a experiência do usuário! 🚀**

**Em caso de dúvidas:** Leia função original e teste incrementalmente
**Em caso de bloqueio:** Documente no REPORT e continue até onde conseguir
