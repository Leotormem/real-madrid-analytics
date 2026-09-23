import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

from utils.dados import (
    carregar_partidas,
    carregar_eventos
)


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Análises | Real Madrid Analytics",
    page_icon="🔬",
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
# FUNÇÃO DE RESUMO DA TEMPORADA
# ==========================================================

@st.cache_data(show_spinner=False)
def gerar_base_analitica():

    partidas = carregar_partidas()

    registros = []

    for _, partida in partidas.iterrows():

        eventos = carregar_eventos(
            partida["match_id"]
        )

        eventos_real = eventos[
            eventos["team"] == "Real Madrid"
        ].copy()

        passes = eventos_real[
            eventos_real["type"] == "Pass"
        ]

        chutes = eventos_real[
            eventos_real["type"] == "Shot"
        ]

        if "pass_outcome" in passes.columns:

            passes_completos = (
                passes[
                    "pass_outcome"
                ]
                .isna()
                .sum()
            )

        else:

            passes_completos = len(
                passes
            )

        if "shot_outcome" in chutes.columns:

            gols = (
                chutes[
                    "shot_outcome"
                ]
                == "Goal"
            ).sum()

        else:

            gols = 0

        if "shot_statsbomb_xg" in chutes.columns:

            xg = (
                chutes[
                    "shot_statsbomb_xg"
                ]
                .fillna(0)
                .sum()
            )

        else:

            xg = 0

        total_passes = len(
            passes
        )

        total_chutes = len(
            chutes
        )

        precisao = (
            passes_completos
            / total_passes
            * 100
            if total_passes > 0
            else 0
        )

        conversao = (
            gols
            / total_chutes
            * 100
            if total_chutes > 0
            else 0
        )

        registros.append(
            {
                "match_id": partida["match_id"],
                "data": partida["match_date"],
                "adversario": partida["adversario"],
                "local": partida["local"],
                "resultado": partida["resultado"],
                "gols": int(gols),
                "chutes": total_chutes,
                "passes": total_passes,
                "passes_completos": int(
                    passes_completos
                ),
                "precisao_passes": precisao,
                "conversao": conversao,
                "xG": xg
            }
        )

    df = pd.DataFrame(
        registros
    )

    df["jogo"] = (
        df.index
        + 1
    )

    return df


# ==========================================================
# TÍTULO
# ==========================================================

st.title(
    "🔬 Análises Avançadas"
)

st.caption(
    "Relações estatísticas entre desempenho ofensivo, "
    "volume de jogo e eficiência."
)


# ==========================================================
# CARREGAMENTO
# ==========================================================

with st.spinner(
    "Preparando base analítica da temporada..."
):

    df = gerar_base_analitica()


# ==========================================================
# MÉTRICAS
# ==========================================================

st.markdown(
    '<div class="section-label">Resumo analítico</div>',
    unsafe_allow_html=True
)


m1, m2, m3, m4 = st.columns(4)


with m1:

    st.metric(
        "⚽ Gols",
        int(
            df["gols"].sum()
        )
    )


with m2:

    st.metric(
        "🎯 Chutes",
        int(
            df["chutes"].sum()
        )
    )


with m3:

    st.metric(
        "🔄 Passes",
        int(
            df["passes"].sum()
        )
    )


with m4:

    st.metric(
        "📊 xG acumulado",
        f'{df["xG"].sum():.2f}'
    )


# ==========================================================
# MATPLOTLIB
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Matplotlib</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Gols e chutes ao longo da temporada"
)


fig, ax = plt.subplots(
    figsize=(12, 5)
)

ax.plot(
    df["jogo"],
    df["chutes"],
    marker="o",
    label="Chutes"
)

ax.plot(
    df["jogo"],
    df["gols"],
    marker="o",
    label="Gols"
)

ax.set_xlabel(
    "Jogo"
)

ax.set_ylabel(
    "Quantidade"
)

ax.set_title(
    "Evolução de chutes e gols"
)

