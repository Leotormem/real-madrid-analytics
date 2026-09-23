import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from mplsoccer import Pitch

from utils.dados import (
    carregar_partidas,
    carregar_chutes
)


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Finalizações | Real Madrid Analytics",
    page_icon="🎯",
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
    "🎯 Finalizações"
)

st.caption(
    "Análise das finalizações do Real Madrid por partida e jogador."
)


# ==========================================================
# PARTIDAS
# ==========================================================

partidas = carregar_partidas()

opcoes_partidas = partidas.copy()

opcoes_partidas["descricao"] = opcoes_partidas.apply(
    lambda linha:
    f'{linha["match_date"]} • {linha["placar"]}',
    axis=1
)


partida_selecionada = st.selectbox(
    "Selecione uma partida",
    options=opcoes_partidas["descricao"].tolist()
)


linha_partida = opcoes_partidas[
    opcoes_partidas["descricao"] == partida_selecionada
].iloc[0]

match_id = linha_partida["match_id"]


# ==========================================================
# CARREGA CHUTES
# ==========================================================

with st.spinner(
    "Carregando finalizações da partida..."
):

    chutes = carregar_chutes(
        match_id=match_id,
        somente_real=True
    )


# ==========================================================
# MÉTRICAS
# ==========================================================

total_chutes = len(chutes)

if "shot_outcome" in chutes.columns:

    gols = chutes[
        chutes["shot_outcome"] == "Goal"
    ]

else:

    gols = pd.DataFrame()


total_gols = len(gols)

taxa_conversao = (
    total_gols
    / total_chutes
    * 100
    if total_chutes > 0
    else 0
)


jogadores_com_chute = (
    chutes["player"]
    .dropna()
    .nunique()
)


m1, m2, m3, m4 = st.columns(4)


with m1:

    st.metric(
        "🎯 Chutes",
        total_chutes
    )


with m2:

    st.metric(
        "⚽ Gols",
        total_gols
    )


with m3:

    st.metric(
        "📈 Conversão",
        f"{taxa_conversao:.1f}%"
    )


with m4:

    st.metric(
        "👤 Jogadores que chutaram",
        jogadores_com_chute
    )


# ==========================================================
# LATEX
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Indicador</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Taxa de conversão"
)

st.latex(
    r"""
    \text{Taxa de Conversão}
    =
    \frac{\text{Gols}}{\text{Chutes}}
    \times 100
    """
)

st.write(
    f"Nesta partida, a taxa de conversão foi de "
    f"**{taxa_conversao:.1f}%**."
)


# ==========================================================
# CHUTES POR JOGADOR
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Jogadores</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Finalizações por jogador"
)

chutes_jogador = (
    chutes["player"]
    .dropna()
    .value_counts()
    .reset_index()
)

chutes_jogador.columns = [
    "Jogador",
    "Chutes"
]

st.bar_chart(
    chutes_jogador,
    x="Jogador",
    y="Chutes"
)


# ==========================================================
# MAPA DE CHUTES
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Mapa de chutes</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Localização das finalizações"
)


if total_chutes == 0:

    st.warning(
        "Não há finalizações disponíveis para esta partida."
    )

else:

    coordenadas = chutes[
        chutes["location"].notna()
    ].copy()

    if coordenadas.empty:

        st.warning(
            "Não há coordenadas disponíveis para os chutes."
        )

    else:

        coordenadas["x"] = coordenadas[
            "location"
        ].apply(
            lambda local: local[0]
        )

        coordenadas["y"] = coordenadas[
            "location"
        ].apply(
            lambda local: local[1]
        )

        pitch = Pitch(
            pitch_type="statsbomb",
            pitch_color="#0B1020",
            line_color="#E5E7EB"
        )

        fig, ax = pitch.draw(
            figsize=(12, 7)
        )

        for _, chute in coordenadas.iterrows():

            resultado = chute.get(
                "shot_outcome",
                ""
            )

            tamanho = 180

            if resultado == "Goal":

                tamanho = 320

            pitch.scatter(
                chute["x"],
                chute["y"],
                s=tamanho,
                ax=ax,
                alpha=0.75
            )

        ax.set_title(
            f'Finalizações do Real Madrid\n{linha_partida["placar"]}',
            fontsize=16
        )

        st.pyplot(
            fig,
            use_container_width=True
        )


# ==========================================================
# FILTRO DE JOGADOR
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Filtro individual</div>',
    unsafe_allow_html=True
)

jogadores = sorted(
    chutes["player"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

opcao_jogador = st.selectbox(
    "Selecione um jogador",
    options=[
        "Todos"
    ] + jogadores
)


if opcao_jogador == "Todos":

    chutes_filtrados = chutes.copy()

else:

    chutes_filtrados = chutes[
        chutes["player"] == opcao_jogador
    ].copy()


# ==========================================================
# TABELA
# ==========================================================

st.subheader(
    "Dados das finalizações"
)

colunas_disponiveis = [
    coluna
    for coluna in [
        "minute",
        "second",
        "player",
        "shot_outcome",
        "shot_type",
        "shot_body_part",
        "shot_statsbomb_xg",
        "location"
    ]
    if coluna in chutes_filtrados.columns
]

st.dataframe(
    chutes_filtrados[
        colunas_disponiveis
    ],
    use_container_width=True,
    hide_index=True,
    height=450
)


# ==========================================================
# RESUMO
# ==========================================================

st.caption(
    "Fonte: StatsBomb Open Data • Visualização de campo com mplsoccer"
)