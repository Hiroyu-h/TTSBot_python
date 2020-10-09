import asyncio
import configparser
import errno
import os
import pathlib
import re
import subprocess
import sys
import traceback

import discord  # dicordライブラリのインポート
import ffmpeg
from discord.ext import commands

from voice_generator import create_WAV

# ----------------------------------------- #
# ◆変更履歴◆
# 絵文字が含まれていると文章呼んでくれない
# ＿(　_´ω`)_ﾍﾟｼｮ　「おめが ぺしょ」って読み上げる
# チャット同時だと読み上げない ⇒ ◆対応済
# ｗｗをダブリュダブリュって呼んでしまう
# メンション読ませると壊れたみたいに読み上げる ⇒ ◆対応済
# メンションでニックネームを呼ばせる　⇒　◆対応済
# ロールメンションの読み ⇒　◆対応済
# config.ini から値を読み取って起動させる ⇒　◆対応済
# ----------------------------------------- #
global version
global voice_num
global voice_speed

# このファイルがあるディレクトリ
cwdp = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------
# iniファイルの読み込み
config_ini = configparser.ConfigParser()
config_path = f'{cwdp}\\config.ini'

if os.path.exists(config_path):
    # iniファイルを開く
    with open(config_path, encoding='utf-8') as cfp:
        config_ini.read_file(cfp)
        # デフォルト値取得
        read_bot = config_ini['DEFAULT']
        bot_name = read_bot.get('BOT')
        
        # 稼働するBOTの値取得
        read_config = config_ini[bot_name]
        bot_token = read_config.get('BOT_TOKEN')
        version = read_config.get('Version')
        voice_num = read_config.get('Voice')
        voice_speed = read_config.get('Speed')
                       
else:
    # 指定したiniファイルが存在しない場合、エラー発生
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_path)


hanasu = commands.Bot(command_prefix='&')
hanasu.remove_command('help')



# async def send2devloper(text):
#     developer = hanasu.get_user(config.getint('BOT', 'developer'))
#     dm = await developer.create_dm()
#     await dm.send(text)

# def get_data(message):
#     command = message.content
#     data_table = {
#         '/members': message.guild.members, # メンバーのリスト
#         '/roles': message.guild.roles, # 役職のリスト
#         '/text_channels': message.guild.text_channels, # テキストチャンネルのリスト
#         '/voice_channels': message.guild.voice_channels, # ボイスチャンネルのリスト
#         '/category_channels': message.guild.categories, # カテゴリチャンネルのリスト
#     }
#     return data_table.get(command, '無効なコマンドです')


@hanasu.event
async def on_ready():
    # コマンドラインに表示される
    print('-------------------------')
    print('#Logged in as ...')
    print('NAME:',hanasu.user.name)    # botの名前
    print('ID  :',hanasu.user.id)      # botのID
    print('-------------------------')
    
    # text = f'Logged on as {hanasu.user}'
    # await send2devloper(text)

@hanasu.command()
async def help(ctx):
    embed = discord.Embed(title=hanasu.user.name, description=f"◆ {hanasu.user.name} ver {version} ◆ for Discord", color=0xeee657)
    embed.add_field(name="prefix",value="Command prefix : &",inline=False)
    embed.add_field(name="&join / &j ", value="VCに接続します。", inline=False)
    embed.add_field(name="&bye / &b ", value="VCから切断します。", inline=False)
    embed.add_field(name="&voice 0 ~ 6", value="声音を変更します。", inline=False)
    embed.add_field(name="&speed N", value="再生速度を変更します。初期値1.0", inline=False)
    embed.add_field(name="&help", value="helpを表示します。", inline=False)
    embed.add_field(name="ping", value="疎通確認です。", inline=False)
    
    await ctx.send(embed=embed)

@hanasu.command()
async def ping(ctx):
    await ctx.send('pong!')  

@hanasu.command()
async def join(ctx):
    global guild_id
    guild_id = ctx.guild.id
    print('#GET_voicechannel')
    vc = ctx.author.voice.channel
    print('#JOIN_voicechannel')
    print('JOIN TO:',vc)
    print(ctx.guild.members)
    print('-------------------------')
    await vc.connect()

