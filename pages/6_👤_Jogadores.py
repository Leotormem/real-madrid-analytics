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
    page_title="Jogadores | Real Madrid Analytics",
    page_icon="👤",
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
# CARREGA EVENTOS DA TEMPORADA
# ==========================================================

@st.cache_data(show_spinner=False)
def carregar_eventos_temporada():

    partidas = carregar_partidas()

    lista_eventos = []

    for _, partida in partidas.iterrows():

        eventos = carregar_eventos(
            partida["match_id"]
        )

        eventos_real = eventos[
            eventos["team"] == "Real Madrid"
        ].copy()

        eventos_real["match_id_ref"] = (
            partida["match_id"]
        )

        eventos_real["adversario_ref"] = (
            partida["adversario"]
        )

        eventos_real["data_ref"] = (
            partida["match_date"]
        )

        lista_eventos.append(
            eventos_real
        )

    return pd.concat(
        lista_eventos,
        ignore_index=True
    )


# ==========================================================
# RESUMO POR JOGADOR
# ==========================================================

@st.cache_data(show_spinner=False)
def gerar_resumo_jogadores():

    eventos = carregar_eventos_temporada()

    jogadores = (
        eventos["player"]
        .dropna()
        .astype(str)
        .unique()
    )

    registros = []

    for jogador in jogadores:

        eventos_jogador = eventos[
            eventos["player"] == jogador
        ]

        # ------------------------------------------
        # PASSES
        # ------------------------------------------

        passes = eventos_jogador[
            eventos_jogador["type"] == "Pass"
        ]

        total_passes = len(
            passes
        )

        if "pass_outcome" in passes.columns:

            passes_completos = (
                passes[
                    "pass_outcome"
                ]
                .isna()
                .sum()
            )

        else:

            passes_completos = (
                total_passes
            )

        precisao_passes = (
            passes_completos
            / total_passes
            * 100
            if total_passes > 0
            else 0
        )

        # ------------------------------------------
        # CHUTES
        # ------------------------------------------

        chutes = eventos_jogador[
            eventos_jogador["type"] == "Shot"
        ]

        total_chutes = len(
            chutes
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

        # ------------------------------------------
        # XG
        # ------------------------------------------

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

        # ------------------------------------------
        # OUTROS EVENTOS
        # ------------------------------------------

        conducoes = (
            eventos_jogador["type"]
            == "Carry"
        ).sum()

        dribles = (
            eventos_jogador["type"]
            == "Dribble"
        ).sum()

        pressoes = (
            eventos_jogador["type"]
            == "Pressure"
        ).sum()

        recuperacoes = (
            eventos_jogador["type"]
            == "Ball Recovery"
        ).sum()

        # ------------------------------------------
        # PARTIDAS COM EVENTOS
        # ------------------------------------------

        partidas = (
            eventos_jogador[
                "match_id_ref"
            ]
            .nunique()
        )

        registros.append(
            {
                "Jogador": jogador,
                "Partidas": partidas,
                "Passes": total_passes,
                "Passes completos": int(
                    passes_completos
                ),
                "Precisão passes (%)": precisao_passes,
                "Chutes": total_chutes,
                "Gols": int(gols),
                "xG": xg,
                "Conduções": int(conducoes),
                "Dribles": int(dribles),
                "Pressões": int(pressoes),
                "Recuperações": int(
                    recuperacoes
                )
            }
        )

    resumo = pd.DataFrame(
        registros
    )

    resumo = resumo.sort_values(
        by="Gols",
        ascending=False
    ).reset_index(
        drop=True
    )

    return resumo


# ==========================================================
# TÍTULO
# ==========================================================

st.title(
    "👤 Desempenho dos Jogadores"
)

st.caption(
    "Compare a contribuição individual dos jogadores "
    "do Real Madrid durante a La Liga 2015/2016."
)


# ==========================================================
# CARREGAMENTO
# ==========================================================

with st.spinner(
    "Processando eventos dos jogadores..."
):

    resumo = gerar_resumo_jogadores()


# ==========================================================
# DESTAQUES
# ==========================================================

st.markdown(
    '<div class="section-label">Destaques da temporada</div>',
    unsafe_allow_html=True
)


artilheiro = (
    resumo
    .sort_values(
        "Gols",
        ascending=False
    )
    .iloc[0]
)

mais_chutes = (
    resumo
    .sort_values(
        "Chutes",
        ascending=False
    )
    .iloc[0]
)

mais_passes = (
    resumo
    .sort_values(
        "Passes",
        ascending=False
    )
    .iloc[0]
)

maior_xg = (
    resumo
    .sort_values(
        "xG",
        ascending=False
    )
    .iloc[0]
)


m1, m2, m3, m4 = st.columns(4)


with m1:

    st.metric(
        "⚽ Artilheiro",
        artilheiro["Jogador"],
        f'{int(artilheiro["Gols"])} gols'
    )


with m2:

    st.metric(
        "🎯 Mais finalizações",
        mais_chutes["Jogador"],
        f'{int(mais_chutes["Chutes"])} chutes'
    )


with m3:

    st.metric(
        "🔄 Mais passes",
        mais_passes["Jogador"],
        f'{int(mais_passes["Passes"])} passes'
    )


with m4:

    st.metric(
        "📊 Maior xG",
        maior_xg["Jogador"],
        f'{maior_xg["xG"]:.2f} xG'
    )


# ==========================================================
# RANKING DE GOLS
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Ranking ofensivo</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Principais artilheiros"
)


