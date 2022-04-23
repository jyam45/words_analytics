#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
import cgitb
import sys
import json

def main():
	cgitb.enable() # デバッグ用
	form = cgi.FieldStorage()
	nodes=""
	edges=""
	if "edges" in form:
		edges = form.getvalue("edges")
	if "nodes" in form:
		nodes = form.getvalue("nodes")

	if edges == "" :
		printError("少なくともエッジを入力してください")

	if nodes == "" :
		visjs = convertNetworkCsvToVisjs(edges)
	else:
		visjs = convertNetworkCsvToVisjs(edges,nodes)

	#printText(visjs)
	printView(visjs)

def printError(msg):
	print("Content-Type: text/html; charset=UTF-8\n")
	print("<html><body>")
	print("<h1>ERROR!</h1><br>")
	print(msg)
	print("</body></html")
	sys.exit()

def printText(text):
	print("Content-Type: text/html; charset=UTF-8\n")
	print("<html><body>")
	print(text)
	print("</body></html")

def convertNetworkCsvToVisjs( edges_csv, nodes_csv = None ):

	if nodes_csv is None :

		edges = []
		nodes = []

		# エッジの変換
		lines = edges_csv.split("\r\n")
		nodedic= {}
		for line in lines:
			edge = {}
			data = line.split(',')
			# エッジデータでない場合は除外
			if len(data) <= 1 : continue
			if len(data) > 1 :
				edge["from"]  = data[0]
				edge["to"]    = data[1]
				nodedic[data[0]] = data[0]
				nodedic[data[1]] = data[1]
			if len(data) > 2 :
				edge["label"] = data[2]
				#if data[2].isdecimal() :
				#	edge["width"] = int(data[2])
			edges.append(edge)

		# ノードの変換
		for key in nodedic:
			node = {}
			node["id"]    = key
			node["label"] = key
			nodes.append(node)

		visjs = {}
		visjs["nodes"] = nodes
		visjs["edges"] = edges

		return json.dumps(visjs)

	else:
		edges = []
		nodes = []

		# ノードの変換
		lines = nodes_csv.split("\r\n")
		for line in lines:
			node = {}
			data = line.split(',')
			if len(data) > 0 : 
				node["id"]    = data[0]
				node["label"] = data[0]
			if len(data) > 1 :
				node["size"]  = int(data[1])
			nodes.append(node)

		# エッジの変換
		lines = edges_csv.split("\r\n")
		for line in lines:
			edge = {}
			data = line.split(',')
			# エッジデータでない場合は除外
			if len(data) <= 1 : continue
			if len(data) > 1 :
				edge["from"]  = data[0]
				edge["to"]    = data[1]
			if len(data) > 2 :
				edge["label"] = data[2]
				#if data[2].isdecimal() :
				#	edge["width"] = int(data[2])
			edges.append(edge)

		visjs = {}
		visjs["nodes"] = nodes
		visjs["edges"] = edges

		return json.dumps(visjs)

def printView(json):
	print("Content-Type: text/html; charset=UTF-8\n")
	fp = open("./view.html");
	btxt = fp.read();
	html = btxt;
	print( html % json )

main()
