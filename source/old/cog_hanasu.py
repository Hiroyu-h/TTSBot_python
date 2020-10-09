from discord.ext import commands # Bot Commands Frameworkのインポート
import discord
from voice_generator import create_WAV

# Commands.Cogのサブクラスとして Bot_Cogというクラスを定義
class Bot_Cog(commands.Cog):

    # Bot_Cogクラスのコンストラクタ Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    global voice_num
    global voice_speed
    voice_num = '0'
    voice_speed = '1.0'
    

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="華栖", description="TTS Bot for Discord:", color=0xeee657)
        embed.add_field(name="prefix",value="Command prefix : &",inline=False)
        embed.add_field(name="&join / &j ", value="VCに接続します。", inline=False)
        embed.add_field(name="&bye / &b ", value="VCから切断します。", inline=False)
        embed.add_field(name="&voice 0 ~ 5", value="声音を変更します。", inline=False)
        embed.add_field(name="&speed N", value="再生速度を変更します。初期値1.0", inline=False)
        embed.add_field(name="&help", value="helpを表示します。", inline=False)
        embed.add_field(name="ping", value="疎通確認です。", inline=False)
        
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong!')  

    @commands.command()
    async def join(self, ctx):
        print('#GET_voicechannel')
        vc = ctx.author.voice.channel
        print(vc)
        print('#JOIN_voicechannel')
        print('#JOIN TO:',vc)
        print('-------------------------')
        await vc.connect()

    @commands.command()
    async def j(self, ctx):
        print('#GET_voicechannel')
        vc = ctx.author.voice.channel
        print(vc)
        print('#JOIN_voicechannel')
        print('#JOIN TO:',vc)
        print('-------------------------')
        await vc.connect()

    @commands.command()
    async def bye(self, ctx):
        print('#DISCONNECT')
        print('-------------------------')
        await ctx.voice_client.disconnect()
        
    @commands.command()
    async def b(self, ctx):
        print('#DISCONNECT')
        print('-------------------------')
        await ctx.voice_client.disconnect()

    @commands.command()
    async def voice(self, ctx, num):
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

    @commands.command()
    async def speed(self, ctx, snum):
        global voice_speed
        voice_speed = snum
        await ctx.channel.send('再生スピードを変更しました。')
    
    @commands.Cog.listener()
    async def on_message(self, message):
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
        await self.bot.process_commands(message)

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Bot_Cog(bot)) # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
