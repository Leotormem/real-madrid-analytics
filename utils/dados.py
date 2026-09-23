import pandas as pd
import streamlit as st
from statsbombpy import sb


COMPETITION_ID = 11
SEASON_ID = 27
TEAM_NAME = "Real Madrid"


@st.cache_data(show_spinner=False)
def carregar_competicoes():
    return sb.competitions()


@st.cache_data(show_spinner=False)
def carregar_partidas():
    partidas = sb.matches(
        competition_id=COMPETITION_ID,
        season_id=SEASON_ID
    )

    jogos_real = partidas[
        (partidas["home_team"] == TEAM_NAME)
        |
        (partidas["away_team"] == TEAM_NAME)
    ].copy()

    jogos_real = jogos_real.sort_values(
        by="match_date"
    ).reset_index(drop=True)

    jogos_real["adversario"] = jogos_real.apply(
        lambda linha:
        linha["away_team"]
        if linha["home_team"] == TEAM_NAME
        else linha["home_team"],
        axis=1
    )

    jogos_real["local"] = jogos_real["home_team"].apply(
        lambda time:
        "Casa"
        if time == TEAM_NAME
        else "Fora"
    )

    jogos_real["gols_real"] = jogos_real.apply(
        lambda linha:
        linha["home_score"]
        if linha["home_team"] == TEAM_NAME
        else linha["away_score"],
        axis=1
    )

    jogos_real["gols_adversario"] = jogos_real.apply(
        lambda linha:
        linha["away_score"]
        if linha["home_team"] == TEAM_NAME
        else linha["home_score"],
        axis=1
    )

    jogos_real["resultado"] = jogos_real.apply(
        classificar_resultado,
        axis=1
    )

    jogos_real["placar"] = jogos_real.apply(
        lambda linha:
        f'{linha["home_team"]} '
        f'{linha["home_score"]} x '
        f'{linha["away_score"]} '
        f'{linha["away_team"]}',
        axis=1
    )

    return jogos_real


def classificar_resultado(linha):
    if linha["gols_real"] > linha["gols_adversario"]:
        return "Vitória"

    if linha["gols_real"] < linha["gols_adversario"]:
        return "Derrota"

    return "Empate"


@st.cache_data(show_spinner=False)
def carregar_eventos(match_id):
    return sb.events(
        match_id=int(match_id)
    )


@st.cache_data(show_spinner=False)
def carregar_eventos_real(match_id):
    eventos = carregar_eventos(match_id)

    return eventos[
        eventos["team"] == TEAM_NAME
    ].copy()


@st.cache_data(show_spinner=False)
def carregar_passes(match_id, somente_real=True):
    eventos = carregar_eventos(match_id)

    passes = eventos[
        eventos["type"] == "Pass"
    ].copy()

    if somente_real:
        passes = passes[
            passes["team"] == TEAM_NAME
        ].copy()

    return passes


@st.cache_data(show_spinner=False)
def carregar_chutes(match_id, somente_real=True):
    eventos = carregar_eventos(match_id)

    chutes = eventos[
        eventos["type"] == "Shot"
    ].copy()

    if somente_real:
        chutes = chutes[
            chutes["team"] == TEAM_NAME
        ].copy()

    return chutes


@st.cache_data(show_spinner=False)
def carregar_jogadores_partida(match_id):
    eventos = carregar_eventos_real(match_id)

    jogadores = (
        eventos["player"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    return sorted(jogadores)


def resumo_partida(match_id):
    eventos = carregar_eventos(match_id)

    eventos_real = eventos[
        eventos["team"] == TEAM_NAME
    ]

    passes = eventos_real[
        eventos_real["type"] == "Pass"
    ]

    chutes = eventos_real[
        eventos_real["type"] == "Shot"
    ]

    gols = chutes[
        chutes["shot_outcome"] == "Goal"
    ] if "shot_outcome" in chutes.columns else pd.DataFrame()

    passes_completos = passes[
        passes["pass_outcome"].isna()
    ] if "pass_outcome" in passes.columns else pd.DataFrame()

    total_passes = len(passes)
    total_passes_completos = len(passes_completos)
    total_chutes = len(chutes)
    total_gols = len(gols)

    precisao_passes = (
        total_passes_completos / total_passes * 100
        if total_passes > 0
        else 0
    )

    conversao = (
        total_gols / total_chutes * 100
        if total_chutes > 0
        else 0
    )

    return {
        "passes": total_passes,
        "passes_completos": total_passes_completos,
        "precisao_passes": precisao_passes,
        "chutes": total_chutes,
        "gols": total_gols,
        "conversao": conversao
    }