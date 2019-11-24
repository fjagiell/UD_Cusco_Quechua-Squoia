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
        if '_' in row[9]:
            self._misc = []
        else:
            self._misc = row[9].split('|')
        if '_' in row[5]:
            self._feats = []
        else:
            self._feats = row[5].split('|')
        self._addition = None
        self._suffix = False
        self._old_form = row[1]

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
            return '|'.join(x)
        return '_'

    def to_row(self):
        return [self._index, self._form, self._lemma, self._upos, self._xpos, self.to_column(self._feats),
                self._head, self._deprel, self._deps, self.to_column(self._misc)]

    def convert(self):
        self.convert_form()
        self.convert_deprel()
        self.convert_xpos()
        self.convert_upos()
        self.convert_feats()
        self.convert_punct()
        self.insert_addition()
        if self.deprel() in suffixes:
            self._xpos = 'SUFFIX'
        self.convert_misc()
        self.empty_feats()

    def convert_form(self):
        self._form = self._form.replace('\"', '@quot')
        if self._form == '-':
            self._form == '@dash'

    def convert_misc(self):
        if len(self._feats) > 1:
            self._misc.append('FEATURES=[' + '&'.join(self._feats) + ']')
        elif len(self._feats) == 1:
            self._misc.append('FEATURES=[' + self._feats[0] + ']')
        else:
            self._misc.append('FEATURES')

    def empty_feats(self):
        self._feats = []

    def cleanup(self):
        self.cleanup_form()
        self.cleanup_misc()
        self.cleanup_features()
        self.cleanup_xpos()
        self.cleanup_deprel()

    def cleanup_deprel(self):
        if self._upos == 'PUNCT':
            self._deprel = 'punct'

    def cleanup_misc(self):
        new_misc = []
        misc_items = {}
        for item in self._misc:
            if 'FEATURES' in item:
                self._feats = self.get_FEATURES(item)
            else:
                left_side = item.split('=')[0]
                if left_side in misc_items:
                    misc_items[left_side] = misc_items[left_side] + \
                        '|' + item.replace(left_side + '=', '')
                else:
                    misc_items[left_side] = item.replace(left_side + '=', '')
        for item in misc_items:
            new_misc.append(item + '=[' + misc_items[item] + ']')
        # self._misc = new_misc
        self._misc = ''

    def get_FEATURES(self, item):
        item = item.replace('true', '').replace(
            'FEATURES=', '').replace('][', '&')
        cleaned = []
        if len(item) > 1:
            features = item.split('&')
            for feature in features:
                feature = feature.replace('[', '').replace(']', '')
                feature = feature.replace('psor', '[psor]')
                feature = feature.replace('subj', '[subj]')
                cleaned.append(feature)
        return cleaned

    def convert_deprel(self):
        if self._upos == 'DET':
            self._deprel = 'det'
        if 'Gloss=ser' in self._misc or self._form.lower() == "kan":
            self._deprel = 'cop'
            self._upos = 'AUX'
        if self._deprel == 'neg':
            self._upos = 'NEG'
        elif self._deprel == '--':
            if self._upos == 'SP':
                self._deprel = 'flat:foreign'
            else:
                self._deprel = 'flat'
        elif self._deprel == 'linker' and self._form == 'ima':
            self._upos = 'ADP'
        elif self._deprel == 'nme' and self._upos == 'Cas':
            self._deprel = 'case'
        elif self._deprel == 'nme':
            self._deprel = 'flat'
        if self._deprel in deprel_dict:
            self._deprel = deprel_dict[self._deprel]

    def convert_xpos(self):
        if self._xpos in xpos_dict:
            self._xpos = xpos_dict[self._xpos]

    def convert_feats(self):
        self._misc.append('Feats=' + '|'.join(self._feats))
        new_features = []
        for feat in self._feats:
            if self._upos not in ud_pos_tags:
                self.feat_to_upos(feat)
            self.feat_to_deprel(feat)
            more_feats = self.check_specials(feat)
            if more_feats:
                new_features.extend(more_feats)
            else:
                if feat in feats_dict:
                    from_dict = feats_dict[feat]
                    if len(from_dict.split('|')) > 1:
                        new_features.extend(from_dict.split('|'))
                    else:
                        new_features.append(from_dict)
        self._feats = copy.deepcopy(list(set(new_features)))

    def feat_to_upos(self, feat):
        if feat == 'VRoot' or feat == 'Root_VS' or feat == 'VRootES':
            self._upos = 'VERB'
        elif feat == 'NRootES' or feat == 'NRoot':
            self._upos = 'NOUN'
        elif feat == 'NRootNUM':
            self._upos = 'NUM'
        elif feat == 'PrnDem':
            self._upos = 'DET'
        elif feat == 'Part_Neg':
            self._upos = 'NEG'
        elif feat == 'Part_Contr':
            self._upos = 'PART'
        elif feat == 'NP':
            self._upos = 'NOUN'

    def feat_to_deprel(self, feat):
        if feat == '+SS' or feat == 'SS':
            self._deprel = 'advcl:ss'
        elif feat == '+DS' or feat == 'DS':
            self._deprel = 'advcl:ds'
        elif feat == 'PrnDem':
            self._deprel = 'det'

    def check_specials(self, feat):
        out = None
        if feat == 'PrnPers+3.Sg' and self._form.lower() == 'paykuna':
            out = ['Person=3', 'PronType=Prs']
        elif feat == 'PrnPers+2.Sg' and self._form.lower() == 'qamkuna':
            out = ['Person=3', 'PronType=Prs']
        return out

    def convert_upos(self):
        if self._upos == 'FLM':
            self._feats.append('Foreign=Yes')
        if self._upos in upos_dict:
            self._upos = upos_dict[self._upos]

    def convert_punct(self):
        if self._deprel == 'punct':
            self._upos = 'PUNCT'

    def insert_addition(self):
        if self._addition:
            for i in range(len(self._feats)):
                current = self._feats[i]
                if 'Number' in current or 'Person' in current:
                    currents = current.split('=')
                    currents[0] += '[' + self._addition + ']'
                    current = ''.join(currents)

    def cleanup_form(self):
        self._form = self._form.replace('-', '')
        self._form = self._form.replace('@dash', '-')

    def cleanup_features(self):
        new_feats = []
        for feat in self._feats:
            feat = feat.replace('|', '')
            if len(feat) > 0:
                new_feats.append(feat)
        self._feats = list(set(new_feats))
        if self._feats:
            self._feats.sort()

    def cleanup_xpos(self):
        self._xpos = '_'


