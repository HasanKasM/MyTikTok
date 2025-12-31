import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


TOKEN = "7220281213:AAG8YqvQ-rTJCaCpt3sFXHQo1QC5BH78qqw" #عدل بس هذا


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أرسل لي رابط فيديو أو صور من تيك توك وسأقوم بتحميلها لك بدون علامة مائية.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    if "tiktok.com" not in url:
        await update.message.reply_text("عذراً، يرجى إرسال رابط تيك توك صحيح.")
        return

    msg = await update.message.reply_text("جاري المعالجة... انتظر قليلاً ⏳")

    try:
        
        api_url = f"https://www.tikwm.com/api/?url={url}"
        response = requests.get(api_url).json()

        if response.get('code') == 0:
            data = response['data']
            
            
            if 'images' in data and data['images']:
                for img in data['images']:
                    await update.message.reply_photo(photo=img)
                await msg.delete()
            else:
                
                video_url = data['play']
                caption = data.get('title', 'تم التحميل بواسطة بوتك')
                await update.message.reply_video(video=video_url, caption=caption)
                await msg.delete()
        else:
            await msg.edit_text("فشل استخراج الفيديو، تأكد من أن الرابط عام وليس خاصاً.")

    except Exception as e:
        await msg.edit_text(f"حدث خطأ أثناء المعالجة: {e}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()
