import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="Resta Um: Oscar",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização CSS inspirada no Save One Game (Proporção 250x370 para pôsteres sem cortes)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Oswald:wght@500;700&display=swap');

    /* Remove completamente a barra de deploy, cabeçalhos nativos e o menu sanduíche */
    header[data-testid="stHeader"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    .stApp > header {
        display: none !important;
    }
    
    #MainMenu, footer, [data-testid="stDecoration"] {
        visibility: hidden !important;
        display: none !important;
    }

    /* Container de cabeçalho unificado para centralização absoluta */
    .header-container {
        position: relative;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 5px;
        margin-bottom: 20px;
    }

    .header-title {
        font-family: 'Cinzel', serif;
        font-size: 2.2rem;
        font-weight: 900;
        color: #e5c158;
        text-shadow: 0 4px 10px rgba(0,0,0,0.8);
        letter-spacing: 2px;
        text-align: center;
        margin: 0;
    }

    .header-close-btn {
        position: absolute;
        right: 0;
        top: 0;
    }
    
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 1rem !important;
    }
    
    .stApp {
        background-color: #120e0b;
        background-image: radial-gradient(#1c1611 15%, transparent 16%);
        background-size: 20px 20px;
        color: #e5c158;
        font-family: 'Oswald', sans-serif;
    }
    
    .site-title {
        font-family: 'Cinzel', serif;
        text-align: center;
        font-size: 2.8rem;
        font-weight: 900;
        color: #e5c158;
        text-shadow: 0 4px 10px rgba(0,0,0,0.8);
        margin-top: 10px;
        margin-bottom: 10px;
        letter-spacing: 2px;
    }
    
    .year-title {
        font-family: 'Cinzel', serif;
        text-align: center;
        font-size: 2.3rem;
        font-weight: 900;
        color: #e5c158;
        margin-bottom: 10px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.9);
    }
    
    /* Centralização perfeita e padronizada dos botões da tela inicial */
    .menu-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        margin-top: 5px;
    }
    
    .menu-container div.stButton {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    
    .menu-container div.stButton > button {
        width: 340px !important;
        background-color: #1a140e !important;
        color: #e5c158 !important;
        border: 2px solid #5a472c !important;
        border-radius: 6px !important;
        font-family: 'Oswald', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        padding: 12px 0 !important;
        margin-bottom: 10px !important;
        transition: all 0.2s ease;
    }
    
    .menu-container div.stButton > button:hover {
        background-color: #e5c158 !important;
        color: #120e0b !important;
        border-color: #e5c158 !important;
        box-shadow: 0 0 15px rgba(229, 193, 88, 0.4);
    }

    /* Slot do Cartaz */
    .movie-box {
        background: #000000;
        border: 2px solid #5a472c;
        border-radius: 6px;
        padding: 3px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 280px;
        margin-bottom: 6px;
        overflow: hidden;
    }
    .movie-box img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        border-radius: 4px;
    }
    
    /* Títulos dos filmes embaixo dos pôsteres */
    .stButton > button {
        width: 100% !important;
    }
    .stButton button[kind="secondary"] {
        font-size: 0.78rem !important;
        white-space: normal !important;
        height: auto !important;
        min-height: 48px;
        line-height: 1.2;
        padding: 8px 6px !important;
        margin-top: 2px;
        margin-bottom: 12px;
        background-color: #1a140e;
        color: #e5c158;
        border: 2px solid #5a472c;
        border-radius: 6px;
    }
    .stButton button[kind="secondary"]:hover {
        background-color: #e5c158;
        color: #120e0b;
        border-color: #e5c158;
    }
    
    .summary-item {
        background: #1a140e;
        border-left: 4px solid #e5c158;
        padding: 10px 15px;
        margin-bottom: 8px;
        border-radius: 4px;
        color: #fff;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- CARREGAMENTO DO BANCO DE DADOS -----------------

import json
from pathlib import Path

CAMINHO_BD = Path(__file__).parent / "data" / "oscar_filmes.json"

with open(CAMINHO_BD, "r", encoding="utf-8") as arquivo:
    BANCO_DE_DADOS = json.load(arquivo)

BANCO_DE_DADOS = {
    int(ano): filmes
    for ano, filmes in BANCO_DE_DADOS.items()
}

ANOS = sorted(BANCO_DE_DADOS.keys())

# Gerenciamento de Estado do Aplicativo
if "modo" not in st.session_state:
    st.session_state.modo = "menu"
if "indice_ano" not in st.session_state:
    st.session_state.indice_ano = 0
if "filmes_salvos" not in st.session_state:
    st.session_state.filmes_salvos = {}

# ---------------- BARRA DE PROGRESSO ----------------
def renderizar_barra_progresso():
    total_anos = len(ANOS)
    salvos_qtd = len(st.session_state.filmes_salvos)
    porcentagem = (salvos_qtd / total_anos) * 100 if total_anos > 0 else 0
    
    st.markdown(f"""
    <div style="background: #1a140e; border: 1px solid #5a472c; padding: 10px 15px; border-radius: 8px; margin-bottom: 20px; text-align: center;">
        <div style="font-family: 'Cinzel', serif; color: #e5c158; font-size: 0.95rem; font-weight: bold; margin-bottom: 6px;">
            PROGRESSO DA SELEÇÃO: {salvos_qtd} de {total_anos} anos ({porcentagem:.1f}%)
        </div>
        <div style="background: #000000; border-radius: 4px; height: 8px; width: 100%; overflow: hidden; border: 1px solid #3d2f1f;">
            <div style="background: #27ae60; height: 100%; width: {porcentagem}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- POSTER ADAPTATIVOS ----------------
def renderizar_indicados_adaptativo(filmes_do_ano, ano_atual):
    """Mantém rigorosamente o tamanho padrão dos cards igual ao de 3 por linha,
       usando a sua lógica de quebra exata e expandindo o layout sem espremer."""
    total = len(filmes_do_ano)
    
    # A sua estrutura exata de quebra por quantidade:
    if total == 5:
        linhas = [filmes_do_ano[:3], filmes_do_ano[3:]] # 3 em cima, 2 embaixo
    elif total == 4:
        linhas = [filmes_do_ano[:2], filmes_do_ano[2:]] # 2 em cima, 2 embaixo
    elif total == 10:
        linhas = [filmes_do_ano[:5], filmes_do_ano[5:]] # 5 em cima, 5 embaixo
    elif total <= 3:
        linhas = [filmes_do_ano]
    else:
        linhas = [filmes_do_ano[i:i + 4] for i in range(0, total, 4)]
    
    global_idx = 0
    for linha in linhas:
        tamanho = len(linha)
        
        # Atribui colunas proporcionais para garantir que o tamanho do card 
        # seja sempre idêntico ao de 3 colunas, centralizando as linhas menores
        if tamanho == 3:
            cols_linha = st.columns(3)
        elif tamanho == 2:
            # Mantém a proporção exata para que os 2 cards tenham a mesma largura dos 3 de cima
            _, c1, c2, _ = st.columns([0.5, 1, 1, 0.5])
            cols_linha = [c1, c2]
        elif tamanho == 5:
            cols_linha = st.columns(5)
        elif tamanho == 4:
            cols_linha = st.columns(4)
        elif tamanho == 1:
            _, c1, _ = st.columns([1, 1, 1])
            cols_linha = [c1]
        else:
            cols_linha = st.columns(tamanho)
            
        for idx, filme in enumerate(linha):
            with cols_linha[idx]:
                titulo_maiusculo = filme['titulo'].upper()
                
                st.markdown(f"""
                <div style="text-align: center; margin-bottom: 15px;">
                    <div style="background: #000; border: 2px solid #5a472c; border-radius: 8px; padding: 4px; height: 340px; display: flex; align-items: center; justify-content: center; overflow: hidden; margin-bottom: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.5);">
                        <img src="{filme['imagem']}" style="max-height: 100%; max-width: 100%; object-fit: contain; border-radius: 4px;" onerror="this.src='https://via.placeholder.com/250x370/1a140e/e5c158?text={titulo_maiusculo.replace(' ', '+')}'">
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(titulo_maiusculo, key=f"btn_{ano_atual}_{global_idx}"):
                    st.session_state.filmes_salvos[ano_atual] = filme['titulo']
                    st.session_state.indice_ano += 1
                    st.rerun()
            global_idx += 1


# ----------------- MENU PRINCIPAL -----------------
if st.session_state.modo == "menu":
    # 🌟 CSS para padronizar a largura e o formato dos dois botões do topo
    st.markdown("""
    <style>
        div.stLinkButton > a {
            width: 100% !important;
            border-radius: 6px !important;
            font-weight: 700 !important;
            text-align: center !important;
        }

        /* 🌟 Efeito verde ao passar o mouse nos botões */
        div.stButton > button:hover,
        div.stLinkButton > a:hover {
            background-color: #008000 !important;
            color: white !important;
            border-color: #008000 !important;
            transition: all 0.2s ease-in-out !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # 🌟 TOPBAR COM OS DOIS BOTÕES DE NAVEGAÇÃO LADO A LADO COM A MESMA LARGURA
    col_aba1, col_aba2 = st.columns(2)
    with col_aba1:
        # Botão Ativo (Oscar) estilizado com destaque dourado
        st.markdown("""
        <div style="background: linear-gradient(135deg, #5a472c, #3a2e1b); color: #e5c158; padding: 0.55rem 1rem; border-radius: 6px; text-align: center; border: 2px solid #e5c158; font-weight: 700; font-size: 0.9rem; box-shadow: 0 4px 10px rgba(0,0,0,0.4);">
            🏆 VERSÃO OSCAR <span style="font-size: 0.7rem; background: #e5c158; color: #000; padding: 2px 6px; border-radius: 4px; margin-left: 6px;">ATIVO</span>
        </div>
        """, unsafe_allow_html=True)
    with col_aba2:
        # Botão para alternar para a versão nacional
        st.link_button("🇧🇷 VERSÃO CINEMA NACIONAL", "https://resta-um-cinema-nacional.streamlit.app/", use_container_width=True)
    
    st.markdown('<div class="site-title" style="margin-top: 20px;">FILMES DO OSCAR</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="menu-container">', unsafe_allow_html=True)
    if len(st.session_state.filmes_salvos) > 0:
        if st.button("CONTINUAR"):
            st.session_state.modo = "jogo"
            st.rerun()
            
    if st.button("NOVO JOGO"):
        st.session_state.indice_ano = 0
        st.session_state.filmes_salvos = {}
        st.session_state.modo = "jogo"
        st.rerun()
        
    if st.button("MATA-MATA"):
        qtd_salvos = len(st.session_state.filmes_salvos)
        if qtd_salvos >= 2:
            st.session_state.modo = "mata_mata_config"
            st.rerun()
        elif qtd_salvos == 1:
            st.warning("Falta mais 1 filme salvo para começar o mata-mata!")
        else:
            st.warning("Faltam 2 filmes salvos para começar o mata-mata!")
            
    if st.button("PULAR PARA O ANO"):
        st.session_state.modo = "pular"
        st.rerun()

    if st.button("MINHA SELEÇÃO"):
        st.session_state.modo = "rankings"
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- PULAR PARA O ANO -----------------
elif st.session_state.modo == "pular":
    # Cabeçalho unificado com o botão X alinhado na mesma linha horizontal
    c_espaco, c_titulo, c_fechar = st.columns([1, 8, 1])
    with c_titulo:
        st.markdown('<div style="text-align: center;"><h1 style="font-family: \'Cinzel\', serif; font-size: 2.2rem; font-weight: 900; color: #e5c158; text-shadow: 0 4px 10px rgba(0,0,0,0.8); letter-spacing: 2px; margin: 0; display: inline-block;">PULAR PARA O ANO</h1></div>', unsafe_allow_html=True)
    with c_fechar:
        if st.button("✕", key="fechar_pular"):
            st.session_state.modo = "menu"
            st.rerun()

    st.write("")

    # Exibe a barra de progresso aqui
    renderizar_barra_progresso()

    # Estilização baseada nos tipos NATIVOS do Streamlit (Primary = Concluído / Secondary = Pendente)
    st.markdown("""
    <style>
        /* Compacta o espaçamento entre colunas */
        [data-testid="column"] {
            padding: 0 2px !important;
        }

        /* 1. ANOS JÁ CONCLUÍDOS (type="primary") -> VERDE ELEGANTE */
        div.stButton > button[kind="primary"] {
            background-color: #15291b !important;
            color: #a3e4d7 !important;
            border: 2px solid #27ae60 !important;
            width: 100% !important;
            height: 48px !important;
            border-radius: 6px !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #1e3b27 !important;
            border-color: #2ecc71 !important;
            color: #ffffff !important;
            box-shadow: 0 0 10px rgba(46, 204, 113, 0.4) !important;
        }

        /* 2. ANOS PENDENTES (type="secondary") -> DOURADO PADRÃO */
        div.stButton > button[kind="secondary"] {
            background-color: #1a140e !important;
            color: #e5c158 !important;
            border: 2px solid #5a472c !important;
            width: 100% !important;
            height: 48px !important;
            border-radius: 6px !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            margin: 0 !important;
        }
        div.stButton > button[kind="secondary"]:hover {
            background-color: #e5c158 !important;
            color: #120e0b !important;
            border-color: #e5c158 !important;
            box-shadow: 0 0 10px rgba(229, 193, 88, 0.4) !important;
        }
    </style>
    """, unsafe_allow_html=True)

    anos_lista = ANOS
    num_colunas = 8  
    
    for i in range(0, len(anos_lista), num_colunas):
        cols = st.columns(num_colunas)
        bloco_anos = anos_lista[i:i + num_colunas]
        
        for j, ano in enumerate(bloco_anos):
            with cols[j]:
                ja_salvo = ano in st.session_state.filmes_salvos
                label = f"{ano} ✓" if ja_salvo else str(ano)
                
                # Passa o tipo nativo para o Streamlit identificar no HTML final sem falhar
                tipo_botao = "primary" if ja_salvo else "secondary"
                
                if st.button(label, key=f"grid_ano_{ano}", type=tipo_botao):
                    st.session_state.indice_ano = ANOS.index(ano)
                    st.session_state.modo = "jogo"
                    st.rerun()

# ----------------- JOGO (GAMEPLAY) -----------------
elif st.session_state.modo == "jogo":
    total_anos = len(ANOS)
    
    if st.session_state.indice_ano < total_anos:
        ano_atual = ANOS[st.session_state.indice_ano]
        filmes = BANCO_DE_DADOS[ano_atual]
        
        # Cabeçalho do Ano com o botão de fechar (✕) no canto superior direito
        col_cab1, col_cab2 = st.columns([9, 1])
        with col_cab1:
            st.markdown(f'<div class="year-title" style="margin-left: 40px;">OSCAR {ano_atual}</div>', unsafe_allow_html=True)
        with col_cab2:
            if st.button("✕", key="btn_fechar_jogo"):
                st.session_state.modo = "menu"
                st.rerun()
        
        st.write("")
        
        # Substitui a grade fixa antiga pela nossa função adaptativa inteligente
        renderizar_indicados_adaptativo(filmes, ano_atual)
        
        st.write("")
        # Botão de voltar rodada anterior
        b_col1, b_col2, b_col3 = st.columns([1, 2, 1])
        with b_col1:
            if st.session_state.indice_ano > 0:
                if st.button("⬅ VOLTAR"):
                    st.session_state.indice_ano -= 1
                    st.rerun()
    else:
        st.session_state.modo = "rankings"
        st.rerun()

# ----------------- MATA-MATA: CONFIGURAÇÃO DE CHAVEAMENTO -----------------
elif st.session_state.modo == "mata_mata_config":
    c_espaco, c_titulo, c_fechar = st.columns([1, 8, 1])
    with c_titulo:
        st.markdown('<div style="text-align: center;"><h1 style="font-family: \'Cinzel\', serif; font-size: 2.2rem; font-weight: 900; color: #e5c158; text-shadow: 0 4px 10px rgba(0,0,0,0.8); letter-spacing: 2px; margin: 0; display: inline-block;">MATA-MATA</h1></div>', unsafe_allow_html=True)
    with c_fechar:
        if st.button("✕", key="fechar_mm_config"):
            st.session_state.modo = "menu"
            st.rerun()

    st.write("")

    st.markdown('<div class="menu-container">', unsafe_allow_html=True)
    st.write("### Escolha o tipo de chaveamento:")
    
    tipo_chave = st.radio("", ["Por Ordem de Seleção", "Por Chaveamento Aleatório"])
    
    if st.button("INICIAR MATA-MATA"):
        import random
        filmes_para_batalha = list(st.session_state.filmes_salvos.items()) # Lista de (ano, titulo)
        
        if tipo_chave == "Chaveamento Aleatório":
            random.shuffle(filmes_para_batalha)
            
        st.session_state.mm_concorrentes = filmes_para_batalha
        st.session_state.mm_rodada = 1
        st.session_state.modo = "mata_mata_arena"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- MATA-MATA: ARENA DE BATALHA -----------------
elif st.session_state.modo == "mata_mata_arena":
    # Inicializa o histórico de confrontos se não existir
    if "historico_confrontos" not in st.session_state:
        st.session_state.historico_confrontos = []

    c_espaco, c_titulo, c_fechar = st.columns([1, 8, 1])
    with c_titulo:
        st.markdown('<div style="text-align: center;"><h1 style="font-family: \'Cinzel\', serif; font-size: 2.3rem; font-weight: 900; color: #e5c158; text-shadow: 0 4px 10px rgba(0,0,0,0.8); letter-spacing: 2px; margin: 0; display: inline-block;">RESTA UM</h1></div>', unsafe_allow_html=True)
    with c_fechar:
        if st.button("✕", key="fechar_mm_arena"):
            st.session_state.modo = "menu"
            st.rerun()

    st.write("")

    concorrentes = st.session_state.mm_concorrentes
    
    if len(concorrentes) == 1:
        ano_c, titulo_c = concorrentes[0]
        
        img_c = ""
        if ano_c in BANCO_DE_DADOS:
            for f in BANCO_DE_DADOS[ano_c]:
                if f['titulo'] == titulo_c:
                    img_c = f['imagem']

        st.markdown(f"""
        <div style="text-align: center; background: #1a140e; border: 2px solid #5a472c; padding: 18px; border-radius: 10px; margin: 0 auto; max-width: 420px; box-shadow: 0 0 20px rgba(229, 193, 88, 0.25);">
            <div style="font-family: 'Cinzel', serif; font-size: 2rem; font-weight: 900; color: #e5c158; margin-bottom: 8px;">{ano_c}</div>
            <div style="background: #000; border: 2px solid #5a472c; border-radius: 8px; padding: 4px; height: 380px; margin-bottom: 14px; display: flex; align-items: center; justify-content: center; overflow: hidden;">
                <img src="{img_c}" style="width: 100%; height: 100%; object-fit: contain; border-radius: 6px;" onerror="this.src='https://via.placeholder.com/250x370/1a140e/e5c158?text={titulo_c.replace(' ', '+')}'">
            </div>
            <div style="color: #ffffff; font-size: 1.25rem; font-weight: 700; line-height: 1.3; text-transform: uppercase; letter-spacing: 1px;">{titulo_c}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        # Exibe o histórico de todo o torneio na tela de vitória
        with st.expander("🏆 VER HISTÓRICO DE CONFRONTOS DO RESTA UM"):
            if st.session_state.historico_confrontos:
                for conf in st.session_state.historico_confrontos:
                    st.markdown(f"""
                    <div style="background: #1a140e; border-left: 3px solid #e5c158; padding: 8px 12px; margin-bottom: 6px; border-radius: 4px; font-size: 0.9rem;">
                        <span style="color: #a88a44; font-weight: bold;">{conf['fase']}:</span> 
                        <span style="color: #27ae60; font-weight: bold;">✓ {conf['vencedor']} ({conf['ano_vencedor']})</span> 
                        <span style="color: #8c8c9b;">derrotou</span> 
                        <span style="color: #c0392b; text-decoration: line-through;">{conf['perdedor']} ({conf['ano_perdedor']})</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("Nenhum confronto registrado.")
    else:
        ano1, tit1 = concorrentes[0]
        ano2, tit2 = concorrentes[1]
        
        total_restantes = len(concorrentes)
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <p style="color: #a88a44; font-weight: bold; letter-spacing: 1px; font-size: 1.1rem;">
                RODADA {st.session_state.mm_rodada} · {total_restantes} RESTANTES
            </p>
            <p style="color: #8c8c9b; font-size: 0.9rem;">ESCOLHA O FILME QUE VOCÊ DESEJA SALVAR</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_esq, col_vs, col_dir = st.columns([5, 1, 5])
        
        img1, img2 = "", ""
        if ano1 in BANCO_DE_DADOS:
            for f in BANCO_DE_DADOS[ano1]:
                if f['titulo'] == tit1:
                    img1 = f['imagem']
        if ano2 in BANCO_DE_DADOS:
            for f in BANCO_DE_DADOS[ano2]:
                if f['titulo'] == tit2:
                    img2 = f['imagem']
                    
        with col_esq:
            st.markdown(f'<div class="year-title" style="font-size: 1.8rem;">{ano1}</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="movie-box" style="height: 350px;">
                <img src="{img1}" onerror="this.src='https://via.placeholder.com/250x370/1a140e/e5c158?text={tit1.replace(' ', '+')}'">
            </div>
            """, unsafe_allow_html=True)
            if st.button(tit1, key="escolha_filme_1"):
                # Registra o confronto no histórico antes de avançar
                st.session_state.historico_confrontos.append({
                    "fase": f"Rodada {st.session_state.mm_rodada}",
                    "vencedor": tit1,
                    "ano_vencedor": ano1,
                    "perdedor": tit2,
                    "ano_perdedor": ano2
                })
                st.session_state.mm_concorrentes = concorrentes[2:] + [concorrentes[0]]
                st.session_state.mm_rodada += 1
                st.rerun()
                
        with col_vs:
            st.markdown('<div style="text-align: center; font-size: 2.5rem; font-weight: 900; color: #e5c158; margin-top: 150px;">VS</div>', unsafe_allow_html=True)
            
        with col_dir:
            st.markdown(f'<div class="year-title" style="font-size: 1.8rem;">{ano2}</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="movie-box" style="height: 350px;">
                <img src="{img2}" onerror="this.src='https://via.placeholder.com/250x370/1a140e/e5c158?text={tit2.replace(' ', '+')}'">
            </div>
            """, unsafe_allow_html=True)
            if st.button(tit2, key="escolha_filme_2"):
                # Registra o confronto no histórico antes de avançar
                st.session_state.historico_confrontos.append({
                    "fase": f"Rodada {st.session_state.mm_rodada}",
                    "vencedor": tit2,
                    "ano_vencedor": ano2,
                    "perdedor": tit1,
                    "ano_perdedor": ano1
                })
                st.session_state.mm_concorrentes = concorrentes[2:] + [concorrentes[1]]
                st.session_state.mm_rodada += 1
                st.rerun()
                
        # Expander discreto para consultar o histórico durante o torneio
        st.write("")
        with st.expander("📊 Ver Histórico de Confrontos desta Edição"):
            if st.session_state.historico_confrontos:
                for conf in st.session_state.historico_confrontos:
                    st.markdown(f"""
                    <div style="background: #1a140e; border-left: 3px solid #e5c158; padding: 6px 10px; margin-bottom: 4px; border-radius: 4px; font-size: 0.85rem;">
                        <span style="color: #a88a44;">{conf['fase']}:</span> 
                        <span style="color: #27ae60;">✓ {conf['vencedor']}</span> derrotou <span style="color: #c0392b; text-decoration: line-through;">{conf['perdedor']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("Nenhum confronto nesta rodada ainda.")

# ----------------- RESULTADOS (RANKINGS) -----------------
elif st.session_state.modo == "rankings":
    c_espaco, c_titulo, c_fechar = st.columns([1, 8, 1])
    with c_titulo:
        st.markdown('<div style="text-align: center;"><h1 style="font-family: \'Cinzel\', serif; font-size: 2.2rem; font-weight: 900; color: #e5c158; text-shadow: 0 4px 10px rgba(0,0,0,0.8); letter-spacing: 2px; margin: 0; display: inline-block;">SUAS SELEÇÕES</h1></div>', unsafe_allow_html=True)
    with c_fechar:
        if st.button("✕", key="fechar_rankings"):
            st.session_state.modo = "menu"
            st.rerun()
    
    st.write("")

    # Exibe a barra de progresso aqui
    renderizar_barra_progresso()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not st.session_state.filmes_salvos:
            st.write("Nenhum filme foi salvo ainda!")
        else:
            salvos_ordenados = sorted(st.session_state.filmes_salvos.items())
            
            for ano, titulo in salvos_ordenados:
                st.markdown(f"""
                <div class="summary-item">
                    <strong style="color: #e5c158;">{ano}:</strong> {titulo}
                </div>
                """, unsafe_allow_html=True)