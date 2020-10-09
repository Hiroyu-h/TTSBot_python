import discord  # dicordライブラリのインポート
from discord.ext import commands
import asyncio
import os
import configparser
import subprocess
import traceback
import ffmpeg
from voice_generator import create_WAV


# ----------------------------------------- #

# config = configparser.ConfigParser()
# config.read('src/config.ini')

hanasu = commands.Bot(command_prefix='&')
hanasu.remove_command('help')
global voice_num
global voice_speed
voice_num = '0'
voice_speed = '1.0'

# async def send2devloper(text):
#     developer = hanasu.get_user(config.getint('BOT', 'developer'))
#     dm = await developer.create_dm()
#     await dm.send(text)

@hanasu.event
async def on_ready():
    # コマンドラインに表示される
    print('-------------------------')
    print('#Logged in as ...')
    print('#NAME:',hanasu.user.name)    # botの名前
    print('#ID  :',hanasu.user.id)      # botのID
    print('-------------------------')
    
    # text = f'Logged on as {hanasu.user}'
    # Hanasu_Cog.setup(hanasu)
    # await send2devloper(text)

@hanasu.command()
async def help(ctx):
    embed = discord.Embed(title="華栖", description="TTS Bot for Discord:", color=0xeee657)
    embed.add_field(name="prefix",value="Command prefix : &",inline=False)
    embed.add_field(name="&join / &j ", value="VCに接続します。", inline=False)
    embed.add_field(name="&bye / &b ", value="VCから切断します。", inline=False)
    embed.add_field(name="&voice 0 ~ 5", value="声音を変更します。", inline=False)
    embed.add_field(name="&speed N", value="再生速度を変更します。初期値1.0", inline=False)
    embed.add_field(name="&help", value="helpを表示します。", inline=False)
    embed.add_field(name="ping", value="疎通確認です。", inline=False)
    
    await ctx.send(embed=embed)

@hanasu.command()
async def ping(ctx):
    await ctx.send('pong!')  

@hanasu.command()
async def join(ctx):
    print('#GET_voicechannel')
    vc = ctx.author.voice.channel
    print(vc)
    print('#JOIN_voicechannel')
    print('#JOIN TO:',vc)
    print('-------------------------')
    await vc.connect()

@hanasu.command()
async def j(ctx):
    print('#GET_voicechannel')
    vc = ctx.author.voice.channel
    print(vc)
    print('#JOIN_voicechannel')
    print('#JOIN TO:',vc)
    print('-------------------------')
    await vc.connect()

@hanasu.command()
async def bye(ctx):
    print('#DISCONNECT')
    print('-------------------------')
    await ctx.voice_client.disconnect()
    
@hanasu.command()
async def b(ctx):
    print('#DISCONNECT')
    print('-------------------------')
    await ctx.voice_client.disconnect()

@hanasu.command()
async def voice(ctx, num):
    global voice_num
    voice_num = num

    if voice_num == '0':
        await ctx.channel.send('声音を女声_0に変更しました。')
    elif voice_num == '1':
        await ctx.channel.send('声音を女声_1に変更しました。')
    elif voice_num == '2':
        await ctx.channel.send('声音を女声_2に変更しました。')
    elif voice_num == '3':
        await ctx.channel.send('声音を女声_3に変更しました。')
    elif voice_num == '4':
        await ctx.channel.send('声音を女声_4に変更しました。')
    else:
        await ctx.channel.send('声音を男声に変更しました。')

@hanasu.command()
async def speed(ctx, snum):
    global voice_speed
    voice_speed = snum
    await ctx.channel.send('再生スピードを変更しました。')

@hanasu.event
async def on_message(message):
    msgclient = message.guild.voice_client
    if message.author.bot:
        return
    else:
        if message.content.startswith('&'):
            pass

        else:
            if message.guild.voice_client:
                print(message.content)
                create_WAV(message.content, voice_num, voice_speed)
                source = discord.FFmpegPCMAudio("C:\\open_jtalk\\output.wav")
                msgclient.play(source)
                
                print('-------------------------')
            else:
                pass
    await hanasu.process_commands(message)

hanasu.run('NzYxNzc2OTI4MDU4NzY5NDQ4.X3fiDA.FraNHwdRc1Yaww4C8pmMHgU1Ips')

#bot.run('NzYxNzc2OTI4MDU4NzY5NDQ4.X3fiDA.DHgJ7qAV1sE4k7d1xogI9Cf-3WY') # Botのトークン