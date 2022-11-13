class Wordlist(list):
    """Sorted list with unique, equal-length strings"""
    def __init__(self, dictionary: list = [], letters_per_word: int = 5):
        self.letters_per_word = letters_per_word
        self.wordset = set()

        if dictionary == []: return
        self.extend(dictionary)


    def append(self, __object: str) -> None:
        if type(__object) != str or len(__object) != self.letters_per_word or not __object.isalpha() or __object in self.wordset: return
        
        self.__insert(self.__find_index_to_insert(__object), __object)
        self.wordset.add(__object)

    def extend(self, __iterable) -> None:
        for word in __iterable:
            self.append(word)

    def __insert(self, __index: int, __object: str) -> None:
        return super().insert(__index, __object)

    def __find_index_to_insert(self, word: str) -> int:
        if self.__len__() == 0: return 0

        upper_bound = self.__len__()-1
        lower_bound = 0

        # Check if the value should be inserted at any end
        if word < self[lower_bound]: return 0
        if word > self[upper_bound]: return upper_bound+1

        while True:
            i = len(self[lower_bound:upper_bound]) // 2
            # print(word, self, self[lower_bound+i], self[lower_bound+i+1], lower_bound, i, upper_bound)
            if self[lower_bound+i] < word < self[lower_bound+i+1]: return lower_bound+i+1
            if self[lower_bound+i] >= word: upper_bound = lower_bound + i
            else: lower_bound = lower_bound + i


    def __disable_attribute() -> None:
        raise Exception("Operation not permitted")

    def insert(self, __index, __object): Wordlist.__disable_attribute()
    def reverse(self): Wordlist.__disable_attribute()



class ScoringRubric(dict):
    """Special dict that follows scoring rubric format. Check format.txt for details."""
    def __init__(self, letters_per_word: int = 5) -> None:
        self.letters_per_word = letters_per_word
        self.update({chr(k): [0 for i in range(letters_per_word + 1)] for k in range(97, 123)})



class Positions(dict):
    """Special dict that follows positions format. Check format.txt for details."""
    def __init__(self, letters_per_word: int = 5) -> None:
        self.letters_per_word = letters_per_word
        self.update({
        **{chr(k): [0, letters_per_word, set(range(1, letters_per_word + 1)), set()] for k in range(97, 123)},
        **{i: [set("abcdefghijklmnopqrstuvwxyz"), set()] for i in range(1, letters_per_word + 1)},
    })