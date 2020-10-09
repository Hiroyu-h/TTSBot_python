import discord  # dicordライブラリのインポート
from discord.ext import commands
import asyncio
import os
import subprocess
import traceback
import ffmpeg
from voice_generator import create_WAV
import cogs.cog as Bot_Cog

# INITIAL_EXTENSIONS = [
#     'cogs.testcog'
# ]




global voice_num
global voice_speed

# クラスの定義。ClientのサブクラスであるBotクラスを継承。
class Hanasu_Bot(commands.Bot(command_prefix='&')):

    # MyBotのコンストラクタ。
    def __init__(self, command_prefix):
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix)

        # INITIAL_COGSに格納されている名前から、コグを読み込む。
        # エラーが発生した場合は、エラー内容を表示。
        # for cog in INITIAL_EXTENSIONS:
        #     try:
        #         self.load_extension(cog)
        #     except Exception:
        #         traceback.print_exc()

    #@client.event
    async def on_ready(self):
        print('#START...')
        print('#READY...')
        print('#NAME:',self.user.name)
        print('#ID:',self.user.id)
        print('-------------------------')

if __name__ == '__main__':
    bot = MyBot(command_prefix='&') # command_prefixはコマンドの最初の文字として使うもの。 e.g. !ping
    
    voice_num = '0'
    voice_speed = '1.0'
    
    bot.remove_command('help')
    @bot.command()
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


    @bot.command()
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

    @bot.command()
    async def speed(ctx, snum):
        global voice_speed
        voice_speed = snum
        await ctx.channel.send('再生スピードを変更しました。:')

    @bot.event
    async def on_message(message):
        msgclient = message.guild.voice_client
        if message.author.bot:
            return
        else:
            if bot.user in message.mentions: # 話しかけられたかの判定
                await reply(message) # 返信する非同期関数を実行
            if message.content.startswith('&'):
                pass

            else:
                if message.guild.voice_client:
                    print(message.content)
                    create_WAV(message.content, voice_num, voice_speed)
                    source = discord.FFmpegPCMAudio("C:\\open_jtalk\\output.wav")
                    #message.guild.voice_client.play(source)
                    msgclient.play(source)
                    
                    print('-------------------------')
                else:
                    pass
        await bot.process_commands(message)

        # 返信する非同期関数を定義
    async def reply(message):
        reply = f'{message.author.mention} 呼んだ？' # 返信メッセージの作成
        await message.channel.send(reply) # 返信メッセージを送信
        

    bot.run('NzYxNzc2OTI4MDU4NzY5NDQ4.X3fiDA.DHgJ7qAV1sE4k7d1xogI9Cf-3WY') # Botのトークン
# client.run("NzYxNzc2OTI4MDU4NzY5NDQ4.X3fiDA.DHgJ7qAV1sE4k7d1xogI9Cf-3WY")
