from WordleSolver import players, utils, data_types, evaluate_player, dictionary

class MyComputerPlayer(players.ComputerPlayer):

    def guess(self):
        self._round += 1

        # Available instance variables
        # self._round
        # self._wordlist
        # self._potential_solutions
        # self._positions
        # self._global_scoring_rubric
        # self._letters_per_word
        # self._rounds_per_game

        # Suggested fcn's
        # reduced = utils.reduce(self._wordlist, self._global_scoring_rubric, self._positions)
        # guessed = utils.guess(self._potential_solutions, self._global_scoring_rubric, self._positions)
        # rfg = utils.reduce(self._wordlist, utils.merge_scoring_rubrics(utils.create_scoring_rubric(guessed[0]), self._global_scoring_rubric), self._positions) # is merging scoring rubrics necessary AND beneficial?
        # gar = utils.guess(utils.create_wordlist_with_unique_letters(self._wordlist), self._global_scoring_rubric, self._positions)

        # Return format
        # tuple(guessed word: str, description of the return: str, number of potential solutions: int)

if __name__ == "__main__":
    print(
        evaluate_player.evaluate_player(data_types.Wordlist(dictionary.wordlist),
            dictionary.solution_list,
            MyComputerPlayer,
            player_kwargs={},
        )
    )