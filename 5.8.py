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

#################################################################################
sent1 = Sentence("")
sent2 = Sentence("")
f = open("Джуринський водоспад.txt")
while True:
    try:
        s = f.readline()
    except EOFError:
        break
    if s:
        sent1 + Sentence(s)
        sent2 + Sentence(s)
    else:
        break
f.close()

to_change = {"водоспад" : "ВОДА_З_НЕБЕС", "водоспаду" : "ВОДИ_З_НЕБЕС", "турки" : "ОСМАНИ", "замок" : "ФОРТЕЦЯ", "замку" : "ФОРТЕЦІ"}
to_del = ["місцина", "Джуринський", "невимовно", "та"]

# change
for key, val in to_change.items():
    for i in range(len(sent1)):
        if sent1[i] == key:
            sent1[i] = val

# remove
for word in to_del:
    if word in sent2:
        sent2 - word

print("Words in sent1:", len(sent1))
print(sent1)
print()
print("Words in sent2:", len(sent2))
print(sent2)
