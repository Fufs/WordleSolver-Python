"""
utils.py
by Fufs

This module contains:
    - create_scoring_rubric                 - Returns a scoring rubric for scoring words in wordlist. Check format.txt.
    - merge_scoring_rubrics                 - Returns a merged scoring rubric of a master and slave scoring rubric.
    - create_wordlist_with_unique_letters   - Returns a new wordlist that only contains unique letters.
    - solution_finder                       - Returns a list of words that qualify as a solution in alphabetical order.
    - score_by_letters                      - Returns a dict with scores for each word to establish the closest match to the solution.
    - score_by_letters_at_positions         - Same as score_by_letters but takes into considaration the position of each letter.
    - find_word                             - Returns the index of a word in a sorted wordlist or -1 if not found.
    - letter_checked                        - Returns True if the letter has appeared in previous queries (Think crossed-of letters in Hangman). 
    - reduce                                - Returns a list of words that best reduce the number of potential solutions in order of significance.
    - guess                                 - Returns a list of words that are the closest match to the solution in order of significance.
"""


from . import data_types

import math
import statistics

alphabet = "abcdefghijklmnopqrstuvwxyz"


def create_scoring_rubric(wordlist: data_types.Wordlist) -> data_types.ScoringRubric:
    """Returns a scoring rubric for scoring words in wordlist. Check format.txt."""

    scoring_rubric = data_types.ScoringRubric(wordlist.letters_per_word)

    if len(wordlist) == 0: return scoring_rubric

    # Count total number of occurances
    for word in wordlist:
        for l in range(wordlist.letters_per_word):
            scoring_rubric[word[l]][0] += 1
            scoring_rubric[word[l]][l+1] += 1

    # Calculate weights of letters in wordlist and at each position
    total = len(wordlist) * wordlist.letters_per_word
    lowest_occurance = 1.0
    for key in scoring_rubric:
        for i in range(1, wordlist.letters_per_word + 1):
            if scoring_rubric[key][0] != 0:
                scoring_rubric[key][i] /= scoring_rubric[key][0]
            else:
                scoring_rubric[key][i] = 0
        scoring_rubric[key][0] /= total
        if scoring_rubric[key][0] != 0:
            lowest_occurance = min(lowest_occurance, scoring_rubric[key][0])

    # Scale the ratios of number of occurances for higher diversity between scores.
    for key in scoring_rubric:
        scoring_rubric[key][0] /= lowest_occurance

    return scoring_rubric


def merge_scoring_rubrics(master_rubric: data_types.ScoringRubric, slave_rubric: data_types.ScoringRubric, master_multiplier: int = 1, slave_multiplier: int = 1) -> data_types.ScoringRubric:
    """Returns a merged scoring rubric of a master and slave scoring rubric."""
    if master_rubric.letters_per_word != slave_rubric.letters_per_word: raise TypeError("letters_per_word don't match")

    merged_rubric = data_types.ScoringRubric(master_rubric.letters_per_word)
    
    total_score = 0
    lowest_occurance = 1.0
    for key in merged_rubric:
        # Calculate weighted average of the general score
        merged_rubric[key][0] = (master_rubric[key][0]*master_multiplier + slave_rubric[key][0]*slave_multiplier) / (master_multiplier+slave_multiplier)
        total_score += merged_rubric[key][0]
        
        # Calculate weighted averages of weights
        total_weight = 0
        for i in range(1,merged_rubric.letters_per_word+1):
            merged_rubric[key][i] = (master_rubric[key][i]*master_multiplier + slave_rubric[key][i]*slave_multiplier) / (master_multiplier+slave_multiplier)
            total_weight += merged_rubric[key][i]
        
        # Normalize the weights
        for i in range(1,merged_rubric.letters_per_word+1):
            merged_rubric[key][i] /= total_weight
            
    # Present score as a ratio of all the scores
    for key in merged_rubric:
        merged_rubric[key][0] /= total_score
        lowest_occurance = min(lowest_occurance, merged_rubric[key][0])

    # Scale the ratios of scores for higher diversity between scores.
    for key in merged_rubric:
        merged_rubric[key][0] /= lowest_occurance


    return merged_rubric


