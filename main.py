import praw
import os
import re
from dotenv import load_dotenv


DEFAULT_SUBREDDITS = 'MyTestPostSub'
DISPATCH_LINK = 'dispatch.com/story/'
URL_RE = r"(?P<url>https?://[^\s]+)"


def reddit_wrapper():
    """
    Sets up PRAW and returns the client
    :return: PRAW Reddit API wrapper
    """
    return praw.Reddit(
        client_id=os.environ.get('BOT_CLIENT_ID'),
        user_agent='test',
        client_secret=os.environ.get('BOT_SECRET'),
        username=os.environ.get('BOT_USERNAME'),
        password=os.environ.get('BOT_PASS'),
    )


def check_posts(reddit_client, subreddits=DEFAULT_SUBREDDITS):
    subreddit = reddit_client.subreddit(subreddits)
    for submission in subreddit.stream.submissions():
        print(submission)
        # if not submission.archived:
        #     reply(submission)


def reply_links(item):
    """

    :param item: A post or comment
    :return: A list of URLs to the free versions of the articles found in the item
    """
    links = []
    matches = re.findall(URL_RE, item.body)
    for match in matches:
        if DISPATCH_LINK in match:
            links.append(match.replace("www.dispatch.com", "www.thisweeknews.com"))

    return links


def reply_with_links(links):
    links_str = "links" if len(links) > 1 else "a link"
    links_str_two = "links" if len(links) > 1 else "link"
    formatted_links = ''
    for link in links:
        formatted_links += f"\n\n{link}"

    comment_reply = f"Hello! Your submission contains {links_str} to the Dispatch, which is paywalled."
    comment_reply += f" You can instead use the following {links_str_two} to view the articles"
    comment_reply += f" for free.{formatted_links}\n\n"
    comment_reply += "^^Bot ^^acting ^^up? ^^PM ^^me, ^^or ^^open ^^an ^^issue ^^on ^^[GitHub](https://www.google.com)"

    return comment_reply


def process_item(item):
    """
    Takes a post or comment and handles checking for Dispatch links, along with replying if any exist

    :param item: A post or a comment
    """

    links = reply_links(item)

    if len(links) > 0:
        reply_text = reply_with_links(links)
        item.reply(reply_text)


def stream_comments(reddit_client, subreddits=DEFAULT_SUBREDDITS):
    for comment in reddit_client.subreddit(subreddits).stream.comments(skip_existing=True):
        print(comment.body)
        process_item(comment)


if __name__ == '__main__':
    print("Starting DispatchLinkBot")
    load_dotenv()
    reddit = reddit_wrapper()
    # check_posts(reddit, 'Columbus')
    # check_posts()
    stream_comments(reddit, 'Columbus')
