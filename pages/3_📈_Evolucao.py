import pandas as pd
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
    page_title="Evolução | Real Madrid Analytics",
    page_icon="📈",
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
# FUNÇÃO PARA RESUMO DOS 38 JOGOS
# ==========================================================

@st.cache_data(show_spinner=False)
def carregar_resumo_temporada():

    partidas = carregar_partidas()

    registros = []

    total = len(partidas)

    progresso = st.progress(0)

    status = st.empty()

    for indice, partida in partidas.iterrows():

        status.write(
            f"Processando jogo {indice + 1} de {total}..."
        )

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

        if "shot_outcome" in chutes.columns:

            gols = chutes[
                chutes["shot_outcome"] == "Goal"
            ]

        else:

            gols = pd.DataFrame()

        if "pass_outcome" in passes.columns:

            passes_completos = passes[
                passes["pass_outcome"].isna()
            ]

        else:

            passes_completos = pd.DataFrame()

        total_passes = len(passes)

        total_passes_completos = len(
            passes_completos
        )

        total_chutes = len(chutes)

        total_gols = len(gols)

        precisao_passes = (
            total_passes_completos
            / total_passes
            * 100
            if total_passes > 0
            else 0
        )

        conversao = (
            total_gols
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
                "placar": partida["placar"],
                "gols": total_gols,
                "chutes": total_chutes,
                "passes": total_passes,
                "passes_completos": total_passes_completos,
                "precisao_passes": precisao_passes,
                "conversao": conversao
            }
        )

        progresso.progress(
            (indice + 1) / total
        )

    progresso.empty()

    status.empty()

    return pd.DataFrame(
        registros
    )


# ==========================================================
# TÍTULO
# ==========================================================

st.title(
    "📈 Evolução da Temporada"
)

st.caption(
    "Análise jogo a jogo do desempenho ofensivo do Real Madrid."
)


# ==========================================================
# CARREGAMENTO
# ==========================================================

with st.spinner(
    "Carregando e processando eventos dos 38 jogos..."
):

    resumo = carregar_resumo_temporada()


# ==========================================================
# MÉTRICAS GERAIS
# ==========================================================

st.markdown(
    '<div class="section-label">Resumo ofensivo</div>',
    unsafe_allow_html=True
)

media_chutes = resumo["chutes"].mean()

media_passes = resumo["passes"].mean()

media_precisao = resumo[
    "precisao_passes"
].mean()

media_conversao = resumo[
    "conversao"
].mean()


m1, m2, m3, m4 = st.columns(4)


with m1:

    st.metric(
        "🎯 Média de chutes",
        f"{media_chutes:.1f}"
    )


with m2:

    st.metric(
        "🔄 Média de passes",
        f"{media_passes:.1f}"
    )


with m3:

    st.metric(
        "✅ Precisão média de passes",
        f"{media_precisao:.1f}%"
    )


with m4:

    st.metric(
        "⚽ Conversão média",
        f"{media_conversao:.1f}%"
    )


# ==========================================================
# EVOLUÇÃO DE GOLS
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Gols</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Gols por partida"
)

resumo["jogo"] = (
    resumo.index
    + 1
)

fig_gols = px.line(
    resumo,
    x="jogo",
    y="gols",
    markers=True,
    hover_data=[
        "data",
        "adversario",
        "local",
        "placar"
    ],
    labels={
        "jogo": "Jogo",
        "gols": "Gols"
    },
    title="Evolução dos gols ao longo da temporada"
)

fig_gols.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig_gols,
    use_container_width=True
)


# ==========================================================
# EVOLUÇÃO DE CHUTES
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Finalizações</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Chutes por partida"
)

fig_chutes = px.bar(
    resumo,
    x="jogo",
    y="chutes",
    hover_data=[
        "data",
        "adversario",
        "placar"
    ],
    labels={
        "jogo": "Jogo",
        "chutes": "Chutes"
    },
    title="Volume de finalizações por jogo"
)

fig_chutes.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig_chutes,
    use_container_width=True
)


# ==========================================================
# PASSES
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Construção ofensiva</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Volume de passes"
)

fig_passes = px.line(
    resumo,
    x="jogo",
    y="passes",
    markers=True,
    hover_data=[
        "data",
        "adversario",
        "placar",
        "precisao_passes"
    ],
    labels={
        "jogo": "Jogo",
        "passes": "Passes"
    },
    title="Quantidade de passes por partida"
)

fig_passes.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig_passes,
    use_container_width=True
)


# ==========================================================
# PRECISÃO DOS PASSES
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Eficiência</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Precisão de passes"
)

fig_precisao = px.area(
    resumo,
    x="jogo",
    y="precisao_passes",
    hover_data=[
        "data",
        "adversario",
        "placar"
    ],
    labels={
        "jogo": "Jogo",
        "precisao_passes": "Precisão (%)"
    },
    title="Precisão de passes ao longo da temporada"
)

fig_precisao.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig_precisao,
    use_container_width=True
)


# ==========================================================
# RELAÇÃO CHUTES X GOLS
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Relação ofensiva</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Chutes x gols"
)

fig_relacao = px.scatter(
    resumo,
    x="chutes",
    y="gols",
    hover_name="adversario",
    hover_data=[
        "data",
        "placar",
        "local",
        "conversao"
    ],
    labels={
        "chutes": "Chutes",
        "gols": "Gols"
    },
    title="Relação entre volume de chutes e gols marcados"
)

fig_relacao.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig_relacao,
    use_container_width=True
)


# ==========================================================
# TABELA COMPLETA
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Dados jogo a jogo</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Resumo ofensivo das partidas"
)

st.dataframe(
    resumo[
        [
            "data",
            "adversario",
            "local",
            "resultado",
            "gols",
            "chutes",
            "passes",
            "passes_completos",
            "precisao_passes",
            "conversao"
        ]
    ],
    use_container_width=True,
    hide_index=True,
    height=500
)


st.caption(
    "Fonte: StatsBomb Open Data"
)