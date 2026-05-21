import os
import re
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8842988324:AAFqEHucbIgEHdvyVxkvCvp20_12mVgIRWA"

def is_instagram_url(text):
    return bool(re.search(r'instagram\.com/(reel|p|tv)/', text))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    
    urls = re.findall(r'https?://\S+', text)
    instagram_urls = [u for u in urls if is_instagram_url(u)]
    
    if not instagram_urls:
        return
    
    url = instagram_urls[0]
    await update.message.reply_text("⏳ Скачую відео...")
    
    output_path = f"video_{update.message.message_id}.mp4"
    
    try:
        subprocess.run([
            "python", "-m", "yt_dlp",
            "-o", output_path,
            "--merge-output-format", "mp4",
            url
        ], check=True, timeout=60)
        
        with open(output_path, "rb") as video_file:
            await update.message.reply_video(video=video_file)
    
    except subprocess.TimeoutExpired:
        await update.message.reply_text("❌ Час очікування вийшов.")
    except Exception as e:
        await update.message.reply_text(f"❌ Помилка: {e}")
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.run_polling()
