from discord.ext import commands

class utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def ping(self, ctx):
        """
        used to check if the bot is alive
        """
        await ctx.send("pong! {0:.2f}ms".format(self.bot.latency * 1000))
        
    @commands.command(no_pm=True)
    async def poll(self, ctx, *, question: str):
        """
        Quick and easy yes/no poll, for multiple answers, see !quickpoll
        """
        msg = await ctx.send("**{}** asks: {}".format(ctx.message.author, question.replace("@", "@\u200b")))
        try:
            await ctx.message.delete()
        except:
            pass
        yes_thumb = "👍"
        no_thumb = "👎"
        await msg.add_reaction(yes_thumb)
        await msg.add_reaction(no_thumb)
        
    @commands.command(no_pm=True)
    async def quickpoll(self, ctx, *, questions_and_choices: str):
        """
        delimit questions and answers by either | or , 
        supports up to 10 choices
        """
        if "|" in questions_and_choices:
            delimiter = "|"
        elif "," in questions_and_choices:
            delimiter = ","
        else:
            delimiter = None
        if delimiter is not None:
            questions_and_choices = questions_and_choices.split(delimiter)
        else:
            questions_and_choices = shlex.split(questions_and_choices)

        if len(questions_and_choices) < 3:
            return await ctx.send('Need at least 1 question with 2 choices.')
        elif len(questions_and_choices) > 11:
            return await ctx.send('You can only have up to 10 choices.')

        perms = ctx.channel.permissions_for(ctx.guild.me)
        if not (perms.read_message_history or perms.add_reactions):
            return await ctx.send('Need Read Message History and Add Reactions permissions.')

        question = questions_and_choices[0]
        choices = [(to_keycap(e), v)
                   for e, v in enumerate(questions_and_choices[1:], 1)]

        try:
            await ctx.message.delete()
        except:
            pass

        fmt = '{0} asks: {1}\n\n{2}'
        answer = '\n'.join('%s: %s' % t for t in choices)
        poll = await ctx.send(fmt.format(ctx.message.author, question.replace("@", "@\u200b"), answer.replace("@", "@\u200b")))
        for emoji, _ in choices:
            await poll.add_reaction(emoji)
            

def setup(bot):
    bot.add_cog(utility(bot))
