# 📖 Guia de Uso - APP_SLIDE_OBA

Este guia fornece instruções detalhadas sobre como usar o APP_SLIDE_OBA para gerar apresentações automaticamente.

## 📋 Índice

1. [Pré-requisitos](#-pré-requisitos)
2. [Iniciando a Aplicação](#-iniciando-a-aplicação)
3. [Preparando os Arquivos](#-preparando-os-arquivos)
4. [Processo de Geração](#-processo-de-geração)
5. [Solução de Problemas](#-solução-de-problemas)
6. [Dicas e Melhores Práticas](#-dicas-e-melhores-práticas)

## ✅ Pré-requisitos

Antes de começar, certifique-se de que você tem:

### 1. Instalação Completa

```bash
# Verifique se as dependências estão instaladas
pip list | grep streamlit
pip list | grep python-docx
pip list | grep python-pptx
```

### 2. Arquivos de Recursos

Verifique se os seguintes arquivos estão presentes no diretório raiz:

- `logo_jornada.png` - Logo exibido no topo da interface
- `tiapamela.gif` - Animação de sucesso após geração

### 3. Arquivos de Entrada Prontos

- **Arquivo DOCX**: Documento Word com dados das equipes em formato de tabela
- **Template PPTX**: Apresentação PowerPoint modelo com placeholders configurados

## 🚀 Iniciando a Aplicação

### Passo 1: Navegue até o Diretório do Projeto

```bash
cd /caminho/para/APP_SLIDE_OBA
```

### Passo 2: Ative o Ambiente Virtual (se aplicável)

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Passo 3: Execute o Streamlit

```bash
streamlit run APP.py
```

### Passo 4: Acesse a Interface

O navegador abrirá automaticamente em `http://localhost:8501`. Se não abrir, acesse manualmente.

## 📁 Preparando os Arquivos

### Arquivo DOCX (Dados das Equipes)

O arquivo DOCX deve conter uma **tabela** com as seguintes informações:

#### Colunas Obrigatórias

A aplicação reconhece automaticamente as seguintes colunas por diversos nomes:

| Campo | Aliases Aceitos |
|-------|----------------|
| **Alcance/Válido** | "Válido", "Alcance", "Lançamentos Válidos", "Alcance (m)", "Distância", "Distância (m)" |
| **Equipe** | "Equipe", "Nome da Equipe" |
| **Escola** | "Escola", "Nome da Escola", "Instituição", "Nome da Instituição", "Colégio", "Nome do Colégio" |
| **Cidade** | "Cidade", "Município" |
| **Estado** | "Estado", "UF" |
| **Nome** | "Nome", "Nome do Integrante", "Nome Integrante", "Nome do Aluno", "Nome Participante", "Integrante", "Participante", "Aluno" |
| **Função** | "Função", "Função/Role", "Função na Equipe", "Função Integrante", "Papel", "Cargo" |

#### Exemplo de Estrutura da Tabela

```
| Válido | Equipe    | Nome           | Função       | Escola                | Cidade      | Estado |
|--------|-----------|----------------|--------------|----------------------|-------------|--------|
| 45.5   | Alpha 01  | João Silva     | Líder        | Colégio Estadual XYZ | São Paulo   | SP     |
| 45.5   | Alpha 01  | Maria Santos   | Acompanhante | Colégio Estadual XYZ | São Paulo   | SP     |
| 45.5   | Alpha 01  | Pedro Costa    | Aluno        | Colégio Estadual XYZ | São Paulo   | SP     |
| 45.5   | Alpha 01  | Ana Oliveira   | Aluno        | Colégio Estadual XYZ | São Paulo   | SP     |
| 38.2   | Beta 02   | Carlos Souza   | Líder        | Escola Municipal ABC | Rio Claro   | SP     |
```

#### Regras de Formatação

- **Alcance**: Pode usar vírgula ou ponto como separador decimal (45,5 ou 45.5)
- **Função**: Deve incluir as palavras "líder", "acompanhante" ou "aluno" (case-insensitive)
- **Equipe**: O número da equipe será extraído da última palavra (ex: "Alpha 01" → "01")
- **Nomes**: Serão formatados automaticamente (primeira letra maiúscula)

### Template PPTX (Modelo de Apresentação)

O template deve conter **pelo menos um slide** com os seguintes **placeholders**:

#### Placeholders Disponíveis

| Placeholder | Descrição | Formato de Saída |
|-------------|-----------|------------------|
| `{{LANCAMENTOS_VALIDOS}}` | Alcance dos lançamentos | "ALCANCE: XX.X m" |
| `{{NOME_EQUIPE}}` | Nome/número da equipe | "Equipe: XX" |
| `{{NOME_ESCOLA}}` | Nome da escola | Texto formatado |
| `{{CIDADE_UF}}` | Cidade e estado | "Cidade / UF" |
| `{{NOMES_ALUNOS}}` | Lista de participantes | Lista com quebras de linha |

#### Exemplo de Slide Modelo

```
┌─────────────────────────────────────┐
│                                     │
│     {{LANCAMENTOS_VALIDOS}}         │
│                                     │
│     {{NOMES_ALUNOS}}                │
│     {{NOME_EQUIPE}}                 │
│                                     │
│     {{NOME_ESCOLA}}                 │
│     {{CIDADE_UF}}                   │
│                                     │
└─────────────────────────────────────┘
```

#### Dicas para o Template

- Use caixas de texto separadas para cada placeholder
- Mantenha espaço suficiente para múltiplos nomes (até 5+ participantes)
- Teste com dados reais antes de usar em produção
- Imagens e elementos visuais serão preservados automaticamente

## 🎨 Processo de Geração

### Passo 1: Upload do Arquivo DOCX

1. Clique no botão **"📄 Arquivo DOCX"**
2. Selecione seu arquivo `.docx` com os dados das equipes
3. Aguarde o upload completar (indicador de progresso aparecerá)

### Passo 2: Upload do Template PPTX

1. Clique no botão **"📊 Arquivo PPTX modelo"**
2. Selecione seu template `.pptx` com os placeholders
3. Aguarde o upload completar

### Passo 3: Definir Nome do Arquivo (Opcional)

1. Digite o nome desejado no campo **"Nome do arquivo (sem extensao)"**
2. Clique em **"Confirmar nome do arquivo"**
3. Caracteres inválidos serão removidos automaticamente
4. Se não definir, o nome padrão será "Apresentacao_Final_Equipes"

### Passo 4: Gerar Apresentação

1. Clique no botão **"✨ Gerar Apresentação"**
2. Aguarde o processamento (pode levar alguns segundos para muitas equipes)
3. Mensagem de sucesso aparecerá com o número de slides gerados
4. Uma animação GIF será exibida

### Passo 5: Baixar o Resultado

1. Clique no botão **"📥 Baixar Apresentação Final"**
2. O arquivo será salvo na pasta de downloads do seu navegador
3. Nome do arquivo: `{nome_escolhido}.pptx`

## 🔧 Solução de Problemas

### Problema: "Envie ambos os arquivos"

**Causa**: Um ou ambos os arquivos não foram enviados.

**Solução**: Certifique-se de fazer upload de DOCX e PPTX antes de clicar em "Gerar".

### Problema: "Nenhum dado encontrado"

**Causa**: A tabela no DOCX está vazia ou não foi reconhecida.

**Solução**:
- Verifique se o DOCX contém uma tabela
- Confirme que a tabela tem linhas com dados (além do cabeçalho)
- Verifique os nomes das colunas (use aliases aceitos)

### Problema: Colunas Não Reconhecidas

**Causa**: Os nomes das colunas não correspondem aos aliases conhecidos.

**Solução**:
- Consulte a lista de aliases aceitos na seção [Arquivo DOCX](#arquivo-docx-dados-das-equipes)
- Renomeie as colunas no DOCX para corresponder aos aliases
- Evite caracteres especiais nos nomes das colunas

### Problema: Alcance Aparece como "inf"

**Causa**: O valor do alcance não pôde ser convertido para número.

**Solução**:
- Certifique-se de que a coluna de alcance contém apenas números
- Use vírgula ou ponto como separador decimal
- Remova texto adicional (ex: "metros", "m")

### Problema: Nomes Não Aparecem na Ordem Correta

**Causa**: As funções não estão identificadas corretamente.

**Solução**:
- Use as palavras-chave corretas: "líder", "acompanhante", "aluno"
- Verifique acentuação (aceita com ou sem acento)
- Coluna de função deve estar preenchida para todos

### Problema: Equipes Fora de Ordem

**Causa**: Valores de alcance inválidos ou inconsistentes.

**Solução**:
- Verifique se todos os membros da mesma equipe têm o mesmo alcance
- Certifique-se de que o alcance é um número válido

### Problema: Formatação Incorreta no Slide

**Causa**: Placeholders colados ou mal formatados no template.

**Solução**:
- Use caixas de texto separadas para cada placeholder
- Não cole placeholders juntos (ex: `{{NOME_ESCOLA}}{{CIDADE_UF}}`)
- Se precisar de dois placeholders juntos, coloque em linhas separadas

## 💡 Dicas e Melhores Práticas

### Para Arquivos DOCX

1. **Use Nomes de Colunas Padrão**: Prefira os aliases mais comuns (Válido, Equipe, Escola, etc.)
2. **Mantenha Consistência**: Use o mesmo formato para todas as linhas
3. **Evite Células Vazias**: Preencha todas as informações obrigatórias
4. **Teste com Dados Pequenos**: Faça um teste com 2-3 equipes antes de processar todas

### Para Templates PPTX

1. **Crie um Backup**: Sempre mantenha uma cópia do template original
2. **Use Fontes Comuns**: A fonte Lexend é aplicada automaticamente, mas fontes do template são preservadas onde não há placeholders
3. **Teste Visualmente**: Gere slides de teste e verifique espaçamento e alinhamento
4. **Considere Muitos Nomes**: Deixe espaço para até 6+ participantes por equipe

### Para Desempenho

1. **Arquivos Otimizados**: Use DOCX e PPTX sem elementos desnecessários
2. **Feche Outros Programas**: Para arquivos grandes, libere memória RAM
3. **Conexão Estável**: Se executando remotamente, garanta conexão de rede estável

### Para Organização

1. **Nomeie Arquivos Claramente**: Use nomes descritivos (ex: "Equipes_OBA_2024_Final")
2. **Organize por Evento**: Crie pastas para cada evento ou edição
3. **Versione os Templates**: Mantenha versões do template (v1, v2, etc.)

### Para Qualidade

1. **Revise os Dados**: Sempre revise o DOCX antes de processar
2. **Valide o Resultado**: Abra a apresentação gerada e verifique alguns slides
3. **Teste com Dados Reais**: Use dados de eventos anteriores para testar

## 📞 Precisa de Ajuda?

Se encontrar problemas não listados aqui:

1. Verifique a documentação em [INPUT_FORMAT.md](INPUT_FORMAT.md)
2. Consulte exemplos em [EXAMPLES.md](EXAMPLES.md)
3. Reporte bugs no repositório do projeto

---

**Próximos Passos**: Consulte [INPUT_FORMAT.md](INPUT_FORMAT.md) para especificações técnicas detalhadas do formato de entrada.
