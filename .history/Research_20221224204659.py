from Info import Info
import requests
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from requests_html import HTMLSession

options = Options()
options.add_argument("headless")
browser = webdriver.Chrome(options=options)

# TODO - One of two things: either make selenium more efficient, or replace it with more efficient library.
# ??? Maybe use Threading to create multiple tabs on Chrome simultaneously, and access multiple websites simultaneously to avoid waiting for processes to complete.???
# For above suggestion, important: 15 tabs in Chrome = ~1.5 GB RAM.

class Research():
    def __init__(self, keywords: list):
        self.keywords = keywords
        self.infos = []



    def strip_name(self, filename) -> str:
        chars = ['\\', '/', ':', '*', '?', '\"', '<', '>', '|']

        """for char in chars:
            filename.replace(char, '')"""
        return filename.replace("\\", "").replace("/", "").replace(":", "").replace("*", "").replace("?", "").replace("\"", "").replace("<", "").replace(">", "").replace("|", "")


    
    def retrieve_image(self, title, image_url):
        filename = title + ".jpg"
        r = requests.get(image_url, stream=True)

        filename = self.strip_name(filename)
        
        if r.status_code == 200:
            r.raw.decode_content = True

            with open(filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            if shutil.sys.platform.__contains__("win"):
                return shutil.os.getcwd() + "\\" + filename
            return shutil.os.getcwd() + "/" + filename
        else:
            return None
        

    # Arguments: sub - list of urls.
    # "Cleanses" urls in sub, returning a new list containing all urls **without** the word "google" in them.
    # Note: Might make it difficult to conduct research on Google itself.
    def cleanse_google(self, sub):
        result = []
        for link in sub:
            if not (link.__contains__("google")):
                result.append(link)
        return result

    
    # Scrapes Google Search engine. Retrieves relevant links for research.
    # Sends GET requests to www.google.com, using search keywords found in self.keywords.
    # Updates self.infos, appending all found relevant urls to the list.
    def scrape_art(self):
        urls = []
        for key in self.keywords:
            page = requests.get("https://www.google.com/search?q=" + key).text
            index = None
            try:
                index = page.index("href=\"http")
            except:
                print("No links were found.")
            while (index != None):
                extract = ""
                check = index + 6
                while (len(page) > check and page[check] != '\"'):
                    extract += page[check]
                    check += 1
                urls.append(extract)
                page = page[check:]
                try:
                    if (page.index("href=\"http")):
                        index = page.index("href=\"http")
                    else:
                        index = None
                except:
                    index = None

        urls = self.cleanse_google(urls)
        for url in urls:
            self.infos.append(url)

            
    """ Scrape YouTube for video links, thumbnail images and video names and store
        in research.infos """        
    def scrape_vid(self):
        global browser
        videos = []

        for key in self.keywords:
            browser.get("https://www.youtube.com/results?search_query=" + "+".join(key.split(" ")))

            body = browser.find_element(By.CSS_SELECTOR, "body")
            body.send_keys(Keys.PAGE_DOWN)

            videos = browser.find_elements(By.TAG_NAME, "ytd-video-renderer")
            for video in videos:
                if video.find_element(By.TAG_NAME, "img").get_attribute("src"):
                    self.infos.append(
                        Info(video.find_element(By.ID, "video-title").get_attribute("title"),
                                           self.retrieve_image(video.find_element(By.ID, "video-title").get_attribute("title"), video.find_element(By.TAG_NAME, "img").get_attribute("src")),
                                           video.find_element(By.ID, "video-title").get_attribute("href"),
                                           type="video",
                                           file=self.retrieve_image(video.find_element(By.ID, "video-title").get_attribute("title"), video.find_element(By.TAG_NAME, "img").get_attribute("src"))))

    def scrape_vid_b(self):
        videos = []
        for key in self.keywords:
            session = HTMLSession()