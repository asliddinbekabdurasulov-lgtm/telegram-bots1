import telebot
import random
from PIL import Image, ImageDraw, ImageFont
import os

# Bot tokeningizni yozing (8021039998:AAG2wT2I30rwbvFWrYtF7G8CoA6Yh-JUUdI)
TOKEN = "8021039998:AAG2wT2I30rwbvFWrYtF7G8CoA6Yh-JUUdI"
bot = telebot.TeleBot(TOKEN)

# Foydalanuvchi hisoblari
scores = {}

# Start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    scores[message.chat.id] = 0
    bot.send_message(
        message.chat.id,
        "?? Penalti o‘yiniga xush kelibsiz!\nQaysi tomonga tepmoqchisiz?",
        reply_markup=penalty_keyboard()
    )

# Tugmalar
def penalty_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("?? Chap", "?? Markaz", "?? O‘ng")
    return markup

# Natija rasmi yaratish
def create_result_image(user_choice, goalie_choice, result, score, chat_id):
    img = Image.new("RGB", (420, 260), (0, 120, 0))  # yashil fon
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
    except:
        font = ImageFont.load_default()

    draw.text((10, 20), f"Siz: {user_choice}", fill="white", font=font)
    draw.text((10, 60), f"Darvozabon: {goalie_choice}", fill="white", font=font)
    draw.text((10, 110), f"Natija: {result}", fill="yellow", font=font)
    draw.text((10, 170), f"Hisob: {score}", fill="cyan", font=font)

    filename = f"penalty_{chat_id}.jpg"
    img.save(filename)
    return filename

# O‘yin jarayoni
@bot.message_handler(func=lambda m: m.text in ["?? Chap", "?? Markaz", "?? O‘ng"])
def penalty_game(message):
    chat_id = message.chat.id
    user_choice = message.text
    goalie_choice = random.choice(["?? Chap", "?? Markaz", "?? O‘ng"])

    if user_choice == goalie_choice:
        result = "? Uslab qoldi!"
    else:
        result = "? GOOOOOL!"
        scores[chat_id] = scores.get(chat_id, 0) + 1

    score = scores.get(chat_id, 0)
    filename = create_result_image(user_choice, goalie_choice, result, score, chat_id)

    with open(filename, "rb") as photo:
        bot.send_photo(chat_id, photo)

    # Rasmni saqlashni tugatgandan so'ng o'chirib yuborish
    os.remove(filename)

# Botni ishga tushirish
try:
    bot.polling(none_stop=True)
except Exception as e:
    print(f"Xatolik yuz berdi: {e}")