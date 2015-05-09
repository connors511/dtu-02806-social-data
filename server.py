import tornado.ioloop
import tornado.web
import json
import os
from import_data import reddit_info

class DataHandler(tornado.web.RequestHandler):
        def get(self):
                self.set_header('Content-Type', 'application/json')
                self.set_header('Access-Control-Allow-Origin', '*')
                self.write(json.dumps(comments))

class ScoringHandler(tornado.web.RequestHandler):
        def post(self):
                data = json.loads(self.request.body.decode('utf-8'))
                self.write("Hello, world: " + data["comment"])

class WordHandler(tornado.web.RequestHandler):
        def get(self):
                self.set_header('Content-Type', 'application/json')
                self.set_header('Access-Control-Allow-Origin', '*')
                self.write(json.dumps(words))

application = tornado.web.Application([
        (r"/data", DataHandler),
        (r"/score", ScoringHandler),
        (r"/words", WordHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, { 'path': os.path.join(os.getcwd(), 'app') })
])

if __name__ == "__main__":
        print("Fetching")
        X, y_score, attributeNames, count, authorNames, subredditNames, words = reddit_info(0)

        attributeNames = ["gilded", "downs", "edited", "commentLength", "sentimentScore", "controversiality",
                              "authorNameLength", "archived", "timestamp", "tod", "dow", "hod","thread score","external link", "author", "subreddit"]
        attributeNamesShort = ["g", "d", "e", "cL", "sS", "c",
                              "aNL", "a", "t", "tod", "dow", "hod","ts","el","an","s"]

        print("Transforming")
        comments = [dict(zip(attributeNamesShort, record)) for record in X]
        for i in range(len(y_score)):
                comments[i]["an"] = authorNames[i]
                comments[i]["s"] = subredditNames[i]
        print("Server listening")
        application.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

