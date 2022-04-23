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
word_stop_list= ["する","ある","なる","やる","できる","*"]
#word_stop_list= ["する","*"]
#word_stop_list= []

#fontpath = "System/Library/Fonts/HelveticaNeue.ttc"
#fontpath = "/System/Library/Fonts/Hiragino Sans GB.ttc" # 日本語
font = "Hiragino Sans GB" # 日本語

threshold = 1
max_shown = 50  # top number of frequency words
max_size = 2000 # max circle size

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
		# ワードリスト追加
		word_list.append(word)
		# ワードの出現頻度
		if not word in freq_dic:
			freq_dic[word] = 0
		freq_dic[word] += 1
		# 重複削除
		#if word in word_list : continue
		# 品詞辞書を作成
		if not word in pos_dic :
			pos_dic[word] = pos
	# ワードリストを文書リストに追加
	#print(word_list)
	doc_list.append(word_list)

#print(doc_list)

# 3 gram のワードペアの頻度を算出する
word_pair_freq = {}
for words in doc_list:
	n = len(words)
	i = 0
	# n > 2
	while i < n-2:
		word1 = words[i]
		word2 = words[i+1]
		word3 = words[i+2]
		pair12 = (word1,word2)
		pair13 = (word1,word3)
		pair21 = (word2,word1)
		pair31 = (word3,word1)
		# 重複除外
		if not pair12 in word_pair_freq and not pair21 in word_pair_freq :
			word_pair_freq[pair12] = 0	
		if pair12 in word_pair_freq:
			word_pair_freq[pair12] += 1
		else:
			word_pair_freq[pair21] += 1

		if not pair13 in word_pair_freq and not pair31 in word_pair_freq:
			word_pair_freq[pair13] = 0	
		if pair13 in word_pair_freq:
			word_pair_freq[pair13] += 1
		else:
			word_pair_freq[pair31] += 1
		i += 1
	# 終端処理
	if n > 2 :
		pair23 = (word2,word3)
		if not pair23 in word_pair_freq:
			word_pair_freq[pair23] = 0	
		word_pair_freq[pair23] += 1
	# n = 2 の場合
	if n == 2 :
		word1 = words[i]
		word2 = words[i+1]
		pair12 = (word1,word2)
		if not pair12 in word_pair_freq:
			word_pair_freq[pair12] = 0	
		word_pair_freq[pair12] += 1

print(word_pair_freq)

# エッジリストを計算する
edge_list = []
word_pair_list = sorted(word_pair_freq.items(), key=lambda x:x[1], reverse=True) # 出現回数順に並べ替え
n = min( len(word_pair_list), max_shown )
max_common = max(word_pair_freq.values())
print(word_pair_list[0:n])
i=0
while i < n :
	pair,nfreq = word_pair_list[i]
	if nfreq > threshold :
		edge_list.append((pair[0],pair[1],nfreq))
	i += 1

print(edge_list)

# ノードの保存
nodetext = ""
words = []
for item in word_pair_list[0:n]:
	pair,dfreq = item
	j = 0
	while j < 2 :
		word = pair[j]
		if not word in words :
			freq = freq_dic[word]
			pos  = pos_dic[word]
			text = word+","+str(freq)+","+pos+"\n"
			nodetext += text
			words.append(word)
		j+=1
csv_file=open(node_file,mode="w")
csv_file.write(nodetext)

# エッジの保存
edgetext = ""
for item in edge_list :
	text = item[0]+","+item[1]+","+str(item[2])+"\n"
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
	pair, efreq = word_pair_list[i]
	j = 0
	while j < 2 :
		word = pair[j]
		freq = freq_dic[word]
		pos = pos_dic[word].split(",")[0] # 品詞
		if not word in node_size:
			node_size[word]=0
		node_size[word] += int(freq)
		max_freq = max(max_freq, int(freq))
		if not pos in node_type:
			node_type[pos]=[]
		node_type[pos].append(word)
		j+=1
	i+=1



# サイズを調整する
for word in node_size:
	node_size[word] = node_size[word] * max_size / max_freq

print(node_size)
print(node_type)

# エッジを作る
edges = []
widths= []
colors= []
width_coeff = 10/max_common
color_coeff = 10/max_common 
for item in edge_list :
	node1 = item[0]
	node2 = item[1]
	width = item[2] # freq
	edges.append((node1,node2,{'weight':width}))
	widths.append(int(width)*width_coeff)
	colors.append(int(width)*color_coeff)

print("edges",edges,len(edges))
print("widths",widths,len(widths))
print("colors",colors,len(colors))


# グラフを作る
graph = nx.Graph(edges)
print(len(graph.edges()))

# 図の作成
plt.figure(figsize=(10,8))

# 図のレイアウトを作成
layout = nx.spring_layout(graph,k=0.8)

# ノードとエッジの描画
nx.draw_networkx_edges(graph, layout, width=widths, edge_color=colors, edge_cmap=plt.cm.Blues, edge_vmin=0, edge_vmax=10, alpha=0.6)
#nx.draw_networkx_edges(graph, layout, width=widths, edge_color="blue", edge_cmap=plt.cm.Blues, edge_vmin=0, edge_vmax=10, alpha=0.6)
nx.draw_networkx_nodes(graph, layout, nodelist=[node for node in graph.nodes() if node in node_type["名詞"]],   node_size=[node_size[node] for node in graph.nodes() if node in node_type["名詞"]],   node_color="orange" , alpha=0.5)
nx.draw_networkx_nodes(graph, layout, nodelist=[node for node in graph.nodes() if node in node_type["動詞"]],   node_size=[node_size[node] for node in graph.nodes() if node in node_type["動詞"]],   node_color="tomato"    , alpha=0.5)
nx.draw_networkx_nodes(graph, layout, nodelist=[node for node in graph.nodes() if node in node_type["形容詞"]], node_size=[node_size[node] for node in graph.nodes() if node in node_type["形容詞"]], node_color="yellowgreen", alpha=0.5)
nx.draw_networkx_labels(graph, layout, font_size=10, font_family=font)

# 軸表示なし
plt.axis('off')

plt.savefig(image_file)
#plt.show()