def create_wordlist_with_unique_letters(wordlist: data_types.Wordlist = data_types.Wordlist(), letters_per_word: int = 5) -> data_types.Wordlist:
    """Returns a new wordlist that only contains unique letters."""

    if wordlist == data_types.Wordlist(): wordlist

    unique_letters_wordset = set()

    for word in wordlist:
        unique_letters_in_word = set()
        for letter in word:
            unique_letters_in_word.add(letter)
        if len(word) == len(unique_letters_in_word):
            unique_letters_wordset.add(word)

    return data_types.Wordlist(unique_letters_wordset, letters_per_word)


def solution_finder(wordlist: data_types.Wordlist, positions: data_types.Positions) -> data_types.Wordlist:
    """Returns a list of words that qualify as a solution in alphabetical order."""
    if wordlist.letters_per_word != positions.letters_per_word: raise TypeError("letters_per_word mismatch")

    solution_wordset = set()

    for word in wordlist:
        letters = {}
        for i in range(wordlist.letters_per_word):
            if word[i] not in letters:
                letters[word[i]] = set()
            letters[word[i]].add(i + 1)

        issolution = True
        broken = False
        for letter in letters:
            if not positions[letter][0] <= len(letters[letter]) <= positions[letter][
                1
            ] or not letters[letter].issubset(positions[letter][2]):
                issolution = False
                break
            for position in letters[letter]:
                if (
                    len(positions[position][1]) > 0
                    and letter not in positions[position][1]
                ):
                    issolution = False
                    broken = True
                    break

            if broken:
                break

        if issolution:
            solution_wordset.add(word)

    return data_types.Wordlist(solution_wordset)


def score_by_letters(wordlist: data_types.Wordlist, scoring_rubric: data_types.ScoringRubric) -> dict:
    """Returns a dict with scores for each word to establish the closest match to the solution."""

    results = {}
    for word in wordlist:
        score = 0
        for l in range(len(word)):
            score += scoring_rubric[word[l]][0]
        results[word] = score

    return results


# TODO: Make a Wordlist class to ensure all words in the worldlist are the same length
def score_by_letters_at_positions(wordlist: data_types.Wordlist, scoring_rubric: data_types.ScoringRubric) -> dict:
    """Same as score_by_letters but takes into considaration the position of each letter."""

    results = {}
    for word in wordlist:
        score = 0
        for l in range(len(word)):
            score += scoring_rubric[word[l]][0] * scoring_rubric[word[l]][l + 1]
        results[word] = score

    return results


def find_word(wordlist: data_types.Wordlist, query: str) -> int:
    """Returns the index of a word in a Wordlist or -1 if not found."""

    upper_bound = len(wordlist)
    lower_bound = 0

    while True:
        i = len(wordlist[lower_bound:upper_bound]) // 2
        if wordlist[lower_bound + i] == query:
            return lower_bound + i
        elif i == 0:
            return -1
        if wordlist[lower_bound + i] > query:
            upper_bound = lower_bound + i
        else:
            lower_bound = lower_bound + i


def letter_checked(letter: str, positions: data_types.Positions):
    """Returns True if the letter has appeared in previous queries (Think crossed-of letters in Hangman)."""
    return (
        positions[letter][0] != 0
        or positions[letter][1] != positions.letters_per_word
        or len(positions[letter][2]) != positions.letters_per_word
        or len(positions[letter][3]) != 0
    )


