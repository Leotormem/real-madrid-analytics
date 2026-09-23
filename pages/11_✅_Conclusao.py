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
    page_title="Conclusão | Real Madrid Analytics",
    page_icon="✅",
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

.answer-box {
    padding: 28px;
    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(30,64,175,0.18),
            rgba(15,23,42,0.88)
        );

    border:
        1px solid rgba(96,165,250,0.25);

    margin-top: 20px;
    margin-bottom: 25px;

    line-height: 1.7;
}

</style>
""",
    unsafe_allow_html=True
)


# ==========================================================
# BASE ANALÍTICA
# ==========================================================

@st.cache_data(show_spinner=False)
def gerar_conclusao_temporada():

    partidas = carregar_partidas()

    registros_jogos = []

    registros_jogadores = []


    for _, partida in partidas.iterrows():

        eventos = carregar_eventos(
            partida["match_id"]
        )

        eventos_real = eventos[
            eventos["team"] == "Real Madrid"
        ].copy()


        # --------------------------------------------------
        # PASSES
        # --------------------------------------------------

        passes = eventos_real[
            eventos_real["type"] == "Pass"
        ].copy()


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


        # --------------------------------------------------
        # CHUTES
        # --------------------------------------------------

        chutes = eventos_real[
            eventos_real["type"] == "Shot"
        ].copy()


        # --------------------------------------------------
        # REGISTRO DO JOGO
        # --------------------------------------------------

        registros_jogos.append(
            {
                "match_id": partida["match_id"],
                "data": partida["match_date"],
                "adversario": partida["adversario"],
                "gols": partida["gols_real"],
                "chutes": len(chutes),
                "passes": len(passes),
                "passes_completos": int(
                    passes_completos
                ),
                "resultado": partida["resultado"]
            }
        )


        # --------------------------------------------------
        # DADOS INDIVIDUAIS
        # --------------------------------------------------

        jogadores = (
            eventos_real[
                "player"
            ]
            .dropna()
            .astype(str)
            .unique()
        )


        for jogador in jogadores:

            eventos_jogador = eventos_real[
                eventos_real["player"]
                == jogador
            ]


            passes_jogador = eventos_jogador[
                eventos_jogador["type"]
                == "Pass"
            ]


            chutes_jogador = eventos_jogador[
                eventos_jogador["type"]
                == "Shot"
            ]


            if (
                "shot_outcome"
                in chutes_jogador.columns
            ):

                gols_jogador = (
                    chutes_jogador[
                        "shot_outcome"
                    ]
                    == "Goal"
                ).sum()

            else:

                gols_jogador = 0


            registros_jogadores.append(
                {
                    "Jogador": jogador,
                    "Passes": len(
                        passes_jogador
                    ),
                    "Chutes": len(
                        chutes_jogador
                    ),
                    "Gols": int(
                        gols_jogador
                    )
                }
            )


    jogos = pd.DataFrame(
        registros_jogos
    )


    jogadores = pd.DataFrame(
        registros_jogadores
    )


    resumo_jogadores = (
        jogadores
        .groupby(
            "Jogador",
            as_index=False
        )
        .agg(
            {
                "Passes": "sum",
                "Chutes": "sum",
                "Gols": "sum"
            }
        )
    )


    return jogos, resumo_jogadores


# ==========================================================
# TÍTULO
# ==========================================================

st.title(
    "✅ Conclusão da Análise"
)

st.caption(
    "Síntese dos principais resultados obtidos "
    "durante a análise da La Liga 2015/2016."
)


# ==========================================================
# PERGUNTA CENTRAL
# ==========================================================

st.markdown(
    '<div class="section-label">Pergunta central</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Como evoluiu o desempenho ofensivo do Real Madrid?"
)

st.info(
    """
    **Como evoluiu o desempenho ofensivo do Real Madrid
    ao longo da La Liga 2015/2016, considerando passes,
    chutes, gols e contribuição individual dos jogadores?**
    """
)


# ==========================================================
# CARREGAMENTO
# ==========================================================

with st.spinner(
    "Consolidando os dados dos 38 jogos..."
):

    jogos, jogadores = (
        gerar_conclusao_temporada()
    )


# ==========================================================
# MÉTRICAS GERAIS
# ==========================================================

total_jogos = len(
    jogos
)

total_gols = int(
    jogos["gols"].sum()
)

total_chutes = int(
    jogos["chutes"].sum()
)

total_passes = int(
    jogos["passes"].sum()
)

total_passes_completos = int(
    jogos[
        "passes_completos"
    ].sum()
)


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


st.divider()

st.markdown(
    '<div class="section-label">Temporada completa</div>',
    unsafe_allow_html=True
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
        "✅ Precisão dos passes",
        f"{precisao_passes:.1f}%"
    )


# ==========================================================
# PRIMEIRA X SEGUNDA METADE
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Evolução</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Primeira metade x segunda metade da temporada"
)


primeira_metade = jogos.iloc[
    :19
]

segunda_metade = jogos.iloc[
    19:
]


gols_primeira = int(
    primeira_metade[
        "gols"
    ].sum()
)

gols_segunda = int(
    segunda_metade[
        "gols"
    ].sum()
)


chutes_primeira = (
    primeira_metade[
        "chutes"
    ].mean()
)

chutes_segunda = (
    segunda_metade[
        "chutes"
    ].mean()
)


passes_primeira = (
    primeira_metade[
        "passes"
    ].mean()
)

passes_segunda = (
    segunda_metade[
        "passes"
    ].mean()
)


c1, c2, c3 = st.columns(3)


with c1:

    st.metric(
        "⚽ Gols",
        gols_segunda,
        (
            gols_segunda
            - gols_primeira
        )
    )

    st.caption(
        f"1ª metade: {gols_primeira}"
    )


with c2:

    st.metric(
        "🎯 Chutes por jogo",
        f"{chutes_segunda:.1f}",
        f"{chutes_segunda - chutes_primeira:.1f}"
    )

    st.caption(
        f"1ª metade: {chutes_primeira:.1f}"
    )


with c3:

    st.metric(
        "🔄 Passes por jogo",
        f"{passes_segunda:.1f}",
        f"{passes_segunda - passes_primeira:.1f}"
    )

    st.caption(
        f"1ª metade: {passes_primeira:.1f}"
    )


# ==========================================================
# JOGADORES
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Contribuição individual</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Principais destaques individuais"
)


artilheiro = (
    jogadores
    .sort_values(
        "Gols",
        ascending=False
    )
    .iloc[0]
)


mais_chutes = (
    jogadores
    .sort_values(
        "Chutes",
        ascending=False
    )
    .iloc[0]
)


mais_passes = (
    jogadores
    .sort_values(
        "Passes",
        ascending=False
    )
    .iloc[0]
)


j1, j2, j3 = st.columns(3)


with j1:

    st.metric(
        "⚽ Mais gols",
        artilheiro[
            "Jogador"
        ],
        f'{int(artilheiro["Gols"])} gols'
    )


with j2:

    st.metric(
        "🎯 Mais chutes",
        mais_chutes[
            "Jogador"
        ],
        f'{int(mais_chutes["Chutes"])} chutes'
    )


with j3:

    st.metric(
        "🔄 Mais passes",
        mais_passes[
            "Jogador"
        ],
        f'{int(mais_passes["Passes"])} passes'
    )


# ==========================================================
# INTERPRETAÇÃO AUTOMÁTICA
# ==========================================================

def comparar(
    valor_inicial,
    valor_final
):

    if valor_final > valor_inicial:

        return "aumentou"

    if valor_final < valor_inicial:

        return "diminuiu"

    return "permaneceu estável"


tendencia_gols = comparar(
    gols_primeira,
    gols_segunda
)

tendencia_chutes = comparar(
    chutes_primeira,
    chutes_segunda
)

tendencia_passes = comparar(
    passes_primeira,
    passes_segunda
)


# ==========================================================
# RESPOSTA FINAL
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Resposta à pergunta central</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Síntese dos resultados"
)


resposta_html = f"""
<div class="answer-box">

