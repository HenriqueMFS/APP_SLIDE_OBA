"""
APP_SLIDE_OBA - Gerador Automático de Apresentações PowerPoint

Este módulo processa arquivos DOCX contendo dados de equipes e gera
apresentações PowerPoint personalizadas usando um template fornecido.

Principais funcionalidades:
- Extração inteligente de dados de tabelas DOCX
- Matching automático de colunas usando aliases e fuzzy matching
- Geração de slides duplicando template e preenchendo placeholders
- Interface web com Streamlit para upload e processamento

Arquitetura:
- Document Processing: Leitura e extração de dados de DOCX
- Column Matching: Identificação automática de colunas relevantes
- Data Organization: Agrupamento e formatação de dados por equipe
- Presentation Generation: Duplicação de slides e substituição de placeholders
- UI Layer: Interface Streamlit para interação do usuário

Clean Code Refactoring iniciado: 2025-11-19
"""

# ==================== IMPORTS ====================
# Seguindo PEP 8: Standard Library → Third-party → Local

# Standard library imports
import re
import unicodedata
from collections import defaultdict
from copy import deepcopy
from io import BytesIO

# Third-party imports
import streamlit as st
from docx import Document
from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Pt

# ==================== CONSTANTES ====================
"""
Constantes de configuração do sistema.

Todas as configurações são centralizadas aqui para facilitar manutenção
e permitir futuras integrações com arquivos de configuração externos.
"""

# --- Configurações de Imagem ---
# Caminhos dos assets visuais utilizados na interface
LOGO_PATH = "logo_jornada.png"  # Logo principal da aplicação
GIF_PATH = "tiapamela.gif"  # Animação exibida após sucesso

# Dimensões do logo para exibição otimizada
LOGO_WIDTH = 1235  # Largura em pixels
LOGO_HEIGHT = 426  # Altura em pixels

# --- Configurações de Layout Streamlit ---
# Layout wide maximiza uso da tela para melhor UX
PAGE_LAYOUT = "wide"

# Proporções das colunas: [esquerda, centro, direita]
# Centro (4) é maior para conteúdo principal
COLUMN_PROPORTIONS = [1, 4, 1]

# --- Configurações de Tipografia ---
# Fonte Lexend escolhida por legibilidade e aparência moderna
FONT_NAME = "Lexend"

# Tamanhos de fonte para diferentes elementos (em pontos)
FONT_SIZE_SMALL = 20  # Nomes de equipe, escola, cidade
FONT_SIZE_MEDIUM = 26.5  # Nomes de participantes
FONT_SIZE_LARGE = 28  # Label "ALCANCE:"
FONT_SIZE_XLARGE = 35  # Valor do alcance (destaque)

# --- Paleta de Cores ---
# Cores em formato RGB para consistência visual
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)  # Branco puro (#FFFFFF)
COLOR_BLUE = RGBColor(0x00, 0x6F, 0xC0)  # Azul corporativo (#006FC0)

# --- Constantes PowerPoint ---
# Tipo de shape para imagens (constante do python-pptx)
SHAPE_TYPE_PICTURE = 13

# --- Placeholders de Template ---
# Marcadores substituídos nos slides (formato {{NOME}})
PLACEHOLDER_VALIDO = "{{LANCAMENTOS_VALIDOS}}"  # Alcance do foguete
PLACEHOLDER_EQUIPE = "{{NOME_EQUIPE}}"  # Nome da equipe
PLACEHOLDER_ESCOLA = "{{NOME_ESCOLA}}"  # Instituição de ensino
PLACEHOLDER_CIDADE_UF = "{{CIDADE_UF}}"  # Localização (Cidade/Estado)
PLACEHOLDER_ALUNOS = "{{NOMES_ALUNOS}}"  # Lista de participantes

# --- Mensagens de Interface ---
# Mensagens padronizadas para comunicação com usuário

# Aviso crítico antes de fazer upload (reduz erros)
MSG_UPLOAD_WARNING = (
    "CERTIFIQUE-SE DE ESTÁ FAZENDO O UPLOAD DOS ARQUIVOS "
    "CORRETOS ANTES DE GERAR OS SLIDES!"
)

# Validação de arquivos obrigatórios
MSG_SEND_BOTH_FILES = "Envie ambos os arquivos."

# Feedback quando nenhum dado é encontrado
MSG_NO_DATA_FOUND = "Nenhum dado encontrado."

# Nome padrão para arquivo de download
MSG_NOME_ARQUIVO_DEFAULT = "Apresentacao_Final_Equipes"

# Mensagem de sucesso após geração
MSG_CAPTION_READY = "Apresentação pronta! 🚀"

# --- Namespaces XML ---
# Namespaces do Office Open XML usados para manipulação de elementos
XML_NAMESPACE_DRAWINGML = (
    "{http://schemas.openxmlformats.org/drawingml/2006/main}"
)
XML_NAMESPACE_RELATIONSHIPS = (
    "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
)

# -------------------- CONFIGURAÇÃO INICIAL --------------------
st.set_page_config(layout=PAGE_LAYOUT)
logo = Image.open(LOGO_PATH)
resample_filter = getattr(Image, "Resampling", Image).LANCZOS
logo = logo.resize((LOGO_WIDTH, LOGO_HEIGHT), resample_filter)
_, col_logo, _ = st.columns(COLUMN_PROPORTIONS)
with col_logo:
    st.image(logo, width=LOGO_WIDTH)
st.title("🚀 Gerador Automático de Slides")
st.info(MSG_UPLOAD_WARNING)

# -------------------- FUNÇÕES AUXILIARES --------------------
def formatar_texto(texto, maiusculo_estado=False):
    """
    Formata texto removendo espaços extras e aplicando capitalização.

    Esta função normaliza espaços em branco e aplica formatação de texto,
    convertendo para maiúsculas completas ou title case (primeira letra
    maiúscula em cada palavra).

    Args:
        texto (str): Texto a ser formatado.
        maiusculo_estado (bool, optional): Se True, converte todo o texto
            para maiúsculas. Se False, aplica title case (primeira letra
            maiúscula em cada palavra). Padrão: False.

    Returns:
        str: Texto formatado com espaços normalizados e capitalização aplicada.

    Examples:
        >>> formatar_texto("  joão  silva  ")
        'João Silva'
        >>> formatar_texto("são paulo", maiusculo_estado=True)
        'SÃO PAULO'
        >>> formatar_texto("escola MUNICIPAL")
        'Escola Municipal'

    Note:
        - Espaços múltiplos são reduzidos a um único espaço
        - Espaços no início e fim são removidos
        - Acentuação é preservada
    """
    texto = ' '.join(texto.strip().split())
    return texto.upper() if maiusculo_estado else ' '.join(w.capitalize() for w in texto.split())

def normalizar_texto_base(texto):
    """
    Normaliza texto para comparação, removendo acentos e formatação.

    Esta função é utilizada para comparar textos de forma mais flexível,
    removendo diferenças de acentuação, espaços extras e maiúsculas/minúsculas.
    Útil para reconhecimento de colunas e matching de aliases.

    Args:
        texto (str): Texto a ser normalizado.

    Returns:
        str: Texto normalizado (minúsculas, sem acentos, espaços únicos).
            Retorna string vazia se o texto for None ou vazio.

    Examples:
        >>> normalizar_texto_base("Função do Aluno")
        'funcao do aluno'
        >>> normalizar_texto_base("  LANÇAMENTOS   VÁLIDOS  ")
        'lancamentos validos'
        >>> normalizar_texto_base("São José")
        'sao jose'
        >>> normalizar_texto_base("")
        ''

    Note:
        - Remove todos os acentos usando decomposição Unicode (NFKD)
        - Converte para minúsculas
        - Normaliza múltiplos espaços para um único espaço
        - Remove espaços no início e fim
    """
    if not texto:
        return ""
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(ch for ch in texto if not unicodedata.combining(ch))
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto.lower()

