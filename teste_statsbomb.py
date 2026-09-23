from statsbombpy import sb


competition_id = 11
season_id = 27
time_escolhido = "Real Madrid"

partidas = sb.matches(
    competition_id=competition_id,
    season_id=season_id
)

jogos_real = partidas[
    (partidas["home_team"] == time_escolhido)
    |
    (partidas["away_team"] == time_escolhido)
].copy()

jogos_real = jogos_real[
    [
        "match_id",
        "match_date",
        "home_team",
        "away_team",
        "home_score",
        "away_score"
    ]
].sort_values(
    by="match_date"
)

print("\n==============================")
print("JOGOS DO REAL MADRID")
print("==============================\n")

print(
    jogos_real.to_string(
        index=False
    )
)

print("\nQuantidade de jogos:")
print(len(jogos_real))


print("\n==============================")
print("TESTANDO EVENTOS DISPONÍVEIS")
print("==============================\n")

jogos_com_eventos = []

for _, jogo in jogos_real.iterrows():

    match_id = jogo["match_id"]

    try:

        eventos = sb.events(
            match_id=match_id
        )

        quantidade_eventos = len(eventos)

        jogos_com_eventos.append(
            {
                "match_id": match_id,
                "data": jogo["match_date"],
                "mandante": jogo["home_team"],
                "visitante": jogo["away_team"],
                "placar": (
                    f'{jogo["home_score"]} x '
                    f'{jogo["away_score"]}'
                ),
                "eventos": quantidade_eventos
            }
        )

        print(
            f"OK - {match_id} - "
            f'{jogo["home_team"]} '
            f'{jogo["home_score"]} x '
            f'{jogo["away_score"]} '
            f'{jogo["away_team"]} - '
            f"{quantidade_eventos} eventos"
        )

    except Exception as erro:

        print(
            f"SEM EVENTOS - {match_id} - "
            f"{erro}"
        )


print("\n==============================")
print("RESUMO")
print("==============================\n")

print(
    f"Jogos do Real Madrid: "
    f"{len(jogos_real)}"
)

print(
    f"Jogos com eventos disponíveis: "
    f"{len(jogos_com_eventos)}"
)
