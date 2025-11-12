# 📚 Exemplos Práticos - APP_SLIDE_OBA

Este documento apresenta exemplos completos de uso do APP_SLIDE_OBA, incluindo dados de entrada e saída esperada.

## 📋 Índice

1. [Exemplo Básico](#-exemplo-básico)
2. [Exemplo com Múltiplas Equipes](#-exemplo-com-múltiplas-equipes)
3. [Exemplo com Variações de Colunas](#-exemplo-com-variações-de-colunas)
4. [Casos de Uso Especiais](#-casos-de-uso-especiais)
5. [Troubleshooting com Exemplos](#-troubleshooting-com-exemplos)

## 🎯 Exemplo Básico

### Cenário

Uma única equipe com 4 participantes: 1 líder, 1 acompanhante e 2 alunos.

### Arquivo DOCX (Entrada)

```
┌────────┬───────────┬──────────────────┬──────────────┬──────────────────────┬──────────┬────────┐
│ Válido │ Equipe    │ Nome             │ Função       │ Escola               │ Cidade   │ Estado │
├────────┼───────────┼──────────────────┼──────────────┼──────────────────────┼──────────┼────────┤
│ 45.5   │ Alpha 01  │ João Silva       │ Líder        │ Colégio Estadual XYZ │ Campinas │ SP     │
│ 45.5   │ Alpha 01  │ Maria Santos     │ Acompanhante │ Colégio Estadual XYZ │ Campinas │ SP     │
│ 45.5   │ Alpha 01  │ Pedro Costa      │ Aluno        │ Colégio Estadual XYZ │ Campinas │ SP     │
│ 45.5   │ Alpha 01  │ Ana Oliveira     │ Aluno        │ Colégio Estadual XYZ │ Campinas │ SP     │
└────────┴───────────┴──────────────────┴──────────────┴──────────────────────┴──────────┴────────┘
```

### Template PPTX (Entrada)

```
┌─────────────────────────────────────────┐
│                                         │
│     {{LANCAMENTOS_VALIDOS}}             │
│                                         │
│     {{NOMES_ALUNOS}}                    │
│     {{NOME_EQUIPE}}                     │
│                                         │
│     {{NOME_ESCOLA}}                     │
│     {{CIDADE_UF}}                       │
│                                         │
└─────────────────────────────────────────┘
```

### Slide Gerado (Saída)

```
┌─────────────────────────────────────────┐
│                                         │
│     ALCANCE: 45.5 m                     │
│                                         │
│     João Silva                          │
│     Maria Santos                        │
│     Ana Oliveira                        │
│     Pedro Costa                         │
│     Equipe: 01                          │
│                                         │
│     Colégio Estadual Xyz                │
│     Campinas / SP                       │
│                                         │
└─────────────────────────────────────────┘
```

### Observações

- ✓ Nomes dos alunos (Ana e Pedro) ordenados alfabeticamente
- ✓ Líder aparece primeiro, acompanhante em segundo
- ✓ Alcance formatado com prefixo "ALCANCE:" e sufixo "m"
- ✓ Equipe extraída como "01" (última palavra)
- ✓ Nome da escola formatado (primeira letra maiúscula)
- ✓ Cidade e estado combinados com " / "

## 🏆 Exemplo com Múltiplas Equipes

### Cenário

Três equipes com diferentes alcances, demonstrando ordenação automática.

### Arquivo DOCX (Entrada)

```
┌────────┬──────────┬────────────────┬──────────────┬─────────────────────┬──────────┬────────┐
│ Válido │ Equipe   │ Nome           │ Função       │ Escola              │ Cidade   │ Estado │
├────────┼──────────┼────────────────┼──────────────┼─────────────────────┼──────────┼────────┤
│ 38.2   │ Beta 02  │ Carlos Souza   │ Líder        │ Escola Municipal ABC│ São Paulo│ SP     │
│ 38.2   │ Beta 02  │ Julia Lima     │ Aluno        │ Escola Municipal ABC│ São Paulo│ SP     │
│ 38.2   │ Beta 02  │ Bruno Mendes   │ Aluno        │ Escola Municipal ABC│ São Paulo│ SP     │
├────────┼──────────┼────────────────┼──────────────┼─────────────────────┼──────────┼────────┤
│ 52.8   │ Gamma 03 │ Fernanda Costa │ Líder        │ Instituto Federal   │ Sorocaba │ SP     │
│ 52.8   │ Gamma 03 │ Roberto Dias   │ Acompanhante │ Instituto Federal   │ Sorocaba │ SP     │
│ 52.8   │ Gamma 03 │ Carla Nunes    │ Aluno        │ Instituto Federal   │ Sorocaba │ SP     │
├────────┼──────────┼────────────────┼──────────────┼─────────────────────┼──────────┼────────┤
│ 45.5   │ Alpha 01 │ João Silva     │ Líder        │ Colégio Estadual XYZ│ Campinas │ SP     │
│ 45.5   │ Alpha 01 │ Ana Oliveira   │ Aluno        │ Colégio Estadual XYZ│ Campinas │ SP     │
└────────┴──────────┴────────────────┴──────────────┴─────────────────────┴──────────┴────────┘
```

### Ordem dos Slides Gerados

**Slide 1 - Beta 02 (38.2 m)**
```
ALCANCE: 38.2 m

Carlos Souza
Bruno Mendes
Julia Lima
Equipe: 02

Escola Municipal Abc
São Paulo / SP
```

**Slide 2 - Alpha 01 (45.5 m)**
```
ALCANCE: 45.5 m

João Silva
Ana Oliveira
Equipe: 01

Colégio Estadual Xyz
Campinas / SP
```

**Slide 3 - Gamma 03 (52.8 m)**
```
ALCANCE: 52.8 m

Fernanda Costa
Roberto Dias
Carla Nunes
Equipe: 03

Instituto Federal
Sorocaba / SP
```

### Observações

- ✓ Equipes ordenadas por alcance (38.2 → 45.5 → 52.8)
- ✓ Ordem de entrada no DOCX não importa
- ✓ Alunos ordenados alfabeticamente dentro de cada equipe
- ✓ Total de slides: 3

## 🔄 Exemplo com Variações de Colunas

### Cenário

Demonstração de diferentes nomes de colunas que são reconhecidos automaticamente.

### Variação 1: Nomes Alternativos

```
┌─────────────────────┬─────────────┬─────────────┬────────────┬─────────────┬──────────┬────┐
│ Lançamentos Válidos │ Nome Equipe │ Integrante  │ Papel      │ Instituição │ Município│ UF │
├─────────────────────┼─────────────┼─────────────┼────────────┼─────────────┼──────────┼────┤
│ 40.0                │ Delta 04    │ Paulo Ramos │ lider      │ ETEC Exemplo│ Jundiaí  │ sp │
│ 40.0                │ Delta 04    │ Laura Silva │ aluno      │ ETEC Exemplo│ Jundiaí  │ sp │
└─────────────────────┴─────────────┴─────────────┴────────────┴─────────────┴──────────┴────┘
```

**Resultado**: ✓ Todas as colunas reconhecidas corretamente

### Variação 2: Colunas com Pontuação

```
┌───────────┬──────────────┬─────────────────┬────────────────┬──────────────┬────────┬────────┐
│ Alcance(m)│ Equipe       │ Nome do Aluno   │ Função/Role    │ Nome Escola  │ Cidade │ Estado │
├───────────┼──────────────┼─────────────────┼────────────────┼──────────────┼────────┼────────┤
│ 35,5      │ Epsilon 05   │ RICARDO SANTOS  │ Líder          │ escola abc   │ itu    │ SP     │
└───────────┴──────────────┴─────────────────┴────────────────┴──────────────┴────────┴────────┘
```

**Resultado**: ✓ Reconhecido como:
- "Alcance(m)" → Campo Válido
- "Nome do Aluno" → Campo Nome
- "Função/Role" → Campo Função
- Formatação aplicada: "Ricardo Santos", "Escola Abc", "Itu"

### Variação 3: Ordem Diferente das Colunas

```
┌─────────────┬────────┬──────────┬───────────┬────────────┬──────────┬────────┐
│ Nome        │ Função │ Equipe   │ Válido    │ Cidade     │ Estado   │ Escola │
├─────────────┼────────┼──────────┼───────────┼────────────┼──────────┼────────┤
│ Sofia Costa │ aluno  │ Zeta 06  │ 42.3      │ Campinas   │ SP       │ EMEF X │
└─────────────┴────────┴──────────┴───────────┴────────────┴──────────┴────────┘
```

**Resultado**: ✓ Ordem das colunas não importa - todas reconhecidas

## 🎭 Casos de Uso Especiais

### Caso 1: Equipe Sem Acompanhante

**Entrada**:
```
┌────────┬──────────┬──────────────┬────────┬─────────┬────────┬────────┐
│ Válido │ Equipe   │ Nome         │ Função │ Escola  │ Cidade │ Estado │
├────────┼──────────┼──────────────┼────────┼─────────┼────────┼────────┤
│ 40.0   │ Solo 07  │ Marcos Silva │ Líder  │ EMEF AB │ Itu    │ SP     │
│ 40.0   │ Solo 07  │ Lucia Gomes  │ Aluno  │ EMEF AB │ Itu    │ SP     │
│ 40.0   │ Solo 07  │ Tiago Rocha  │ Aluno  │ EMEF AB │ Itu    │ SP     │
└────────┴──────────┴──────────────┴────────┴─────────┴────────┴────────┘
```

**Saída**:
```
ALCANCE: 40.0 m

Marcos Silva
Lucia Gomes
Tiago Rocha
Equipe: 07

Emef Ab
Itu / SP
```

**Observação**: ✓ Funciona perfeitamente sem acompanhante

### Caso 2: Equipe Sem Líder

**Entrada**:
```
┌────────┬──────────┬────────────────┬──────────────┬─────────┬────────┬────────┐
│ Válido │ Equipe   │ Nome           │ Função       │ Escola  │ Cidade │ Estado │
├────────┼──────────┼────────────────┼──────────────┼─────────┼────────┼────────┤
│ 35.0   │ NoLdr 08 │ Prof. João     │ Acompanhante │ EMEF CD │ Salto  │ SP     │
│ 35.0   │ NoLdr 08 │ Alice Martins  │ Aluno        │ EMEF CD │ Salto  │ SP     │
│ 35.0   │ NoLdr 08 │ Diego Santos   │ Aluno        │ EMEF CD │ Salto  │ SP     │
└────────┴──────────┴────────────────┴──────────────┴─────────┴────────┴────────┘
```

**Saída**:
```
ALCANCE: 35.0 m

Prof. João
Alice Martins
Diego Santos
Equipe: 08

Emef Cd
Salto / SP
```

**Observação**: ✓ Acompanhante aparece primeiro, seguido por alunos

### Caso 3: Equipe Grande (6+ Membros)

**Entrada**:
```
┌────────┬──────────┬────────────────┬──────────────┬─────────┬──────────┬────────┐
│ Válido │ Equipe   │ Nome           │ Função       │ Escola  │ Cidade   │ Estado │
├────────┼──────────┼────────────────┼──────────────┼─────────┼──────────┼────────┤
│ 50.0   │ Big 09   │ Roberto Lima   │ Líder        │ ETEC XY │ Sorocaba │ SP     │
│ 50.0   │ Big 09   │ Profª Ana      │ Acompanhante │ ETEC XY │ Sorocaba │ SP     │
│ 50.0   │ Big 09   │ Carlos Dias    │ Aluno        │ ETEC XY │ Sorocaba │ SP     │
│ 50.0   │ Big 09   │ Beatriz Costa  │ Aluno        │ ETEC XY │ Sorocaba │ SP     │
│ 50.0   │ Big 09   │ Eduardo Nunes  │ Aluno        │ ETEC XY │ Sorocaba │ SP     │
│ 50.0   │ Big 09   │ Fernanda Silva │ Aluno        │ ETEC XY │ Sorocaba │ SP     │
│ 50.0   │ Big 09   │ Gabriel Souza  │ Aluno        │ ETEC XY │ Sorocaba │ SP     │
└────────┴──────────┴────────────────┴──────────────┴─────────┴──────────┴────────┘
```

**Saída**:
```
ALCANCE: 50.0 m

Roberto Lima
Profª Ana
Beatriz Costa
Carlos Dias
Eduardo Nunes
Fernanda Silva
Gabriel Souza
Equipe: 09

Etec Xy
Sorocaba / SP
```

**Observação**: ✓ Todos os 7 membros listados, alunos em ordem alfabética

### Caso 4: Vírgula vs. Ponto no Alcance

**Entrada**:
```
┌────────┬──────────┬──────────────┬────────┬─────────┬────────┬────────┐
│ Válido │ Equipe   │ Nome         │ Função │ Escola  │ Cidade │ Estado │
├────────┼──────────┼──────────────┼────────┼─────────┼────────┼────────┤
│ 45,5   │ Comma 10 │ João Silva   │ Líder  │ EMEF AA │ Itu    │ SP     │
│ 45.5   │ Dot 11   │ Maria Santos │ Líder  │ EMEF BB │ Salto  │ SP     │
└────────┴──────────┴──────────────┴────────┴─────────┴────────┴────────┘
```

**Saída**: ✓ Ambos reconhecidos como 45.5 (mesma ordenação)

### Caso 5: Nomes em MAIÚSCULAS

**Entrada**:
```
┌────────┬──────────┬───────────────────┬────────┬──────────────┬────────┬────────┐
│ Válido │ Equipe   │ Nome              │ Função │ Escola       │ Cidade │ Estado │
├────────┼──────────┼───────────────────┼────────┼──────────────┼────────┼────────┤
│ 40.0   │ CAPS 12  │ JOÃO PAULO SILVA  │ LÍDER  │ EMEF EXEMPLO │ ITU    │ sp     │
│ 40.0   │ CAPS 12  │ MARIA CLARA COSTA │ ALUNO  │ EMEF EXEMPLO │ ITU    │ sp     │
└────────┴──────────┴───────────────────┴────────┴──────────────┴────────┴────────┘
```

**Saída**:
```
ALCANCE: 40.0 m

João Paulo Silva
Maria Clara Costa
Equipe: 12

Emef Exemplo
Itu / SP
```

**Observação**: ✓ Formatação aplicada corretamente (Title Case)

### Caso 6: Valores de Alcance Inválidos

**Entrada**:
```
┌────────┬──────────┬──────────────┬────────┬─────────┬────────┬────────┐
│ Válido │ Equipe   │ Nome         │ Função │ Escola  │ Cidade │ Estado │
├────────┼──────────┼──────────────┼────────┼─────────┼────────┼────────┤
│ N/A    │ Inv 13   │ Pedro Silva  │ Líder  │ EMEF AA │ Itu    │ SP     │
│ 40.0   │ Val 14   │ Ana Costa    │ Líder  │ EMEF BB │ Salto  │ SP     │
│ --     │ Inv2 15  │ João Santos  │ Líder  │ EMEF CC │ Indaiatuba│ SP  │
└────────┴──────────┴──────────────┴────────┴─────────┴────────┴────────┘
```

**Ordem dos Slides**:
1. Val 14 (40.0)
2. Inv 13 (inválido → ordenação = infinito)
3. Inv2 15 (inválido → ordenação = infinito)

**Observação**: ⚠ Equipes com alcance inválido vão para o final

## 🔧 Troubleshooting com Exemplos

### Problema 1: Nomes Não Aparecem

**Entrada Problemática**:
```
┌────────┬──────────┬────────────┬────────┬─────────┬────────┬────────┐
│ Válido │ Equipe   │ Estudante  │ Função │ Escola  │ Cidade │ Estado │
├────────┼──────────┼────────────┼────────┼─────────┼────────┼────────┤
│ 40.0   │ Test 16  │ João Silva │ Líder  │ EMEF AA │ Itu    │ SP     │
└────────┴──────────┴────────────┴────────┴─────────┴────────┴────────┘
```

**Diagnóstico**: ⚠ Coluna "Estudante" não é reconhecida como "Nome"

**Solução**: Renomear para um dos aliases aceitos:
- "Nome"
- "Nome do Integrante"
- "Integrante"
- "Participante"
- "Aluno"

### Problema 2: Ordenação Errada

**Entrada Problemática**:
```
┌────────┬──────────┬──────────────┬────────┬─────────┬────────┬────────┐
│ Válido │ Equipe   │ Nome         │ Função │ Escola  │ Cidade │ Estado │
├────────┼──────────┼──────────────┼────────┼─────────┼────────┼────────┤
│ 40.0   │ Team A   │ João Silva   │ Líder  │ EMEF AA │ Itu    │ SP     │
│ 40.0   │ Team A   │ Maria Santos │ Aluno  │ EMEF AA │ Itu    │ SP     │
│ 50.0   │ Team B   │ Pedro Costa  │ Líder  │ EMEF BB │ Salto  │ SP     │
│ 35.0   │ Team B   │ Ana Oliveira │ Aluno  │ EMEF BB │ Salto  │ SP     │
└────────┴──────────┴──────────────┴────────┴─────────┴────────┴────────┘
```

**Diagnóstico**: ⚠ Team B tem alcances diferentes (50.0 e 35.0)

**Solução**: Garantir que **todos os membros da mesma equipe** tenham o **mesmo valor** de alcance.

**Entrada Corrigida**:
```
┌────────┬──────────┬──────────────┬────────┬─────────┬────────┬────────┐
│ Válido │ Equipe   │ Nome         │ Função │ Escola  │ Cidade │ Estado │
├────────┼──────────┼──────────────┼────────┼─────────┼────────┼────────┤
│ 40.0   │ Team A   │ João Silva   │ Líder  │ EMEF AA │ Itu    │ SP     │
│ 40.0   │ Team A   │ Maria Santos │ Aluno  │ EMEF AA │ Itu    │ SP     │
│ 35.0   │ Team B   │ Pedro Costa  │ Líder  │ EMEF BB │ Salto  │ SP     │
│ 35.0   │ Team B   │ Ana Oliveira │ Aluno  │ EMEF BB │ Salto  │ SP     │
└────────┴──────────┴──────────────┴────────┴─────────┴────────┴────────┘
```

### Problema 3: Placeholders Não Substituídos

**Template Problemático**:
```
┌─────────────────────────────────────────┐
│                                         │
│     {{ALCANCE_VALIDO}}                  │  ← Nome errado
│                                         │
│     {{NOMES}}                           │  ← Nome errado
│                                         │
└─────────────────────────────────────────┘
```

**Diagnóstico**: ⚠ Nomes dos placeholders incorretos

**Solução**: Usar os nomes exatos:
- `{{LANCAMENTOS_VALIDOS}}` (não "ALCANCE_VALIDO")
- `{{NOMES_ALUNOS}}` (não "NOMES")

**Template Corrigido**:
```
┌─────────────────────────────────────────┐
│                                         │
│     {{LANCAMENTOS_VALIDOS}}             │  ✓
│                                         │
│     {{NOMES_ALUNOS}}                    │  ✓
│                                         │
└─────────────────────────────────────────┘
```

### Problema 4: Acentos e Caracteres Especiais

**Entrada**:
```
┌────────┬──────────┬────────────────┬────────┬─────────────┬────────────┬────────┐
│ Válido │ Equipe   │ Nome           │ Função │ Escola      │ Cidade     │ Estado │
├────────┼──────────┼────────────────┼────────┼─────────────┼────────────┼────────┤
│ 40.0   │ Açaí 17  │ José João      │ Líder  │ EMEF São José│ São Paulo │ SP     │
└────────┴──────────┴────────────────┴────────┴─────────────┴────────────┴────────┘
```

**Saída**: ✓ Funciona corretamente
```
ALCANCE: 40.0 m

José João
Equipe: 17

Emef São José
São Paulo / SP
```

**Observação**: ✓ Acentos são preservados nos dados, normalizados apenas para comparação

## 📊 Resumo de Boas Práticas

### Para Arquivos DOCX

✓ **Faça**:
- Use nomes de colunas da lista de aliases
- Mantenha alcance igual para todos os membros da equipe
- Preencha todas as informações obrigatórias
- Use palavras-chave claras para funções (líder, acompanhante, aluno)

✗ **Evite**:
- Nomes de colunas inventados
- Alcances diferentes para mesma equipe
- Células vazias em campos obrigatórios
- Funções sem palavras-chave reconhecidas

### Para Templates PPTX

✓ **Faça**:
- Use placeholders exatos: `{{LANCAMENTOS_VALIDOS}}`, `{{NOME_EQUIPE}}`, etc.
- Deixe espaço suficiente para múltiplos nomes
- Teste com dados reais antes de produção
- Mantenha backup do template original

✗ **Evite**:
- Placeholders com nomes incorretos
- Caixas de texto muito pequenas
- Modificar template durante processamento

---

**Documentação Relacionada**:
- [USAGE.md](USAGE.md) - Guia de uso passo a passo
- [INPUT_FORMAT.md](INPUT_FORMAT.md) - Especificações técnicas detalhadas