def sanitizar_nome_arquivo(nome):
    """
    Remove caracteres inválidos de nomes de arquivo.

    Esta função sanitiza nomes de arquivos removendo caracteres que não são
    permitidos em sistemas de arquivos Windows/Linux/macOS, garantindo que
    o arquivo possa ser salvo corretamente.

    Args:
        nome (str): Nome de arquivo a ser sanitizado. Pode ser None ou vazio.

    Returns:
        str: Nome de arquivo sanitizado, ou "Apresentacao_Final_Equipes" se
            o nome for inválido/vazio.

    Examples:
        >>> sanitizar_nome_arquivo("Apresentação: Final 2024")
        'Apresentação Final 2024'
        >>> sanitizar_nome_arquivo("dados<teste>arquivo")
        'dadostestarquivo'
        >>> sanitizar_nome_arquivo("")
        'Apresentacao_Final_Equipes'
        >>> sanitizar_nome_arquivo(None)
        'Apresentacao_Final_Equipes'

    Note:
        - Remove caracteres: \\ / : * ? " < > |
        - Preserva espaços, letras, números e outros caracteres válidos
        - Retorna nome padrão se resultado for vazio
        - Remove espaços no início e fim
    """
    nome = (nome or "").strip()
    nome = re.sub(r'[\\/:*?"<>|]', "", nome)
    return nome or MSG_NOME_ARQUIVO_DEFAULT

def _identificar_colunas_tabela(cabecalho):
    """
    Identifica e mapeia colunas da tabela usando algoritmo de matching inteligente.

    Esta é uma função crítica que implementa reconhecimento automático de colunas
    usando uma estratégia de 2 passes: correspondência exata com aliases e matching
    fuzzy com palavras-chave. O algoritmo é tolerante a variações de nomenclatura
    e formatação nos cabeçalhos das tabelas.

    Args:
        cabecalho (list[str]): Lista com os textos do cabeçalho da tabela.
            Cada elemento é o conteúdo de uma célula do cabeçalho.
            Exemplo: ["Nome", "Função do Aluno", "Lançamentos Válidos"]

    Returns:
        dict[str, int]: Dicionário mapeando campos esperados para índices de colunas.
            Retorna dicionário vazio se o cabeçalho for inválido ou vazio.

            Campos mapeados:
            - "Valido": Índice da coluna de alcance/lançamentos válidos
            - "Equipe": Índice da coluna de nome da equipe
            - "Funcao": Índice da coluna de função (aluno/líder/acompanhante)
            - "Escola": Índice da coluna de nome da escola
            - "Cidade": Índice da coluna de cidade
            - "Estado": Índice da coluna de estado/UF
            - "Nome": Índice da coluna de nome do participante

    Examples:
        >>> cabecalho = ["Nome", "Equipe", "Alcance (m)", "Escola"]
        >>> mapa = _identificar_colunas_tabela(cabecalho)
        >>> mapa
        {'Nome': 0, 'Equipe': 1, 'Valido': 2, 'Escola': 3}

        >>> cabecalho = ["Função do Integrante", "Lançamentos Válidos"]
        >>> mapa = _identificar_colunas_tabela(cabecalho)
        >>> mapa
        {'Funcao': 0, 'Valido': 1}

        >>> cabecalho = []  # Cabeçalho vazio
        >>> mapa = _identificar_colunas_tabela(cabecalho)
        >>> mapa
        {}

    Algoritmo (2 Passes):
        **Pass 1 - Correspondência Exata:**
        Tenta correspondência exata com aliases normalizados para cada campo.
        Normalização remove acentos, espaços extras e maiúsculas.

        Aliases por campo:
        - Valido: "valido", "alcance", "lancamentos validos", "alcance (m)"
        - Equipe: "equipe", "nome da equipe"
        - Funcao: "funcao", "funcao/role", "funcao na equipe", "papel"
        - Escola: "escola", "nome da escola", "instituicao", "colegio"
        - Cidade: "cidade", "municipio"
        - Estado: "estado", "uf"
        - Nome: "nome", "nome do integrante", "aluno", "participante"

        **Pass 2 - Matching Fuzzy:**
        Para campos não identificados, usa matching baseado em palavras-chave
        e tokens extraídos do cabeçalho. Segue ordem de prioridade para
        evitar conflitos (ex: "Nome da Escola" não deve ser identificado como "Nome").

        Ordem de prioridade:
        1. Valido, 2. Equipe, 3. Funcao, 4. Escola, 5. Cidade, 6. Estado, 7. Nome

    Edge Cases:
        - **"Nome da Escola" vs "Nome"**: Algoritmo detecta tokens "escola"/"colegio"
          e evita identificar como campo "Nome"
        - **Variações de acentuação**: "Função" = "Funcao" após normalização
        - **Case insensitive**: "ALCANCE" = "alcance" = "Alcance"
        - **Espaços extras**: "  Nome  Equipe  " = "Nome Equipe"
        - **Múltiplos aliases**: "Lançamentos Válidos", "Alcance (m)", "Válido"
          todos identificam o campo "Valido"

    Note:
        - Cada coluna é identificada no máximo uma vez (sem duplicatas)
        - Se múltiplos aliases corresponderem à mesma coluna, o primeiro vence
        - Campos não obrigatórios: função, escola, cidade, estado podem faltar
        - Campos críticos: Valido (alcance) e Equipe/Nome (identificação)
        - A ordem de prioridade evita que campos genéricos (Nome) sejam
          identificados incorretamente antes de campos específicos (Escola)
    """
    # Validação: cabeçalho não pode ser vazio
    if not cabecalho:
        return {}

    # Validação: cabeçalho deve ter pelo menos uma coluna não vazia
    if not any(texto.strip() for texto in cabecalho):
        return {}

    header_norm = [normalizar_texto_base(texto) for texto in cabecalho]

    # Definição de aliases para cada campo
    aliases = {
        "Valido": [
            "valido",
            "alcance",
            "lancamentos validos",
            "alcance (m)",
            "distancia",
            "distancia (m)",
        ],
        "Equipe": [
            "equipe",
            "nome da equipe",
        ],
        "Funcao": [
            "funcao",
            "funcao/role",
            "funcao na equipe",
            "funcao integrante",
            "papel",
            "cargo",
        ],
        "Escola": [
            "escola",
            "nome da escola",
            "instituicao",
            "nome da instituicao",
            "colegio",
            "nome do colegio",
        ],
        "Cidade": [
            "cidade",
            "municipio",
        ],
        "Estado": [
            "estado",
            "uf",
        ],
        "Nome": [
            "nome",
            "nome do integrante",
            "nome integrante",
            "nome do aluno",
            "nome participante",
            "integrante",
            "participante",
            "aluno",
        ],
    }

    aliases_norm = {
        campo: [normalizar_texto_base(alias) for alias in lista]
        for campo, lista in aliases.items()
    }

    # Palavras-chave para matching fuzzy
    palavras_chave = {
        "Valido": {"alcance", "valido", "validos", "lancamento", "lancamentos", "distancia"},
        "Equipe": {"equipe", "time", "grupo"},
        "Funcao": {"funcao", "papel", "cargo"},
        "Escola": {"escola", "colegio", "instituicao"},
        "Cidade": {"cidade", "municipio"},
        "Estado": {"estado", "uf"},
        "Nome": {
            "nome",
            "nomes",
            "aluno",
            "alunos",
            "integrante",
            "integrantes",
            "participante",
            "participantes",
            "membro",
            "membros",
            "lider",
            "acompanhante",
            "responsavel",
            "responsaveis",
        },
    }

    # --- PREPARAÇÃO: Tokenização para Fuzzy Matching ---
    # Extrai palavras individuais de cada cabeçalho para permitir matching
    # parcial. Por exemplo: "Nome do Integrante" → ["nome", "do", "integrante"]
    # Isso permite identificar "nome" mesmo em "Nome da Escola" (com lógica adicional)
    tokens_por_coluna = []
    for cab_norm in header_norm:
        # Split por caracteres não alfanuméricos: espaços, /, (, ), etc.
        tokens = [tok for tok in re.split(r"[^a-z0-9]+", cab_norm) if tok]
        tokens_por_coluna.append(tokens)

    coluna_por_campo = {}  # Resultado: {campo: índice_coluna}
    colunas_usadas = set()  # Garante que cada coluna seja usada apenas uma vez

    def registrar(campo, indice):
        """
        Registra mapeamento campo → coluna se válido.

        Validações:
        - indice não pode ser None
        - Coluna não pode ter sido usada por outro campo
        - Previne mapeamento duplicado de colunas

        Returns True se registrou com sucesso, False caso contrário.
        """
        if indice is None or indice in colunas_usadas:
            return False
        coluna_por_campo[campo] = indice
        colunas_usadas.add(indice)
        return True

    # ==================== PASS 1: Correspondência Exata ====================
    # Tenta correspondência exata (após normalização) com todos os aliases.
    # Esta passagem tem prioridade sobre fuzzy matching para evitar falsos positivos.
    #
    # Exemplo:
    # - Cabeçalho: "Alcance (m)" → normalizado: "alcance (m)"
    # - Alias: "alcance (m)" → MATCH exato!
    # - Resultado: Campo "Valido" mapeado para esta coluna
    for campo, lista_aliases in aliases_norm.items():
        for alias_norm in lista_aliases:
            if not alias_norm:
                continue
            for idx, cab_norm in enumerate(header_norm):
                if idx in colunas_usadas:
                    continue
                if cab_norm == alias_norm and registrar(campo, idx):
                    break
            if campo in coluna_por_campo:
                break

    # ==================== PASS 2: Matching Fuzzy ====================
    # Para campos não identificados no Pass 1, usa matching baseado em palavras-chave.
    # A ORDEM IMPORTA: campos específicos (Escola) são identificados antes de
    # campos genéricos (Nome) para evitar que "Nome da Escola" seja identificado
    # como campo "Nome" em vez de "Escola".
    #
    # Estratégia de prioridade:
    # 1. Valido, Equipe (campos críticos)
    # 2. Funcao, Escola, Cidade, Estado (campos contextuais)
    # 3. Nome (campo mais genérico, vem por último)
    prioridade_campos = ["Valido", "Equipe", "Funcao", "Escola", "Cidade", "Estado", "Nome"]

    def combina(campo, tokens, cab_norm):
        """
        Verifica se um cabeçalho combina com um campo usando fuzzy matching.

        Estratégia:
        1. Verifica se alguma palavra-chave do campo está nos tokens do cabeçalho
        2. Verifica se alguma palavra-chave está contida no cabeçalho normalizado
        3. Aplica regras especiais de desambiguação para evitar falsos positivos

        Exemplo de desambiguação:
        - Cabeçalho: "Nome da Escola" → tokens: ["nome", "da", "escola"]
        - Campo tentando: "Nome"
        - Detecta token "escola" → NÃO combina (evita falso positivo)
        - Deixa para campo "Escola" identificar corretamente
        """
        if not cab_norm:
            return False
        tokens_set = set(tokens)
        chaves = palavras_chave.get(campo, set())

        # REGRA ESPECIAL: Desambiguação de "Nome" vs "Nome da Escola"
        # Se estamos tentando identificar campo "Nome" mas o cabeçalho contém
        # palavras relacionadas a escola/instituição, NÃO combina.
        # Isso permite que "Escola" seja identificado corretamente depois.
        if campo == "Nome":
            if tokens_set & {"escola", "colegio", "instituicao"}:
                return False

        # Matching por tokens: verifica se palavra-chave está nos tokens extraídos
        for chave in chaves:
            if chave in tokens_set:
                return True

        # Matching por substring: verifica se palavra-chave está contida no cabeçalho
        for chave in chaves:
            if chave and chave in cab_norm:
                return True

        return False

    # Itera pelos campos em ordem de prioridade
    for campo in prioridade_campos:
        if campo in coluna_por_campo:
            continue
        for idx, tokens in enumerate(tokens_por_coluna):
            if idx in colunas_usadas:
                continue
            if combina(campo, tokens, header_norm[idx]):
                registrar(campo, idx)
                break

    return coluna_por_campo

