# Example solver
# 
# Work in progress

from WordleSolver import players, utils, data_types, evaluate_player, dictionary

class FufsPlayer(players.ComputerPlayer):

    def guess(self):
        self._round += 1

        if self._round == 1: 
            reduced = utils.reduce(self._wordlist, self._global_scoring_rubric, self._positions)
            return reduced[0][0], "reduce initial", len(self._potential_solutions)

        guessed = utils.guess(self._potential_solutions, self._global_scoring_rubric, self._positions)
        self._potential_solutions = guessed[0]
        
        if len(self._potential_solutions) <= (self._rounds_per_game - self._round + 1): return guessed[0][0], "guess", len(self._potential_solutions)

        if self._round < 3: 
            rfg = utils.reduce(self._wordlist, utils.merge_scoring_rubrics(utils.create_scoring_rubric(guessed[0]), self._global_scoring_rubric), self._positions)
            if rfg[0][0] != '': return rfg[0][0], "reduce from guess", len(self._potential_solutions)

        gar = utils.guess(utils.create_wordlist_with_unique_letters(self._wordlist), self._global_scoring_rubric, self._positions)

        if self._round <= 5: 
            gar = utils.guess(utils.create_wordlist_with_unique_letters(self._wordlist), self._global_scoring_rubric, self._positions)
            if gar[0][0] != '': return gar[0][0], "guess and reduce", len(self._potential_solutions)

        return guessed[0][0], "guess final", len(self._potential_solutions)


if __name__ == "__main__":
    print(
        evaluate_player.evaluate_player(data_types.Wordlist(dictionary.wordlist),
            dictionary.solution_list,
            FufsPlayer,
            player_kwargs={},
        )
    )