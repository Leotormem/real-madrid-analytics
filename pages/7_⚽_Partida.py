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
    page_title="Partida | Real Madrid Analytics",
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

st.title("⚽ Análise de Partida")

st.caption(
    "Explore os principais eventos e indicadores "
    "de qualquer jogo do Real Madrid na La Liga 2015/2016."
)


# ==========================================================
# PARTIDAS
# ==========================================================

partidas = carregar_partidas()

partidas_opcoes = partidas.copy()

partidas_opcoes["descricao"] = partidas_opcoes.apply(
    lambda linha:
    f'{linha["match_date"]} • {linha["placar"]}',
    axis=1
)

lista_partidas = partidas_opcoes[
    "descricao"
].tolist()


# ==========================================================
# SESSION STATE
# ==========================================================

if "partida_selecionada" not in st.session_state:

    st.session_state[
        "partida_selecionada"
    ] = lista_partidas[0]


if (
    st.session_state["partida_selecionada"]
    not in lista_partidas
):

    st.session_state[
        "partida_selecionada"
    ] = lista_partidas[0]


indice_atual = lista_partidas.index(
    st.session_state[
        "partida_selecionada"
    ]
)


partida_selecionada = st.selectbox(
    "Selecione uma partida",
    lista_partidas,
    index=indice_atual
)


st.session_state[
    "partida_selecionada"
] = partida_selecionada


# ==========================================================
# PARTIDA SELECIONADA
# ==========================================================

linha_partida = partidas_opcoes[
    partidas_opcoes["descricao"]
    == partida_selecionada
].iloc[0]


match_id = linha_partida["match_id"]


# ==========================================================
# EVENTOS
# ==========================================================

with st.spinner(
    "Carregando eventos da partida..."
):

    eventos = carregar_eventos(
        match_id
    )


eventos_real = eventos[
    eventos["team"] == "Real Madrid"
].copy()


adversario = linha_partida[
    "adversario"
]


eventos_adversario = eventos[
    eventos["team"] == adversario
].copy()


# ==========================================================
# DADOS DO REAL MADRID
# ==========================================================

passes = eventos_real[
    eventos_real["type"] == "Pass"
].copy()


chutes = eventos_real[
    eventos_real["type"] == "Shot"
].copy()


if "shot_outcome" in chutes.columns:

    gols = chutes[
        chutes["shot_outcome"] == "Goal"
    ].copy()

else:

    gols = pd.DataFrame()


if "pass_outcome" in passes.columns:

    passes_completos = passes[
        passes["pass_outcome"].isna()
    ].copy()

else:

    passes_completos = passes.copy()


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


taxa_conversao = (
    total_gols
    / total_chutes
    * 100
    if total_chutes > 0
    else 0
)


# ==========================================================
# CABEÇALHO
# ==========================================================

st.markdown(
    '<div class="section-label">Partida selecionada</div>',
    unsafe_allow_html=True
)

st.subheader(
    linha_partida["placar"]
)

st.write(
    f'**Data:** {linha_partida["match_date"]}  '
    f'• **Local:** {linha_partida["local"]}  '
    f'• **Resultado:** {linha_partida["resultado"]}'
)


# ==========================================================
# TABS
# ==========================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Resumo",
        "⏱️ Timeline",
        "📋 Eventos",
        "🧩 Dados técnicos"
    ]
)


# ==========================================================
# TAB 1 - RESUMO
# ==========================================================

