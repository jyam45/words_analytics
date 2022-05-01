#!/usr/bin/python3
import argparse
import networkx as nx
import matplotlib.pyplot as plt
import jpn_analyzer as jp

_DICPATH  = "/usr/local/lib/mecab/dic/mecab-ipadic-neologd" # 辞書
_FONTNAME = "Hiragino Sans GB" # 日本語

def main(input_file,output_file,parser="mecab",dicpath=_DICPATH,method="jaccard",edge_tol=None,max_view=50,max_size=2000,font=_FONTNAME):

	text_file = open(input_file)
	bindata = text_file.read()
	txt = bindata
	
	analyzer = jp.JapaneseAnalyzer(parser=parser,mecab_dicpath=dicpath)
	
	node_list,edge_list = analyzer.to_network_data(txt,method=method,edge_tol=edge_tol,max_view=max_view)
	
	# ノード属性を作る
	node_type = {}
	node_size = {}
	max_freq = 0
	for node in node_list:
		word,freq,pos = node
		if not word in node_size:
			node_size[word]=0
		if not pos in node_type:
			node_type[pos]=[]
		node_size[word] += int(freq)
		node_type[pos].append(word)

	# ノードの最大サイズ
	max_freq = 0
	for word in node_size:
		freq = node_size[word]
		max_freq = max(max_freq, int(freq))

	# エッジの最大サイズ
	max_common = 0
	for edge in edge_list:
		word1,word2,common,weight=edge
		max_common = max(max_common,int(common))

	# 円のサイズを調整する
	for word in node_size:
		node_size[word] = node_size[word] * max_size / max_freq
	
	#print(node_size)
	#print(node_type)
	
	# エッジを作る
	edges = []
	widths= []
	colors= []
	width_coeff = 10/max_common
	color_coeff = 10/max_common 
	for item in edge_list :
		node1 = item[0]
		node2 = item[1]
		width = item[2] # common
		weight= item[3] # Jaccard
		edges.append((node1,node2,{'weight':weight}))
		widths.append(int(width)*width_coeff)
		colors.append(int(width)*color_coeff)
	
	#print(edges)
	
	# グラフを作る
	graph = nx.Graph(edges)
	
	# 図の作成
	plt.figure(figsize=(10,8))
	
	# 図のレイアウトを作成
	layout = nx.spring_layout(graph,k=0.4)
	
	# ノードとエッジの描画
	nx.draw_networkx_edges(graph, layout, width=widths, edge_color=colors, 
	                       edge_vmin=0, edge_vmax=10, alpha=0.6, edge_cmap=plt.cm.Blues)

	color_list=["orange","tomato","yellowgreen","grey"]
	color_size=len(color_list)
	icolor=0
	for pos in node_type:
		nx.draw_networkx_nodes(graph, layout,
		                 nodelist=[node for node in graph.nodes() if node in node_type[pos]],
		                 node_size=[node_size[node] for node in graph.nodes() if node in node_type[pos]],
		                 node_color=color_list[icolor] , alpha=0.5)
		if icolor < color_size-1 : icolor += 1

	nx.draw_networkx_labels(graph, layout, font_size=10, font_family=font)
	
	# 軸表示なし
	plt.axis('off')
	
	plt.savefig(output_file)
	#plt.show()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="共起ネットワーク画像を作成します。")
	parser.add_argument("input_file",help="解析するテキストファイル名")
	parser.add_argument("output_file",help="出力画像ファイル名")
	parser.add_argument("-p","--parser",default="mecab",help="日本語の形態素解析器 ['mecab'|'janome'] (default:mecab)")
	parser.add_argument("-f","--font",default=_FONTNAME,help="日本語フォントファミリー (default:"+str(_FONTNAME)+")")
	parser.add_argument("-d","--dict",default=_DICPATH,help="日本語形態素辞書へのパス")
	parser.add_argument("-c","--cov_method",default="jaccard",help="共起計算方法 ['jaccard'|'2gram'|'3gram'] (default:jaccard)")
	parser.add_argument("-m","--max",default=50,help="最大表示数 (default:50)")
	parser.add_argument("-s","--max_size",default=2000,help="ノード最大サイズ (default:2000)")
	parser.add_argument("-t","--edge_tol",default=None,help="共起判定の閾値 (default:None)")
	args = parser.parse_args()
	main(args.input_file,args.output_file,
	     parser=args.parser, dicpath=args.dict, method=args.cov_method, edge_tol=args.edge_tol,
	     max_view=int(args.max), max_size=int(args.max_size), font=args.font
	)
