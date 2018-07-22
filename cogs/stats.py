import discord, os
from discord.ext import commands
from utils import checks, output, parsing
from aiohttp import ClientSession
import urllib.request
import json

class Stats:
    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def stats(self, ctx, amount=1):
        """
        Show stats about NORT
        """
        channel_name = ctx.message.channel.name
        allowed_channels = parsing.parse_json('config.json')['command_channels'][ctx.command.name]
        if channel_name not in allowed_channels:
            return

        headers={"user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"}
        try:
            async with ClientSession() as session:
                async with session.get("https://coinlib.io/api/v1/coin?key=593ce9b1bef849c6&pref=BTC&symbol=NORT", headers=headers) as response:
                    responseRaw = await response.read()
                    priceData = json.loads(responseRaw)
                    for item in priceData:
                        embed= discord.Embed(colour=0x00FF00)
                        embed.set_author(name='NORT Information', icon_url="http://explorer.nort.network/images/logo.png")
                        embed.add_field(name="Price (BTC)", value="${}".format(item['price']))                    
                        embed.set_footer(text="https://wallet.crypto-bridge.org/market/BRIDGE.NORT_BRIDGE.BTC", icon_url="http://explorer.nort.network/images/logo.png")
                    await self.bot.say(embed=embed)
        except:
            await self.bot.say(":warning: Error fetching prices!")


def setup(bot):
    bot.add_cog(Stats(bot))
