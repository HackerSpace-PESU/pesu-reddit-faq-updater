import logging
import os
import re
import threading
import traceback
from typing import Optional

import praw


class PESURedditHandler:
    def __init__(self):
        self.client = praw.Reddit(
            client_id=os.environ["CLIENT_ID"],
            client_secret=os.environ["CLIENT_SECRET"],
            user_agent=os.environ["USER_AGENT"],
            username=os.environ["USERNAME"],
            password=os.environ["PASSWORD"],
        )

        self.subreddit = self.client.subreddit("PESU")

    def get_wiki_page(self, page_name: str) -> Optional[praw.models.WikiPage]:
        try:
            return self.subreddit.wiki[page_name]
        except Exception:
            logging.error(
                f"Failed to fetch wiki page {page_name}\n{traceback.format_exc()}"
            )

    def get_submission(self, url: str) -> Optional[praw.models.Submission]:
        try:
            return self.client.submission(url=url)
        except Exception:
            logging.error(f"Failed to fetch submission {url}\n{traceback.format_exc()}")

    def get_answer__and_upvotes_from_comment_or_post_url(
        self, url: str, faqs: list, idx: int
    ) -> Optional[str]:
        try:
            comment = self.client.comment(url=url)
            answer = comment.body.strip()
            upvotes = comment.score
        except praw.exceptions.InvalidURL:
            try:
                post = self.client.submission(url=url)
                answer = post.selftext.strip()
                upvotes = post.score
            except Exception:
                logging.warning(
                    f"Failed to fetch answer for {url}\n{traceback.format_exc()}"
                )
                answer = url
                upvotes = 1
        except Exception:
            answer = url
            upvotes = 1
            logging.warning(
                f"Failed to fetch answer for {url}\n{traceback.format_exc()}"
            )

        answer = re.sub(r"\n+", "\n\n", answer)
        faqs[idx]["answer"] = answer
        faqs[idx]["upvotes"] = upvotes

    def get_formatted_faqs(self):
        # fetch the FAQs post and obtain the markdown text
        try:
            faq_post = self.get_submission(
                "https://www.reddit.com/r/PESU/comments/14c1iym/faqs/"
            )
            content = faq_post.selftext
        except Exception:
            logging.error(f"Failed to fetch FAQs post\n{traceback.format_exc()}")
            return []

        # find all markdown text which have a link: [example test for link](https://example.com)
        question_links = re.findall(r"\[(.*?)\]\((.*?)\)", content)

        total_faqs = len(question_links)
        faqs = [None] * total_faqs
        threads = [None] * total_faqs
        for idx, (question, link) in enumerate(question_links):
            faqs[idx] = {"question": question, "link": link}
            threads[idx] = threading.Thread(
                target=self.get_answer__and_upvotes_from_comment_or_post_url,
                args=(link, faqs, idx),
            )
            threads[idx].start()

        for thread in threads:
            thread.join()

        return faqs
