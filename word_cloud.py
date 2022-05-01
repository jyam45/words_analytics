#!/usr/bin/python3
import argparse
import wordcloud as wc
import jpn_analyzer as jp

#from wordcloud import WordCloud

#default values
_FONTPATH = "/System/Library/Fonts/Hiragino Sans GB.ttc" # 日本語
_DICPATH  = "/usr/local/lib/mecab/dic/mecab-ipadic-neologd" # 辞書

def main(input_file,output_file,bg_color="white",fontpath=_FONTPATH,width=800,height=600,parser="mecab",dicpath=_DICPATH):
	text_file = open(input_file)
	bindata = text_file.read()
	txt = bindata
	
	analyzer = jp.JapaneseAnalyzer(parser=parser,mecab_dicpath=dicpath)
	
	words = analyzer.to_seperated_text(txt)
	
	wordcloud = wc.WordCloud(background_color=bg_color,font_path=fontpath,width=width,height=height).generate(words)
	wordcloud.to_file(output_file)



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="日本語のワードクラウド画像を生成します。")
	parser.add_argument("input_file",help="解析するテキストファイル名")
	parser.add_argument("output_file",help="出力画像ファイル名")
	parser.add_argument("-p","--parser",default="mecab",help="['mecab'|'janome'] 日本語の形態素解析器 (default:mecab)")
	parser.add_argument("-f","--font",default=_FONTPATH,help="日本語フォントファイルへのパス")
	parser.add_argument("-d","--dict",default=_DICPATH,help="日本語形態素辞書へのパス")
	parser.add_argument("--bgcolor",default="white",help="ワードクラウド画像の背景色")
	parser.add_argument("--width",default=800,help="ワードクラウド画像の横幅")
	parser.add_argument("--height",default=600,help="ワードクラウド画像の高さ")
	args = parser.parse_args()
	main(args.input_file,args.output_file,
	     parser=args.parser, dicpath=args.dict,
	     bg_color=args.bgcolor, fontpath=args.font, width=int(args.width), height=int(args.height)
	)
