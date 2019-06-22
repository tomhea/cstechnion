from cstechnion.kombi.Basics import n_letter_words


class L:
    def __init__(self, S, f):
        self.S = S      # Alphabet for language L
        self.f = f      # Boolean function. f(w) == True iff w in language L

    def __contains__(self, item):
        return self.f(item)

    def __getitem__(self, i):
        """ return the language of all words in L, with no more then i letters
            if i in -1,False,True then return a generator that produce words in L alphabetically """
        lazy = i in [-1, True, False]

        def lazy__getitem__():          # yields once if i >= 0
            Li, n = [], 0
            while n <= i or lazy:
                for w in n_letter_words(self.S, n):     # for every n-letter world w∈S*:
                    if w in self:                           # if w∈L:
                        if lazy:                                # if generator asked:
                            yield w                                 # yield the word found
                        else:                                   # if language under i (Li) asked:
                            Li.append(w)                            # append the word found to Li
                n += 1                                  # next n (n++)
            yield Li                                # ~~language under i (Li) asked~~  -->  yield calculated Li

        Li = lazy__getitem__()
        return Li if lazy else list(Li)[0]  # get the generator if lazy,  else get the first yield from the generator
