import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
import os
import datetime

import nana

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

NOTICE_CHANNEL_ID = int(os.environ.get("NOTICE_CHANNEL_ID"))
DIFF_JST_FROM_UTC = 9

class BotMain(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

    async def on_ready(self):
        print('on ready.')

    async def on_voice_state_update(self, member, before, after):
        channel = bot.get_channel(NOTICE_CHANNEL_ID)
        if before.channel.guild is channel.guild:
        # 通知チャンネルと同じサーバーにのみ反応させる
          now = datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)
          now_str = now.strftime('%Y-%m-%d %H:%M:%S')
          if before.channel is None and after.channel:
              await channel.send(f'{now_str} - {member.name} が{after.channel.name} に参加したよ。')
          elif after.channel is None and before.channel:
              await channel.send(f'{now_str} - {member.name} が{before.channel.name} から出たよ。')
          elif after.channel is not before.channel:
              await channel.send(f'{now_str} - {member.name} が{before.channel.name} から {after.channel.name}に移動したよ。')


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
