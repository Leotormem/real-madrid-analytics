import pandas as pd
import streamlit as st
from mplsoccer import Pitch

from utils.dados import (
    carregar_partidas,
    carregar_passes
)


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Passes | Real Madrid Analytics",
    page_icon="🔄",
    layout="wide"
)


# ==========================================================
# ESTILO
# ==========================================================

st.markdown(
    """
<style>

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.section-label {
    color: #60A5FA;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 5px;
}

div[data-testid="stMetric"] {
    background:
        linear-gradient(
            145deg,
            rgba(30,41,59,0.85),
            rgba(15,23,42,0.85)
        );

    border:
        1px solid rgba(148,163,184,0.12);

    padding: 18px;

    border-radius: 16px;
}

</style>
""",
    unsafe_allow_html=True
)


# ==========================================================
# TÍTULO
# ==========================================================

st.title(
    "🔄 Análise de Passes"
)

st.caption(
    "Explore o volume, precisão e distribuição dos passes "
    "do Real Madrid em cada partida."
)


# ==========================================================
# SELEÇÃO DA PARTIDA
# ==========================================================

partidas = carregar_partidas()

partidas_opcoes = partidas.copy()

partidas_opcoes["descricao"] = partidas_opcoes.apply(
    lambda linha:
    f'{linha["match_date"]} • {linha["placar"]}',
    axis=1
)


partida_selecionada = st.selectbox(
    "Selecione uma partida",
    options=partidas_opcoes["descricao"].tolist()
)


linha_partida = partidas_opcoes[
    partidas_opcoes["descricao"]
    == partida_selecionada
].iloc[0]

match_id = linha_partida["match_id"]


# ==========================================================
# CARREGAMENTO DOS PASSES
# ==========================================================

with st.spinner(
    "Carregando passes da partida..."
):

    passes = carregar_passes(
        match_id=match_id,
        somente_real=True
    )


# ==========================================================
# CÁLCULOS
# ==========================================================

total_passes = len(passes)


if "pass_outcome" in passes.columns:

    passes_completos = passes[
        passes["pass_outcome"].isna()
    ].copy()

    passes_incompletos = passes[
        passes["pass_outcome"].notna()
    ].copy()

else:

    passes_completos = passes.copy()
    passes_incompletos = pd.DataFrame()


total_completos = len(
    passes_completos
)

total_incompletos = len(
    passes_incompletos
)


precisao = (
    total_completos
    / total_passes
    * 100
    if total_passes > 0
    else 0
)


jogadores_com_passe = (
    passes["player"]
    .dropna()
    .nunique()
)


# ==========================================================
# MÉTRICAS
# ==========================================================

st.markdown(
    '<div class="section-label">Resumo da partida</div>',
    unsafe_allow_html=True
)

m1, m2, m3, m4 = st.columns(4)


with m1:

    st.metric(
        "🔄 Total de passes",
        total_passes
    )


with m2:

    st.metric(
        "✅ Passes completos",
        total_completos
    )


with m3:

    st.metric(
        "🎯 Precisão",
        f"{precisao:.1f}%"
    )


with m4:

    st.metric(
        "👤 Jogadores envolvidos",
        jogadores_com_passe
    )


# ==========================================================
# PASSES POR JOGADOR
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Participação</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Jogadores com mais passes"
)


passes_por_jogador = (
    passes["player"]
    .dropna()
    .value_counts()
    .reset_index()
)

passes_por_jogador.columns = [
    "Jogador",
    "Passes"
]


st.bar_chart(
    passes_por_jogador.head(12),
    x="Jogador",
    y="Passes"
)


# ==========================================================
# FILTROS
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Filtros</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Personalizar mapa de passes"
)