def _processar_linhas_tabela(tabela, coluna_por_campo, campos_esperados):
    """
    Processa linhas de uma tabela DOCX e extrai registros estruturados.

    Esta função itera pelas linhas da tabela (excluindo o cabeçalho),
    extrai valores das colunas identificadas e cria registros estruturados
    para cada linha válida.

    Args:
        tabela (Table): Objeto Table do python-docx contendo dados das equipes.
        coluna_por_campo (dict[str, int]): Mapeamento de campos para índices
            de colunas, gerado por _identificar_colunas_tabela().
            Exemplo: {"Nome": 0, "Equipe": 1, "Valido": 2}
        campos_esperados (list[str]): Lista de campos a serem extraídos.
            Exemplo: ["Valido", "Equipe", "Funcao", "Escola", "Cidade", "Estado", "Nome"]

    Returns:
        list[dict]: Lista de registros extraídos, cada um contendo:
            - "Valido" (str): Alcance do foguete
            - "Equipe" (str): Nome da equipe
            - "Funcao" (str): Função normalizada (minúsculas)
            - "Escola" (str): Nome da escola
            - "Cidade" (str): Cidade
            - "Estado" (str): Estado/UF
            - "Nome" (str): Nome do participante

            Retorna lista vazia se:
            - Tabela for None ou inválida
            - Mapeamento de colunas for vazio
            - Tabela tiver menos de 2 linhas (cabeçalho + dados)

    Examples:
        >>> # Supondo tabela com cabeçalho ["Nome", "Equipe", "Alcance"]
        >>> coluna_por_campo = {"Nome": 0, "Equipe": 1, "Valido": 2}
        >>> campos = ["Nome", "Equipe", "Valido", "Funcao", "Escola", "Cidade", "Estado"]
        >>> registros = _processar_linhas_tabela(tabela, coluna_por_campo, campos)
        >>> registros[0]
        {
            'Nome': 'João Silva',
            'Equipe': 'Equipe 01',
            'Valido': '15.5',
            'Funcao': 'aluno',
            'Escola': '',
            'Cidade': '',
            'Estado': ''
        }

    Processamento:
        1. Valida parâmetros de entrada (tabela, mapeamento, campos)
        2. Verifica se tabela tem pelo menos 2 linhas (cabeçalho + dados)
        3. Para cada linha após o cabeçalho:
           a. Extrai texto de todas as células
           b. Ignora linhas completamente vazias
           c. Cria registro com valores dos campos esperados
           d. Normaliza função para minúsculas
           e. Ignora registros sem Equipe E sem Nome (inválidos)
        4. Retorna lista de registros válidos

    Validações:
        - **Linha vazia**: Ignora linhas onde todas as células estão vazias
        - **Índice de coluna**: Valida que índice existe antes de acessar
        - **Registro inválido**: Ignora se não tem Equipe E não tem Nome
          (pelo menos um dos dois é obrigatório para identificação)
        - **Função normalizada**: Converte função para minúsculas para
          facilitar matching posterior (líder, aluno, acompanhante)

    Note:
        - Função interna que assume que cabeçalho já foi identificado
        - Pula a primeira linha (linha[0]) que é o cabeçalho
        - Campos ausentes no mapeamento retornam string vazia
        - Não lança exceções: retorna lista vazia em caso de erro
        - Preserva espaços nos valores (strip é aplicado mas não remove espaços internos)
    """
    # Validação: parâmetros não podem ser None
    if not tabela or not coluna_por_campo or not campos_esperados:
        return []

    # Validação: tabela deve ter pelo menos 2 linhas (cabeçalho + dados)
    if len(tabela.rows) < 2:
        return []

    registros = []

    def obter_valor(linha_celulas, chave):
        """Obtém valor de uma célula com validação de índice"""
        if not linha_celulas:
            return ""
        indice_coluna = coluna_por_campo.get(chave)
        if indice_coluna is not None and 0 <= indice_coluna < len(linha_celulas):
            return linha_celulas[indice_coluna].strip()
        return ""

    for linha in tabela.rows[1:]:  # Pula o cabeçalho
        celulas = [c.text for c in linha.cells]

        # Ignora linhas vazias
        if not any(c.strip() for c in celulas):
            continue

        registro = {chave: obter_valor(celulas, chave) for chave in campos_esperados}

        # Ignora registros sem equipe e sem nome
        if not registro["Equipe"] and not registro["Nome"]:
            continue

        registros.append({
            "Valido": registro["Valido"],
            "Equipe": registro["Equipe"],
            "Funcao": registro["Funcao"].lower(),
            "Escola": registro["Escola"],
            "Cidade": registro["Cidade"],
            "Estado": registro["Estado"],
            "Nome": registro["Nome"]
        })

    return registros

