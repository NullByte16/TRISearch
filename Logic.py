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

def add_topic(title: str, keywords: list, sources: list):
    if sources == []:
        return None
    topic = Topic(title, keywords, sources)
    col = db[title]
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
    
"""def remove_topic(title: str) -> bool:
    for_deletion = topics[title]
    if for_deletion.delete():
        db.drop_collection(title)
        topics.pop(title)
        if not db.list_collection_names().__contains__(for_deletion):
            return True
    return False"""

# Delete all files in topic, and topic folder.
def remove_topic(title: str) -> bool:
    print(db.list_collection_names())
    db.drop_collection(title)    
    print(db.list_collection_names())
    shutil.rmtree(f"{os.getcwd()}\\{title}")
    return True
