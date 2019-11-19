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
        self._old_form = row[1]
        # self.convert()

    def index(self):
        return self._index

    def old_form(self):
        return self._old_form

    def upos(self):
        return self._upos

    def feats(self):
        return self._feats

    def deprel(self):
        return self._deprel

    def form(self):
        return self._form

    def set_feats(self, feature_list):
        self._feats = feature_list

    def set_head(self, head):
        self._head = head

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
        self.convert_upos()
        self.convert_feats()
        self.convert_punct()
        self.insert_addition()
        if self.deprel() in suffixes:
            self._xpos = "SUFFIX"
        if self._upos == "VERB":
            self.insert_verbform()
            self.insert_aspect()
        self.convert_misc()

    def convert_misc(self):
        if len(self._feats) >= 1:
            self._misc.append("FEATURES=" + "|".join(self._feats) + "")
        else:
            self._misc.append("FEATURES")

    def cleanup(self):
        self.cleanup_form()
        self.cleanup_misc()
        self.cleanup_features()
        self.cleanup_dummies()
        self.cleanup_xpos()

    def cleanup_misc(self):
        for misc in self._misc:
            if "FEATURES" in misc:
                misc = misc.replace("[", "")
                misc = misc.replace("]", "")
                misc = misc.replace("true", "")
                misc = misc.replace("FEATURES=", "")
                if len(misc) > 2:
                    features = misc.split("|")
                    self._feats = features
                break

    def convert_deprel(self):
        if self._deprel in deprel_dict:
            self._deprel = deprel_dict[self._deprel]
        if "Gloss=ser" in self._misc:
            self._deprel = "ser"

    def convert_xpos(self):
        if self._xpos in xpos_dict:
            self._xpos = xpos_dict[self._xpos]

    def convert_feats(self):
        new_features = []
        extra_feats = []
        for feat in self._feats:
            if "." in feat:
                split_feat = feat.split(".")
                if len(split_feat) > 1:
                    extra_feats.extend(split_feat)
        if "Incl" in extra_feats:
            if "+1" in extra_feats:
                extra_feats.append("Person=1+INCL")
                extra_feats.remove("+1")
                extra_feats.remove("Incl")
        elif "Excl" in extra_feats:
            if "+1" in extra_feats:
                extra_feats.append("Person=1+EXCL")
                extra_feats.remove("+1")
                extra_feats.remove("Excl")
        self._feats.extend(extra_feats)
        for feat in self._feats:
            if self._upos not in ud_pos_tags:
                if feat == "VRoot" or feat == "Root_VS" or feat == "VRootES":
                    self._upos = "VERB"
                if feat == "NRootES" or feat == "NRoot":
                    self._upos = "NOUN"
                if feat == "NRootNUM":
                    self._upos = "NUM"
                if feat == "PrnDem":
                    new_features.append("PronType=Det")
                    self._upos = "DET"
            if feat in feats_dict:
                new_features.append(feats_dict[feat])
        self._feats = copy.deepcopy(new_features)

    def convert_upos(self):
        if self._upos in upos_dict:
            self._upos = upos_dict[self._upos]

    def convert_punct(self):
        if self._deprel == "punct":
            self._upos = "PUNCT"

    def insert_verbform(self):
        for item in self._feats:
            if "VerbForm" in item:
                return
        # self._feats.append("VerbForm=NONE")

    def insert_aspect(self):
        for item in self._feats:
            if "Aspect" in item:
                return
        # self._feats.append("Aspect=NONE")

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

    def cleanup_form(self):
        self._form = self._form.replace("-", "")

    def cleanup_features(self):
        if self._feats:
            self._feats.sort()

    def cleanup_dummies(self):
        new_feats = []
        for feat in self._feats:
            if "=NONE" not in feat:
                new_feats.append(feat)
        self._feats = new_feats
        new_misc = []
        for misc in self._misc:
            if "=NONE" not in misc:
                new_misc.append(misc)
        self._misc = new_misc

    def cleanup_xpos(self):
        self._xpos = "_"


suffixes = ["s.neg", "s.obj", "s.subj", "s.subj_iobj", "s.poss.subj", "s.poss"]

