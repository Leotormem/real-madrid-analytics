import pandas as pd
import streamlit as st

from utils.dados import (
    carregar_partidas,
    carregar_eventos
)


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Eventos | Real Madrid Analytics",
    page_icon="📋",
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
    "📋 Eventos da Partida"
)

st.caption(
    "Explore e filtre os eventos detalhados das partidas "
    "do Real Madrid na La Liga 2015/2016."
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
    partidas_opcoes["descricao"].tolist()
)


linha_partida = partidas_opcoes[
    partidas_opcoes["descricao"]
    == partida_selecionada
].iloc[0]


match_id = linha_partida["match_id"]


# ==========================================================
# CARREGAMENTO
# ==========================================================

with st.spinner(
    "Carregando eventos..."
):

    eventos = carregar_eventos(
        match_id
    )


# ==========================================================
# CONTEXTO
# ==========================================================

st.markdown(
    '<div class="section-label">Partida</div>',
    unsafe_allow_html=True
)

st.subheader(
    linha_partida["placar"]
)

st.write(
    f'**Data:** {linha_partida["match_date"]}  '
    f'• **Resultado:** {linha_partida["resultado"]}'
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
    "Filtrar eventos"
)


times = sorted(
    eventos[
        "team"
    ]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


tipos_eventos = sorted(
    eventos[
        "type"
    ]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


jogadores = sorted(
    eventos[
        "player"
    ]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)


filtro1, filtro2 = st.columns(2)


with filtro1:

    time_selecionado = st.selectbox(
        "Equipe",
        [
            "Todas"
        ] + times
    )


with filtro2:

    jogador_selecionado = st.selectbox(
        "Jogador",
        [
            "Todos"
        ] + jogadores
    )


tipos_selecionados = st.multiselect(
    "Tipos de evento",
    options=tipos_eventos,
    default=[
        tipo
        for tipo in [
            "Pass",
            "Shot",
            "Dribble",
            "Pressure"
        ]
        if tipo in tipos_eventos
    ]
)


intervalo = st.slider(
    "Intervalo de minutos",
    min_value=0,
    max_value=120,
    value=(0, 90)
)


quantidade = st.radio(
    "Quantidade de registros",
    [
        "Todos",
        "25",
        "50",
        "100"
    ],
    horizontal=True
)


mostrar_colunas_avancadas = st.checkbox(
    "Mostrar colunas avançadas",
    value=False
)


# ==========================================================
# APLICA FILTROS
# ==========================================================

eventos_filtrados = eventos.copy()


if time_selecionado != "Todas":

    eventos_filtrados = eventos_filtrados[
        eventos_filtrados[
            "team"
        ] == time_selecionado
    ].copy()


if jogador_selecionado != "Todos":

    eventos_filtrados = eventos_filtrados[
        eventos_filtrados[
            "player"
        ] == jogador_selecionado
    ].copy()


if tipos_selecionados:

    eventos_filtrados = eventos_filtrados[
        eventos_filtrados[
            "type"
        ].isin(
            tipos_selecionados
        )
    ].copy()


eventos_filtrados = eventos_filtrados[
    eventos_filtrados[
        "minute"
    ].between(
        intervalo[0],
        intervalo[1]
    )
].copy()


if quantidade != "Todos":

    eventos_filtrados = eventos_filtrados.head(
        int(quantidade)
    )


# ==========================================================
# MÉTRICAS
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Resumo da seleção</div>',
    unsafe_allow_html=True
)


total_eventos = len(
    eventos_filtrados
)


tipos_diferentes = (
    eventos_filtrados[
        "type"
    ]
    .nunique()
)


jogadores_diferentes = (
    eventos_filtrados[
        "player"
    ]
    .dropna()
    .nunique()
)


times_diferentes = (
    eventos_filtrados[
        "team"
    ]
    .nunique()
)


m1, m2, m3, m4 = st.columns(4)


with m1:

    st.metric(
        "📋 Eventos",
        total_eventos
    )


with m2:

    st.metric(
        "🔹 Tipos de evento",
        tipos_diferentes
    )


with m3:

    st.metric(
        "👤 Jogadores",
        jogadores_diferentes
    )


with m4:

    st.metric(
        "⚽ Equipes",
        times_diferentes
    )


# ==========================================================
# TABELA RESUMIDA
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Resumo</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Quantidade por tipo de evento"
)


resumo_eventos = (
    eventos_filtrados[
        "type"
    ]
    .value_counts()
    .reset_index()
)

resumo_eventos.columns = [
    "Evento",
    "Quantidade"
]


st.table(
    resumo_eventos.head(10)
)


# ==========================================================
# DATAFRAME PRINCIPAL
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Base de eventos</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Eventos filtrados"
)


colunas_basicas = [
    coluna
    for coluna in [
        "minute",
        "second",
        "team",
        "player",
        "position",
        "type",
        "location"
    ]
    if coluna in eventos_filtrados.columns
]


colunas_avancadas = [
    coluna
    for coluna in [
        "pass_recipient",
        "pass_length",
        "pass_angle",
        "pass_outcome",
        "shot_outcome",
        "shot_statsbomb_xg",
        "shot_body_part",
        "under_pressure",
        "counterpress"
    ]
    if coluna in eventos_filtrados.columns
]


if mostrar_colunas_avancadas:

    colunas_exibidas = (
        colunas_basicas
        + colunas_avancadas
    )

else:

    colunas_exibidas = (
        colunas_basicas
    )


st.dataframe(
    eventos_filtrados[
        colunas_exibidas
    ],
    use_container_width=True,
    hide_index=True,
    height=520
)


# ==========================================================
# DOWNLOAD CSV
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Exportação</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Baixar dados filtrados"
)


csv = eventos_filtrados.to_csv(
    index=False
).encode(
    "utf-8"
)


st.download_button(
    label="📥 Baixar eventos em CSV",
    data=csv,
    file_name=(
        f"eventos_real_madrid_"
        f"{match_id}.csv"
    ),
    mime="text/csv",
    use_container_width=True
)


# ==========================================================
# INFO
# ==========================================================

st.info(
    """
    Os dados baixados correspondem exatamente aos filtros
    aplicados nesta página.
    """
)


# ==========================================================
# RODAPÉ
# ==========================================================

st.caption(
    "Fonte: StatsBomb Open Data • "
    "Eventos filtráveis e exportáveis em CSV"
)