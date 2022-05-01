#!/usr/bin/python3
import argparse
import json
import jpn_analyzer as jp

_DICPATH  = "/usr/local/lib/mecab/dic/mecab-ipadic-neologd" # 辞書

def main(input_file,max_view=100,parser="mecab",dicpath=_DICPATH,form="keyval"):

	text_file = open(input_file)
	bindata = text_file.read()
	txt = bindata
	
	analyzer = jp.JapaneseAnalyzer(parser=parser,mecab_dicpath=dicpath)
	
	wfreq = analyzer.count_words(txt)
	
	wfreq_sorted = sorted(wfreq.items(), key=lambda x:x[1], reverse=True)
	
	n = min(len(wfreq_sorted),max_view)

	if form == "tsv":
		for word, cnt in wfreq_sorted[:n]:
			print("{0}\t{1}".format(word,cnt), end="\n")
	elif form == "csv":
		for word, cnt in wfreq_sorted[:n]:
			print("{0},{1}".format(word,cnt), end="\n")
	elif form == "keyval":
		for word, cnt in wfreq_sorted[:n]:
			print("word=\"{0}\",freq=\"{1}\"".format(word,cnt), end="\n")
	elif form == "json":
		json_dic={}
		words=[]
		freqs=[]
		for word, cnt in wfreq_sorted[:n]:
			words.append(word)
			freqs.append(cnt)
		json_dic["size"]=n	
		json_dic["words"]=words
		json_dic["freqs"]=freqs
		print(json.dumps(json_dic,separators=(',',':')))
	else:
		raise SyntaxError("Invalid format name : "+form)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="テキストファイル内の名詞、動詞、形容詞を数えます。")
	parser.add_argument("input_file",help="解析するテキストファイル名")
	parser.add_argument("-p","--parser",default="mecab",help="['mecab'|'janome'] 日本語の形態素解析器 (default:mecab)")
	parser.add_argument("-f","--format",default="keyval",help="['tsv'|'csv'|'keyval'|'json'] 出力形式 (default:keyval)")
	parser.add_argument("-d","--dict",default=_DICPATH,help="日本語形態素辞書へのパス")
	parser.add_argument("-m","--max",default=100,help="最大表示数")
	args = parser.parse_args()
	main(args.input_file,
	     parser=args.parser, dicpath=args.dict,
	     max_view=int(args.max), form=args.format
	)
