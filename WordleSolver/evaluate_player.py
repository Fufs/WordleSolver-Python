"""
evaluate_player.py
by Fufs

Evaluates the effectiveness of a sub-class of WordleSolver.player.Player

This module contains:
    - evaluate_player - function used to evaluate a sub-class of WordleSolver.player.Player
"""

from . import data_types, players, wordle


def evaluate_player(
    wordlist: data_types.Wordlist,
    solution_list: list,
    player_class: players.Player,
    player_kwargs: dict,
    rounds_per_game: int = 6,
    extended: bool = True,
) -> dict:
    """
    Tests an instance of a subclass of player.Player with every word in solution_list.
    """
    total_rounds = 0
    points = 0
    wins = 0
    certainty = 0

    try:
        for solution in solution_list:
            print("Testing", solution, "(" + str(total_rounds + 1) + "/" + str(len(solution_list)) + ")",)
            round_score = wordle.play(
                wordlist,
                solution=solution,
                player=player_class(**player_kwargs),
                rounds_per_game=rounds_per_game,
                extended=extended,
                dev=True,
            )
            points += round_score["rounds"]
            if round_score["won"]: wins += 1
            certainty += 100 / round_score["potential_solutions"]

            print(round_score)
            print()
            
            total_rounds += 1

    except KeyboardInterrupt:
        pass

    return {
        "avg_rounds": round(points / total_rounds, 2),
        "win_rate": round(wins / total_rounds * 100, 2),
        "certainty": round(certainty / total_rounds, 2),
    }


if __name__ == "__main__":
    import argparse
    import importlib

    import dictionary

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--player", type=str, default="player.HumanPlayer")
    parser.add_argument("-k", "--player_kwargs", type=dict, default={})
    args = parser.parse_args()

    playerName = args.player
    playerModuleName = playerName[: -1 * playerName[::-1].index(".") - 1]
    playerModule = importlib.import_module(playerModuleName)
    playerClassName = playerName[-1 * playerName[::-1].index(".") :]
    playerKwargs = args.player_kwargs

    print(
        evaluate_player(
            data_types.Wordlist(dictionary.wordlist),
            dictionary.solution_list,
            getattr(playerModule, playerClassName),
            player_kwargs=playerKwargs,
        )
    )
