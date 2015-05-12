def classScore(comment, Author_Name, UCT_Time, Thread_Score, External_link, model): #comment?

	import os
	AFINN_path = os.getcwd() + '/AFINN/AFINN-111form.csv'
	import csv
	import datetime
	import numpy as np
	#from sklearn.ensemble import RandomForestClassifier

	ANEW_words = {}
	with open(AFINN_path) as f:
		try:
			reader = csv.reader(f, delimiter=';')
			for row in reader:
				try:
					ANEW_words[row[0]]=row[1] # Each element in the csv row, is a word
				except:
					print("empty end field")
		except:
			pass

	attributeNames = ["comment_length", "sentiment_Score"
						  "Author_name_length", "UCT Timestamp", "time of day", "Day of week",
						  "Hour of day", "Thread Score", "External Link"]

	X_input = np.empty([1, len(attributeNames)+1])

	X_input[0,0] =len(comment) # Length of comment

	for words in ANEW_words:
		X_input[0,1] += comment.count(words) * int(ANEW_words[words])

	X_input[0,2] = len(Author_Name) # Author_Name_Length

	# X_input[0,3] = UCT_Time

	tempTime = datetime.datetime.utcfromtimestamp(UCT_Time).hour-5.5
	if tempTime <= 0: # roll over til cat coding 5
		X_input[0,3] = 5
	elif  tempTime <= 4: # Early morning
		X_input[0,3] = 0
	elif tempTime <= 8: # morning to middle of day and not early
		X_input[0,3] = 1
	elif tempTime <= 12: # morning to middle of day
		X_input[0,3] = 2
	elif tempTime <= 16: # Late afternoon
		X_input[0,3] = 3
	elif tempTime <= 20: # Early eevening
		X_input[0,3] = 4
	else:
		X_input[0,3] = 5 # Late evening to night

	X_input[0,4] = datetime.datetime.utcfromtimestamp(UCT_Time-19800).weekday()

	X_input[0,5] = tempTime+5.5

	X_input[0,6] = Thread_Score

	X_input[0,7] = External_link # 0 or 1

	prediction = model.predict(X_input)
	return prediction