suffixes = ['s.neg', 's.obj', 's.subj', 's.subj_iobj', 's.poss.subj', 's.poss']

deprel_dict = {
    'arg': 'obl:arg',
    'aux': 'aux',
    'ben': 'obl:ben',
    'caus': 'obl:caus',
    'co': 'cc',
    'iobj': 'iobj',
    # 'adv': '@advmod',
    'punc': 'punct',
    'r.disl': 'dislocated',  # ?
    'src': 'obl:src',
    'loc': 'nmod:loc',  # @obl:loc
    # 'subj': '@csubj',  # @usubj
    'acmp': 'nmod',  # @obl
    'mod': 'nmod',  # @obl, @advmod
    's.arg.claus': 's.arg',
    # 'sntc': 'root',
    'det': 'det',
    'goal': 'goal',
    'hab': 'hab',
    'qnt': 'nummod',
    'poss': 'case',
    'flm': 'flat:foreign',
    # 'p.arg': 'case',
    '--': 'flat'

}

xpos_dict = {
    'Root_VDeriv': 'Root',
    'Root_Num': 'Root',
    'Root_VS': 'Root'
}

upos_dict = {
    'Root_VDeriv': 'VERB',
    'Root_Num': 'NUM',
    'VDeriv': 'VERB',
    'NRootNUM': 'NUM',
    'Root_VS': 'VERB',
    'VRootES': 'VERB',
    'NRootES': 'NOUN',
    'FLM': 'X',
    'DUMMY': 'X',
    '$.': 'PUNCT',
    'SP': 'X',
    'NDeriv': 'NOUN',
    'Root_VDeriv_VDeriv': 'VERB'
}

