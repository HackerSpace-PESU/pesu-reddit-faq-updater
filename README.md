# pesu-reddit-faq-updater

This script fetches [FAQs](https://www.reddit.com/r/PESU/comments/14c1iym/faqs/) from
the [r/PESU](https://www.reddit.com/r/PESU/) subreddit and updates the [r/PESU FAQ Wiki](https://www.reddit.com/r/PESU/)
post with the fetched FAQs.

## How to run the script

1. Clone the repository
2. Install the dependencies using `pip install -r requirements.txt`
3. Create a Reddit app and note down the `CLIENT_ID` and `CLIENT_SECRET`
4. Create a Reddit account and note down the `USERNAME` and `PASSWORD`. Make sure the account has wiki edit permissions
   on the subreddit.
5. Set the following environment variables:
   - `CLIENT_ID`: The client ID of the Reddit app
   - `CLIENT_SECRET`: The client secret of the Reddit app
   - `USER_AGENT`: The user agent of the Reddit app
   - `USERNAME`: The username of the Reddit account
   - `PASSWORD`: The password of the Reddit account
6. Run the script using `python src/main.py`
   Example:
   ```bash
   CLIENT_ID={CLIENT_ID} \
   CLIENT_SECRET={CLIENT_SECRET} \
   USER_AGENT={USER_AGENT} \
   USERNAME={USERNAME} \
   PASSWORD={PASSWORD} \
   python src/main.py
   ```
