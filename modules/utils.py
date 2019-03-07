"""
Recruitment utilities
"""
import requests
from datetime import datetime as dt
import discord
from discord.ext import commands

# pylint: disable=invalid-name

class Utils:
    """
    Utility functions for KarmaFleet Recruitment
    """

    def __init__(self, bot):
        """
        Initialise the class
        """
        self.bot = bot

    @staticmethod
    def _query_evepraisal(item, market='jita'):
        """

        Example curl command to ping evepraisal:

        curl -XPOST "https://evepraisal.com/appraisal.json?market=jita&raw_textarea=avatar&persist=no"
        """
        ep_api = "https://evepraisal.com/appraisal.json"
        headers = {
            'User-Agent': 'Recruitment Tool v0.1',
            'From': 'jmccormac001@gmail.com'}
        params = {'market': market,
                  'raw_textarea': item,
                  'persist': 'no'}
        r = requests.post(ep_api, params=params, headers=headers)
        return r

    @staticmethod
    def _get_buy_sell_from_appraisal(appraisal):
        """
        Grab the buy and sell values from the appraisal
        """
        try:
            buy = appraisal.json()['appraisal']['totals']['buy']
            sell = appraisal.json()['appraisal']['totals']['sell']
        except KeyError:
            buy, sell = None, None
        return buy, sell

    @commands.command(pass_context=True, description='Calculate amount of skill injection')
    async def injectors(self, ctx, *data: str):
        """
        Takes a character's birthdate and their current
        SP level and estimates the amount of SP injection
        along with the corresponding isk value in large
        skill injectors in today's money
        """
        try:
            birthdate, sp = data
            # estimate that in isk
        except ValueError:
            await self.bot.say("Format is YYYY-MM-DD CURRENT_SP")
            return

        # get the birthdate in datetime format
        bd = dt.strptime(birthdate, "%Y-%m-%d")
        print(bd)
        current_sp = int(sp)
        print(current_sp)
        now = dt.utcnow()
        print(now)
        age_in_hours = (now - bd).total_seconds()/(3600.)
        print(age_in_hours)

        # correct the current SP for a baseline level of 700,00
        baseline_sp = 700000
        sp_trained = current_sp - baseline_sp

        # expected sp - 1800 per hour
        expected_trained_sp_min = age_in_hours * 1800
        diff_min = round(int(sp_trained - expected_trained_sp_min)/1E6, 3)
        expected_trained_min = round(int(baseline_sp + expected_trained_sp_min)/1E6, 3)

        # expected sp - 2700 per hour
        expected_trained_sp_max = age_in_hours * 2700
        diff_max = round(int(sp_trained - expected_trained_sp_max)/1E6, 3)
        expected_trained_max = round(int(baseline_sp + expected_trained_sp_max)/1E6, 3)

        # how many injectors min?
        # this is a fudge and does not account for the 500k, 400k and 300k SP
        # limits. It simply assumes 400k for all
        n_injectors_min = diff_min/0.4
        n_injectors_max = diff_max/0.4

        # how much is an injector currently worth?
        response = self._query_evepraisal('Large Skill Injector', market='jita')
        print(response.json())
        _, sell = self._get_buy_sell_from_appraisal(response)

        # work out total in isk spent using jita sell
        total_spend_min = round((n_injectors_min * sell)/1E9, 4)
        total_spend_max = round((n_injectors_max * sell)/1E9, 4)

        # fix this later
        author = ctx.message.author
        title = ('Estimated levels of injection ' \
                '\n 1 injector = {}b isk (Jita sell)'.format(round(sell/1E9, 4)))
        em = discord.Embed(author=author, title=title)
        em.add_field(name="Min Expected", value="{}m".format(expected_trained_min))
        em.add_field(name="Max Expected", value="{}m".format(expected_trained_max))
        em.add_field(name="Min Difference", value="{}m".format(diff_min))
        em.add_field(name="Max Difference", value="{}m".format(diff_max))
        em.add_field(name="Min Isk", value="{}b isk".format(total_spend_min))
        em.add_field(name="Max Isk", value="{}b isk".format(total_spend_max))
        await self.bot.say(embed=em)

    @commands.command(pass_context=True, description='Ping evepraisal for buy/sell price')
    async def jitaprice(self, ctx, *data: str):
        """
        Get the Jita buy/sell price of an item
        """
        try:
            item = " ".join(data).lower()
        except:
            await self.bot.say('WTF!')
            return
        response = self._query_evepraisal(item, market='jita')
        print(response.json())
        buy, sell = self._get_buy_sell_from_appraisal(response)
        
        # format the response
        author = ctx.message.author
        title = ("Evepraisal result for item: " \
                 "{}".format(item))
        em = discord.Embed(author=author, title=title)
        if buy and sell:
            em.add_field(name="Buy", value="{:.3f}m isk".format(buy/1E6))
            em.add_field(name="Sell", value="{:.3f}m isk".format(sell/1E6))
        else:
            em.add_field(name="No such item", value="rekt")
        await self.bot.say(embed=em)

def setup(bot):
    bot.add_cog(Utils(bot))
