"""Reddit fetching basic answering cog."""
import random
from difflib import SequenceMatcher
from typing import List

import praw
from discord.ext import commands

class Chat(commands.Cog):
    """Chat Cog."""
    
    def __init__(self, bot: commands.Bot):
        """Salt and pepper."""
        self.bot = bot

    @commands.command(aliases=['c', 'ch'])
    async def chat(self, ctx: commands.Context, *, you: str) -> None:
        """Chat function."""
        reply: str = str(self.grab_reply(you))
        await ctx.send(reply)
        #logger.info("Chat command requested!")
    #----------------------------------------#

    @staticmethod
    def similar(a: str, b: str) -> float:
        """Get ratio of similarity."""
        return SequenceMatcher(None, a, b).ratio()
    #----------------------------------------#

    def grab_reply(self, question):
        """Grab the reply from reddit."""
        reddit: praw.Reddit = self.bot.reddit_client
        x: int = 0
        submission_ids = []
        for results in reddit.subreddit('all').search(question):
            id = results.id
            title = results.title
            comments = results.num_comments
            if comments > 1 and self.similar(question, title) > .6:
                submission_ids.append(id)
                x += 1
            if x >= 20:
                break
        if len(submission_ids) == 0:
            return "I have no idea"
        submission: praw.reddit.Submission = reddit.submission(
            id = submission_ids[random.randint(0, len(submission_ids)-1)])
        comment_list: List[str] = []
        x: int = 0
        for top_level_comment in submission.comments:
            body = top_level_comment.body
            comment_list.append(body)
            x += 1
            if x >= 5:
                break
        if len(comment_list) == 0:
            return "I have no clue"
        return comment_list[random.randint(0, len(comment_list)-1)]
    #----------------------------------------#

def setup(bot: commands.Bot) -> None:
    """Into pan goes the cog."""
    bot.add_cog(Chat(bot))
