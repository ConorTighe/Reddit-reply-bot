import praw
import BotAccess
import sqlite3
import time

USERAGENT = "A template account that will reply under certain users comments,   "
USERNAME = BotAccess.username
PASS = BotAccess.password
ACCOUNT = BotAccess.account
SUBREDDIT = "test"
MAXPOSTS = 100

print("Setting up database..")
sql = sqlite3.connect("sql.db")
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)')
sql.commit()

print("Logging into reddit")
r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASS, disable_warning=True)


def bot():
    subreddit = r.get_subreddit(SUBREDDIT)
    comments = subreddit.get_comments(limit=MAXPOSTS)
    for comment in comments:
        cur.execute('SELECT * FROM oldposts WHERE ID=?', [comment.id])
        if not cur.fetchone():
            try:
                myComment = comment.author.name
                if myComment == ACCOUNT:
                    print("Replying..")
                    comment.reply("Reply to " + ACCOUNT + "!!")
                    print("Replied")
            except AttributeError:
                pass

            cur.execute('INSERT INTO oldposts VALUES(?)', [comment.id])
            sql.commit()


while True:
    try:
        bot()
    except praw.errors.RateLimitExceeded as error:
            print("Sleeping for %d seconds" % error.sleep_time)
            time.sleep(error.sleep_time)
            print("Sleep done")