deprel_dict = {
    "arg": "obl:arg",
    "aux": "aux",
    "ben": "obl:ben",
    "caus": "obl:caus",
    "co": "conj",
    "iobj": "iobj",
    # "adv": "@advmod",
    "punc": "punct",
    "r.disl": "dislocated",  # ?
    "src": "obl:src",
    "loc": "nmod:loc",  # @obl:loc
    # "subj": "@csubj",  # @usubj
    "acmp": "nmod",  # @obl
    "mod": "nmod",  # @obl, @advmod
    "s.arg.claus": "s.arg",
    # "sntc": "root",
    "det": "det",
    "goal": "goal",
    "hab": "hab"

}

xpos_dict = {
    "Root_VDeriv": "Root",
    "Root_Num": "Root",
    "Root_VS": "Root"
}

upos_dict = {
    "Root_VDeriv": "VERB",
    "Root_Num": "NUM",
    "VDeriv": "VERB",
    "NRootNUM": "NUM",
    "Root_VS": "VERB",
    "VRootES": "VERB",
    "NRootES": "NOUN"
}

feats_dict = {
    "abbrev": "Abbr=Yes",  # moved from deprels
    "+Abl": "Case=Abl",
    "+Acc": "Case=Acc",
    "+Add": "Case=Add",
    "+Aff": "Aspect=Affective",
    "+Ag": "VerbForm=Vnoun|Deriv=Ag",
    "Asmp_Emph": "Evident=Assumptive",
    "+Ben": "Case=Ben",
    "+Caus": "Voice=Caus",
    "+Con_Inst": "Case=Ins",  # wan?
    "+Con_Intr": "",
    "+Dat": "Case=Dat",
    "+Def": "Definite=Def",
    "+Des": "Mood=Desiderative",
    "+Dim": "Deriv=Dim",
    "+Dir": "Motion=Dir",
    "+DirE": "Evident=DirE",
    "+Distr": "Case=Distr",
    "+DS": "DS",
    "+Fact": "Evident=Fact",
    "FLM": "Foreign=Yes",
    "+Foc": "FOC",
    "+Fut": "Tense=Fut",
    "+Gen": "Case=Gen",
    "+Hab": "Tense=Past|Aspect=Hab",
    "+Imp": "Mood=Imp",
    "+Inch": "Aspect=Inch",
    "+IndE": "Evident=IndE",
    "+Inf": "VerbForm=Inf",
    "+Ipst": "Tense=Past|Evident=Sqa",
    "+Instr": "Case=Ins",
    "+Lim": "Case=Lim",
    "+Loc": "Case=Loc",
    "_Neg": "Polarity=Neg",
    "+Obl": "Mood=Obligative",
    "Person=1+EXCL": "Person=1+EXCL",
    "Person=1+INCL": "Person=1+INCL",
    "+Perf": "Aspect=Perf",
    "+Pl=true": "Number=Plur",
    "+Pl": "Number=Plur",
    "Pl": "Number=Plur",
    "+Poss": "Poss=Yes",
    "Poss": "Poss=Yes",
    "+Pres": "Tense=Pres",
    "+Prog": "Aspect=Prog",
    "+Pst": "Tense=Past",
    "+Rflx": "Reflex=Yes",
    "+Rptn": "Deriv=Rptn",
    "+Sg": "Number=Sing",
    "Sg": "Number=Sing",
    "+3": "Person=3",
    "FLM": "Foreign=Yes",
    "+Con_Intr": "",  # blank on purpose
    "+Aff": "Mood=Affective",
    "+Ag": "VerbForm=Vnoun|Deriv=Ag",
    "Asmp_Emph": "Evident=Assumptive",
    "+Def": "Definite=Def",
    "+Des": "Mood=Desiderative",
    "+Dir": "Motion=Dir",
    "+Distr": "Case=Distr",
    "+1.Pl.Excl": "1+EXCL",
    "+Foc": "Focus=Yes",
    "+Fact": "Evident=Fact",
    "+1.Pl.Incl": "1+INCL",
    "+IndE": "Evident=IndE",
    "+DS": "",  # advcl:ds
    "+SS": "",  # advcl:ss
    "_Neg": "Polarity=Neg",
    "+Lim": "Case=Lim",
    "+Obl": "Mood=Obligative",
    "+Rptn": "Deriv=Rptn",
    "+Term": "Case=Term",
    "+Vdim": "Degree=Dim",
    "+Top": "Topic=Yes",
    "+3": "Person=3",
    "+1": "Person=1"
}

ud_pos_tags = ["ADJ", "ADV", "INTJ", "NOUN", "PROPN", "VERB", "ADP", "AUX",
               "CCONJ", "DET", "NUM", "PART", "PRON", "SCONJ", "PUNCT", "SYM", "X"]
