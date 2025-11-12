# 📄 Especificação de Formato de Entrada

Este documento detalha as especificações técnicas dos arquivos de entrada para o APP_SLIDE_OBA.

## 📋 Índice

1. [Arquivo DOCX - Estrutura](#-arquivo-docx---estrutura)
2. [Reconhecimento de Colunas](#-reconhecimento-de-colunas)
3. [Arquivo PPTX - Template](#-arquivo-pptx---template)
4. [Regras de Processamento](#-regras-de-processamento)
5. [Validação de Dados](#-validação-de-dados)

## 📝 Arquivo DOCX - Estrutura

### Formato Geral

O arquivo DOCX deve conter **uma ou mais tabelas** com dados das equipes e participantes.

### Estrutura da Tabela

```
┌──────────┬─────────┬────────────┬──────────────┬─────────────┬─────────┬────────┐
│ Válido   │ Equipe  │ Nome       │ Função       │ Escola      │ Cidade  │ Estado │
├──────────┼─────────┼────────────┼──────────────┼─────────────┼─────────┼────────┤
│ (número) │ (texto) │ (texto)    │ (texto)      │ (texto)     │ (texto) │ (texto)│
└──────────┴─────────┴────────────┴──────────────┴─────────────┴─────────┴────────┘
```

### Linha de Cabeçalho (Obrigatória)

- A **primeira linha** da tabela deve conter os nomes das colunas
- Os nomes podem variar conforme os aliases aceitos (veja seção [Reconhecimento de Colunas](#-reconhecimento-de-colunas))
- Case-insensitive (maiúsculas/minúsculas não importam)
- Acentuação é tratada automaticamente

### Linhas de Dados

- **Linha por participante**: Cada linha representa um membro da equipe
- **Agrupamento por equipe**: Múltiplas linhas com o mesmo nome de equipe são agrupadas
- **Linhas vazias**: São ignoradas automaticamente

### Formato dos Campos

#### 1. Válido/Alcance (Obrigatório)

**Tipo**: Número decimal

**Formato Aceito**:
- Com vírgula: `45,5`
- Com ponto: `45.5`
- Apenas inteiro: `45`

**Regras**:
- Todos os membros da mesma equipe devem ter o **mesmo valor**
- Usado para ordenar equipes (menor para maior)
- Valores inválidos resultam em equipe no final da lista

**Exemplos Válidos**:
```
45.5
45,5
45
0.5
100
```

**Exemplos Inválidos**:
```
"45.5 metros"  ← Texto adicional
"N/A"          ← Não é número
"45.5m"        ← Unidade anexada
```

#### 2. Equipe (Obrigatório)

**Tipo**: Texto

**Formato**: Nome ou código da equipe

**Regras**:
- O **número da equipe** é extraído da **última palavra**
- Case-insensitive
- Espaços são preservados

**Exemplos**:
```
"Alpha 01"     → Exibido como "Equipe: 01"
"Beta 02"      → Exibido como "Equipe: 02"
"Equipe 10"    → Exibido como "Equipe: 10"
"Gamma"        → Exibido como "Equipe: Gamma"
```

#### 3. Nome (Obrigatório)

**Tipo**: Texto

**Formato**: Nome completo do participante

**Regras**:
- Será formatado com **primeira letra maiúscula** em cada palavra
- Espaços extras são removidos
- Ordem alfabética aplicada aos alunos

**Exemplos de Transformação**:
```
"joão silva"        → "João Silva"
"MARIA  SANTOS"     → "Maria Santos"
"  pedro costa  "   → "Pedro Costa"
```

#### 4. Função (Obrigatório)

**Tipo**: Texto

**Valores Aceitos** (case-insensitive):
- **"líder"** ou **"lider"**: Líder da equipe
- **"acompanhante"**: Acompanhante/Professor
- **"aluno"**: Aluno participante

**Regras**:
- A palavra-chave deve estar contida no texto da função
- Pode ter texto adicional (ex: "Aluno participante" → reconhecido como "aluno")

**Exemplos Válidos**:
```
"Líder"
"lider"
"Líder da equipe"
"Acompanhante"
"Professor Acompanhante"
"Aluno"
"aluno participante"
```

#### 5. Escola (Obrigatório)

**Tipo**: Texto

**Formato**: Nome da instituição de ensino

**Regras**:
- Formatado com primeira letra maiúscula
- Espaços normalizados

**Exemplos**:
```
"COLÉGIO ESTADUAL XYZ"  → "Colégio Estadual Xyz"
"escola municipal abc"  → "Escola Municipal Abc"
```

#### 6. Cidade (Obrigatório)

**Tipo**: Texto

**Formato**: Nome da cidade

**Regras**:
- Formatado com primeira letra maiúscula
- Combinado com UF na saída

**Exemplos**:
```
"são paulo"    → "São Paulo"
"RIO CLARO"    → "Rio Claro"
```

#### 7. Estado/UF (Obrigatório)

**Tipo**: Texto

**Formato**: Sigla ou nome completo do estado

**Regras**:
- Convertido para **MAIÚSCULAS** automaticamente
- Aceita siglas (SP, RJ) ou nomes completos

**Exemplos**:
```
"sp"          → "SP"
"São Paulo"   → "SÃO PAULO"
"RJ"          → "RJ"
```

## 🔍 Reconhecimento de Colunas

O sistema usa **três estratégias** para identificar colunas:

### 1. Correspondência Exata com Aliases

O sistema primeiro tenta encontrar uma correspondência exata com os aliases conhecidos.

#### Lista Completa de Aliases

##### Válido/Alcance
```python
Aliases: [
    "valido",
    "alcance",
    "lancamentos validos",
    "alcance (m)",
    "distancia",
    "distancia (m)"
]
```

##### Equipe
```python
Aliases: [
    "equipe",
    "nome da equipe"
]
```

##### Função
```python
Aliases: [
    "funcao",
    "funcao/role",
    "funcao na equipe",
    "funcao integrante",
    "papel",
    "cargo"
]
```

##### Escola
```python
Aliases: [
    "escola",
    "nome da escola",
    "instituicao",
    "nome da instituicao",
    "colegio",
    "nome do colegio"
]
```

##### Cidade
```python
Aliases: [
    "cidade",
    "municipio"
]
```

##### Estado
```python
Aliases: [
    "estado",
    "uf"
]
```

##### Nome
```python
Aliases: [
    "nome",
    "nome do integrante",
    "nome integrante",
    "nome do aluno",
    "nome participante",
    "integrante",
    "participante",
    "aluno"
]
```

### 2. Busca por Palavras-chave em Tokens

Se a correspondência exata falhar, o sistema divide o cabeçalho em tokens e busca palavras-chave.

#### Palavras-chave por Campo

```python
"Válido": {"alcance", "valido", "validos", "lancamento", "lancamentos", "distancia"}
"Equipe": {"equipe", "time", "grupo"}
"Função": {"funcao", "papel", "cargo"}
"Escola": {"escola", "colegio", "instituicao"}
"Cidade": {"cidade", "municipio"}
"Estado": {"estado", "uf"}
"Nome": {"nome", "nomes", "aluno", "alunos", "integrante", "integrantes",
         "participante", "participantes", "membro", "membros", "lider",
         "acompanhante", "responsavel", "responsaveis"}
```

### 3. Substring Matching

Como último recurso, busca a palavra-chave como substring no cabeçalho completo.

### Prioridade de Campos

Quando múltiplas colunas podem corresponder ao mesmo campo, a ordem de prioridade é:

1. Válido
2. Equipe
3. Função
4. Escola
5. Cidade
6. Estado
7. Nome

### Normalização de Texto

Antes de qualquer comparação, os cabeçalhos passam por normalização:

```python
Etapas:
1. Decomposição Unicode (NFKD)
2. Remoção de caracteres combinantes (acentos)
3. Normalização de espaços em branco
4. Conversão para minúsculas

Exemplo:
"Função do Aluno  " → "funcao do aluno"
```

## 📊 Arquivo PPTX - Template

### Estrutura Geral

- **Mínimo**: 1 slide
- **Recomendado**: Slide único que será duplicado
- **Elementos preservados**: Imagens, formas, fundo, layout

### Placeholders

#### Sintaxe

Todos os placeholders usam a sintaxe `{{NOME_PLACEHOLDER}}`:

```
{{LANCAMENTOS_VALIDOS}}
{{NOME_EQUIPE}}
{{NOME_ESCOLA}}
{{CIDADE_UF}}
{{NOMES_ALUNOS}}
```

#### Localização

- **Caixas de texto**: Coloque placeholders em caixas de texto do PowerPoint
- **Paragrafos separados**: Cada placeholder pode estar em seu próprio parágrafo
- **Múltiplos placeholders**: Podem estar na mesma caixa de texto se em linhas diferentes

#### Regras de Substituição

##### 1. {{LANCAMENTOS_VALIDOS}}

**Entrada**: Valor numérico do campo Válido
**Saída**: "ALCANCE: XX.X m"

**Formatação Aplicada**:
- "ALCANCE: " → Lexend, 28pt, azul (#006FC0), regular
- "XX.X m" → Lexend, 35pt, azul (#006FC0), negrito + sublinhado

**Exemplo**:
```
Placeholder: {{LANCAMENTOS_VALIDOS}}
Valor: 45.5
Resultado: "ALCANCE: 45.5 m"
```

##### 2. {{NOME_EQUIPE}}

**Entrada**: Nome da equipe
**Saída**: "Equipe: XX" (XX = última palavra do nome)

**Formatação Aplicada**:
- Lexend, 20pt, branco (#FFFFFF), negrito
- Alinhamento: Centro

**Exemplo**:
```
Placeholder: {{NOME_EQUIPE}}
Valor: "Alpha 01"
Resultado: "Equipe: 01"
```

##### 3. {{NOME_ESCOLA}}

**Entrada**: Nome da escola
**Saída**: Nome formatado

**Formatação Aplicada**:
- Lexend, 20pt, branco (#FFFFFF), negrito
- Alinhamento: Centro

##### 4. {{CIDADE_UF}}

**Entrada**: Cidade e Estado
**Saída**: "Cidade / UF"

**Formatação Aplicada**:
- Lexend, 20pt, branco (#FFFFFF), negrito
- Alinhamento: Centro

**Exemplo**:
```
Placeholder: {{CIDADE_UF}}
Valores: Cidade="São Paulo", Estado="SP"
Resultado: "São Paulo / SP"
```

##### 5. {{NOMES_ALUNOS}}

**Entrada**: Lista de participantes
**Saída**: Lista com quebras de linha

**Formatação Aplicada**:
- Lexend, 26.5pt, branco (#FFFFFF), negrito
- Alinhamento: Centro
- Um nome por linha

**Ordem dos Nomes**:
1. Líder (se houver)
2. Acompanhante (se houver)
3. Alunos (ordem alfabética)

**Exemplo**:
```
Placeholder: {{NOMES_ALUNOS}}
Entrada:
  - João Silva (Líder)
  - Maria Santos (Acompanhante)
  - Pedro Costa (Aluno)
  - Ana Oliveira (Aluno)

Resultado:
João Silva
Maria Santos
Ana Oliveira
Pedro Costa
```

#### Combinações Especiais

##### {{NOMES_ALUNOS}} + {{NOME_EQUIPE}}

Se ambos estiverem na **mesma caixa de texto**, são tratados juntos:
- Nomes: 26.5pt
- Equipe (última linha): 20pt

##### {{NOME_ESCOLA}} + {{CIDADE_UF}}

Se ambos estiverem na **mesma caixa de texto**, são criados em parágrafos separados:
- Escola (primeira linha): 20pt
- Cidade/UF (segunda linha): 20pt

### Preservação de Elementos

Durante a duplicação de slides, os seguintes elementos são preservados:

- ✅ Imagens (incluindo dados binários)
- ✅ Formas geométricas
- ✅ Fundo do slide
- ✅ Layout do slide
- ✅ Relações e referências XML
- ✅ Posicionamento e tamanho

## ⚙️ Regras de Processamento

### Agrupamento de Equipes

1. Todas as linhas com o mesmo nome de equipe são agrupadas
2. Informações comuns (escola, cidade, alcance) são obtidas da primeira linha

### Ordenação

#### Equipes
- Ordenadas por **alcance** (crescente)
- Equipes com alcance inválido vão para o final

#### Participantes (dentro de cada equipe)
1. Líder (se houver) → primeiro
2. Acompanhante (se houver) → segundo
3. Alunos → ordem alfabética (normalizada)

### Normalização de Nomes

Algoritmo aplicado a nomes de pessoas:

```python
1. Remove espaços extras
2. Converte para Title Case (primeira letra maiúscula)

Exemplo:
"  joão   SILVA  " → "João Silva"
```

### Tratamento de Dados Faltantes

| Campo | Se Vazio | Comportamento |
|-------|----------|---------------|
| Válido | Vazio | Equipe vai para o final (ordenação = infinito) |
| Equipe | Vazio | Linha é ignorada |
| Nome | Vazio | Linha é ignorada |
| Função | Vazio | Tratado como aluno |
| Escola | Vazio | String vazia no slide |
| Cidade | Vazio | String vazia no slide |
| Estado | Vazio | String vazia no slide |

## ✅ Validação de Dados

### Pré-processamento (Automático)

Antes do processamento, o sistema:

1. ✓ Remove linhas completamente vazias
2. ✓ Normaliza espaços em branco
3. ✓ Remove acentos para comparação de cabeçalhos
4. ✓ Converte valores para formatos apropriados

### Validações Aplicadas

#### Durante Extração

- ✗ Tabela sem linhas de dados → "Nenhum dado encontrado"
- ✗ Nenhuma coluna reconhecida → Ignorada
- ✗ Linha sem equipe E sem nome → Ignorada

#### Durante Geração

- ✗ Lista de dados vazia → Apresentação original sem alterações
- ✗ Template sem slides → Apresentação original sem alterações

### Recomendações de Validação Manual

Antes de processar, verifique:

1. ☑ Tabela tem cabeçalho na primeira linha
2. ☑ Todas as colunas obrigatórias estão presentes
3. ☑ Valores de alcance são numéricos
4. ☑ Membros da mesma equipe têm o mesmo alcance
5. ☑ Funções contêm palavras-chave corretas
6. ☑ Template PPTX contém todos os placeholders desejados

---

**Próximos Passos**: Consulte [EXAMPLES.md](EXAMPLES.md) para ver exemplos práticos de arquivos de entrada e saída.
