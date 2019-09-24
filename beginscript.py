IN=open('DW.conllu')
OUT=open('DW.conllu.begin', 'w')
line='xx'
while True:
	line=IN.readline()
	if not line: 
		break
	line = line.strip('\n')
	if line == '':
		continue
	if line[0]=='#':
		continue
	line=line.split("\t")
	if line[5]=='+Abl':
		line[5]='Case=Abl'
	if line[5]=='+Acc':
		line[5]='Case=Acc'
	if line[5]=='+Add':
		line[5]='Case=Add'
	if line[5]=='+Ben':
		line[5]='Case=Ben'
	if line[5]=='+Gen':
		line[5]='Case=Gen'
	if line[5]=='+Dat':
		line[5]='Case=Dat'
	if line[5]=='+Loc':
		line[5]='Case=Loc'
	if 'Inst' in line[5]:
		line[5]='Case=Ins'
	if line[5]=='+Perf':
		line[5]='Aspect=Perf'
	if line[5]=='+Prog':
		line[5]='Aspect=Prog'
	if line[5]=='+Caus':
		line[5]='Voice=Caus'
	if '+Dim' in line[5]:
		line[5]=line[5]+'|Deriv=Dim'
	if 'Fut' in line[5]:
		line[5]=line[5]+'|Tense=Fut'
	if 'Hab' in line[5]:
		line[5]=line[5]+'|Tense=Past|Aspect=Hab'
	if 'Imp' in line[5]:
		line[5]=line[5]+'|Mood=Imp'
	if 'Ipst' in line[5]:
		line[5]=line[5]+'|Tense=Past|Evident=Sqa'
	if 'Pres' in line[5]:
		line[5]=line[5]+'|Tense=Pres'
	if 'Pst' in line[5]:
		line[5]=line[5]+'|Tense=Past'
	if 'Rflx' in line[5]:
		line[5]=line[5]+'|Reflexive=Yes'
	if 'Sg' in line[5]:
		line[5]=line[5]+'|Number=Sing'
	




IN.close()
OUT.close()