import streamlit as st
from docx import Document
from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from collections import defaultdict
from copy import deepcopy
from io import BytesIO
from lxml import etree
import re
import unicodedata
from PIL import Image

# -------------------- CONSTANTES --------------------
# Configurações de imagem
LOGO_PATH = "logo_jornada.png"
LOGO_WIDTH = 1235
LOGO_HEIGHT = 426
GIF_PATH = "tiapamela.gif"

# Configurações de layout Streamlit
PAGE_LAYOUT = "wide"
COLUMN_PROPORTIONS = [1, 4, 1]

# Configurações de fonte
FONT_NAME = "Lexend"
FONT_SIZE_SMALL = 20
FONT_SIZE_MEDIUM = 26.5
FONT_SIZE_LARGE = 28
FONT_SIZE_XLARGE = 35

# Cores RGB
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
COLOR_BLUE = RGBColor(0x00, 0x6F, 0xC0)

# Shape types
SHAPE_TYPE_PICTURE = 13

# Placeholders de template
PLACEHOLDER_VALIDO = "{{LANCAMENTOS_VALIDOS}}"
PLACEHOLDER_EQUIPE = "{{NOME_EQUIPE}}"
PLACEHOLDER_ESCOLA = "{{NOME_ESCOLA}}"
PLACEHOLDER_CIDADE_UF = "{{CIDADE_UF}}"
PLACEHOLDER_ALUNOS = "{{NOMES_ALUNOS}}"

# Mensagens de interface
MSG_UPLOAD_WARNING = "CERTIFIQUE-SE DE ESTÁ FAZENDO O UPLOAD DOS ARQUIVOS CORRETOS ANTES DE GERAR OS SLIDES!"
MSG_SEND_BOTH_FILES = "Envie ambos os arquivos."
MSG_NO_DATA_FOUND = "Nenhum dado encontrado."
MSG_NOME_ARQUIVO_DEFAULT = "Apresentacao_Final_Equipes"
MSG_CAPTION_READY = "Apresentação pronta! 🚀"

