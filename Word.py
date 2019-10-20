import copy


class Word:

    def __init__(self, row):
        self._index = row[0]
        self._form = row[1]
        self._lemma = row[2]
        self._upos = row[3]
        self._xpos = row[4]
        self._head = row[6]
        self._deprel = row[7]
        self._deps = row[8]
        if "_" in row[9]:
            self._misc = []
        else:
            self._misc = row[9].split("|")
        if "_" in row[5]:
            self._feats = []
        else:
            self._feats = row[5].split("|")
            self._misc.append("Feats=" + "|".join(self._feats))
        self._addition = None
        self._suffix = False
        self.convert()

    def upos(self):
        return self._upos

    def feats(self):
        return self._feats

    def deprel(self):
        return self._deprel

    def misc(self):
        return self.misc

    def set_feats(self, feature_list):
        self._feats = feature_list

    def to_column(self, x):
        if len(x) > 0:
            return "|".join(x)
        return "_"

    def to_row(self):
        return [self._index, self._form, self._lemma, self._upos, self._xpos, self.to_column(self._feats),
                self._head, self._deprel, self._deps, self.to_column(self._misc)]

    def convert(self):
        self.convert_deprel()
        self.convert_xpos()
        self.convert_feats()
        self.convert_upos()
        self.check_punct()
        self.insert_addition()
        if self.deprel() in suffixes:
            self._xpos = "SUFFIX"

    def convert_deprel(self):
        if self._deprel in deprel_dict:
            self._deprel = deprel_dict[self._deprel]

    def convert_xpos(self):
        if self._xpos in xpos_dict:
            self._xpos = xpos_dict[self._xpos]

    def convert_feats(self):
        new_features = []
        for feat in self._feats:
            if feat == "VRoot" and self._upos == "Root":
                self._upos = "VERB"
            if feat == "NRoot" and self._upos == "Root":
                self._upos = "NOUN"
            if feat in feats_dict:
                new_features.append(feats_dict[feat])
            else:
                split_feat = feat.split(".")
                if len(split_feat) > 1:
                    new_features.extend(self.dotted_feat(split_feat))
        self._feats = copy.deepcopy(new_features)

    def convert_upos(self):
        if self._upos in upos_dict:
            self._upos = upos_dict[self._upos]

    def check_punct(self):
        if self._deprel == "@punct":
            self._upos = "PUNCT"

    def dotted_feat(self, split_feat):
        more_feats = []
        if "Subj" in split_feat:
            self._addition = "subj"
        for feat in split_feat:
            if feat in feats_dict:
                more_feats.append(feats_dict[feat])
        return more_feats

    def insert_addition(self):
        if self._addition:
            for i in range(len(self._feats)):
                current = self._feats[i]
                if "Number" in current or "Person" in current:
                    currents = current.split("=")
                    currents[0] += "[" + self._addition + "]"
                    current = "".join(currents)


suffixes = ["s.neg", "s.obj", "s.co", "s.subj", "s.subj_iobj", "s.poss.subj"]

deprel_dict = {
    "arg": "@obl:arg",
    "aux": "@aux",
    "ben": "@obl:ben",
    "caus": "@obl:caus",
    "co": "@conj",
    "iobj": "@iobj",
    "adv": "@advmod",
    "punc": "@punct",
    "r.disl": "@dislocated",  # ?
    "src": "@obl:src",
    "loc": "@nmod:loc",  # @obl:loc
    "subj": "@csubj",  # @usubj
    "acmp": "@nmod",  # @obl
    "mod": "@nmod",  # @obl, @advmod
    "s.arg.claus": "s.arg",
    "sntc": "root"
}

xpos_dict = {
    "Root_VDeriv": "Root",
    "Root_Num": "Root"
}

upos_dict = {
    "Root_VDeriv": "VERB",
    "Root_Num": "NUM",
    "VDeriv": "VERB"
}

feats_dict = {
    "+Abl": "Case=Abl",
    "+Acc": "Case=Acc",
    "+Add": "Case=Add",
    "+Ben": "Case=Ben",
    "+Caus": "Voice=Caus",
    "+Dat": "Case=Dat",
    "+Dim": "Deriv=Dim",
    "+Fut": "Tense=Fut",
    "+Gen": "Case=Gen",
    "+Hab": "Tense=Past|Aspect=Hab",
    "+Imp": "Mood=Imp",
    "+Instr": "Case=Ins",
    "+Ipst": "Tense=Past|Evident=Sqa",
    "+Loc": "Case=Loc",
    "+Perf": "Aspect=Perf",
    "+Pres": "Tense=Pres",
    "+Prog": "Aspect=Prog",
    "+Pst": "Tense=Past",
    "+Rflx": "Reflexive=Yes",
    "+Sg": "Number=Sing",
    "+Pl=true": "Number=Plur",
    "+Pl": "Number=Plur",
    "+Con_Inst": "Case=Ins",  # wan?
    "+Rflx": "Reflex=Yes",
    "+Poss": "Poss=Yes",
    "+Inch": "Aspect=Inch",
    "+Inf": "VerbForm=Inf",
    "+DirE": "Evident=DirE",
    "Sg": "Number=Sing",
    "Poss": "Possessive=Yes",
    "+3": "Person=3"
}
