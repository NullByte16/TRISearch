# Contains all functions that interact continuously with the Graphics.py module.
# For example: "submit" button on the "New Topic" page, implemented graphically in Graphics.py,
# will activate a function in Logic.py when clicked.
from Topic import Topic
from Info import Info
import pymongo
import os
import shutil

mdb_client = pymongo.MongoClient("mongodb://localhost:27017")
db = mdb_client["TRISearch"]
topics = {}

def fetch(arg: str) -> list:
    col = db.get_collection(arg)
    names = []
    for doc in col.find():
        names.append(doc["Name"])

    return names

def pass_infos(title: str) -> list[dict]:
    return db[title].find()
        

def add_topic(*args):
    if args[2] == []:
        return None
    topic = Topic(args[0], args[1], args[2])
    col = db[args[0]]
    docs = []
    for info in topic.research.infos:
        docs.append({
            "Name": info.name,
            "Thumbnail": info.thumbnail,
            "Type": info.type,
            "Link": info.url,
            "File": info.file
        })
    col.insert_many(docs)

# Delete all files in topic, and topic folder.
def remove_topic(title: str) -> bool:
    db.drop_collection(title)    
    shutil.rmtree(f"{os.getcwd()}\\{title}")
    return True