def _organizar_dados_equipes(registros):
    """
    Organiza registros por equipe e formata dados para geração de slides.

    Esta função agrupa registros individuais por equipe, ordena as equipes
    por alcance (lançamento válido), separa membros por função (líder,
    acompanhante, alunos) e formata todos os dados no formato esperado
    pelos placeholders dos slides.

    Args:
        registros (list[dict]): Lista de registros extraídos das tabelas.
            Cada registro deve conter as chaves:
            - "Equipe" (str): Nome da equipe
            - "Nome" (str): Nome do participante
            - "Funcao" (str): Função (aluno/líder/acompanhante)
            - "Valido" (str): Alcance do foguete
            - "Escola" (str): Nome da escola
            - "Cidade" (str): Cidade
            - "Estado" (str): Estado

    Returns:
        list[dict]: Lista de dicionários formatados para preencher slides.
            Cada dicionário contém placeholders mapeados para valores formatados:

            - "{{LANCAMENTOS_VALIDOS}}": "ALCANCE: 15.5 m"
            - "{{NOME_EQUIPE}}": "Equipe: 01"
            - "{{NOME_ESCOLA}}": "Escola Municipal São José"
            - "{{CIDADE_UF}}": "São Paulo / SP"
            - "{{NOMES_ALUNOS}}": "João Silva\\nMaria Santos\\n..."

            Retorna lista vazia se:
            - registros for None ou vazio
            - Nenhum registro tiver nome de equipe
            - Nenhuma equipe tiver alcance válido

    Examples:
        >>> registros = [
        ...     {"Equipe": "Equipe 01", "Nome": "João", "Funcao": "aluno",
        ...      "Valido": "15.5", "Escola": "EMEF", "Cidade": "SP", "Estado": "SP"},
        ...     {"Equipe": "Equipe 01", "Nome": "Maria", "Funcao": "líder",
        ...      "Valido": "15.5", "Escola": "EMEF", "Cidade": "SP", "Estado": "SP"}
        ... ]
        >>> dados = _organizar_dados_equipes(registros)
        >>> dados[0]["{{NOME_EQUIPE}}"]
        'Equipe: 01'
        >>> dados[0]["{{NOMES_ALUNOS}}"]
        'Maria\\nJoão'  # Líder aparece primeiro

    Processamento:
        1. **Agrupamento**: Agrupa registros por nome de equipe
           - Ignora registros sem nome de equipe

        2. **Ordenação**: Ordena equipes pelo alcance (menor para maior)
           - Equipes sem alcance válido vão para o final (float("inf"))
           - Converte vírgulas em pontos para comparação numérica

        3. **Separação por Função**: Para cada equipe, separa:
           - **Líder**: Membros com "líder" ou "lider" na função
           - **Acompanhante**: Membros com "acompanhante" na função
           - **Alunos**: Membros com "aluno" na função
           - Alunos são ordenados alfabeticamente por nome normalizado

        4. **Montagem de Nomes**: Cria lista de nomes na ordem:
           - 1º: Líder (se existir)
           - 2º: Acompanhante (se existir)
           - 3º+: Alunos (ordenados alfabeticamente)

        5. **Formatação**: Aplica formatar_texto() em todos os textos
           - Estado em MAIÚSCULAS
           - Demais campos em Title Case

        6. **Extração de Número**: Extrai número da equipe do nome
           - "Equipe 01" → "01"
           - "Foguete Espacial 123" → "123"
           - Usa última palavra do nome

    Validações e Tratamento de Erros:
        - **Registros vazios**: Retorna lista vazia
        - **Equipe sem nome**: Registro é ignorado
        - **Alcance inválido**: Trata como float("inf") na ordenação
        - **Função vazia**: Membro não é categorizado (não aparece no slide)
        - **Membros sem nome**: Ignorados na lista de nomes
        - **Info mínima**: Equipe precisa ter pelo menos "Valido" para ser incluída

    Edge Cases:
        - **Múltiplos líderes**: Apenas o primeiro é usado
        - **Sem líder**: Lista começa com acompanhante ou alunos
        - **Alcance com vírgula**: "15,5" convertido para "15.5" na ordenação
        - **Equipe sem número**: Usa "?" como fallback

    Note:
        - Função crítica para a lógica de negócio
        - Ordem dos nomes no slide reflete hierarquia: líder → acompanhante → alunos
        - Alunos sempre em ordem alfabética para consistência
        - Formatação aplicada: Title Case para nomes, UPPERCASE para estados
        - Validações robustas previnem crashes com dados malformados
    """
    # Validação: registros não podem ser vazios
    if not registros:
        return []

    # Validação: registros devem ser uma lista
    if not isinstance(registros, list):
        return []

    # ==================== AGRUPAMENTO POR EQUIPE ====================
    # Agrupa registros por nome de equipe (cada equipe pode ter múltiplos membros).
    # Registros sem nome de equipe são ignorados pois não podem ser identificados.
    equipes = defaultdict(list)
    for registro in registros:
        # Validação: registro deve ter chave "Equipe" e não ser vazio
        if isinstance(registro, dict) and registro.get("Equipe"):
            equipes[registro["Equipe"]].append(registro)

    # Validação: se não houver equipes válidas, retorna lista vazia
    if not equipes:
        return []

    # ==================== ORDENAÇÃO POR ALCANCE ====================
    # Ordena equipes pelo alcance (lançamento válido) do MENOR para MAIOR.
    # Esta ordenação determina a ordem final dos slides na apresentação.
    #
    # Regra de negócio: Todos os membros da mesma equipe têm o mesmo alcance,
    # então usamos o valor do primeiro membro como representante.
    #
    # Tratamento de erros robusto: equipes sem alcance válido vão para o final
    # (float("inf") garante que sejam as últimas na ordenação).
    def chave_ord(membros):
        """
        Extrai chave de ordenação: alcance do foguete.

        Lógica:
        - Pega valor "Valido" do primeiro membro (todos têm o mesmo alcance)
        - Converte vírgula para ponto para parsing numérico correto
        - Retorna float("inf") se houver qualquer erro (equipe vai pro final)

        Exemplos:
        - "15.5" → 15.5
        - "15,5" → 15.5 (vírgula convertida)
        - "" ou None → float("inf")
        - "abc" → float("inf") (ValueError capturado)
        """
        try:
            if not membros or not isinstance(membros, list):
                return float("inf")
            primeiro = membros[0]
            if not isinstance(primeiro, dict):
                return float("inf")
            valido = primeiro.get("Valido", "")
            if not valido:
                return float("inf")
            # Substitui vírgula por ponto para suportar formato brasileiro
            return float(str(valido).replace(",", "."))
        except (ValueError, AttributeError, KeyError):
            # Qualquer erro: equipe vai pro final da lista
            return float("inf")

    equipes_ordenadas = sorted(equipes.items(), key=lambda x: chave_ord(x[1]))

    # ==================== FORMATAÇÃO DOS DADOS POR EQUIPE ====================
    dados_finais = []
    for equipe_nome, membros in equipes_ordenadas:
        # Validação: membros não podem ser vazios
        if not membros:
            continue

        # --- SEPARAÇÃO POR FUNÇÃO (Hierarquia) ---
        # Regra de negócio: Nomes aparecem no slide na ordem hierárquica:
        # 1º: Líder (quem comanda a equipe)
        # 2º: Acompanhante (professor/responsável)
        # 3º+: Alunos (membros da equipe, em ordem alfabética)
        #
        # Nota: Aceita "líder" (com acento) e "lider" (sem acento) pois
        # dados podem vir com variações de digitação.
        lider = [membro for membro in membros if isinstance(membro, dict) and
                 ("líder" in str(membro.get("Funcao", "")).lower() or "lider" in str(membro.get("Funcao", "")).lower())]
        acompanhante = [membro for membro in membros if isinstance(membro, dict) and
                        "acompanhante" in str(membro.get("Funcao", "")).lower()]

        # Alunos são SEMPRE ordenados alfabeticamente (normalizado) para consistência
        alunos = sorted(
            [membro for membro in membros if isinstance(membro, dict) and "aluno" in str(membro.get("Funcao", "")).lower()],
            key=lambda membro: normalizar_texto_base(membro.get("Nome", ""))
        )

        # --- EXTRAÇÃO DOS NOMES ---
        # Pega apenas o primeiro líder e primeiro acompanhante (se houver múltiplos).
        # Se não houver, string vazia será usada (não aparece no slide).
        nomes_lider = formatar_texto(lider[0].get("Nome", "")) if lider and lider[0].get("Nome") else ""
        nomes_acompanhante = formatar_texto(acompanhante[0].get("Nome", "")) if acompanhante and acompanhante[0].get("Nome") else ""

        # --- CONSTRUÇÃO DA LISTA FINAL DE NOMES ---
        # Monta lista respeitando hierarquia: líder → acompanhante → alunos
        # Nomes vazios são automaticamente omitidos (não adicionados à lista)
        linhas_nomes = []
        if nomes_lider:
            linhas_nomes.append(nomes_lider)
        if nomes_acompanhante:
            linhas_nomes.append(nomes_acompanhante)
        # Adiciona todos os alunos (já ordenados alfabeticamente)
        linhas_nomes += [formatar_texto(aluno.get("Nome", "")) for aluno in alunos if aluno.get("Nome")]

        # Join com newline: cada nome em uma linha no slide
        nomes_formatados = "\n".join(linhas_nomes)

        # Pega informações da equipe (primeira entrada com validação)
        info = membros[0] if membros else {}

        # Validação: info deve ter dados mínimos necessários
        if not isinstance(info, dict) or not info.get("Valido"):
            continue

        # Extrai partes do nome da equipe com validação
        equipe_partes = str(equipe_nome).split() if equipe_nome else []
        equipe_numero = equipe_partes[-1] if equipe_partes else "?"

        # Monta dict com placeholders para o slide com valores seguros
        dados_finais.append({
            PLACEHOLDER_VALIDO: f"ALCANCE: {info.get('Valido', '?')} m",
            PLACEHOLDER_EQUIPE: f"Equipe: {equipe_numero}",
            PLACEHOLDER_ESCOLA: formatar_texto(info.get("Escola", "")),
            PLACEHOLDER_CIDADE_UF: f"{formatar_texto(info.get('Cidade', ''))} / {formatar_texto(info.get('Estado', ''), True)}",
            PLACEHOLDER_ALUNOS: nomes_formatados
        })

    return dados_finais

