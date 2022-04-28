from pymongo import MongoClient

client = MongoClient("mongodb://root:example@172.20.0.13:27017/")
db = client.admin
serverStatusResult=db.command("serverStatus")
print(serverStatusResult)