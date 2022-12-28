from Research import Research
import os
import shutil
import threading

class Topic():
    def __init__(self, title: str, keywords: list, sources: list):
        # Initialize variables.
        self.title = title
        self.keywords = keywords
        self.sources = sources
        self.research = Research(self.keywords)
        
        # Create new directory for topic. Move into directory.
        self.path = f"{os.getcwd()}\\{self.title}"
        
        if not os.listdir().__contains__(self.title):
            os.mkdir(self.path)
        os.chdir(self.path)

        # Retrieve information and place in directory. Methods are run in a thread to allow user to continue using the GUI while information is retrieved.
        article_thread = threading.Thread(target = self.research.scrape_art())
        article_thread.start()
        
        video_thread = threading.Thread(target = self.research.scrape_vid())
        video_thread.start()
        
        # Switch back to main directory.
        os.chdir('..')
        
    # Delete all files in topic, and topic folder.
    def delete(self) -> bool:
        
        shutil.rmtree(self.path)
        return True