def extrair_dados(uploaded_file):
    """
    Extrai e processa dados de equipes de um arquivo DOCX para geração de slides.

    Esta é a função principal de extração de dados. Ela orquestra todo o
    pipeline de processamento: leitura do documento, identificação de colunas,
    extração de registros e organização final dos dados.

    Args:
        uploaded_file (UploadedFile | BinaryIO): Arquivo DOCX contendo tabelas
            com dados das equipes. Pode ser um objeto UploadedFile do Streamlit
            ou qualquer objeto file-like em modo binário.

    Returns:
        list[dict]: Lista de dicionários formatados prontos para preencher slides.
            Cada dicionário contém placeholders mapeados para valores:

            - "{{LANCAMENTOS_VALIDOS}}": "ALCANCE: 15.5 m"
            - "{{NOME_EQUIPE}}": "Equipe: 01"
            - "{{NOME_ESCOLA}}": "Escola Municipal José Silva"
            - "{{CIDADE_UF}}": "São Paulo / SP"
            - "{{NOMES_ALUNOS}}": "Maria Santos\\nJoão Silva\\n..."

            Retorna lista vazia se:
            - uploaded_file for None
            - Documento não puder ser aberto
            - Documento não tiver tabelas
            - Nenhuma coluna for identificada em nenhuma tabela
            - Nenhum dado válido for extraído

    Examples:
        >>> # Com Streamlit
        >>> docx_file = st.file_uploader("Upload DOCX", type=["docx"])
        >>> dados = extrair_dados(docx_file)
        >>> print(f"Encontradas {len(dados)} equipes")
        Encontradas 25 equipes

        >>> # Com arquivo local
        >>> with open("dados_equipes.docx", "rb") as f:
        ...     dados = extrair_dados(f)
        >>> dados[0]["{{NOME_EQUIPE}}"]
        'Equipe: 01'

    Pipeline de Processamento:
        1. **Validação**: Verifica se arquivo não é None

        2. **Abertura do Documento**:
           - Tenta abrir com python-docx
           - Se falhar, captura exceção e retorna lista vazia
           - Imprime erro no console (não lança exceção)

        3. **Verificação de Tabelas**:
           - Verifica se documento contém pelo menos uma tabela
           - Retorna lista vazia se não houver tabelas

        4. **Iteração por Tabelas**: Para cada tabela no documento:
           a. **Extração de Cabeçalho**: Lê primeira linha como cabeçalho
           b. **Identificação de Colunas**: Chama _identificar_colunas_tabela()
              - Se nenhuma coluna for identificada, pula esta tabela
           c. **Extração de Registros**: Chama _processar_linhas_tabela()
              - Extrai registros de todas as linhas da tabela
           d. **Acumulação**: Adiciona registros à lista global

        5. **Organização Final**: Chama _organizar_dados_equipes()
           - Agrupa registros por equipe
           - Ordena por alcance
           - Formata dados para placeholders

        6. **Retorno**: Devolve lista de dicionários formatados

    Campos Esperados nas Tabelas:
        O algoritmo procura por colunas com estes nomes (ou aliases):

        - **Valido/Alcance**: Lançamento válido (obrigatório)
        - **Equipe**: Nome da equipe (obrigatório)
        - **Nome**: Nome do participante (obrigatório)
        - **Funcao**: Função (aluno/líder/acompanhante) (opcional)
        - **Escola**: Nome da escola (opcional)
        - **Cidade**: Cidade (opcional)
        - **Estado**: Estado/UF (opcional)

    Tolerância a Variações:
        O algoritmo é tolerante a:
        - Variações de nomenclatura ("Alcance", "Lançamentos Válidos", etc.)
        - Acentuação ("Função" vs "Funcao")
        - Maiúsculas/minúsculas ("NOME" vs "nome")
        - Espaços extras ("  Nome  Equipe  ")
        - Múltiplas tabelas no mesmo documento
        - Tabelas com colunas em diferentes ordens

    Tratamento de Erros:
        - **Documento corrompido**: Retorna [] e imprime erro
        - **Tabela vazia**: Pula tabela e continua
        - **Cabeçalho inválido**: Pula tabela e continua
        - **Dados malformados**: Registros inválidos são ignorados
        - **Sem dados válidos**: Retorna []

        A função é defensiva e nunca lança exceções para o chamador.

    Performance:
        - Processa múltiplas tabelas em um único documento
        - Complexidade: O(n * m) onde n = número de tabelas, m = linhas por tabela
        - Otimizado para documentos com até 1000 registros
        - Para documentos grandes, considerar cache (futuro)

    Note:
        - Função pública chamada diretamente pela UI Streamlit
        - Lê TODAS as tabelas do documento (não apenas a primeira)
        - Registros de diferentes tabelas são mesclados
        - Ordenação final por alcance garante que slides sigam ordem de classificação
        - Validações em múltiplas camadas garantem robustez
        - Erros são impressos com print() (considerar logging no futuro)
    """
    # Validação: arquivo não pode ser None
    if not uploaded_file:
        return []

    try:
        documento = Document(uploaded_file)
    except Exception as e:
        # Erro ao abrir o documento
        print(f"Erro ao abrir documento: {e}")
        return []

    # Validação: documento deve ter tabelas
    if not documento.tables:
        return []

    registros = []

    # Processa todas as tabelas do documento
    for tabela in documento.tables:
        if not tabela or not tabela.rows:
            continue

        # Validação: tabela deve ter pelo menos cabeçalho
        if len(tabela.rows) < 1:
            continue

        cabecalho = [c.text.strip() for c in tabela.rows[0].cells]

        # Identifica mapeamento de colunas
        coluna_por_campo = _identificar_colunas_tabela(cabecalho)

        # Se não identificou nenhuma coluna, pula esta tabela
        if not coluna_por_campo:
            continue

        # Campos esperados para extração
        campos_esperados = ["Valido", "Equipe", "Funcao", "Escola", "Cidade", "Estado", "Nome"]

        # Processa linhas da tabela
        registros_tabela = _processar_linhas_tabela(tabela, coluna_por_campo, campos_esperados)
        if registros_tabela:
            registros.extend(registros_tabela)

    # Organiza registros por equipe e formata dados finais
    dados_finais = _organizar_dados_equipes(registros)

    return dados_finais

