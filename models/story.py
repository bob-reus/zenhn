import re

import httpx
from readability import Document


class Story:
    def __init__(
        self,
        id: int,
        type: str = None,
        descendants: int = None,
        parent: int = None,
        kids: list = None,
        title: str = None,
        by: str = None,
        url: str = None,
        time: int = None,
        text: str = None,
        score: int = None,
    ):
        self.id = id
        self.type = type
        self.descendants = descendants
        self.parent = parent
        self.kids = kids
        self.title = title
        self.by = by
        if not url:
            url = f"https://news.ycombinator.com/item?id={self.id}"
        self.url = url
        self.time = time
        self.text = text
        self.score = score

        self.domain = self._generate_domain(self.url)
        self.article = None
        self.article_title = None
        self.article_short_title = None

    @staticmethod
    def _generate_domain(url):
        domain = re.search(
            "(https?:\/\/(www\.)?)(([\w-]+\.)+(\w+))",
            url,
        ).group(3)
        return domain

    def create_summary(self):
        response = httpx.get(self.url)
        doc = Document(response.text)
        self.article = doc.summary(html_partial=True)
        self.article_title = doc.title()
        self.article_short_title = doc.short_title()
