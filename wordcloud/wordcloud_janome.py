from wordcloud import WordCloud
from janome.tokenizer import Tokenizer
from janome.tokenfilter import CompoundNounFilter
from janome.tokenfilter import POSKeepFilter
from janome.tokenfilter import POSStopFilter

input_file = "jptest.txt"
output_file= "jptest.png"

pos_keep_list = ["名詞","動詞","形容詞"] # pos = 品詞
pos_stop_list = ["名詞,非自立","名詞,代名詞","名詞,接尾","動詞,非自立","動詞,接尾"]
word_stop_list= ["する","し","なっ","やっ","あっ"]

fontpath = "/System/Library/Fonts/Hiragino Sans GB.ttc" # 日本語
#fontpath = "System/Library/Fonts/HelveticaNeue.ttc"

#--------------------------------------------

tknizer = Tokenizer()
tkfilter= CompoundNounFilter()
keepfilter = POSKeepFilter(pos_keep_list)
stopfilter = POSStopFilter(pos_stop_list)

text_file = open(input_file)
bindata = text_file.read()
txt = bindata

lines = txt.split("\r\n")
words = ""
for line in lines:
	tokens = tknizer.tokenize(line)
	tokens = tkfilter.apply(tokens)
	tokens = keepfilter.apply(tokens)
	tokens = stopfilter.apply(tokens)
	for token in tokens:
		word = token.surface
		if word in word_stop_list : continue
		ps = token.part_of_speech # 品詞
		print(word,ps)
		words += word
		words += " "

wordcloud = WordCloud(background_color="white",font_path=fontpath,width=800,height=600).generate(words)
wordcloud.to_file(output_file)

