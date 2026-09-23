import pandas as pd
import plotly.express as px
import streamlit as st

from streamlit_extras.metric_cards import style_metric_cards

from utils.dados import carregar_partidas


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Temporada | Real Madrid Analytics",
    page_icon="⚽",
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

</style>
""",
    unsafe_allow_html=True
)


# ==========================================================
# TÍTULO
# ==========================================================

st.title(
    "⚽ Temporada 2015/2016"
)

st.caption(
    "Visão geral do desempenho do Real Madrid na La Liga."
)


# ==========================================================
# CARREGAMENTO
# ==========================================================

with st.spinner(
    "Carregando dados da temporada..."
):
    partidas = carregar_partidas()


# ==========================================================
# CÁLCULOS
# ==========================================================

total_jogos = len(partidas)

vitorias = (
    partidas["resultado"] == "Vitória"
).sum()

empates = (
    partidas["resultado"] == "Empate"
).sum()

derrotas = (
    partidas["resultado"] == "Derrota"
).sum()

gols_marcados = (
    partidas["gols_real"]
    .sum()
)

gols_sofridos = (
    partidas["gols_adversario"]
    .sum()
)

saldo_gols = (
    gols_marcados
    - gols_sofridos
)

media_gols = (
    gols_marcados
    / total_jogos
    if total_jogos > 0
    else 0
)

aproveitamento = (
    (
        vitorias * 3
        + empates
    )
    /
    (
        total_jogos * 3
    )
    * 100
    if total_jogos > 0
    else 0
)


# ==========================================================
# MÉTRICAS
# ==========================================================

st.markdown(
    '<div class="section-label">Resumo da temporada</div>',
    unsafe_allow_html=True
)

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.metric(
        "📅 Jogos",
        total_jogos
    )

with m2:

    st.metric(
        "✅ Vitórias",
        int(vitorias)
    )

with m3:

    st.metric(
        "⚽ Gols marcados",
        int(gols_marcados)
    )

with m4:

    st.metric(
        "📊 Média de gols/jogo",
        f"{media_gols:.2f}"
    )


m5, m6, m7, m8 = st.columns(4)

with m5:

    st.metric(
        "🤝 Empates",
        int(empates)
    )

with m6:

    st.metric(
        "❌ Derrotas",
        int(derrotas)
    )

with m7:

    st.metric(
        "🥅 Gols sofridos",
        int(gols_sofridos)
    )

with m8:

    st.metric(
        "📈 Aproveitamento",
        f"{aproveitamento:.1f}%"
    )


# ==========================================================
# STREAMLIT EXTRAS
# ==========================================================

style_metric_cards(
    background_color="#111827",
    border_left_color="#60A5FA",
    border_color="#1F2937",
    border_size_px=1,
    border_radius_px=12,
    box_shadow=True
)


# ==========================================================
# RESULTADOS
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Resultados</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Distribuição dos resultados"
)


dados_resultados = pd.DataFrame(
    {
        "Resultado": [
            "Vitórias",
            "Empates",
            "Derrotas"
        ],

        "Quantidade": [
            int(vitorias),
            int(empates),
            int(derrotas)
        ]
    }
)


fig_resultados = px.pie(
    dados_resultados,
    names="Resultado",
    values="Quantidade",
    hole=0.45,
    title="Resultados na La Liga 2015/2016"
)


fig_resultados.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)


st.plotly_chart(
    fig_resultados,
    use_container_width=True
)


# ==========================================================
# GOLS POR PARTIDA
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Produção ofensiva</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Gols marcados por partida"
)


dados_gols = partidas.copy()

dados_gols["jogo"] = (
    dados_gols.index
    + 1
)


fig_gols = px.bar(
    dados_gols,
    x="jogo",
    y="gols_real",
    hover_data=[
        "match_date",
        "adversario",
        "local",
        "placar"
    ],
    labels={
        "jogo": "Jogo",
        "gols_real": "Gols"
    },
    title="Evolução dos gols marcados ao longo da temporada"
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
# CASA X FORA
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Mandante e visitante</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Desempenho em casa e fora"
)


desempenho_local = (
    partidas
    .groupby("local")
    .agg(
        jogos=("match_id", "count"),
        gols_marcados=("gols_real", "sum"),
        gols_sofridos=("gols_adversario", "sum")
    )
    .reset_index()
)


fig_local = px.bar(
    desempenho_local,
    x="local",
    y=[
        "gols_marcados",
        "gols_sofridos"
    ],
    barmode="group",
    labels={
        "local": "Local",
        "value": "Gols",
        "variable": "Indicador"
    },
    title="Gols marcados e sofridos em casa e fora"
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
# DESTAQUES
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Destaques</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Principais partidas"
)


maior_vitoria = (
    partidas
    .assign(
        saldo=lambda df:
        df["gols_real"]
        - df["gols_adversario"]
    )
    .sort_values(
        by="saldo",
        ascending=False
    )
    .iloc[0]
)


mais_gols = (
    partidas
    .sort_values(
        by="gols_real",
        ascending=False
    )
    .iloc[0]
)


d1, d2, d3 = st.columns(3)


with d1:

    st.metric(
        "🏆 Maior vitória",
        maior_vitoria["placar"]
    )


with d2:

    st.metric(
        "🔥 Maior número de gols",
        int(mais_gols["gols_real"]),
        mais_gols["adversario"]
    )


with d3:

    st.metric(
        "➕ Saldo de gols",
        int(saldo_gols)
    )


# ==========================================================
# TABELA DE PARTIDAS
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Partidas</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Todos os jogos"
)


filtro_resultado = st.multiselect(
    "Filtrar por resultado",
    options=[
        "Vitória",
        "Empate",
        "Derrota"
    ],
    default=[
        "Vitória",
        "Empate",
        "Derrota"
    ]
)


tabela_filtrada = partidas[
    partidas["resultado"].isin(
        filtro_resultado
    )
]


st.dataframe(
    tabela_filtrada[
        [
            "match_date",
            "local",
            "adversario",
            "gols_real",
            "gols_adversario",
            "resultado",
            "placar"
        ]
    ],
    use_container_width=True,
    hide_index=True,
    height=500
)


# ==========================================================
# RODAPÉ
# ==========================================================

st.caption(
    "Fonte: StatsBomb Open Data • "
    "La Liga 2015/2016"
)