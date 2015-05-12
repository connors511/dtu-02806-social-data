import tornado.ioloop
import tornado.web
import json
import os
import numpy as np
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
from import_data import reddit_info
from classifier import classScore
from datetime import datetime
import calendar

class DataHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_header('Content-Type', 'application/json')
		self.set_header('Access-Control-Allow-Origin', '*')
		self.write(json.dumps(comments))

class ScoringHandler(tornado.web.RequestHandler):
	def post(self):
		data = json.loads(self.request.body.decode('utf-8'))


		d = datetime.utcnow()
		unixtime = calendar.timegm(d.utctimetuple())
		score = classScore(data["comment"], data["username"], unixtime, data["threadscore"], data["external"], clfrand)

		self.set_header('Content-Type', 'application/json')
		self.set_header('Access-Control-Allow-Origin', '*')
		self.write(json.dumps({"prediction": score}))

class WordHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_header('Content-Type', 'application/json')
		self.set_header('Access-Control-Allow-Origin', '*')
		self.write(json.dumps(words))

application = tornado.web.Application([
	(r"/data", DataHandler),
	(r"/score", ScoringHandler),
	(r"/words", WordHandler),
	(r"/bower_components/(.*)", tornado.web.StaticFileHandler, { 'path': os.path.join(os.getcwd(), 'bower_components') }),
	(r"/(.*)", tornado.web.StaticFileHandler, { 'path': os.path.join(os.getcwd(), 'app') })
])

if __name__ == "__main__":
	print("Fetching")
	startTime = datetime.now()
	X, y_score, attributeNames, count, authorNames, subredditNames, words = reddit_info(0)
	print("Fetched in " + str(datetime.now()-startTime))

	attributeNames = ["gilded", "downs", "edited", "commentLength", "sentimentScore", "controversiality",
							"authorNameLength", "archived", "timestamp", "tod", "dow", "hod","thread score","external link", "author", "subreddit"]
	attributeNamesShort = ["g", "d", "e", "cL", "sS", "c",
							"aNL", "a", "t", "tod", "dow", "hod","ts","el","an","s"]

	print("Transforming")
	comments = [dict(zip(attributeNamesShort, record)) for record in X]
	for i in range(len(y_score)):
		comments[i]["an"] = authorNames[i]
		comments[i]["s"] = subredditNames[i]

	print("Building predictor")
	startTime = datetime.now()
	# Shave off to fit with stuff aviable at page
	X_shave = np.delete(X, np.c_[[0,1,2,5,7,8,14,15,16]], 1)

	y_binned = [0] * len(y_score)
	for i in range(len(y_score)):
		if y_score[i] < 5:
			y_binned[i] = 0
		else:
			y_binned[i] = 1

	# Optimal model
	clfrand = RandomForestClassifier(n_estimators = 400 , max_features=7, bootstrap=True, oob_score=True)
	clfrand.fit(X_shave, y_binned)
	print("Built in " + str(datetime.now()-startTime))

	print("Server listening")
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()