@hanasu.command()
async def j(ctx):
    print('#GET_voicechannel')
    vc = ctx.author.voice.channel
    print('#JOIN_voicechannel')
    print('JOIN TO:',vc)
    print(ctx.guild.members)
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
    # voiceコマンドのメッセージ
    tuple_voice = (
        '声音を女声_0に変更しました。',
        '声音を女声_1に変更しました。',
        '声音を女声_2に変更しました。',
        '声音を女声_3に変更しました。',
        '声音を女声_4に変更しました。',
        '声音を女声_5に変更しました。',
        '声音を男声に変更しました。'
    )
    # 入力された数がタプルより大きいなら変更しない
    if int(num) > len(tuple_voice) - 1 or int(num) < 0:
        await ctx.channel.send('無効な値です。')
        await ctx.channel.send(f'0から{len(tuple_voice) - 1}までの値を入力してください。')
    else:
        await ctx.channel.send(tuple_voice[int(num)])
        voice_num = num


@hanasu.command()
async def speed(ctx, snum):
    global voice_speed
    voice_speed = snum
    await ctx.channel.send('再生スピードを変更しました。')

# メッセージ受信時
@hanasu.event
async def on_message(message):
    msgclient = message.guild.voice_client

    # BOTからのメッセージは無視
    if message.author.bot:
        return
    else:
        # コマンドプレフィックスは無視
        if message.content.startswith('&'):
            pass

        else:
            if msgclient:
                print('SERVER:',message.guild.id)
                print('AUTHOR:',message.author.id)
                print('CONTENT:',message.content)

                # mention と channel_mentionを名前へ置換
                mn_list = message.raw_mentions
                ch_list = message.raw_channel_mentions
                rl_list = message.raw_role_mentions
                print('mn_list:',message.raw_mentions)
                # IDに対応する名前の辞書を作成
                mn_dict = {}
                ch_dict = {}
                rl_dict = {}
                                
                # mentionの、ユーザネームへの置換
                for ment in mn_list:
                    fetchmember = await message.guild.fetch_member(ment)
                    print(fetchmember)
                    # print(fetchmember.name)
                    # print(fetchmember.nick)
                    ptrn = '^<@!'
                    # print('re:',re.match(ptrn,message.content))
                    
                    if fetchmember.nick:
                        fetch_name = fetchmember.nick
                    else:
                        fetch_name = fetchmember.name
                    
                    if re.match(ptrn,message.content):
                        mn_dict['<@!{}>'.format(str(ment))] = fetch_name
                    else:
                        mn_dict['<@{}>'.format(str(ment))] = fetch_name
                                           
                # channel_mentionの、チャンネル名への置換
                for cnls in ch_list:
                    ch_dict['<#{}>'.format(str(cnls))] = message.guild.get_channel(cnls).name
                
                for roles in rl_list:
                    rl_dict['<@&{}>'.format(str(roles))] = message.guild.get_role(roles).name
                    
                # 変換テーブルの作成
                for me_key in mn_dict.keys():
                    message.content = message.content.replace(me_key, mn_dict[me_key], 1)
                for ch_key in ch_dict.keys():
                    message.content = message.content.replace(ch_key, ch_dict[ch_key], 1)
                for rl_key in rl_dict.keys():
                    message.content = message.content.replace(rl_key, rl_dict[rl_key], 1)
                
                # 音声ファイルの場所
                voice_file = 'C:\\open_jtalk\\output.wav'
                
                # 再生中の場合は待つ
                print('IS_PLAYING:',msgclient.is_playing())
                while(msgclient.is_playing()):
                    await asyncio.sleep(1.0)
                    print('*** waiting... ***')
                print('VOICE:',voice_num)
                print('SPEED:',voice_speed)
                # 音声ファイル作成モジュールに投げる
                create_WAV(message.content, voice_num, voice_speed)
                source = discord.FFmpegPCMAudio(voice_file)
                # 音声を再生する
                msgclient.play(source)
                await asyncio.sleep(0.5)
                # os.remove(voice_file)

                print('-------------------------')
            else:
                pass
    await hanasu.process_commands(message)

hanasu.run(bot_token)