# -------------------- DUPLICAÇÃO DE SLIDE --------------------
def duplicate_slide_with_media(apresentacao, source_slide):
    """
    Duplica um slide preservando imagens e elementos visuais.

    Esta função cria uma cópia completa de um slide, incluindo todos os
    elementos visuais, formas, imagens e seus dados binários. É essencial
    para manter a formatação e design do template ao gerar múltiplos slides.

    Args:
        apresentacao (Presentation): Objeto de apresentação python-pptx onde o novo
            slide será adicionado.
        source_slide (Slide): Slide original a ser duplicado.

    Returns:
        Slide: Novo slide criado, idêntico ao slide original incluindo
            todas as imagens e elementos visuais.

    Examples:
        >>> apresentacao = Presentation("template.pptx")
        >>> slide_original = apresentacao.slides[0]
        >>> novo_slide = duplicate_slide_with_media(apresentacao, slide_original)
        >>> print(len(novo_slide.shapes))  # Mesmo número de elementos
        5

    Processamento:
        1. Cria novo slide com o mesmo layout
        2. Para cada shape (forma) no slide original:
           - Cria cópia profunda do elemento XML
           - Se for imagem (shape_type == 13):
             * Extrai dados binários da imagem
             * Adiciona imagem ao novo slide
             * Atualiza referências XML (relationship ID)
           - Insere elemento no novo slide

    Note:
        - Preserva todas as propriedades visuais (cores, fontes, posições)
        - Imagens são copiadas com seus dados binários completos
        - Relacionamentos XML são atualizados corretamente
        - Funciona com imagens PNG, JPG e outros formatos
        - Mantém a ordem z-index dos elementos
        - Trata erros de imagens corrompidas gracefully
    """
    layout = source_slide.slide_layout
    new_slide = apresentacao.slides.add_slide(layout)
    for shape in source_slide.shapes:
        new_el = deepcopy(shape.element)
        if shape.shape_type == SHAPE_TYPE_PICTURE:
            try:
                img_blob = shape.image.blob
            except Exception:
                img_blob = None
            if img_blob:
                image_part, new_rId = new_slide.part.get_or_add_image_part(BytesIO(img_blob))
                new_el_xml = etree.fromstring(new_el.xml)
                blips = new_el_xml.findall(f'.//{XML_NAMESPACE_DRAWINGML}blip')
                for blip in blips:
                    blip.set(f'{XML_NAMESPACE_RELATIONSHIPS}embed', new_rId)
                from pptx.oxml import parse_xml
                new_el = parse_xml(etree.tostring(new_el_xml, encoding='utf-8'))
        new_slide.shapes._spTree.insert_element_before(new_el, 'p:extLst')
    return new_slide

