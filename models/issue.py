from datetime import datetime
import json

import httpx

import rfeed as rf
from models.story import Story


class Issue:
    def __init__(self, story_count: int = 30):
        self.story_count: int = story_count
        self.story_ids: list[int] = self.get_story_ids()
        self.stories: list = self.get_stories()
        self.update_time = datetime.now()
        self.feed = self.create_feed()

    def get_story_ids(self) -> list:
        response = httpx.get(
            f'https://hacker-news.firebaseio.com/v0/topstories.json?orderBy="$key"&limitToFirst={self.story_count}'
        )
        return list(response.json())

    def get_stories(self):
        def story_decoder(story_dict: dict):
            return Story(**story_dict)

        stories = []
        with httpx.Client() as client:
            for story_id in self.story_ids:
                response = client.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                )
                stories.append(json.loads(response.text, object_hook=story_decoder))
        return stories

    def get_story(self, story_id: int):
        def story_decoder(story_dict: dict):
            return Story(**story_dict)

        response = httpx.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        )
        return json.loads(response.text, object_hook=story_decoder)

    def create_feed(self):
        feed = rf.Feed(
            title="zenHN",
            link="https://zenhn.bobre.us",
            description="a calmer way to keep up",
            language="en-US",
            lastBuildDate=self.update_time,
        )
        for story in self.stories:
            item = rf.Item(
                title=story.title,
                link=story.url,
                description=f"on {story.domain}",
                guid=rf.Guid(story.url),
                pubDate=self.update_time,
            )
            feed.items.append(item)
        return feed.rss()