top_gols = (
    resumo
    .sort_values(
        "Gols",
        ascending=False
    )
    .head(10)
)


fig_gols = px.bar(
    top_gols,
    x="Jogador",
    y="Gols",
    hover_data=[
        "Chutes",
        "xG",
        "Partidas"
    ],
    title="Gols por jogador",
    labels={
        "Jogador": "Jogador",
        "Gols": "Gols"
    }
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
# PASSES
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Construção de jogo</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Jogadores com maior volume de passes"
)


top_passes = (
    resumo
    .sort_values(
        "Passes",
        ascending=False
    )
    .head(10)
)


fig_passes = px.bar(
    top_passes,
    x="Jogador",
    y="Passes",
    hover_data=[
        "Passes completos",
        "Precisão passes (%)",
        "Partidas"
    ],
    title="Volume de passes por jogador"
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
# FORMULÁRIO DE COMPARAÇÃO
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Comparação individual</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Comparar dois jogadores"
)

st.write(
    "Escolha dois jogadores e selecione o tipo de "
    "informação que deseja comparar."
)


lista_jogadores = (
    resumo["Jogador"]
    .sort_values()
    .tolist()
)


indice_segundo = (
    1
    if len(lista_jogadores) > 1
    else 0
)


with st.form(
    "form_comparacao"
):

    c1, c2 = st.columns(2)


    with c1:

        jogador_1 = st.selectbox(
            "Jogador 1",
            lista_jogadores,
            index=0
        )


    with c2:

        jogador_2 = st.selectbox(
            "Jogador 2",
            lista_jogadores,
            index=indice_segundo
        )


    categoria = st.radio(
        "Categoria principal",
        [
            "Ataque",
            "Passes",
            "Participação"
        ],
        horizontal=True
    )


    mostrar_detalhes = st.checkbox(
        "Mostrar tabela comparativa",
        value=True
    )


    comparar = st.form_submit_button(
        "⚖️ Comparar jogadores",
        use_container_width=True
    )


# ==========================================================
# COMPARAÇÃO
# ==========================================================

if comparar:

    dados_1 = resumo[
        resumo["Jogador"]
        == jogador_1
    ].iloc[0]

    dados_2 = resumo[
        resumo["Jogador"]
        == jogador_2
    ].iloc[0]


    if categoria == "Ataque":

        metricas = [
            "Gols",
            "Chutes",
            "xG"
        ]

    elif categoria == "Passes":

        metricas = [
            "Passes",
            "Passes completos",
            "Precisão passes (%)"
        ]

    else:

        metricas = [
            "Conduções",
            "Dribles",
            "Pressões",
            "Recuperações"
        ]


    dados_comparacao = []


    for metrica in metricas:

        dados_comparacao.append(
            {
                "Métrica": metrica,
                jogador_1: dados_1[
                    metrica
                ],
                jogador_2: dados_2[
                    metrica
                ]
            }
        )


    comparacao = pd.DataFrame(
        dados_comparacao
    )


    st.markdown(
        "### Resultado da comparação"
    )


    fig_comparacao = px.bar(
        comparacao,
        x="Métrica",
        y=[
            jogador_1,
            jogador_2
        ],
        barmode="group",
        title=(
            f"{jogador_1} x {jogador_2}"
        ),
        labels={
            "value": "Valor",
            "variable": "Jogador"
        }
    )


    fig_comparacao.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )


    st.plotly_chart(
        fig_comparacao,
        use_container_width=True
    )


    if mostrar_detalhes:

        st.dataframe(
            comparacao,
            use_container_width=True,
            hide_index=True
        )


# ==========================================================
# SCATTER - CHUTES X GOLS
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Eficiência ofensiva</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Relação entre chutes e gols"
)


fig_scatter = px.scatter(
    resumo[
        resumo["Chutes"] > 0
    ],
    x="Chutes",
    y="Gols",
    hover_name="Jogador",
    size="Partidas",
    hover_data=[
        "xG",
        "Partidas"
    ],
    title=(
        "Volume de finalizações x gols marcados"
    )
)


fig_scatter.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)


st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


# ==========================================================
# TABELA GERAL
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Dataset de jogadores</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Resumo individual da temporada"
)


st.dataframe(
    resumo,
    use_container_width=True,
    hide_index=True,
    height=520
)


# ==========================================================
# RODAPÉ
# ==========================================================

st.caption(
    "Fonte: StatsBomb Open Data • "
    "La Liga 2015/2016"
)