ax.legend()

ax.grid(
    alpha=0.2
)

st.pyplot(
    fig,
    use_container_width=True
)


# ==========================================================
# SEABORN
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Seaborn</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Relação entre chutes e gols"
)


fig2, ax2 = plt.subplots(
    figsize=(10, 6)
)

sns.regplot(
    data=df,
    x="chutes",
    y="gols",
    ax=ax2
)

ax2.set_title(
    "Chutes x Gols"
)

ax2.set_xlabel(
    "Chutes"
)

ax2.set_ylabel(
    "Gols"
)

st.pyplot(
    fig2,
    use_container_width=True
)


# ==========================================================
# CORRELAÇÃO
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Correlação</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Matriz de correlação"
)


colunas_correlacao = [
    "gols",
    "chutes",
    "passes",
    "precisao_passes",
    "conversao",
    "xG"
]


corr = df[
    colunas_correlacao
].corr()


fig3, ax3 = plt.subplots(
    figsize=(9, 6)
)

sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    ax=ax3
)

ax3.set_title(
    "Correlação entre indicadores ofensivos"
)

st.pyplot(
    fig3,
    use_container_width=True
)


# ==========================================================
# PLOTLY - DISPERSÃO
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Plotly</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Eficiência ofensiva por partida"
)


fig_plotly = px.scatter(
    df,
    x="chutes",
    y="gols",
    size="xG",
    color="resultado",
    hover_name="adversario",
    hover_data=[
        "data",
        "local",
        "conversao",
        "precisao_passes"
    ],
    title=(
        "Relação entre chutes, gols e xG"
    )
)


fig_plotly.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)


st.plotly_chart(
    fig_plotly,
    use_container_width=True
)


# ==========================================================
# CASA X FORA
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Contexto</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Comparação entre jogos em casa e fora"
)


resumo_local = (
    df
    .groupby(
        "local"
    )
    .agg(
        gols=("gols", "mean"),
        chutes=("chutes", "mean"),
        passes=("passes", "mean"),
        conversao=("conversao", "mean")
    )
    .reset_index()
)


fig_local = px.bar(
    resumo_local,
    x="local",
    y=[
        "gols",
        "chutes"
    ],
    barmode="group",
    title=(
        "Média de gols e chutes por local"
    ),
    labels={
        "local": "Local",
        "value": "Média",
        "variable": "Indicador"
    }
)


fig_local.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)


st.plotly_chart(
    fig_local,
    use_container_width=True
)


# ==========================================================
# FILTRO INTERATIVO
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Exploração</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Explorar relação entre duas variáveis"
)


col1, col2 = st.columns(2)


variaveis = [
    "gols",
    "chutes",
    "passes",
    "precisao_passes",
    "conversao",
    "xG"
]


with col1:

    eixo_x = st.selectbox(
        "Variável do eixo X",
        variaveis,
        index=1
    )


with col2:

    eixo_y = st.selectbox(
        "Variável do eixo Y",
        variaveis,
        index=0
    )


fig_exploracao = px.scatter(
    df,
    x=eixo_x,
    y=eixo_y,
    color="resultado",
    hover_name="adversario",
    hover_data=[
        "data",
        "local"
    ],
    title=(
        f"{eixo_x} x {eixo_y}"
    )
)


fig_exploracao.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)


st.plotly_chart(
    fig_exploracao,
    use_container_width=True
)


# ==========================================================
# TABELA
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Base analítica</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Indicadores por partida"
)


st.dataframe(
    df[
        [
            "data",
            "adversario",
            "local",
            "resultado",
            "gols",
            "chutes",
            "passes",
            "precisao_passes",
            "conversao",
            "xG"
        ]
    ],
    use_container_width=True,
    hide_index=True,
    height=520
)


# ==========================================================
# RODAPÉ
# ==========================================================

st.caption(
    "Fonte: StatsBomb Open Data • "
    "Análises com Matplotlib, Seaborn e Plotly"
)