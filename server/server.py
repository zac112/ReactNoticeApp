# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import pymongo

try:
    with open("conf.json") as f:
        conf = json.load(f)
except Exception as e:
    print(e)
    exit()
    
hostName = conf["host"]
serverPort = conf["port"]

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
mongo = mongoclient["Notices"]
data = {}

class MyServer(BaseHTTPRequestHandler):

    def getDays(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        self.wfile.write(bytes(json.dumps(mongo.list_collection_names()), 'utf-8'))

    def getDay(self, path):
        year,month,day = path.split("/")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        doc = mongo[year][month][day]
        res = list(doc.find())

        for x in res:
            del x["_id"]
            
        print(res)
        self.wfile.write(bytes(json.dumps(res), 'utf-8'))
        
    def sendError(self,error,msg):
        self.send_response(error)
        self.end_headers()
        self.wfile.write(bytes(msg, 'utf-8'))
        return

    def parse(self, path):
        path = path.strip("/")
        if not path.startswith("api/"):
            return None
        path = path[4:]
        return path
        
    def do_GET(self):
        path = self.parse(self.path)
        if path == None:
            self.sendError(400,"Malformed url")
            return
                
        if path == "days":
            self.getDays()
            return
        
        try:
            self.getDay(path)   
        except:
            self.sendError(400,"Malformed url")
            return        

    def do_POST(self):
        path = self.parse(self.path)
        if path == None:
            self.sendError(400,"Malformed url")
            return
        
        try:
            year,month,day = path.strip("/").split("/")
        except:
            self.sendError(400,"Malformed url")
            return
        
        try:
            payload = self.rfile.read1(10240)
            print("pload",payload)
            payload = json.loads(payload)
        except Exception as e:
            self.sendError(400,"No payload")
            print("Error:",e)
            return

        print("pload",payload)
        keys = ["title", "data"]
        for k in keys:
            if k not in payload:
                self.sendError(400,"Malformed json: no "+str(k))
                return

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        
        doc = mongo[year][month][day]
        doc.insert_one(dict(payload))
        
        print(payload)
        self.wfile.write(bytes(json.dumps(payload), 'utf-8'))
        
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
