import janome as jn
import MeCab  as mb

class JapaneseAnalyzer:

	def __init__ (self,parser="janome",mecab_dicpath=None):
		self.parser_     = parser
		self.keep_poses_ = ["名詞","動詞","形容詞"]  
		self.stop_poses_ = ["名詞,非自立","名詞,代名詞","名詞,接尾","動詞,非自立","動詞,接尾"]
		self.stop_words_ = ["する","なる","やる","ある","できる","し","なっ","やっ","あっ"]
		self.mecab_dic_  = mecab_dicpath

	def _create_wordcloud_textdata_by_janome(self,text):
		tknizer    = jn.tokenizer.Tokenizer()
		tkfilter   = jn.tokenfilter.CompoundNounFilter()
		keepfilter = jn.tokenfilter.CPOSKeepFilter(self.keep_poses_)
		stopfilter = jn.tokenfilter.CPOSStopFilter(self.stop_poses_)
		
		lines = text.split("\r\n")
		words = ""
		for line in lines:
			tokens = tknizer.tokenize(line)
			tokens = tkfilter.apply(tokens)
			tokens = keepfilter.apply(tokens)
			tokens = stopfilter.apply(tokens)
			for token in tokens:
				word = token.surface
				if word in self.stop_words_ : continue
				#ps = token.part_of_speech # 品詞
				#print(word,ps)
				words += word
				words += " "
		return words

	def _create_wordcloud_textdata_by_mecab(self,text):
		dicpath = ""
		if self.mecab_dic_ is not None:
			dicpath = "-d " + self.mecab_dic_
		parser = mb.Tagger(dicpath)
		
		lines = text.split("\r\n")
		words = ""
		for line in lines:
			token_iter = parser.parseToNode(line)
			while token_iter:
				#word = token_iter.surface
				word = token_iter.feature.split(',')[6] #基本形
				pos  = token_iter.feature
				token_iter = token_iter.next
				target = False
				for item in self.keep_poses_:
					if pos.find(item) == 0 : 
						target = True
						break
				if not target : continue
				target = True
				for item in self.stop_poses_:
					if pos.find(item) == 0 :
						target = False
						break
				if not target : continue
				if word in self.stop_words_ : continue
				words += word
				words += " "
		return words

	def _count_word_frequency_by_janome(self,text):
		tknizer    = jn.tokenizer.Tokenizer()
		tkfilter   = jn.tokenfilter.CompoundNounFilter()
		keepfilter = jn.tokenfilter.CPOSKeepFilter(self.keep_poses_)
		stopfilter = jn.tokenfilter.CPOSStopFilter(self.stop_poses_)
		
		lines = text.split("\r\n")
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
				#print(word,pos)

		# 未対応語"*"を削除する
		wfreq.pop("*",0)
		
		return wfreq

	def _count_word_frequency_by_mecab(self,text):
		dicpath = ""
		if self.mecab_dic_ is not None:
			dicpath = "-d " + self.mecab_dic_
		parser = mb.Tagger(dicpath)
	
		lines = text.split("\r\n")
		wfreq = {}
		for line in lines:
			token_iter = parser.parseToNode(line)
			while token_iter:
				#word = token_iter.surface
				word = token_iter.feature.split(',')[6] #基本形
				pos  = token_iter.feature
				token_iter = token_iter.next
				target = False
				for item in self.keep_poses_:
					if pos.find(item) == 0 : 
						target = True
						break
				if not target : continue
				target = True
				for item in self.stop_poses_:
					if pos.find(item) == 0 :
						target = False
						break
				if not target : continue
				if word in self.stop_words_ : continue
				if not word in wfreq :
					wfreq[word] = 0
				wfreq[word] += 1
				#print(word,"\t",pos)

		# 未対応語"*"を削除する
		wfreq.pop("*",0)
		
		return wfreq

	def _parse_to_documents_by_mecab(self,text):
		dicpath = ""
		if self.mecab_dic_ is not None:
			dicpath = "-d " + self.mecab_dic_
		parser = mb.Tagger(dicpath)
	
		lines = text.split("\n")
		
		# 形態素解析で、一つの文書（一行）をワードリストに変換し、文書リストを作成する。
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
				for item in self.keep_poses_:
					if pos.find(item) == 0 : 
						target = True
						break
				if not target : continue
				# 不要な品詞を除外
				target = True
				for item in self.stop_poses_:
					if pos.find(item) == 0 :
						target = False
						break
				if not target : continue
				# 除外ワード削除
				if word in self.stop_words_ : continue
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
					#pos_dic[word] = pos.split(",")[0] # 品詞のみ
					pos_dic[word] = pos
			# ワードリストを文書リストに追加
			#print(word_list)
			doc_list.append(word_list)

		# 未対応語"*"を削除する
		freq_dic.pop("*",0)
		
		return doc_list,freq_dic,pos_dic


	def _create_network_by_jaccard(self,doc_list,freq_dic,pos_dic,tol=0.1,max_view=50):

		# Jaccard係数を計算する
		edge_list = []
		word_list = sorted(freq_dic.items(), key=lambda x:x[1], reverse=True) # 出現回数順に並べ替え
		n = min( len(word_list), max_view )
		max_common = 0
		#print(word_list[0:n])
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
				if jaccard > tol :
					edge_list.append((word1,word2,common,jaccard))
				j += 1
			i += 1

		# ノードリスト(name,size,type)を作成する
		words = []
		node_list= []
		for word,nsolo in word_list[:n]:
			freq = freq_dic[word]
			pos  = pos_dic[word].split(",")[0] # 品詞のみ
			node_list.append((word,freq,pos))

		return node_list,edge_list # nodes,edges

	def _compute_pair_freq_by_2gram(self,doc_list):
		# 2 gram のワードペアの頻度を算出する
		word_pair_freq = {}
		for words in doc_list:
			n = len(words)
			i = 0
			# n > 1
			while i < n-1:
				word1 = words[i]
				word2 = words[i+1]
				pair12 = (word1,word2)
				pair21 = (word2,word1)
				# 重複除外
				if not pair12 in word_pair_freq and not pair21 in word_pair_freq :
					word_pair_freq[pair12] = 0	
				if pair12 in word_pair_freq:
					word_pair_freq[pair12] += 1
				else:
					word_pair_freq[pair21] += 1
				i += 1
		
		#print(word_pair_freq)
		return word_pair_freq
	
	def _compute_pair_freq_by_3gram(self,doc_list):
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
		
		#print(word_pair_freq)
		return word_pair_freq

	def _create_network_by_ngram(self,doc_list,freq_dic,pos_dic,method="3gram",tol=1,max_view=50):
		if method == "3gram":
			word_pair_freq = self._compute_pair_freq_by_3gram(doc_list)
		elif method == "2gram":
			word_pair_freq = self._compute_pair_freq_by_2gram(doc_list)
		else:
			raise SyntaxError("Not found method: 2-gram and 3-gram are only available")

		# エッジリスト(word1,word2,freq,weight)を作成する
		edge_list = []
		word_pair_list = sorted(word_pair_freq.items(), key=lambda x:x[1], reverse=True) # 出現回数順に並べ替え
		n = min( len(word_pair_list), max_view )
		max_common = max(word_pair_freq.values())
		#print(word_pair_list[0:n])
		i=0
		while i < n :
			pair,nfreq = word_pair_list[i]
			if nfreq > tol :
				edge_list.append((pair[0],pair[1],nfreq,nfreq))
			i += 1
		
		#print(edge_list)

		# ノードリスト(name,size,type)を作成する
		words = []
		node_list= []
		for item in word_pair_list[0:n]: # エッジがないノードも含めるためedge_listは使用しない
			pair,dfreq = item
			j = 0
			while j < 2 :
				word = pair[j]
				if not word in words :
					freq = freq_dic[word]
					pos  = pos_dic[word]
					node_list.append((word,freq,pos))	
					words.append(word)
				j+=1

		return node_list,edge_list



	def to_seperated_text(self,text):
		if self.parser_ == "janome":
			return self._create_wordcloud_textdata_by_janome(text)
		elif self.parser_ == "mecab" :
			return self._create_wordcloud_textdata_by_mecab(text)
		else:
			raise SyntaxError("Not found a parser for Japanese")

	def count_words(self,text):
		if self.parser_ == "janome":
			return self._count_word_frequency_by_janome(text)
		elif self.parser_ == "mecab" :
			return self._count_word_frequency_by_mecab(text)
		else:
			raise SyntaxError("Not found a parser for Japanese")

	def to_network_data(self,text,method="jaccard",edge_tol=None,max_view=50):
		if self.parser_ == "mecab" :
			doc_list,freq_dic,pos_dic = self._parse_to_documents_by_mecab(text)
		elif self.parser_ == "janome":
			raise SyntaxError("Not available of parsing to a network by Janome")
		else:
			raise SyntaxError("Not found a parser for Japanese")
	
		if method == "jaccard":
			if edge_tol is None: edge_tol = 0.1
			node_list,edge_list = self._create_network_by_jaccard(doc_list,freq_dic,pos_dic,tol=edge_tol,max_view=max_view)
		elif method == "2gram" or method == "3gram" :
			if edge_tol is None: edge_tol = 1
			node_list,edge_list = self._create_network_by_ngram(doc_list,freq_dic,pos_dic,method=method,tol=edge_tol,max_view=max_view)
		else :
			raise SyntaxError("Unsupported method for computing network")

		return node_list,edge_list