jogadores = sorted(
    passes["player"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


col1, col2 = st.columns(2)


with col1:

    jogador_selecionado = st.selectbox(
        "Jogador",
        options=[
            "Todos"
        ] + jogadores
    )


with col2:

    tipo_passe = st.radio(
        "Situação do passe",
        [
            "Todos",
            "Completos",
            "Incompletos"
        ],
        horizontal=True
    )


mostrar_tabela = st.checkbox(
    "Mostrar tabela detalhada",
    value=True
)


# ==========================================================
# APLICA FILTROS
# ==========================================================

passes_filtrados = passes.copy()


if jogador_selecionado != "Todos":

    passes_filtrados = passes_filtrados[
        passes_filtrados["player"]
        == jogador_selecionado
    ].copy()


if tipo_passe == "Completos":

    if "pass_outcome" in passes_filtrados.columns:

        passes_filtrados = passes_filtrados[
            passes_filtrados[
                "pass_outcome"
            ].isna()
        ].copy()


elif tipo_passe == "Incompletos":

    if "pass_outcome" in passes_filtrados.columns:

        passes_filtrados = passes_filtrados[
            passes_filtrados[
                "pass_outcome"
            ].notna()
        ].copy()


# ==========================================================
# MAPA DE PASSES
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Visualização em campo</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Mapa de passes"
)


coordenadas = passes_filtrados[
    passes_filtrados["location"].notna()
].copy()


if "pass_end_location" in coordenadas.columns:

    coordenadas = coordenadas[
        coordenadas[
            "pass_end_location"
        ].notna()
    ].copy()


if coordenadas.empty:

    st.warning(
        "Não existem passes com coordenadas disponíveis "
        "para os filtros selecionados."
    )

else:

    coordenadas["x"] = coordenadas[
        "location"
    ].apply(
        lambda local:
        local[0]
    )

    coordenadas["y"] = coordenadas[
        "location"
    ].apply(
        lambda local:
        local[1]
    )

    coordenadas["end_x"] = coordenadas[
        "pass_end_location"
    ].apply(
        lambda local:
        local[0]
    )

    coordenadas["end_y"] = coordenadas[
        "pass_end_location"
    ].apply(
        lambda local:
        local[1]
    )


    pitch = Pitch(
        pitch_type="statsbomb",
        pitch_color="#0B1020",
        line_color="#E5E7EB"
    )


    fig, ax = pitch.draw(
        figsize=(13, 8)
    )


    completos_mapa = coordenadas.copy()

    if "pass_outcome" in coordenadas.columns:

        completos_mapa = coordenadas[
            coordenadas[
                "pass_outcome"
            ].isna()
        ]

        incompletos_mapa = coordenadas[
            coordenadas[
                "pass_outcome"
            ].notna()
        ]

    else:

        incompletos_mapa = pd.DataFrame()


    if not completos_mapa.empty:

        pitch.arrows(
            completos_mapa["x"],
            completos_mapa["y"],
            completos_mapa["end_x"],
            completos_mapa["end_y"],
            width=1.2,
            headwidth=3,
            headlength=3,
            alpha=0.45,
            ax=ax,
            label="Passes completos"
        )


    if not incompletos_mapa.empty:

        pitch.arrows(
            incompletos_mapa["x"],
            incompletos_mapa["y"],
            incompletos_mapa["end_x"],
            incompletos_mapa["end_y"],
            width=1.1,
            headwidth=3,
            headlength=3,
            alpha=0.30,
            ax=ax,
            label="Passes incompletos"
        )


    titulo_jogador = (
        jogador_selecionado
        if jogador_selecionado != "Todos"
        else "Real Madrid"
    )


    ax.set_title(
        f"Mapa de passes — {titulo_jogador}\n"
        f'{linha_partida["placar"]}',
        fontsize=16
    )


    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.03),
        ncol=2
    )


    st.pyplot(
        fig,
        use_container_width=True
    )


# ==========================================================
# MÉTRICAS DO FILTRO
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Seleção atual</div>',
    unsafe_allow_html=True
)


total_filtrado = len(
    passes_filtrados
)


if "pass_outcome" in passes_filtrados.columns:

    completos_filtrados = (
        passes_filtrados[
            "pass_outcome"
        ]
        .isna()
        .sum()
    )

else:

    completos_filtrados = (
        total_filtrado
    )


precisao_filtrada = (
    completos_filtrados
    / total_filtrado
    * 100
    if total_filtrado > 0
    else 0
)


f1, f2, f3 = st.columns(3)


with f1:

    st.metric(
        "Passes selecionados",
        total_filtrado
    )


with f2:

    st.metric(
        "Passes completos",
        int(
            completos_filtrados
        )
    )


with f3:

    st.metric(
        "Precisão da seleção",
        f"{precisao_filtrada:.1f}%"
    )


# ==========================================================
# TABELA
# ==========================================================

if mostrar_tabela:

    st.divider()

    st.markdown(
        '<div class="section-label">Eventos</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "Detalhes dos passes"
    )


    colunas_tabela = [
        coluna
        for coluna in [
            "minute",
            "second",
            "player",
            "pass_recipient",
            "pass_length",
            "pass_angle",
            "pass_height",
            "pass_outcome",
            "location",
            "pass_end_location"
        ]
        if coluna in passes_filtrados.columns
    ]


    st.dataframe(
        passes_filtrados[
            colunas_tabela
        ],
        use_container_width=True,
        hide_index=True,
        height=450
    )


# ==========================================================
# RODAPÉ
# ==========================================================

st.caption(
    "Fonte: StatsBomb Open Data • "
    "Mapa de campo desenvolvido com mplsoccer"
)