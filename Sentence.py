class Sentence:
    def __init__(self, sent_id):
        self._text_seg = ""
        self._id = sent_id
        self._words = []
        self._sentence_converted = self.calc_sentence()
        self._root = "-1"
        self._contains_quotes = False

    def append_word(self, word):
        self._words.append(word)

    def set_seg(self, seg):
        self._text_seg = seg.replace("text", "text[seg]")

    def set_text(self, text):
        text = text.replace("\"", "@quot")
        self._text_seg = text

    def words(self):
        return self._words

    def seg(self):
        return self._text_seg

    def id(self):
        return self._id

    def contains_quotes(self):
        self.update_contains_quotes()
        return self._contains_quotes

    def update_contains_quotes(self):
        if "\"" in self._text_seg:
            self._contains_quotes = True
        else:
            self._contains_quotes = False

    def find_root(self):
        for item in self._words:
            if item.deprel() == "root":
                return item.index()
        return "none"

    def sentence_converted(self):
        return self._sentence_converted

    def to_rows(self):
        rows = []
        rows.append([str(self._id)])
        rows.append([self._text_seg])
        # rows.append([self.calc_sentence()])
        for word in self._words:
            rows.append(word.to_row())
        rows.append([])
        return rows

    def __str__(self):
        w = []
        for word in self._words:
            w.extend(word.to_row())
            w.append("\n")
        return str(self._id) + "\n" + self._text_seg + "\n" + self.calc_sentence() + "\n" + " ".join(w) + "\n"

    def calc_sentence(self):
        full_sentence = ["# text = "]
        for word in self._words:
            full_sentence.append(word.form())
        return " ".join(full_sentence)
