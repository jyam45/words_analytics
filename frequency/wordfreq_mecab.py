import MeCab

input_file = "jptest.txt"
output_file= "jptest.png"

pos_keep_list = ["名詞","動詞","形容詞"] # pos = 品詞
pos_stop_list = ["名詞,非自立","名詞,代名詞","名詞,接尾","動詞,非自立","動詞,接尾"]
#pos_stop_list = ["非自立","代名詞","接尾"]
word_stop_list= ["する","なる","やる","ある","できる"]

parser = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")

text_file = open(input_file)
bindata = text_file.read()
txt = bindata

lines = txt.split("\r\n")
wfreq = {}
for line in lines:
	token_iter = parser.parseToNode(line)
	while token_iter:
		#word = token_iter.surface
		word = token_iter.feature.split(',')[6] #基本形
		pos  = token_iter.feature
		token_iter = token_iter.next
		target = False
		for item in pos_keep_list:
			if pos.find(item) == 0 : 
				target = True
				break
		if not target : continue
		target = True
		for item in pos_stop_list:
			if pos.find(item) == 0 :
				target = False
				break
		if not target : continue
		if word in word_stop_list : continue
		if not word in wfreq :
			wfreq[word] = 0
		wfreq[word] += 1
		print(word,"\t",pos)

wfreq_sorted = sorted(wfreq.items(), key=lambda x:x[1], reverse=True)
for word, cnt in wfreq_sorted[:100]:
	print("word=\"{0}\",freq=\"{1}\"".format(word,cnt), end="\n")


