"""
wordle.py
by Fufs

This module contains:
    - play      - play this implementation of the game wordle
"""

import random
from . import data_types, dictionary, players, utils


def play(wordlist: data_types.Wordlist = data_types.Wordlist(dictionary.wordlist, 5), solution: str | list = dictionary.solution_list, player: players.Player = players.HumanPlayer(), rounds_per_game=6, extended: bool = False, dev: bool = False):
    if type(solution) == list:
        solution = random.choice(solution)

    if utils.find_word(wordlist, solution) == -1:
        raise ValueError("Solution not in wordlist, win is unachievable")

    solution_letters = {}
    for i in range(wordlist.letters_per_word):
        if solution[i] not in solution_letters:
            solution_letters[solution[i]] = set()
        solution_letters[solution[i]].add(i + 1)

    for i in range(1, len(wordlist) + 1 if extended else wordlist.letters_per_word + 1):
        guessed = player.guess()
        if dev:
            print(guessed)

        if guessed[0] == solution:
            return {
                "solution": solution,
                "rounds": i,
                "won": i <= rounds_per_game,
                "potential_solutions": guessed[2],
            }

        round_state = {"excluded": {}, "included": {}, "correct": {}}
        guessed_letters = {}

        for j in range(wordlist.letters_per_word):
            if guessed[0][j] not in guessed_letters:
                guessed_letters[guessed[0][j]] = set()
            guessed_letters[guessed[0][j]].add(j + 1)

        for letter in guessed_letters:
            if letter in solution_letters:
                if (len(solution_letters[letter].intersection(guessed_letters[letter])) > 0):
                    round_state["correct"][letter] = solution_letters[letter].intersection(guessed_letters[letter])
                    other_green_positions = solution_letters[letter].difference(round_state["correct"][letter])
                else:
                    other_green_positions = solution_letters[letter]

                nongreen_guessed_positions = sorted(list(guessed_letters[letter].difference(solution_letters[letter])))
                round_state["included"][letter] = set(nongreen_guessed_positions[: len(other_green_positions)])
                if len(nongreen_guessed_positions[len(other_green_positions):]) > 0:
                    round_state["excluded"][letter] = set(nongreen_guessed_positions[len(other_green_positions):])

            else:
                round_state["excluded"][letter] = guessed_letters[letter]

        # print(round_state)
        player.check_letters(round_state)

    return {
        "solution": solution,
        "rounds": len(wordlist) + 1 if extended else wordlist.letters_per_word + 1,
        "won": False,
    }


if __name__ == "__main__":
    print(play())
