from wordcloud import WordCloud
import MeCab

input_file = "jptest.txt"
output_file= "jptest.png"

pos_keep_list = ["名詞","動詞","形容詞"] # pos = 品詞
pos_stop_list = ["名詞,非自立","名詞,代名詞","名詞,接尾","動詞,非自立","動詞,接尾"]
word_stop_list= ["する","なる","やる","ある","できる"]
#word_stop_list= ["する","し","なっ","やっ","あっ"]

fontpath = "/System/Library/Fonts/Hiragino Sans GB.ttc" # 日本語
#fontpath = "System/Library/Fonts/HelveticaNeue.ttc"

#--------------------------------------------

parser = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")

text_file = open(input_file)
bindata = text_file.read()
txt = bindata

lines = txt.split("\r\n")
words = ""
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
		words += word
		words += " "

wordcloud = WordCloud(background_color="white",font_path=fontpath,width=800,height=600).generate(words)
wordcloud.to_file(output_file)

