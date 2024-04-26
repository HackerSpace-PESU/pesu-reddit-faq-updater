import pytz
import datetime
from reddit import PESURedditHandler

# set up the subreddit and the wiki page and get the FAQs
reddit = PESURedditHandler()
faq_wiki = reddit.get_wiki_page('faq')
faqs = reddit.get_formatted_faqs()

markdown = f""

for faq in faqs:
    question = faq['question']
    question_md = f"**{question}**\n"
    answer = faq['answer']
    answer_md = f"{answer}\n\n---\n\n"
    markdown += question_md + answer_md

markdown = markdown.strip()

# write the markdown to the wiki page
current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d %B %Y %I:%M:%S %p")
faq_wiki.edit(content=markdown, reason=f"Updated FAQs on {current_time}")