A análise dos <strong>{total_jogos} jogos</strong> mostra que
o Real Madrid encerrou a La Liga 2015/2016 com
<strong>{total_gols} gols marcados</strong>.

Ao comparar as duas metades da competição, a quantidade
de gols <strong>{tendencia_gols}</strong>, passando de
<strong>{gols_primeira}</strong> gols nos primeiros 19 jogos
para <strong>{gols_segunda}</strong> nos últimos 19.

O volume médio de finalizações
<strong>{tendencia_chutes}</strong>, saindo de
<strong>{chutes_primeira:.1f}</strong> para
<strong>{chutes_segunda:.1f} chutes por partida</strong>.

O volume de passes também
<strong>{tendencia_passes}</strong>, passando de
<strong>{passes_primeira:.1f}</strong> para
<strong>{passes_segunda:.1f} passes por jogo</strong>.

Durante toda a temporada, o time realizou
<strong>{total_chutes} finalizações</strong> e
<strong>{total_passes} passes</strong>, com precisão de
<strong>{precisao_passes:.1f}%</strong>.

Individualmente,
<strong>{artilheiro["Jogador"]}</strong> liderou a equipe
em gols, com <strong>{int(artilheiro["Gols"])}</strong>,
enquanto <strong>{mais_passes["Jogador"]}</strong>
registrou o maior volume de passes.

Assim, os dados mostram que o desempenho ofensivo não deve
ser analisado apenas pelo número final de gols. A combinação
entre volume de finalizações, circulação da bola, eficiência
e participação individual permite observar como a produção
ofensiva se comportou durante diferentes momentos da
temporada.

</div>
"""


st.markdown(
    resposta_html,
    unsafe_allow_html=True
)


# ==========================================================
# CONCLUSÃO ACADÊMICA
# ==========================================================

st.success(
    """
    **Conclusão:** a utilização dos dados de eventos da
    StatsBomb permitiu transformar as 38 partidas em
    indicadores mensuráveis e comparar diferentes dimensões
    do desempenho ofensivo do Real Madrid ao longo da
    temporada.
    """
)


# ==========================================================
# TABELA DE APOIO
# ==========================================================

with st.expander(
    "📊 Ver dados utilizados na comparação"
):

    comparacao = pd.DataFrame(
        {
            "Período": [
                "Primeiros 19 jogos",
                "Últimos 19 jogos"
            ],

            "Gols": [
                gols_primeira,
                gols_segunda
            ],

            "Chutes por jogo": [
                chutes_primeira,
                chutes_segunda
            ],

            "Passes por jogo": [
                passes_primeira,
                passes_segunda
            ]
        }
    )


    st.dataframe(
        comparacao,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# RODAPÉ
# ==========================================================

st.caption(
    "Fonte: StatsBomb Open Data • "
    "Real Madrid • La Liga 2015/2016"
)