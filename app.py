import streamlit as st


# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Real Madrid Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# ESTILO VISUAL
# ==========================================================

st.markdown(
    """
<style>

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(
            circle at top right,
            rgba(21, 101, 192, 0.10),
            transparent 28%
        ),
        #0B1020;
}

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #0F172A,
            #111827
        );

    border-right:
        1px solid rgba(255,255,255,0.08);
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* HERO */

.hero {
    padding: 36px 40px;

    border-radius: 24px;

    background:
        linear-gradient(
            120deg,
            rgba(30, 64, 175, 0.26),
            rgba(59, 130, 246, 0.10)
        );

    border:
        1px solid rgba(147, 197, 253, 0.18);

    box-shadow:
        0 20px 60px rgba(0,0,0,0.18);

    margin-bottom: 25px;
}

.badge-container {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
    flex-wrap: wrap;
}

.badge {
    padding: 5px 12px;

    border-radius: 999px;

    font-size: 0.72rem;

    font-weight: 700;

    letter-spacing: 0.5px;

    background:
        rgba(59, 130, 246, 0.14);

    border:
        1px solid rgba(147, 197, 253, 0.22);

    color:
        #BFDBFE;
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero-subtitle {
    font-size: 1.05rem;
    line-height: 1.65;
    opacity: 0.82;
    max-width: 850px;
}


/* CARDS */

.card {
    padding: 22px;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(30,41,59,0.85),
            rgba(15,23,42,0.85)
        );

    border:
        1px solid rgba(148,163,184,0.12);

    min-height: 160px;
}


/* LABELS */

.section-label {
    color: #60A5FA;

    font-size: 0.78rem;

    font-weight: 800;

    letter-spacing: 1px;

    text-transform: uppercase;

    margin-bottom: 5px;
}


/* FOOTER */

.footer {
    margin-top: 50px;

    padding-top: 20px;

    border-top:
        1px solid rgba(148,163,184,0.10);

    text-align: center;

    font-size: 0.82rem;

    opacity: 0.55;
}

</style>
""",
    unsafe_allow_html=True
)


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("⚽ Real Madrid Analytics")

    st.caption(
        "La Liga 2015/2016"
    )

    st.divider()

    st.markdown(
        """
        ### Projeto

        Dashboard de Sports Analytics com dados
        reais da **StatsBomb**.

        O objetivo é analisar o desempenho ofensivo
        do Real Madrid ao longo da temporada.
        """
    )

    st.divider()

    st.info(
        """
        **Base analisada**

        La Liga 2015/2016

        38 partidas

        Dados de eventos StatsBomb
        """
    )


# ==========================================================
# HERO
# ==========================================================

hero_html = (
    '<div class="hero">'
    '<div class="badge-container">'
    '<span class="badge">SPORTS ANALYTICS</span>'
    '<span class="badge">STATSBOMB</span>'
    '<span class="badge">LA LIGA 2015/16</span>'
    '</div>'
    '<div class="hero-title">'
    '⚽ Real Madrid Analytics'
    '</div>'
    '<div class="hero-subtitle">'
    'Análise interativa do desempenho ofensivo do Real Madrid '
    'durante a temporada 2015/2016 da La Liga, utilizando dados '
    'reais de eventos da StatsBomb.'
    '</div>'
    '</div>'
)

st.markdown(
    hero_html,
    unsafe_allow_html=True
)


# ==========================================================
# PERGUNTA CENTRAL
# ==========================================================

st.markdown(
    '<div class="section-label">Pergunta de análise</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Como evoluiu o desempenho ofensivo do Real Madrid ao longo da temporada?"
)

st.write(
    """
    O dashboard busca analisar a relação entre **gols, chutes,
    passes e participação individual dos jogadores**, permitindo
    observar tendências ao longo dos 38 jogos da La Liga 2015/2016.
    """
)


# ==========================================================
# VISÃO GERAL DO PROJETO
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">O que será analisado</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        """
<div class="card">

### 📈 Evolução da temporada

Acompanhe o desempenho jogo a jogo e veja
como gols, chutes e passes evoluíram ao
longo do campeonato.

</div>
""",
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
<div class="card">

### 🎯 Eficiência ofensiva

Analise volume de finalizações, gols e
taxa de conversão para compreender a
eficiência ofensiva da equipe.

</div>
""",
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
<div class="card">

### 👤 Participação individual

Compare jogadores e identifique quem mais
contribuiu com passes, chutes e gols ao
longo da temporada.

</div>
""",
        unsafe_allow_html=True
    )


# ==========================================================
# TECNOLOGIAS
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Tecnologias</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Ferramentas utilizadas"
)

tec1, tec2, tec3, tec4 = st.columns(4)

with tec1:
    st.metric(
        "Interface",
        "Streamlit"
    )

with tec2:
    st.metric(
        "Dados",
        "StatsBombPy"
    )

with tec3:
    st.metric(
        "Campo",
        "mplsoccer"
    )

with tec4:
    st.metric(
        "Análises",
        "Pandas"
    )


# ==========================================================
# DADOS DO PROJETO
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Dataset</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Dados da temporada"
)

st.write(
    """
    A aplicação utiliza os dados abertos da **StatsBomb**.
    Foram identificadas **38 partidas do Real Madrid**
    na La Liga 2015/2016 e todas possuem dados de eventos
    disponíveis.

    Esses eventos incluem passes, chutes, conduções,
    pressões, recuperações de bola, interceptações,
    dribles e diversas outras ações realizadas durante
    cada partida.
    """
)


# ==========================================================
# NAVEGAÇÃO
# ==========================================================

st.divider()

st.success(
    """
    👈 Utilize o menu lateral do Streamlit para navegar
    entre as diferentes páginas do dashboard.
    """
)


# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
    '<div class="footer">'
    'Real Madrid Analytics • Sports Analytics • '
    'Dados: StatsBomb Open Data'
    '</div>',
    unsafe_allow_html=True
)