def reduce(wordlist: data_types.Wordlist, scoring_rubric: data_types.ScoringRubric, positions: data_types.Positions, num_of_common_letters: int = 0) -> tuple:
    """Returns a list of words that best reduce the number of potential solutions in order of significance."""
    if wordlist.letters_per_word != scoring_rubric.letters_per_word != positions.letters_per_word: raise TypeError("letters_per_word mismatch")

    excluded_letters = set()
    total_potential_candidates = set()
    # Mark letters for exclusion
    for letter in alphabet:
        if letter_checked(letter, positions):
            excluded_letters.add(letter)

    # Create a list of exclusion sets
    if num_of_common_letters == 0 or len(excluded_letters) < num_of_common_letters:
        exclusion_sets = [excluded_letters]
    else:
        num_of_exclusion_sets = math.comb(len(excluded_letters), num_of_common_letters)
        exclusion_sets = [set() for i in range(num_of_exclusion_sets)]
        for offset in range(len(excluded_letters) - num_of_common_letters):
            i = offset
            for letter in excluded_letters:
                if i >= num_of_exclusion_sets:
                    exclusion_sets[i - num_of_exclusion_sets].add(letter)
                else:
                    exclusion_sets[i].add(letter)
                i += 1

    # Create a list of potential best reducing words
    top_potential_candidates = set()
    for exclusion_set in exclusion_sets:
        reduced_wordset = set(wordlist)
        for letter in exclusion_set:
            current_set = set()
            for word in reduced_wordset:
                if letter not in word:
                    current_set.add(word)
            reduced_wordset = current_set
        reduced_wordset = create_wordlist_with_unique_letters(reduced_wordset)
        total_potential_candidates = total_potential_candidates.union(reduced_wordset)
        if len(reduced_wordset) == 0:
            continue
        reduced_scoreboard = score_by_letters(reduced_wordset, scoring_rubric)

        result = ""
        score = 0
        for word in reduced_scoreboard:
            if reduced_scoreboard[word] == score:
                word_duel = score_by_letters_at_positions([word, result], scoring_rubric)
                if word_duel[word] > word_duel[result]:
                    result = word
            elif reduced_scoreboard[word] > score:
                result = word
                score = reduced_scoreboard[word]
        top_potential_candidates.add(result)

    if len(top_potential_candidates) == 0:
        if num_of_common_letters >= wordlist.letters_per_word:
            return [""], 0, 0
        else:
            return reduce(wordlist, scoring_rubric, positions, num_of_common_letters + 1)

    else:
        if len(top_potential_candidates) == 1:
            return ([top_potential_candidates.pop()], len(total_potential_candidates), num_of_common_letters)

        top_potential_candidates = list(top_potential_candidates)
        potential_scoreboard = score_by_letters(top_potential_candidates, scoring_rubric)

        for i in range(len(top_potential_candidates)):
            argMin = i
            for j in range(i + 1, len(top_potential_candidates)):
                if (potential_scoreboard[top_potential_candidates[j]] == potential_scoreboard[top_potential_candidates[argMin]]):
                    word_duel = score_by_letters_at_positions([top_potential_candidates[j], top_potential_candidates[argMin]], scoring_rubric)
                    if (word_duel[top_potential_candidates[j]] > word_duel[top_potential_candidates[argMin]]):
                        argMin = j

                if (potential_scoreboard[top_potential_candidates[j]] > potential_scoreboard[top_potential_candidates[argMin]]):
                    argMin = j

            tmp = top_potential_candidates[argMin]
            top_potential_candidates[argMin] = top_potential_candidates[i]
            top_potential_candidates[i] = tmp

        return (top_potential_candidates, len(total_potential_candidates), num_of_common_letters)


def guess(wordlist: data_types.Wordlist, scoring_rubric: data_types.ScoringRubric, positions: data_types.Positions) -> tuple:
    """Returns a list of words that are the closest match to the solution in order of significance."""
    if wordlist.letters_per_word != scoring_rubric.letters_per_word != positions.letters_per_word: raise TypeError("letters_per_word mismatch")

    all_solutions = solution_finder(wordlist, positions)
    all_scoreboard = score_by_letters_at_positions(all_solutions, scoring_rubric)

    for i in range(len(all_solutions)):
        argMin = i
        for j in range(i + 1, len(all_solutions)):
            if all_scoreboard[all_solutions[j]] > all_scoreboard[all_solutions[argMin]]:
                argMin = j

        tmp = all_solutions[argMin]
        all_solutions[argMin] = all_solutions[i]
        all_solutions[i] = tmp

    if len(all_solutions) == 0:
        return [""], 0
    return (all_solutions, len(all_solutions), statistics.stdev([all_scoreboard[key] for key in all_scoreboard]) if len(all_solutions) > 1 else 0)
