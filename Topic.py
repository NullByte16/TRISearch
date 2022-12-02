from Research import Research

class Topic():
    def __init__(self, title: str, keywords: list, sources: list):
        self.title = title
        self.keywords = keywords
        self.sources = sources
        self.research = Research(self.keywords)

        # Fill information cache.
        self.research.scrape_art()
        self.research.scrape_vid()


