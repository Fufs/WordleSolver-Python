"""
player.py
by Fufs

This module contains:
    - Player            - abstract class used to create players for the wordle game.
    - HumanPlayer       - sub-class of Player, used to play the wordle game directly. Used for testing purposes of the python Wordle implementation.
    - ComputerPlayer    - abstract class used to create computer player (includes check_letters implementation) 
"""

from abc import ABC, abstractmethod
from . import utils
from . import dictionary
from . import data_types


class Player(ABC):
    def __init__(self, dictionary: list = dictionary.wordlist, letters_per_word: int = 5, rounds_per_game: int = 6):
        super().__init__()
        self._letters_per_word = letters_per_word
        self._rounds_per_game = rounds_per_game
        self._wordlist = data_types.Wordlist(dictionary, letters_per_word)
        self._round = 0

    @abstractmethod
    def check_letters(self, round_state):
        pass

    @abstractmethod
    def guess(self):
        pass


class ComputerPlayer(Player):
    def __init__(self, dictionary: list | str = dictionary.wordlist, letters_per_word: int = 5, rounds_per_game: int = 6):

        if type(dictionary) == str:
            super().__init__(
                open(dictionary).read().splitlines(), letters_per_word, rounds_per_game
            )
        else:
            super().__init__(dictionary, letters_per_word, rounds_per_game)

        self._global_scoring_rubric = utils.create_scoring_rubric(self._wordlist)
        self._positions = data_types.Positions(letters_per_word)
        self._potential_solutions = self._wordlist

    def check_letters(self, round_state: dict) -> None:  # TODO: Add exceptions
        """"""
        # Included (Yellow) letters
        for letter in round_state["included"]:
            num_of_letters = len(round_state["included"][letter])
            if letter in round_state["correct"]:
                num_of_letters += len(round_state["correct"][letter])

            if num_of_letters > self._positions[letter][0]:
                self._positions[letter][0] = num_of_letters

            self._positions[letter][2] = self._positions[letter][2].difference(
                round_state["included"][letter]
            )
            for position in round_state["included"][letter]:
                self._positions[position][0].difference({letter})

        # Correct (Green) letters
        for letter in round_state["correct"]:
            num_of_letters = len(round_state["correct"][letter])
            if letter in round_state["included"]:
                num_of_letters += len(round_state["included"][letter])

            if num_of_letters > self._positions[letter][0]:
                self._positions[letter][0] = num_of_letters

            self._positions[letter][3] = self._positions[letter][3].union(
                round_state["correct"][letter]
            )
            for position in round_state["correct"][letter]:
                self._positions[position][1].add(letter)

        # Excluded (Gray) letters
        for letter in round_state["excluded"]:
            if len(round_state["excluded"][letter]) > 0:
                self._positions[letter][1] = self._positions[letter][0]

            self._positions[letter][2] = self._positions[letter][2].difference(
                round_state["excluded"][letter]
            )
            for position in round_state["excluded"][letter]:
                self._positions[position][0].difference({letter})

        # print(self._positions)


class HumanPlayer(Player):
    def __init__(self, dictionary: list = dictionary.wordlist, letters_per_word: int = 5, rounds_per_game: int = 6) -> None:
        super().__init__(dictionary, letters_per_word, rounds_per_game)

    def check_letters(self, round_state: dict) -> None:
        boxes = ["" for i in range(self._letters_per_word)]
        for letter in round_state["excluded"]:
            for position in round_state["excluded"][letter]:
                boxes[position - 1] = "B"

        for letter in round_state["included"]:
            for position in round_state["included"][letter]:
                boxes[position - 1] = "Y"

        for letter in round_state["correct"]:
            for position in round_state["correct"][letter]:
                boxes[position - 1] = "G"

        print("".join(boxes))

    def guess(self) -> None:
        while True:
            query = input("Guess the word: ").strip().lower()

            if not query.isalpha():
                print("Words can only include letters. Try again.")
            elif len(query) != self._letters_per_word:
                print(
                    "The word must have", self._letters_per_word, "letters. Try again."
                )
            elif utils.find_word(self._wordlist, query) == -1:
                print(query, "is not in wordlist. Try again.")
            else:
                return query, "", -1
