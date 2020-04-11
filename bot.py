import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
import os

import nana

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

BOT_TOKEN = os.environ.get("BOT_TOKEN")


class BotMain(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

    async def on_ready(self):
        print('on ready.')


bot = BotMain(['!', '！'])

fields = [
  {"name":"play_counts","disp":"再生数"},
  {"name":"applause_counts","disp":"拍手数"},
  {"name":"comment_counts","disp":"コメント数"},
]

@bot.command(name='info')
async def get_info(ctx, arg):
    """サウンドの情報を表示する"""
    info = nana.get_sound_info(arg)
    embed = discord.Embed(title=info["title"],
                          url=info['sound_url'],
                          description=info["artist_name"])
    embed.set_image(url=info["image"])
    embed.set_author(name=info["user_name"], url=info["user_url"], icon_url=info["icon_url"])
    for field in fields:
        embed.add_field(name=field["disp"],
                        value=info[field['name']],
                        inline=True)

    await ctx.send(embed=embed)



@bot.command(name='changename')
async def get_info(ctx, arg):
    await bot.user.edit(username=arg)
    await ctx.send(content="done.")


if __name__ == '__main__':
    bot.run(os.environ.get("BOT_TOKEN"))
