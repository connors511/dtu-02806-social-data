# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 19:00:19 2015
Imports data with database upcoupling to python kernel

Limit is if a a lower comments amount bound shoul be used, 0 == ignore.

Returns, y_score, X datamatrix, attributeNames

@author: Dag
"""
import os
from collections import OrderedDict
from operator import itemgetter    

def reddit_info(limit):

	MONGO_DB = 'social-data'
	MONGO_URI = 'mongodb://reddit:social@localhost:27017/social-data?authMechanism=MONGODB-CR'
	AFINN_path = os.getcwd() + '/AFINN/AFINN-111form.csv'
	
	#import praw
	#import pymongo
	# all libraries
	from pymongo import MongoClient
	import re
	
	#client = MongoClient(MONGO_HOST, MONGO_PORT)
	client = MongoClient(MONGO_URI)
	db = client[MONGO_DB]
	
	import numpy as np
	
	import datetime # For UTC formatting
	
	# ANEW stuff
	import csv
	
	ANEW_words = {}
	with open(AFINN_path, encoding='utf-8') as f:
		try:
			reader = csv.reader(f, delimiter=';')
			for row in reader:
				try:
					ANEW_words[row[0]]=row[1] # Each element in the csv row, is a word
				except:
					print("empty end field")
		except Exception as e:
			print(e)
			pass
						
	#%%   
	count = 0
	for thread in db.submissions.find({}, {'num_comments':1}):
		count += thread["num_comments"]
	
	
	#%% Creating data matrix
	attributeNames = ["gilded", "downs", "edited", "comment_length", "sentiment_Score", "Controversiality",
					  "Author_name_length", "Archived", "UCT Timestamp", "time of day", "Day of week",
					  "Hour of day", "Thread Score", "External Link", "Author Name", "Subreddit"]
	if limit > count or limit == 0:
		X = np.empty([count, len(attributeNames)])

		y_score = ["None"] * count
		
		authorName =["None"] * count
		subredditName = ["None"] * count
	else:
		X = np.empty([limit, len(attributeNames)])
		y_score = ["None"] * limit
		authorName =["None"] * limit
		subredditName = ["None"] * limit
	
	k = 0

	word_list = {}
	
	try:
		for thread in db.submissions.find(): #.limit(limit)
			for post in thread["comments"]:
				# Response
				y_score[k] = post["score"]
				
				# Data matrix
				X[k,0] = [0,1][post["gilded"] == "True"]
				
				X[k,1] = post["downs"] # down votes
				
				X[k,2] = [0,1][post["edited"] == "True"]
				  
				X[k,3] = len(post["body"]) # length of comment
				
				for words in ANEW_words:
					X[k,4] += post["body"].count(words) * int(ANEW_words[words])
				
				X[k,5] = post["controversiality"]
				
				X[k,6] = len(post["author"]) # Length of auther name
				
				X[k,7] = [0,1][post["archived"] == "True"] # Has post been archived?
				
				X[k,8] = post["created_utc"] # UNIX UTC Timestamp for post
				
				# Time of day ordinal
				tempTime = datetime.datetime.utcfromtimestamp(X[k,8]).hour-5.5
				if tempTime <= 0: # roll over til cat coding 5
					X[k,9] = 5
				elif  tempTime <= 4: # Early morning
					X[k,9] = 0
				elif tempTime <= 8: # morning to middle of day and not early
					X[k,9] = 1
				elif tempTime <= 12: # morning to middle of day
					X[k,9] = 2
				elif tempTime <= 16: # Late afternoon
					X[k,9] = 3
				elif tempTime <= 20: # Early eevening
					X[k,9] = 4 
				else:
					X[k,9] = 5 # Late evening to night
				
				X[k,10] = datetime.datetime.utcfromtimestamp(X[k,8]-19800).weekday() # day of week, 0 monday, 6 sunday
				
				X[k,11] = tempTime+5.5
				
				X[k,12] = thread["score"]
				
				X[k,13] =[0,1][thread["selftext"] == '']
				
				authorName[k] = post["author"]
				
				subredditName[k] = thread["subreddit"]

				tmp = re.findall(r'\b[\w\']+\b', re.sub(r'\bhttps?:\/\/.*?[\s\b]', '', post["body"].lower(), flags=re.MULTILINE))
				words = {word:tmp.count(word) for word in tmp}

				for w,c in words.items():
					word_list[w] = word_list.get(w, 1) + c
				
				k += 1       
	except Exception as e:
		print(e)
		pass
	
	return X, y_score, attributeNames, count, authorName, subredditName, OrderedDict(sorted(word_list.items(), key=itemgetter(1), reverse=True))