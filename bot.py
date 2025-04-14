import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Replace YOUR_BOT_TOKEN with your actual bot token here
BOT_TOKEN = '7416274418:AAFw9IAI6iQ6myROv4w0MT1AbIq4TAdRgag'  

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey hero! Send /download <url> to get started 🚀")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a URL after /download")
        return

    url = context.args[0]
    await update.message.reply_text(f"Downloading from: {url}")

    ydl_opts = {
        'format': 'best',  # You can change this to other formats like 'bestaudio', 'worst', etc.
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,  # Don't download playlists
    }

    try:
        # Use yt-dlp to download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)  # Get the downloaded filename

        # Send the downloaded file to Telegram
        with open(filename, 'rb') as video_file:
            await update.message.reply_video(video_file)

        # Optionally, remove the file after sending
        os.remove(filename)
        await update.message.reply_text("File uploaded successfully! 📤")

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

if __name__ == "__main__":
    # Initialize the bot with your token
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("download", download))
    print("Bot is running...")  # You should see this
    app.run_polling()
