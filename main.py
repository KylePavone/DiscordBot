import json
import random
import requests
import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandInvokeError
from youtube_dl import YoutubeDL

from utils.utils import get_req
from config.settings import settings


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='>', intents=intents)


def play(voice, url):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        if 'https://' in url:
            info = ydl.extract_info(url, download=False)
        else:
            info = ydl.extract_info(f'ytsearch:{url}', download=False)['entries'][0]
    link = info['formats'][0]['url']
    voice.play(discord.FFmpegPCMAudio(executable='ffmpeg\\ffmpeg.exe', source=link, **FFMPEG_OPTIONS))


class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        to_slap = random.choice(ctx.guild.members)
        return f'__{ctx.author.name}__ slapped __{to_slap.name}__ because {argument}'


@bot.command()
async def slap(ctx, *, reason: Slapper):
    await ctx.send(reason)


YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


# sound command
@bot.command()
async def start(ctx, url=None):
    guild = discord.utils.get(bot.guilds, name='MySuperAI')
    if guild is not None:
        channel = discord.utils.get(guild.text_channels, name='Основной')
    ch = ctx.message.author.voice.channel
    await ch.connect()


@bot.command()
async def video(ctx, url):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        play(voice, url)


@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    await voice.stop()


@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Hello {author.mention}!')


@bot.command()
async def fox(ctx):
    response = requests.get('https://some-random-api.ml/img/fox') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON
    embed = discord.Embed(color = 0xff9900, title = 'Random Fox') # Создание Embed'a
    embed.set_image(url=json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed


bot.run(settings['token'])
