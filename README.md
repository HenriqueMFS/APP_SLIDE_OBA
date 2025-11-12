# 🚀 APP_SLIDE_OBA - Gerador Automático de Slides

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-FF4B4B)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Sumário

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Uso Rápido](#-uso-rápido)
- [Documentação Completa](#-documentação-completa)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Tecnologias](#-tecnologias)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

## 🎯 Visão Geral

O **APP_SLIDE_OBA** é uma aplicação web automatizada desenvolvida para gerar apresentações em PowerPoint de forma rápida e eficiente para eventos da **Olimpíada Brasileira de Astronomia (OBA)**. A ferramenta extrai dados de equipes e participantes de um documento Word (DOCX) e os insere automaticamente em um template PowerPoint (PPTX), criando slides personalizados para cada equipe.

### Problema Resolvido

Criar manualmente dezenas ou centenas de slides com informações de equipes é uma tarefa repetitiva, demorada e propensa a erros. Esta aplicação automatiza completamente esse processo, reduzindo horas de trabalho manual para apenas alguns cliques.

### Principais Benefícios

- ⚡ **Rapidez**: Gera dezenas de slides em segundos
- 🎯 **Precisão**: Elimina erros de digitação e formatação inconsistente
- 🔄 **Flexibilidade**: Reconhece múltiplos formatos de colunas no DOCX
- 🎨 **Consistência**: Mantém formatação profissional em todos os slides
- 📊 **Ordenação Inteligente**: Organiza equipes por desempenho automaticamente

## ✨ Funcionalidades

### 1. Extração Inteligente de Dados

- **Reconhecimento Automático de Colunas**: Identifica colunas por múltiplos aliases e palavras-chave
- **Normalização de Texto**: Trata variações de acentuação e formatação
- **Campos Suportados**:
  - ✅ Alcance/Lançamentos válidos
  - ✅ Nome da equipe
  - ✅ Nome da escola
  - ✅ Cidade e Estado (UF)
  - ✅ Nomes dos participantes (líder, acompanhante, alunos)
  - ✅ Função/Role dos membros

### 2. Processamento de Equipes

- **Ordenação Automática**: Organiza equipes por desempenho (alcance dos lançamentos)
- **Agrupamento Hierárquico**: Separa líder, acompanhante e alunos
- **Ordenação Alfabética**: Ordena nomes de alunos alfabeticamente dentro de cada equipe

### 3. Geração de Slides

- **Duplicação com Mídia**: Preserva imagens, formas e elementos visuais do template
- **Substituição de Placeholders**: Substitui automaticamente os seguintes marcadores:
  - `{{LANCAMENTOS_VALIDOS}}` → Alcance formatado
  - `{{NOME_EQUIPE}}` → Nome da equipe
  - `{{NOME_ESCOLA}}` → Nome da escola formatada
  - `{{CIDADE_UF}}` → Cidade e Estado
  - `{{NOMES_ALUNOS}}` → Lista de participantes

### 4. Formatação Avançada

- **Estilos Personalizados por Tipo de Informação**:
  - Alcance: Fonte Lexend, 28-35pt, azul (#006FC0), negrito e sublinhado
  - Nomes: Fonte Lexend, 26.5pt, branco, negrito
  - Equipe: Fonte Lexend, 20pt, branco, negrito
  - Escola/Cidade: Fonte Lexend, 20pt, branco, negrito
- **Alinhamento Centralizado**: Todos os textos centralizados automaticamente
- **Tratamento de Múltiplos Parágrafos**: Lida com placeholders em linhas diferentes

### 5. Interface Streamlit

- **Upload de Arquivos**: Interface drag-and-drop para DOCX e PPTX
- **Nome Customizável**: Define nome do arquivo de saída
- **Sanitização de Nomes**: Remove caracteres inválidos automaticamente
- **Feedback Visual**: Mostra quantidade de slides gerados e GIF de sucesso
- **Download Direto**: Botão para baixar apresentação final

## 🔧 Requisitos

### Requisitos de Sistema

- Python 3.8 ou superior
- 2GB de RAM (mínimo)
- Sistema operacional: Windows, macOS ou Linux

### Dependências Python

```txt
streamlit>=1.0.0
python-docx>=0.8.11
python-pptx>=0.6.21
Pillow>=9.0.0
lxml>=4.9.0
```

## 📥 Instalação

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/APP_SLIDE_OBA.git
cd APP_SLIDE_OBA
```

### 2. Crie um Ambiente Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Verifique os Arquivos de Recursos

Certifique-se de que os seguintes arquivos estão no diretório raiz:

- `logo_jornada.png` - Logo exibido na interface
- `tiapamela.gif` - GIF de sucesso após geração

## 🚀 Uso Rápido

### 1. Inicie a Aplicação

```bash
streamlit run APP.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`

### 2. Prepare Seus Arquivos

- **Arquivo DOCX**: Documento com tabela contendo dados das equipes
- **Template PPTX**: Apresentação modelo com placeholders

### 3. Gere os Slides

1. Faça upload do arquivo DOCX
2. Faça upload do template PPTX
3. (Opcional) Digite um nome para o arquivo de saída
4. Clique em "Confirmar nome do arquivo"
5. Clique em "✨ Gerar Apresentação"
6. Aguarde o processamento
7. Clique em "📥 Baixar Apresentação Final"

## 📚 Documentação Completa

Para informações detalhadas, consulte:

- **[USAGE.md](docs/USAGE.md)** - Guia de uso passo a passo com screenshots
- **[INPUT_FORMAT.md](docs/INPUT_FORMAT.md)** - Especificações do formato DOCX de entrada
- **[EXAMPLES.md](docs/EXAMPLES.md)** - Exemplos práticos e casos de uso

## 📁 Estrutura do Projeto

```
APP_SLIDE_OBA/
├── APP.py                    # Aplicação principal
├── README.md                 # Este arquivo
├── requirements.txt          # Dependências Python
├── logo_jornada.png         # Logo da aplicação
├── tiapamela.gif            # GIF de sucesso
├── docs/                    # Documentação detalhada
│   ├── USAGE.md            # Guia de uso
│   ├── INPUT_FORMAT.md     # Formato de entrada
│   └── EXAMPLES.md         # Exemplos práticos
└── tests/                   # Testes (se houver)
```

## 🛠️ Tecnologias

- **[Streamlit](https://streamlit.io/)** - Framework web para aplicações de dados
- **[python-docx](https://python-docx.readthedocs.io/)** - Leitura de arquivos Word
- **[python-pptx](https://python-pptx.readthedocs.io/)** - Manipulação de PowerPoint
- **[Pillow](https://pillow.readthedocs.io/)** - Processamento de imagens
- **[lxml](https://lxml.de/)** - Parsing XML para manipulação avançada de PPTX

## 🔍 Recursos Técnicos Avançados

### Reconhecimento Inteligente de Colunas

O sistema utiliza três estratégias de reconhecimento:

1. **Correspondência Exata**: Compara com lista de aliases conhecidos
2. **Palavras-chave em Tokens**: Busca palavras-chave em partes do cabeçalho
3. **Substring Matching**: Encontra palavras-chave no texto completo

### Normalização de Texto

```python
# Remove acentos, normaliza espaços, converte para minúsculas
"Função do Aluno" → "funcao do aluno"
```

### Preservação de Mídia em Slides

- Copia imagens com seus dados binários
- Atualiza referências XML corretamente
- Mantém relacionamentos entre partes do PPTX

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Equipe OBA** - Desenvolvimento inicial

## 🙏 Agradecimentos

- Olimpíada Brasileira de Astronomia (OBA)
- Comunidade Streamlit
- Todos os contribuidores

## 📞 Suporte

Para reportar bugs ou solicitar funcionalidades:

- Abra uma [issue no GitHub](https://github.com/seu-usuario/APP_SLIDE_OBA/issues)
- Entre em contato com a equipe OBA

---

**Desenvolvido com ❤️ para a Olimpíada Brasileira de Astronomia**
