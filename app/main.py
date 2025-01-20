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
ALLOWED_CHANNELS = [1260831426669051934]

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
