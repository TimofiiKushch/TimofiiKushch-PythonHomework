class Sentence:
    def __init__(self, string):
        self._words = string.split()
    def __len__(self):
        return len(self._words)
    def __getitem__(self, key):
        return self._words[key]
    def __setitem__(self, key, value):
        if not isinstance(value, str):
            raise SentenceError("Помилка у методі __setitem__() класу Sentence: передане значення має бути рядковим літералом", value)
        else:
            self._words[key] = value
    def __contains__(self, item):
        return item in self._words
    def __add__(self, other):
        if isinstance(other, str):
            self._words.append(other)
        elif isinstance(other, Sentence):
            self._words += other._words.copy()
        else:
            raise SentenceError("Помилка у методі  __add__() класу Sentence: передане значення має бути рядковим літералом або об'єктом класу Sentence", other)
    def __sub__(self, other):
        if isinstance(other, str):
            while other in self._words:
                self._words.remove(other)
        elif isinstance(other, Sentence):
            for word in other._words:
                while word in self._words:
                    self._words.remove(word)
        else:
            raise SentenceError("Помилка у методі  __sub__() класу Sentence: передане значення має бути рядковим літералом або об'єктом класу Sentence", other)
    def __str__(self):
        return " ".join(self._words)

class SentenceError(Exception):
    def __init__(self, message, errorValue):
        Exception.__init__(self)
        self._message = message
        self._errorValue = errorValue
    def __str__(self) -> str:
        return str("\n" + self._message + "\nКласс (тип) значення, що викликало помилку: " + type(self._errorValue).__name__)

#################################################################################
sent1 = Sentence("How do I find out a name of class that created an instance of an object in Python if the function I am doing this from is the base class of which the class of the instance has been derived?")

sent1[17] = "C++"
#sent1[5] = list()
#sent1 - set()
sent1 + 1
