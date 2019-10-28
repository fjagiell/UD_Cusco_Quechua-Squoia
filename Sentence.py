class Sentence:
    def __init__(self, sent_id):
        self._text_seg = ""
        self._id = sent_id
        self._words = []

    def append_word(self, word):
        self._words.append(word)

    def set_seg(self, seg):
        self._text_seg = seg.replace("text", "text[seg]")

    def words(self):
        return self._words

    def seg(self):
        return self._text_seg

    def id(self):
        return self._id
