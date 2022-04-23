import networkx as nx
import matplotlib.pyplot as plt
import MeCab

#設定値
input_file = "jptest.txt"
edge_file  = "jptest_edge.csv"
node_file  = "jptest_node.csv"
image_file = "jptest.png"

pos_keep_list = ["名詞","動詞","形容詞"] # pos = 品詞
pos_stop_list = ["名詞,非自立","名詞,代名詞","名詞,接尾","動詞,非自立","動詞,接尾"]
word_stop_list= ["する","ある","なる","やる","できる"]
#word_stop_list= []

#fontpath = "System/Library/Fonts/HelveticaNeue.ttc"
#fontpath = "/System/Library/Fonts/Hiragino Sans GB.ttc" # 日本語
font = "Hiragino Sans GB" # 日本語

jaccard_threshold = 0.1
max_shown = 50  # top number of frequency words
max_size = 3000 # max circle size

#--------------------------------------------

parser = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")

text_file = open(input_file)
bindata = text_file.read()
txt = bindata

# ひとまず、文書を一行とする。
lines = txt.split("\n")
#print(lines)

# 形態素解析で、一つの文書（一行）をワードリストに変換し、文書リストを作成する。
words = ""
doc_list = []
freq_dic = {} # ワードが含まれる文書の数
pos_dic = {}
for line in lines:
	# ワードリスト初期化
	word_list = []
	token_iter = parser.parseToNode(line)
	while token_iter:
		word = token_iter.feature.split(',')[6] # 基本形に変換
		pos  = token_iter.feature
		token_iter = token_iter.next
		# 必要な品詞を抽出
		target = False
		for item in pos_keep_list:
			if pos.find(item) == 0 : 
				target = True
				break
		if not target : continue
		# 不要な品詞を除外
		target = True
		for item in pos_stop_list:
			if pos.find(item) == 0 :
				target = False
				break
		if not target : continue
		# 除外ワード削除
		if word in word_stop_list : continue
		# 重複削除
		if word in word_list : continue
		# ワードリスト追加
		word_list.append(word)
		# ワードが含まれる文書の数をカウント
		if not word in freq_dic :
			freq_dic[word] = 0
		freq_dic[word] += 1 
		#print(word,freq_dic[word])
		# 品詞辞書を作成
		if not word in pos_dic :
			pos_dic[word] = pos
	# ワードリストを文書リストに追加
	#print(word_list)
	doc_list.append(word_list)

#print(doc_list)

# 未対応語"*"を削除する
freq_dic.pop("*",0)

# Jaccard係数を計算する
edge_list = []
word_list = sorted(freq_dic.items(), key=lambda x:x[1], reverse=True) # 出現回数順に並べ替え
n = min( len(word_list), max_shown )
max_common = 0
print(word_list[0:n])
i=0
while i < n :
	word1,nsolo1 = word_list[i]
	j = i+1
	while j < n :
		word2,nsolo2 = word_list[j]
		common = 0
		# ワードが共通に含まれる文書の数
		for doc in doc_list :
			#print(word1,' ',word2,' ',doc)
			if word1 in doc and word2 in doc :
				common += 1
		max_common = max( max_common, common )
		# Jaccard係数
		#if common > 0 :
		#	print(nsolo1,' ',nsolo2,' ',common)
		jaccard = common / ( nsolo1 + nsolo2 - common )
		# エッジリストの作成
		if jaccard > jaccard_threshold :
			edge_list.append((word1,word2,common,jaccard))
		j += 1
	i += 1

# ノードの保存
nodetext = ""
for item in word_list[0:n]:
	word,freq = item
	pos  = pos_dic[word]
	text = word+","+str(freq)+","+pos+"\n"
	nodetext += text
csv_file=open(node_file,mode="w")
csv_file.write(nodetext)

# エッジの保存
edgetext = ""
for item in edge_list :
	text = item[0]+","+item[1]+","+str(item[2])+","+str(item[3])+"\n"
	#print(text)
	edgetext += text
csv_file=open(edge_file,mode="w")
csv_file.write(edgetext)

# ノード属性を作る
node_type = {"名詞":[],"動詞":[],"形容詞":[]}
node_size = {}
max_freq = 0
i = 0
while i < n :
	word, freq = word_list[i] # 語,出現頻度
	pos = pos_dic[word].split(",")[0] # 品詞
	#print(word,freq,pos)
	if not word in node_size:
		node_size[word]=0
	node_size[word] += int(freq)
	max_freq = max(max_freq, int(freq))
	if not pos in node_type:
		node_type[pos]=[]
	node_type[pos].append(word)
	i+=1

# サイズを調整する
for word in node_size:
	node_size[word] = node_size[word] * max_size / max_freq

print(node_size)
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

print(edges)

# グラフを作る
graph = nx.Graph(edges)

# 図の作成
plt.figure(figsize=(10,8))

# 図のレイアウトを作成
layout = nx.spring_layout(graph,k=0.4)

# ノードとエッジの描画
nx.draw_networkx_edges(graph, layout, width=widths, edge_color=colors, edge_vmin=0, edge_vmax=10, alpha=0.6, edge_cmap=plt.cm.Blues)
nx.draw_networkx_nodes(graph, layout, nodelist=[node for node in graph.nodes() if node in node_type["名詞"]],   node_size=[node_size[node] for node in graph.nodes() if node in node_type["名詞"]],   node_color="orange" , alpha=0.5)
nx.draw_networkx_nodes(graph, layout, nodelist=[node for node in graph.nodes() if node in node_type["動詞"]],   node_size=[node_size[node] for node in graph.nodes() if node in node_type["動詞"]],   node_color="tomato"    , alpha=0.5)
nx.draw_networkx_nodes(graph, layout, nodelist=[node for node in graph.nodes() if node in node_type["形容詞"]], node_size=[node_size[node] for node in graph.nodes() if node in node_type["形容詞"]], node_color="yellowgreen", alpha=0.5)
nx.draw_networkx_labels(graph, layout, font_size=10, font_family=font)

# 軸表示なし
plt.axis('off')

plt.savefig(image_file)
plt.show()