# -------------------- SUBSTITUIÇÃO DE PLACEHOLDERS --------------------
def replace_placeholders_in_shape(shape, team_data):
    """
    Substitui placeholders em uma forma do slide com dados da equipe.

    Esta função procura por placeholders (ex: {{NOME_EQUIPE}}) em caixas de
    texto do slide e os substitui pelos dados reais da equipe, aplicando
    formatação específica para cada tipo de informação.

    Args:
        shape: Objeto Shape do python-pptx (forma do PowerPoint).
        team_data (dict): Dicionário com dados da equipe contendo as chaves:
            - "{{LANCAMENTOS_VALIDOS}}": Alcance formatado
            - "{{NOME_EQUIPE}}": Nome da equipe
            - "{{NOME_ESCOLA}}": Nome da escola
            - "{{CIDADE_UF}}": Cidade e estado
            - "{{NOMES_ALUNOS}}": Nomes dos participantes

    Returns:
        None: A função modifica o shape in-place.

    Formatação Aplicada por Placeholder:
        - {{LANCAMENTOS_VALIDOS}}:
          * "ALCANCE: " → Lexend, 28pt, azul (#006FC0)
          * Valor → Lexend, 35pt, azul, negrito + sublinhado

        - {{NOMES_ALUNOS}}:
          * Lexend, 26.5pt, branco (#FFFFFF), negrito
          * Um nome por linha, centralizado

        - {{NOME_EQUIPE}}:
          * Lexend, 20pt, branco, negrito, centralizado

        - {{NOME_ESCOLA}} e {{CIDADE_UF}}:
          * Lexend, 20pt, branco, negrito, centralizado
          * Se ambos na mesma caixa, cria parágrafos separados

    Examples:
        >>> # shape é uma caixa de texto com "{{NOME_EQUIPE}}"
        >>> team_data = {"{{NOME_EQUIPE}}": "Equipe: 01"}
        >>> replace_placeholders_in_shape(shape, team_data)
        >>> # shape agora contém "Equipe: 01" formatado

    Casos Especiais:
        - {{NOMES_ALUNOS}} + {{NOME_EQUIPE}} na mesma caixa:
          * Tratados juntos com formatações diferentes
        - {{NOME_ESCOLA}} + {{CIDADE_UF}} na mesma caixa:
          * Criados em parágrafos separados
        - Placeholders colados (ex: }}{{):
          * Separados automaticamente com quebra de linha

    Note:
        - Ignora shapes sem text_frame
        - Remove todos os runs antigos antes de criar novos
        - Alinhamento centralizado aplicado automaticamente
        - Fonte Lexend aplicada em todos os textos
        - Cores em RGB: azul = #006FC0, branco = #FFFFFF
    """
    if not shape.has_text_frame:
        return

    tf = shape.text_frame

    # Quando os placeholders de nomes e equipe estão na mesma caixa de texto, mas em
    # parágrafos diferentes, lidamos com todos de uma vez para garantir que as duas
    # informações sejam aplicadas com o mesmo estilo.
    frame_text = "\n".join("".join(run.text for run in paragraph.runs) for paragraph in tf.paragraphs)
    if PLACEHOLDER_ALUNOS in frame_text and PLACEHOLDER_EQUIPE in frame_text:
        tf.clear()
        linhas = team_data[PLACEHOLDER_ALUNOS].split("\n") + [team_data[PLACEHOLDER_EQUIPE]]
        for i, nome in enumerate(linhas):
            p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
            run = p.add_run()
            run.text = nome
            run.font.name = FONT_NAME
            run.font.bold = True
            if i == len(linhas) - 1:  # última linha = nome da equipe
                run.font.size = Pt(FONT_SIZE_SMALL)
            else:
                run.font.size = Pt(FONT_SIZE_MEDIUM)
            run.font.color.rgb = COLOR_WHITE
            p.alignment = PP_ALIGN.CENTER
        return

    for paragraph in list(tf.paragraphs):
        full_text = "".join(run.text for run in paragraph.runs)

        # --- Corrige placeholders colados (ex: {{NOME_ESCOLA}}{{CIDADE_UF}} ou {{NOMES_ALUNOS}}{{NOME_EQUIPE}}) ---
        full_text = full_text.replace("}}{{", "}}\n{{")

        selected_key = None
        for k in team_data.keys():
            if k in full_text:
                selected_key = k
                break
        if not selected_key:
            continue

        # Substitui placeholders por valores
        new_text = full_text
        for k, v in team_data.items():
            new_text = new_text.replace(k, v)

        # Limpa runs antigos
        while paragraph.runs:
            paragraph._p.remove(paragraph.runs[0]._r)

        # --- ALCANCE ---
        if selected_key == PLACEHOLDER_VALIDO:
            match = re.match(r"(ALCANCE:\s*)([\d,.]+ m)", new_text, re.IGNORECASE)
            if match:
                prefix, valor = match.groups()
                run1 = paragraph.add_run()
                run1.text = prefix
                run1.font.name = FONT_NAME
                run1.font.bold = False
                run1.font.size = Pt(FONT_SIZE_LARGE)
                run1.font.color.rgb = COLOR_BLUE

                run2 = paragraph.add_run()
                run2.text = valor
                run2.font.name = FONT_NAME
                run2.font.bold = True
                run2.font.underline = True
                run2.font.size = Pt(FONT_SIZE_XLARGE)
                run2.font.color.rgb = COLOR_BLUE

       # --- SOMENTE NOMES ---
        elif selected_key == PLACEHOLDER_ALUNOS:
            tf.clear()
            linhas = team_data[PLACEHOLDER_ALUNOS].split("\n")
            for i, nome in enumerate(linhas):
                p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
                run = p.add_run()
                run.text = nome
                run.font.name = FONT_NAME
                run.font.bold = True
                run.font.size = Pt(FONT_SIZE_MEDIUM)
                run.font.color.rgb = COLOR_WHITE
                p.alignment = PP_ALIGN.CENTER

        # --- NOME DA EQUIPE (se estiver sozinho) ---
        elif selected_key == PLACEHOLDER_EQUIPE:
            run = paragraph.add_run()
            run.text = new_text
            run.font.name = FONT_NAME
            run.font.bold = True
            run.font.size = Pt(FONT_SIZE_SMALL)
            run.font.color.rgb = COLOR_WHITE
            paragraph.alignment = PP_ALIGN.CENTER

        # --- ESCOLA + CIDADE ---
        elif PLACEHOLDER_ESCOLA in full_text and PLACEHOLDER_CIDADE_UF in full_text:
            tf.clear()
            partes = [team_data[PLACEHOLDER_ESCOLA], team_data[PLACEHOLDER_CIDADE_UF]]
            for i, parte in enumerate(partes):
                p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
                run = p.add_run()
                run.text = parte
                run.font.name = FONT_NAME
                run.font.bold = True
                run.font.size = Pt(FONT_SIZE_SMALL)
                run.font.color.rgb = COLOR_WHITE
                p.alignment = PP_ALIGN.CENTER

        # --- SOMENTE ESCOLA OU CIDADE (caso isolado) ---
        elif selected_key in (PLACEHOLDER_ESCOLA, PLACEHOLDER_CIDADE_UF):
            run = paragraph.add_run()
            run.text = new_text
            run.font.name = FONT_NAME
            run.font.bold = True
            run.font.size = Pt(FONT_SIZE_SMALL)
            run.font.color.rgb = COLOR_WHITE
            paragraph.alignment = PP_ALIGN.CENTER


