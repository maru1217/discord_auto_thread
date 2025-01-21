import discord
from discord.ext import commands
import dotenv
import os
from server import server_thread


# .env ファイルを読み込む
dotenv.load_dotenv()

# TOKEN を取得
TOKEN = os.getenv("TOKEN")


# 必要な権限設定
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # メッセージ内容の取得を有効化
intents.guilds = True  # サーバー情報へのアクセスを有効化
bot = commands.Bot(command_prefix="!", intents=intents)

# 動作を許可するチャンネルのIDリスト（特定のチャンネルIDをここに追加）
ALLOWED_CHANNELS = [1260831426669051934,1260824835215589396,
                    1260825784386453656,1260824444222308383,
                    1260821586064310322,1260820531628736573,
                    1260826270942363688,1260820266142011448,
                    1260821015617863712,1260826318820479037,
                    1303186671747203113,1311494211392110612,
                    1303237728946618378,1311499335418253384
                    ]

@bot.event
async def on_ready():
    print(f"Botが起動しました。ログイン: {bot.user}")

@bot.event
async def on_message(message):
    # ボット自身のメッセージを無視
    if message.author.bot:
        return

    # メッセージが許可されたチャンネルで送信された場合のみ動作
    if message.channel.id in ALLOWED_CHANNELS:
        # メッセージが通常のテキストチャンネルの場合
        if isinstance(message.channel, discord.TextChannel):
        # メッセージが返信かどうかを判定
            if message.reference:
                print(f"返信メッセージが検出されました: {message.content}")
                return  # 返信の場合は何もしない
            # スレッドを作成
            thread_name = f"{message.author.display_name}'s thread"
            thread = await message.create_thread(
                name=thread_name,
                auto_archive_duration=4320  # 3日間
            )            

        # スレッド内のメッセージを無視
        elif isinstance(message.channel, discord.Thread):
            print(f"スレッド {message.channel.name} で送信されたメッセージを無視します。")
            return

# Koyeb用 サーバー立ち上げ
server_thread()
# Botを起動
bot.run(TOKEN)
