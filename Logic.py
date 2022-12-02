# Contains all functions that interact continuously with the Graphics.py module.
# For example: "submit" button on the "New Topic" page, implemented graphically in Graphics.py,
# will activate a function in Logic.py when clicked.
from Topic import Topic

def fetch(arg: str) -> list:
    result = []
    checker = False # Tests if result recevies any name variable from the Topic argument's infos. If yes, changes to true.
    for t in topics:
        if t.title == arg and t.research.infos != None:
            for name in t.research.infos:
                result.append(name.name[:20] + "...")
    if result == []:
        return None
    return result


# Test code for "No information found" popup window.
from Info import Info
topics = []
t = Topic("Dog Training", ["Dogs", "Dog potty training"], [])
t.research.infos = None
topics.append(Topic("Ukraine War", ["Ukraine War"], []))
topics.append(t)


# Create new topic
def new_topic(title: str, keywords: list, sources: list) -> Topic:
    
    t = Topic(title, keywords, sources)
    topics.append(t)
    return t
    