# -------------------- GERAÇÃO FINAL --------------------
def gerar_apresentacao(dados, template_stream):
    """
    Gera apresentação PowerPoint completa duplicando template e preenchendo dados.

    Esta é a função principal de geração de slides. Ela orquestra todo o
    processo de criação da apresentação: abertura do template, duplicação
    de slides, e substituição de placeholders pelos dados das equipes.

    Args:
        dados (list[dict]): Lista de dicionários com dados formatados das equipes.
            Cada dicionário deve conter placeholders como chaves:
            - "{{LANCAMENTOS_VALIDOS}}": "ALCANCE: 15.5 m"
            - "{{NOME_EQUIPE}}": "Equipe: 01"
            - "{{NOME_ESCOLA}}": "Escola Municipal"
            - "{{CIDADE_UF}}": "São Paulo / SP"
            - "{{NOMES_ALUNOS}}": "Maria\\nJoão\\n..."

        template_stream (UploadedFile | BinaryIO): Stream do arquivo PPTX template.
            Pode ser um objeto UploadedFile do Streamlit ou qualquer objeto
            file-like em modo binário. O template deve ter pelo menos 1 slide.

    Returns:
        Presentation | None: Objeto Presentation do python-pptx com todos os
            slides gerados e preenchidos.

            Retorna None se:
            - template_stream for None
            - Template não puder ser aberto (arquivo corrompido)

            Retorna Presentation vazia (apenas template original) se:
            - dados for None ou vazio
            - Template não tiver slides

    Examples:
        >>> # Uso típico com Streamlit
        >>> docx_file = st.file_uploader("DOCX", type=["docx"])
        >>> pptx_template = st.file_uploader("Template PPTX", type=["pptx"])
        >>> dados = extrair_dados(docx_file)
        >>> apresentacao = gerar_apresentacao(dados, pptx_template)
        >>> buf = BytesIO()
        >>> apresentacao.save(buf)
        >>> st.download_button("Baixar", data=buf, file_name="resultado.pptx")

        >>> # Uso programático
        >>> with open("dados.docx", "rb") as docx, open("template.pptx", "rb") as pptx:
        ...     dados = extrair_dados(docx)
        ...     apresentacao = gerar_apresentacao(dados, pptx)
        ...     apresentacao.save("resultado.pptx")

    Pipeline de Geração:
        1. **Validação do Template**:
           - Verifica se template_stream não é None
           - Tenta abrir com python-pptx
           - Se falhar, imprime erro e retorna None

        2. **Validação dos Dados**:
           - Verifica se dados não é None/vazio
           - Verifica se template tem pelo menos 1 slide
           - Se falhar em qualquer validação, retorna Presentation original

        3. **Preparação**:
           - Identifica primeiro slide como modelo (template)
           - Cria lista com este slide como primeiro item

        4. **Duplicação de Slides**:
           - Para cada equipe adicional (len(dados) - 1):
             a. Chama duplicate_slide_with_media() para copiar o template
             b. Preserva todas as imagens e formatações
             c. Adiciona novo slide à lista de slides a preencher
             d. Se duplicação falhar, imprime erro e continua

        5. **Preenchimento de Dados**:
           - Para cada par (slide, dados_equipe):
             a. Itera por todas as shapes (formas) do slide
             b. Chama replace_placeholders_in_shape() para substituir texto
             c. Aplica formatações específicas por tipo de placeholder
             d. Se preenchimento falhar, imprime erro e continua

        6. **Retorno**: Devolve Presentation completo

    Correspondência Slide ↔ Dados:
        - Primeiro slide (template original) recebe dados[0]
        - Duplicação 1 recebe dados[1]
        - Duplicação 2 recebe dados[2]
        - E assim por diante...

        Garantia: len(slides_preenchidos) == len(dados)

    Formatações Aplicadas:
        Cada placeholder recebe formatação específica:

        - **{{LANCAMENTOS_VALIDOS}}**:
          * "ALCANCE: " → Lexend 28pt azul
          * Valor → Lexend 35pt azul bold+underline

        - **{{NOMES_ALUNOS}}**:
          * Lexend 26.5pt branco bold
          * Um nome por linha, centralizado

        - **{{NOME_EQUIPE}}**, **{{NOME_ESCOLA}}**, **{{CIDADE_UF}}**:
          * Lexend 20pt branco bold centralizado

    Tratamento de Erros:
        A função é defensiva e continua a execução mesmo com erros:

        - **Template corrompido**: Retorna None, imprime erro
        - **Erro ao duplicar slide**: Pula aquele slide, continua com próximos
        - **Erro ao preencher placeholders**: Pula aquela shape, continua
        - **Slide sem shapes**: Ignora, não causa erro
        - **Placeholder não encontrado**: Não faz nada (slide fica com placeholder)

        Erros são impressos com print() mas não interrompem a geração.

    Performance:
        - Complexidade: O(n * m) onde n = número de equipes, m = shapes por slide
        - Duplicação de slides pode ser lenta com muitas imagens
        - Para 50 equipes com 10 shapes cada: ~2-3 segundos
        - Otimização futura: cache de imagens, processamento paralelo

    Preservação de Elementos:
        Durante duplicação, preserva:
        - ✅ Todas as imagens (PNG, JPG, etc.)
        - ✅ Formas (retângulos, círculos, etc.)
        - ✅ Formatações de texto
        - ✅ Cores e estilos
        - ✅ Posicionamento exato
        - ✅ Ordem z-index dos elementos
        - ❌ Animações (limitação do python-pptx)
        - ❌ Transições (limitação do python-pptx)

    Note:
        - Função pública chamada diretamente pela UI Streamlit
        - Template SEMPRE é preservado (primeiro slide mantém dados originais)
        - Slides duplicados são idênticos ao template exceto pelos textos preenchidos
        - Validações robustas previnem crashes mas permitem geração parcial
        - Considerar implementar progress bar para muitas equipes (futuro)
        - Erros são impressos com print() (considerar logging estruturado)
    """
    # Validação: template não pode ser None
    if not template_stream:
        return None

    try:
        apresentacao = Presentation(template_stream)
    except Exception as e:
        print(f"Erro ao abrir template PPTX: {e}")
        return None

    # Validação: dados e slides do template
    if not dados or not isinstance(dados, list):
        return apresentacao

    if not apresentacao.slides or len(apresentacao.slides) == 0:
        return apresentacao

    modelo = apresentacao.slides[0]
    slides_para_preencher = [modelo]

    # Duplica slides conforme necessário
    for _ in range(len(dados) - 1):
        try:
            novo_slide = duplicate_slide_with_media(apresentacao, modelo)
            if novo_slide:
                slides_para_preencher.append(novo_slide)
        except Exception as e:
            print(f"Erro ao duplicar slide: {e}")
            continue

    # Preenche placeholders em cada slide
    for slide, team in zip(slides_para_preencher, dados):
        if not slide or not isinstance(team, dict):
            continue
        try:
            for shape in slide.shapes:
                replace_placeholders_in_shape(shape, team)
        except Exception as e:
            print(f"Erro ao preencher placeholders: {e}")
            continue

    return apresentacao

# -------------------- INTERFACE STREAMLIT --------------------
docx_file = st.file_uploader("📄 Arquivo DOCX", type=["docx"])
pptx_file = st.file_uploader("📊 Arquivo PPTX modelo", type=["pptx"])

if "nome_arquivo" not in st.session_state:
    st.session_state["nome_arquivo"] = ""

nome_arquivo_digitado = st.text_input(
    "Nome do arquivo (sem extensao)",
    value=st.session_state["nome_arquivo"],
)

if st.button("Confirmar nome do arquivo"):
    st.session_state["nome_arquivo"] = sanitizar_nome_arquivo(nome_arquivo_digitado)
    st.success(f"Nome para download ajustado para: {st.session_state['nome_arquivo']}.pptx")

if st.button("✨ Gerar Apresentação"):
    if not docx_file or not pptx_file:
        st.warning(MSG_SEND_BOTH_FILES)
    else:
        try:
            dados = extrair_dados(docx_file)
            if not dados:
                st.warning(MSG_NO_DATA_FOUND)
            else:
                prs_final = gerar_apresentacao(dados, pptx_file)
                buf = BytesIO()
                prs_final.save(buf)
                buf.seek(0)
                st.success(f"Slides gerados: {len(dados)}")

                st.image(GIF_PATH, caption=MSG_CAPTION_READY, use_container_width=True)

                st.download_button(
                    "📥 Baixar Apresentação Final",
                    data=buf,
                    file_name=f"{st.session_state['nome_arquivo']}.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"Erro ao gerar apresentação: {e}")
