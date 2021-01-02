# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import pymongo

hostName = "localhost"
serverPort = 8080

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
        
    def do_GET(self):
        path = self.path.strip("/")

        if path == "days":
            self.getDays()
            return
        
        try:
            year,month,day = path.split("/")
        except:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes("Malformed url", 'utf-8'))
            return

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

    def do_POST(self):
        try:
            year,month,day = self.path.strip("/").split("/")
        except:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes("Malformed url", 'utf-8'))
            return
        
        try:
            payload = self.rfile.read1(10240)
            print("pload",payload)
            payload = json.loads(payload)
        except Exception as e:
            print("Error:",e)
            return

        print("pload",payload)
        keys = ["title", "data"]
        for k in keys:
            if k not in payload:
                print("Malformed json: no",k)
                self.send_response(400)
                self.end_headers()
                self.wfile.write(bytes("Malformed json: no "+str(k), 'utf-8'))
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
