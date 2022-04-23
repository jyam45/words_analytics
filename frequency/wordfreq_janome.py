from janome.tokenizer import Tokenizer
from janome.tokenfilter import CompoundNounFilter
from janome.tokenfilter import POSKeepFilter
from janome.tokenfilter import POSStopFilter

input_file = "jptest.txt"
output_file= "jptest.png"

pos_keep_list = ["名詞","動詞","形容詞"] # pos = 品詞
pos_stop_list = ["名詞,非自立","名詞,代名詞","名詞,接尾","動詞,非自立","動詞,接尾"]
word_stop_list= ["する","し","なっ","やっ","あっ"]

tknizer = Tokenizer()
tkfilter= CompoundNounFilter()
keepfilter = POSKeepFilter(pos_keep_list)
stopfilter = POSStopFilter(pos_stop_list)

text_file = open(input_file)
bindata = text_file.read()
txt = bindata

lines = txt.split("\r\n")
wfreq = {}
for line in lines:
	tokens = tknizer.tokenize(line)
	tokens = tkfilter.apply(tokens)
	tokens = keepfilter.apply(tokens)
	tokens = stopfilter.apply(tokens)
	for token in tokens:
		word = token.surface
		pos = token.part_of_speech # 品詞
		#word = pos.split(',')[6] # 基本形
		if word in word_stop_list : continue
		if not word in wfreq :
			wfreq[word] = 0
		wfreq[word] += 1
		print(word,pos)

wfreq_sorted = sorted(wfreq.items(), key=lambda x:x[1], reverse=True)
for word, cnt in wfreq_sorted[:100]:
	print("word=\"{0}\",freq=\"{1}\"".format(word,cnt), end="\n")


