import datetime
import logging

import pytz

from reddit import PESURedditHandler

logging.basicConfig(
    level=logging.INFO,
    filename="main.log",
    format="%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s:%(threadName)s:%(lineno)d - %(message)s",
    filemode="a",
)

current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata")).strftime(
    "%d %B %Y %I:%M:%S %p"
)
logging.info(f"Starting script on {current_time}")

logging.info("Initializing Reddit handler")
reddit = PESURedditHandler()
logging.info("Fetching wiki page")
faq_wiki = reddit.get_wiki_page("faq")
logging.info("Fetching FAQs")
faqs = reddit.get_formatted_faqs()
logging.info(f"Found {len(faqs)} FAQs")

markdown = f""

for faq in faqs:
    link = faq["link"]
    question = faq["question"]
    question_md = f"# **{question}**\n\n"
    answer = faq["answer"]
    answer_md = f"{answer}\n\n---\n\n"
    question_answer_md = question_md + answer_md
    markdown += question_md + answer_md

markdown = markdown.strip()

logging.info("Updating wiki page")
faq_wiki.edit(content=markdown, reason=f"Updated FAQs on {current_time}")
logging.info(f"Successfully updated {len(faqs)} FAQs on {current_time}")
