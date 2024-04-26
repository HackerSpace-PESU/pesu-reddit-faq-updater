import os
import re
import praw
from tqdm.auto import tqdm
from typing import Optional

class PESURedditHandler:
    def __init__(self):
        self.client = praw.Reddit(
            client_id=os.environ['CLIENT_ID'],
            client_secret=os.environ['CLIENT_SECRET'],
            user_agent=os.environ['USER_AGENT'],
            username=os.environ['USERNAME'],
            password=os.environ['PASSWORD']
        )

        self.subreddit = self.client.subreddit("PESU")

    def get_wiki_page(self, page_name: str) -> Optional[praw.models.WikiPage]:
        return self.subreddit.wiki[page_name]
    
    def get_submission(self, url: str) -> Optional[praw.models.Submission]:
        return self.client.submission(url=url)
    
    def get_formatted_faqs(self):
        # fetch the FAQs post and obtain the markdown text
        faq_post = self.get_submission('https://www.reddit.com/r/PESU/comments/14c1iym/faqs/')
        content = faq_post.selftext

        # skip these links
        skip = [
            # "https://www.reddit.com/r/PESU/comments/14c1jiw/how_to_ask_a_question_on_rpesu/",
            # "https://www.reddit.com/r/PESU/comments/142gani/pesu_discord/"
        ]

        # find all markdown text which have a link: [example test for link](https://example.com)
        question_links = re.findall(r'\[(.*?)\]\((.*?)\)', content)
        question_data = list()
        for question, link in tqdm(question_links, desc="Fetching FAQs"):
            try:
                comment = self.client.comment(url=link)
                answer = comment.body.strip()
                upvotes = comment.score
            except praw.exceptions.InvalidURL:
                try:
                    post = self.client.submission(url=link)
                    answer = post.selftext.strip()
                    upvotes = post.score
                except Exception:
                    answer = link
                    upvotes = 1
            except Exception:
                answer = link
                upvotes = 1

            if link in skip:
                continue

            answer = re.sub(r"\n+", "\n\n", answer)

            # add the question and answer to the listt
            question_data.append({
                "question": question.strip(),
                "answer": answer,
                "upvotes": upvotes,
                "link": link,
            })

        return question_data