with tab1:

    st.subheader(
        "Indicadores do Real Madrid"
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "⚽ Gols",
            total_gols
        )

    with m2:

        st.metric(
            "🎯 Chutes",
            total_chutes
        )

    with m3:

        st.metric(
            "🔄 Passes",
            total_passes
        )

    with m4:

        st.metric(
            "✅ Passes completos",
            total_passes_completos
        )


    m5, m6, m7, m8 = st.columns(4)

    with m5:

        st.metric(
            "🎯 Precisão de passes",
            f"{precisao_passes:.1f}%"
        )

    with m6:

        st.metric(
            "📈 Conversão",
            f"{taxa_conversao:.1f}%"
        )

    with m7:

        st.metric(
            "👤 Jogadores",
            eventos_real[
                "player"
            ]
            .dropna()
            .nunique()
        )

    with m8:

        st.metric(
            "📋 Eventos",
            len(eventos_real)
        )


    st.divider()

    st.subheader(
        "Real Madrid x adversário"
    )


    def resumo_time(df_eventos):

        passes_time = df_eventos[
            df_eventos["type"] == "Pass"
        ]

        chutes_time = df_eventos[
            df_eventos["type"] == "Shot"
        ]

        if "shot_outcome" in chutes_time.columns:

            gols_time = (
                chutes_time[
                    "shot_outcome"
                ]
                == "Goal"
            ).sum()

        else:

            gols_time = 0

        return {
            "Passes": len(passes_time),
            "Chutes": len(chutes_time),
            "Gols": int(gols_time)
        }


    resumo_real = resumo_time(
        eventos_real
    )

    resumo_adv = resumo_time(
        eventos_adversario
    )


    comparacao = pd.DataFrame(
        {
            "Métrica": [
                "Passes",
                "Chutes",
                "Gols"
            ],

            "Real Madrid": [
                resumo_real["Passes"],
                resumo_real["Chutes"],
                resumo_real["Gols"]
            ],

            adversario: [
                resumo_adv["Passes"],
                resumo_adv["Chutes"],
                resumo_adv["Gols"]
            ]
        }
    )


    fig_comparacao = px.bar(
        comparacao,
        x="Métrica",
        y=[
            "Real Madrid",
            adversario
        ],
        barmode="group",
        title=(
            "Comparação dos principais indicadores"
        ),
        labels={
            "value": "Quantidade",
            "variable": "Equipe"
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


    st.subheader(
        "Gols do Real Madrid"
    )


    if gols.empty:

        st.info(
            "O Real Madrid não marcou nesta partida."
        )

    else:

        colunas_gols = [
            coluna
            for coluna in [
                "minute",
                "second",
                "player",
                "shot_body_part",
                "shot_statsbomb_xg"
            ]
            if coluna in gols.columns
        ]

        st.dataframe(
            gols[
                colunas_gols
            ],
            use_container_width=True,
            hide_index=True
        )


# ==========================================================
# TAB 2 - TIMELINE
# ==========================================================

with tab2:

    st.subheader(
        "Linha do tempo ofensiva"
    )


    eventos_ofensivos = eventos[
        eventos["type"].isin(
            [
                "Shot",
                "Dribble"
            ]
        )
    ].copy()


    if not eventos_ofensivos.empty:

        fig_timeline = px.scatter(
            eventos_ofensivos,
            x="minute",
            y="team",
            color="type",
            hover_name="player",
            hover_data=[
                "second"
            ],
            title=(
                "Chutes e dribles ao longo da partida"
            ),
            labels={
                "minute": "Minuto",
                "team": "Equipe",
                "type": "Evento"
            }
        )


        fig_timeline.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )


        st.plotly_chart(
            fig_timeline,
            use_container_width=True
        )


    st.subheader(
        "Eventos mais frequentes"
    )


    tipos_eventos = (
        eventos_real[
            "type"
        ]
        .value_counts()
        .head(15)
        .reset_index()
    )


    tipos_eventos.columns = [
        "Evento",
        "Quantidade"
    ]


    fig_eventos = px.bar(
        tipos_eventos,
        x="Evento",
        y="Quantidade",
        title=(
            "Eventos mais frequentes do Real Madrid"
        )
    )


    fig_eventos.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )


    st.plotly_chart(
        fig_eventos,
        use_container_width=True
    )


# ==========================================================
# TAB 3 - EVENTOS
# ==========================================================

with tab3:

    st.subheader(
        "Eventos do Real Madrid"
    )


    tipos_disponiveis = sorted(
        eventos_real[
            "type"
        ]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


    filtro_tipo = st.multiselect(
        "Tipos de evento",
        tipos_disponiveis,
        default=[
            tipo
            for tipo in [
                "Pass",
                "Shot"
            ]
            if tipo in tipos_disponiveis
        ]
    )


    if filtro_tipo:

        eventos_filtrados = eventos_real[
            eventos_real[
                "type"
            ].isin(
                filtro_tipo
            )
        ].copy()

    else:

        eventos_filtrados = (
            eventos_real.copy()
        )


    colunas_eventos = [
        coluna
        for coluna in [
            "minute",
            "second",
            "player",
            "position",
            "type",
            "location"
        ]
        if coluna in eventos_filtrados.columns
    ]


    st.dataframe(
        eventos_filtrados[
            colunas_eventos
        ],
        use_container_width=True,
        hide_index=True,
        height=550
    )


# ==========================================================
# TAB 4 - DADOS TÉCNICOS
# ==========================================================

with tab4:

    st.subheader(
        "Session State"
    )

    st.write(
        """
        Nesta página o **Session State** é utilizado para
        preservar a partida selecionada durante a sessão
        do usuário.
        """
    )


    st.code(
        """
if "partida_selecionada" not in st.session_state:
    st.session_state["partida_selecionada"] = lista_partidas[0]

st.session_state["partida_selecionada"] = partida_selecionada
""",
        language="python"
    )


    st.write(
        "Valor atualmente armazenado:"
    )

    st.json(
        {
            "partida_selecionada":
            st.session_state[
                "partida_selecionada"
            ],

            "match_id":
            int(match_id)
        }
    )


    st.divider()

    st.subheader(
        "Exemplo de evento em JSON"
    )


    if not eventos_real.empty:

        exemplo = (
            eventos_real
            .iloc[0]
            .dropna()
            .to_dict()
        )


        exemplo_convertido = {}


        for chave, valor in exemplo.items():

            if hasattr(
                valor,
                "item"
            ):

                valor = valor.item()

            elif isinstance(
                valor,
                pd.Timestamp
            ):

                valor = str(
                    valor
                )

            elif isinstance(
                valor,
                tuple
            ):

                valor = list(
                    valor
                )


            exemplo_convertido[
                str(chave)
            ] = valor


        st.json(
            exemplo_convertido
        )


# ==========================================================
# RODAPÉ
# ==========================================================

st.caption(
    "Fonte: StatsBomb Open Data • "
    "Análise interativa da partida"
)