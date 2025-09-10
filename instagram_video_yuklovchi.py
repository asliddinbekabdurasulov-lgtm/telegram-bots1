import telebot
import instaloader
import os

# Bot tokeningizni yozing
BOT_TOKEN = "8360733713:AAF-FEPnlYibW5SjZ0rly2N3TUs92DZkm4w"
bot = telebot.TeleBot(BOT_TOKEN)

# Instaloader obyekt
L = instaloader.Instaloader()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! 👋 Menga Instagram video linkini yuboring, men uni sizga yuklab beraman.")

@bot.message_handler(func=lambda m: True)
def download_instagram_video(message):
    url = message.text.strip()

    if "instagram.com" not in url:
        bot.reply_to(message, "❌ Bu Instagram linki emas. Iltimos, to‘g‘ri link yuboring.")
        return

    try:
        shortcode = url.split("/")[-2]  # post shortcodi
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # faqat video bo‘lsa
        if post.is_video:
            filename = f"{shortcode}.mp4"
            L.download_post(post, target="downloads")

            # faylni topib yuboramiz
            for file in os.listdir("downloads"):
                if file.endswith(".mp4"):
                    with open(os.path.join("downloads", file), "rb") as video:
                        bot.send_video(message.chat.id, video)
                    os.remove(os.path.join("downloads", file))
        else:
            bot.reply_to(message, "❌ Bu postda video yo‘q.")

    except Exception as e:
        bot.reply_to(message, f"Xatolik: {e}")

# Botni ishlatamiz
bot.polling(none_stop=True)