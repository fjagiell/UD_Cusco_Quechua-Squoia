span=open('texts/es/DW_es.tok')
quz=open('texts/quz/DW_quz.txt')
conll=open('quz/DW/DW.conllu')
out=open('DWwithsentout.conllu', 'w')
line='xx'
spanlist=[]
while line:
	line=span.readline()
	spanlist.append(line)
line='xx'
quzlist=[]
while line:
	line=quz.readline()
	quzlist.append(line)
line='xx'
num=0
i=0
while line:
	line=conll.readline()
	textline=line.split()
	if num<=len(quzlist)-1 and num<=len(spanlist)-1 and len(textline)>=4:
		if textline[3] in quzlist[num] and 'text' in line:
			if num>0:
				out.write('quz: ' + quzlist[num])
				out.write('es: ' + spanlist[num-1])
				num+=1
			else:
				out.write('quz: ' + quzlist[num])
				num+=1
			
	out.write(line)