# Namespace XML
XML_NAMESPACE_DRAWINGML = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
XML_NAMESPACE_RELATIONSHIPS = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'

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
    Identifica e mapeia as colunas da tabela baseado no cabeçalho.

    Args:
        cabecalho: Lista com os textos do cabeçalho da tabela

    Returns:
        Dict mapeando campos esperados para índices de colunas
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

    # Tokenizar cabeçalhos
    tokens_por_coluna = []
    for cab_norm in header_norm:
        tokens = [tok for tok in re.split(r"[^a-z0-9]+", cab_norm) if tok]
        tokens_por_coluna.append(tokens)

    coluna_por_campo = {}
    colunas_usadas = set()

    def registrar(campo, idx):
        if idx is None or idx in colunas_usadas:
            return False
        coluna_por_campo[campo] = idx
        colunas_usadas.add(idx)
        return True

    # Primeira passagem: correspondência exata com aliases
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

    # Segunda passagem: matching fuzzy com palavras-chave
    prioridade_campos = ["Valido", "Equipe", "Funcao", "Escola", "Cidade", "Estado", "Nome"]

    def combina(campo, tokens, cab_norm):
        if not cab_norm:
            return False
        tokens_set = set(tokens)
        chaves = palavras_chave.get(campo, set())
        # Evita matching incorreto de "Nome" com "Nome da Escola"
        if campo == "Nome":
            if tokens_set & {"escola", "colegio", "instituicao"}:
                return False
        for chave in chaves:
            if chave in tokens_set:
                return True
        for chave in chaves:
            if chave and chave in cab_norm:
                return True
        return False

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
    Processa as linhas de uma tabela e extrai registros.

    Args:
        tabela: Tabela do documento Word
        coluna_por_campo: Dict mapeando campos para índices de colunas
        campos_esperados: Lista de campos a serem extraídos

    Returns:
        Lista de registros (dicts) extraídos da tabela
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
        idx = coluna_por_campo.get(chave)
        if idx is not None and 0 <= idx < len(linha_celulas):
            return linha_celulas[idx].strip()
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
    Organiza registros por equipe e formata dados finais para apresentação.

    Args:
        registros: Lista de registros extraídos das tabelas

    Returns:
        Lista de dicts com dados formatados para os slides
    """
    # Validação: registros não podem ser vazios
    if not registros:
        return []

    # Validação: registros devem ser uma lista
    if not isinstance(registros, list):
        return []

    # Agrupa registros por equipe (ignora registros sem nome de equipe)
    equipes = defaultdict(list)
    for r in registros:
        # Validação: registro deve ter chave "Equipe" e não ser vazio
        if isinstance(r, dict) and r.get("Equipe"):
            equipes[r["Equipe"]].append(r)

    # Validação: se não houver equipes, retorna lista vazia
    if not equipes:
        return []

    # Ordena equipes pelo alcance (lançamento válido)
    def chave_ord(membros):
        """Extrai chave de ordenação com tratamento de erros robusto"""
        try:
            if not membros or not isinstance(membros, list):
                return float("inf")
            primeiro = membros[0]
            if not isinstance(primeiro, dict):
                return float("inf")
            valido = primeiro.get("Valido", "")
            if not valido:
                return float("inf")
            return float(str(valido).replace(",", "."))
        except (ValueError, AttributeError, KeyError):
            return float("inf")

    equipes_ordenadas = sorted(equipes.items(), key=lambda x: chave_ord(x[1]))

    # Formata dados finais para cada equipe
    dados_finais = []
    for equipe_nome, membros in equipes_ordenadas:
        # Validação: membros não podem ser vazios
        if not membros:
            continue

        # Separa membros por função com validação
        lider = [m for m in membros if isinstance(m, dict) and
                 ("líder" in str(m.get("Funcao", "")).lower() or "lider" in str(m.get("Funcao", "")).lower())]
        acompanhante = [m for m in membros if isinstance(m, dict) and
                        "acompanhante" in str(m.get("Funcao", "")).lower()]
        alunos = sorted(
            [m for m in membros if isinstance(m, dict) and "aluno" in str(m.get("Funcao", "")).lower()],
            key=lambda m: normalizar_texto_base(m.get("Nome", ""))
        )

        # Formata nomes com validação
        nomes_lider = formatar_texto(lider[0].get("Nome", "")) if lider and lider[0].get("Nome") else ""
        nomes_acompanhante = formatar_texto(acompanhante[0].get("Nome", "")) if acompanhante and acompanhante[0].get("Nome") else ""

        # Monta lista de nomes na ordem: líder, acompanhante, alunos
        linhas_nomes = []
        if nomes_lider:
            linhas_nomes.append(nomes_lider)
        if nomes_acompanhante:
            linhas_nomes.append(nomes_acompanhante)
        linhas_nomes += [formatar_texto(a.get("Nome", "")) for a in alunos if a.get("Nome")]

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
    Extrai dados de equipes de um arquivo DOCX e formata para geração de slides.

    Args:
        uploaded_file: Arquivo DOCX contendo tabelas com dados das equipes

    Returns:
        Lista de dicts com dados formatados para preencher os slides
    """
    # Validação: arquivo não pode ser None
    if not uploaded_file:
        return []

    try:
        doc = Document(uploaded_file)
    except Exception as e:
        # Erro ao abrir o documento
        print(f"Erro ao abrir documento: {e}")
        return []

    # Validação: documento deve ter tabelas
    if not doc.tables:
        return []

    registros = []

    # Processa todas as tabelas do documento
    for tabela in doc.tables:
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
def duplicate_slide_with_media(prs, source_slide):
    """
    Duplica um slide preservando imagens e elementos visuais.

    Esta função cria uma cópia completa de um slide, incluindo todos os
    elementos visuais, formas, imagens e seus dados binários. É essencial
    para manter a formatação e design do template ao gerar múltiplos slides.

    Args:
        prs (Presentation): Objeto de apresentação python-pptx onde o novo
            slide será adicionado.
        source_slide (Slide): Slide original a ser duplicado.

    Returns:
        Slide: Novo slide criado, idêntico ao slide original incluindo
            todas as imagens e elementos visuais.

    Examples:
        >>> prs = Presentation("template.pptx")
        >>> slide_original = prs.slides[0]
        >>> novo_slide = duplicate_slide_with_media(prs, slide_original)
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
    new_slide = prs.slides.add_slide(layout)
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
    Gera apresentação PPTX com dados das equipes.

    Args:
        dados: Lista de dicts com dados formatados das equipes
        template_stream: Stream do arquivo PPTX template

    Returns:
        Objeto Presentation com os slides gerados
    """
    # Validação: template não pode ser None
    if not template_stream:
        return None

    try:
        prs = Presentation(template_stream)
    except Exception as e:
        print(f"Erro ao abrir template PPTX: {e}")
        return None

    # Validação: dados e slides do template
    if not dados or not isinstance(dados, list):
        return prs

    if not prs.slides or len(prs.slides) == 0:
        return prs

    modelo = prs.slides[0]
    slides_para_preencher = [modelo]

    # Duplica slides conforme necessário
    for _ in range(len(dados) - 1):
        try:
            novo_slide = duplicate_slide_with_media(prs, modelo)
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

    return prs

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
