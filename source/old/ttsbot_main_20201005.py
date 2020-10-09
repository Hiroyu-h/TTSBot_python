import discord  # dicordライブラリのインポート
from discord.ext import commands
import asyncio
import os
import configparser
import subprocess
import traceback
import ffmpeg
from voice_generator import create_WAV
# import cog_hanasu as Hanasu_Cog

# ----------------------------------------- #

# config = configparser.ConfigParser()
# config.read('src/config.ini')

INITIAL_EXTENSIONS = [
    'cog_hanasu'
]

class hanasu(commands.Bot):

 # コンストラクタ
    def __init__(self, command_prefix):
        # スーパークラスのコンストラクタに値を渡して実行
        super().__init__(command_prefix)

        # INITIAL_COGSに格納されている名前から、コグを読み込む。
        # エラーが発生した場合は、エラー内容を表示。
        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()
    
    async def on_ready(self):
        # コマンドラインに表示される
        print('-------------------------')
        print('#Logged in as ...')
        print('#NAME:',self.user.name)    # botの名前
        print('#ID  :',self.user.id)      # botのID
        print('-------------------------')
        # Hanasu_Cog.setup(hanasu)
        # text = f'Logged on as {hanasu.user}'
        # await send2devloper(text)


# async def send2devloper(text):
#     developer = hanasu.get_user(config.getint('BOT', 'developer'))
#     dm = await developer.create_dm()
#     await dm.send(text)


# MyBotのインスタンス化及び起動処理。
if __name__ == '__main__':
    bot = hanasu(command_prefix='&') # command_prefixはコマンドの最初の文字として使うもの。 e.g. !ping
    bot.run('NzYxNzc2OTI4MDU4NzY5NDQ4.X3fiDA.FraNHwdRc1Yaww4C8pmMHgU1Ips') # Botのトークン

# hanasu.run('NzYxNzc2OTI4MDU4NzY5NDQ4.X3fiDA.DHgJ7qAV1sE4k7d1xogI9Cf-3WY')

#bot.run('NzYxNzc2OTI4MDU4NzY5NDQ4.X3fiDA.DHgJ7qAV1sE4k7d1xogI9Cf-3WY') # Botのトークン