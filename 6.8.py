class Iterator:
    def __init__(self, sentence):
        self._sentence = sentence
        self._current = ""
        # оскільки слова можуть повторюватися, то будемо враховувати кількість однакових слів у змінній count
        self._count = 0
    def __next__(self):
        if self._count == 0:
            new_word = None
            for i in range(len(self._sentence)):
                if new_word == None:
                    if self._current < self._sentence[i]:
                        new_word = self._sentence[i]
                else:
                    if self._current < self._sentence[i] < new_word:
                        new_word = self._sentence[i]
            if new_word == None:
                raise StopIteration
            for i in range(len(self._sentence)):
                if self._sentence[i] == new_word:
                    self._count += 1
            self._current = new_word
        self._count -= 1
        return self._current

class Sentence:
    def __init__(self, string):
        self._words = string.split()
    def __len__(self):
        return len(self._words)
    def __getitem__(self, key):
        return self._words[key]
    def __setitem__(self, key, value):
        self._words[key] = value
    def __contains__(self, item):
        return item in self._words
    def __add__(self, other):
        if isinstance(other, str):
            self._words.append(other)
        elif isinstance(other, Sentence):
            self._words += other._words.copy()
    def __sub__(self, other):
        if isinstance(other, str):
            while other in self._words:
                self._words.remove(other)
        elif isinstance(other, Sentence):
            for word in other._words:
                while word in self._words:
                    self._words.remove(word)
    def __str__(self):
        return " ".join(self._words)
    def __iter__(self):
        return Iterator(self)

#################################################################################
sent = Sentence("")
f = open("file.txt")
while True:
    s = f.readline()
    if s:
        sent + Sentence(s)
    else:
        break
f.close()

for word in sent:
    print(word)