feats_dict = {
    'abbrev': 'Abbr=Yes',  # moved from deprels
    '+Abl': 'Case=Abl',
    '+Acc': 'Case=Acc',
    '+Add': 'Case=Add',
    '+Aff': 'Mood=Affective',
    '+Ag': 'VerbForm=Vnoun|Deriv=Ag',
    '+Asmp_Emph': 'Evident=Assumptive',
    '+Ben': 'Case=Ben',
    '+Caus': 'Voice=Caus',
    '+Con_Inst': 'Case=Ins',  # wan?
    '+Con_Intr': '',  # blank on purpose
    '+Dat': 'Case=Dat',
    '+Def': 'Definite=Def',
    '+Des': 'Mood=Desiderative',
    '+Dim': 'Deriv=Dim',
    '+Dir': 'Motion=Dir',
    '+DirE': 'Evident=DirE',
    '+Distr': 'Case=Dis',
    '+DS': '',  # advcl:ds
    '+Fact': 'Evident=Fact',
    'FLM': 'Foreign=Yes',
    '+Foc': 'Focus=Yes',
    '+Fut': 'Tense=Fut',
    'Foreign=Yes': 'Foreign=Yes',
    '+Gen': 'Case=Gen',
    '+Hab': 'Tense=Past|Aspect=Hab',
    '+Imp': 'Mood=Imp',
    '+Inch': 'Aspect=Inch',
    '+IndE': 'Evident=IndE',
    '+Inf': 'VerbForm=Inf',
    '+IPst': 'Tense=Past|Evident=IndE',
    '+Instr': 'Case=Ins',
    '+Lim': 'Case=Lim',
    '+Lim_Aff': 'Case=Lim|Mood=Affective',
    '+Loc': 'Case=Loc',
    '_Neg': 'Polarity=Neg',
    '+Obl': 'Mood=Obligative',
    'Person=1+EXCL': 'Person=1|Inclusive=No',
    'Person=1+INCL': 'Person=1|Inclusive=Yes',
    '+Perf': 'Aspect=Perf',
    '+Pl=true': 'Number=Plur',
    '+Pl': 'Number=Plur',
    'Pl': 'Number=Plur',
    '+Poss': 'Poss=Yes',
    'Poss': 'Poss=Yes',
    '+Pres': 'Tense=Pres',
    '+Prog': 'Aspect=Prog',
    'PrnDem': 'PronType=Dem',
    'PrnPers+3.Sg': 'Number=Sing|Person=3|PronType=Prn',
    'PrnPers+2.Sg': 'Number=Sing|Person=2|PronType=Prn',
    '+Pst': 'Tense=Past',
    '+Rflx': 'Reflex=Yes',
    '+Rptn': 'Deriv=Rptn',
    '+Sg': 'Number=Sing',
    'Sg': 'Number=Sing',
    '+SS': '',  # advcl:ss
    '+Term': 'Case=Term',
    '+Top': 'Topic=Yes',
    '+Vdim': 'Degree=Dim',
    '+1.Pl.Excl': 'Number=Plur|Person=1|Inclusive=No',
    '+1.Pl.Incl': 'Number=Plur|Person=1|Inclusive=Yes',
    '+3': 'Person=3',
    '+2': 'Person=2',
    '+1': 'Person=1',
    '+2.Sg.Poss': 'Number[psor]=Sing|Person[psor]=2',
    '+3.Sg.Poss': 'Number[psor]=Sing|Person[psor]=3',
    '+1.Sg.Poss': 'Number[psor]=Sing|Person[psor]=1',
    '+3.Pl.Poss': 'Number[psor]=Plur|Person[psor]=3',
    '+1.Pl.Poss': 'Number[psor]=Plur|Person[psor]=1',
    '+1.Pl.Excl.Poss': 'Person[psor]=1|Inclusive[psor]=No|Number[psor]=Plur',
    '+1.Pl.Incl.Poss': 'Person[psor]=1|Inclusive[psor]=Yes|Number[psor]=Plur',
    '+1.Pl.Excl.Subj': 'Person[subj]=1|Inclusive[subj]=No|Number[subj]=Plur',
    '+1.Pl.Incl.Subj': 'Person[subj]=1|Inclusive[subj]=Yes|Number[subj]=Plur',
    '+1.Pl.Incl.Subj.Fut': 'Person[subj]=1|Inclusive[subj]=Yes|Number[subj]=Plur|Tense=Fut',
    '+1.Pl.Excl.Subj.Fut': 'Person[subj]=1|Inclusive[subj]=No|Number[subj]=Plur|Tense=Fut',
    '+Ass': 'Mood=Assistive',
    '+Autotrs': '',  # verbalizing suffix, can probably leave blank
    '+Emph': 'PronType=Emp',
    '+Neg': 'Polarity=Neg',
    '+Rem': '',  # denotes act of reflection or meditation
    '+Rgr_Iprs': '',  # regresssive (go back) or impersonal marker
    '+Sim': '',  # similarity, like usually postposition so make ADP?
    '+Int': '',  # marks an intentional or careless action
    '+Rep': '',  # repetitive action
    '+Iclsv': 'Inclusive=Yes',
    '+Dat_Ill': 'Case=Ill',
    '+Pot': 'Mood=Potential',
    '+Kaus': 'Voice=Caus',
    '+Rzpr': 'Tense=Fut|Apesct=Perf|VerbForm=Part',
    '+Rel': 'PronType=Rel',
    '+Disc': '',  # do not think carryover feature necessary
    'Part_Conec': '',  # do not think this should carry over as feature
    '+Intsoc': 'Case=Intrative',
    '+Trs': '',  # translocative. how to do this? motion?
    '+Perdur': 'Aspect=Perdur',  # perdurative, actions takes place over long time
    '+Multi': '',  # multiplier, multiple objects or subjects involved, action happens multiple times
    '+Reub': '',  # reubicative,
    '+Dist': 'Case=Dis',
    '+MRep': '',  # repetitive
    '+Abtmp': '',  # if with pacha make an ADP?
    '+MPoss': 'Poss=Yes',  # multipossessor, possessor of multiple things
    '+Soc': '',  # social means with but can only be used for people
    '+Intrup': '',  # iterative, indicates a recurring or repeated action
    '+QTop': 'Topic=Yes',  # topic marker in questions
    'Part_Affir': 'Polarity=Pos',  # Polarity=Pos??
    '+Char': '',  # characterizer guessing just leave blank
    '+Proloc': 'Case=Prolocative'
}


ud_pos_tags = ['ADJ', 'ADV', 'INTJ', 'NOUN', 'PROPN', 'VERB', 'ADP', 'AUX',
               'CCONJ', 'DET', 'NUM', 'PART', 'PRON', 'SCONJ', 'PUNCT', 'SYM', 'X']
