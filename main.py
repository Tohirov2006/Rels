import telebot
from telebot import types
import json
import os

BOT_TOKEN = '7571461804:AAGyyhLf9Rwq6gWyZamt5H5GHA__pJzRK60'  # bu yerga tokeningizni yozing
ADMIN_ID = 7571461804
DATA_FILE = 'movies.json'

bot = telebot.TeleBot(BOT_TOKEN)

# Fayllarni o‘qish va yozish uchun yordamchi funksiyalar
def load_movies():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_movies(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

movies = load_movies()

# Boshlang'ich tugma
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Kino qidirish", "Yordam")
    if user_is_admin:
        markup.add("Kino qo‘shish", "Kino o‘chirish")
    return markup

def user_is_admin(user_id):
    return user_id == ADMIN_ID

# /start komandasi
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Salom! Kino botiga xush kelibsiz.", reply_markup=main_menu())

# Kino qidirish
@bot.message_handler(func=lambda m: m.text == "Kino qidirish")
def search_handler(message):
    msg = bot.send_message(message.chat.id, "Kino raqamini kiriting:")
    bot.register_next_step_handler(msg, search_movie)

def search_movie(message):
    movie_id = message.text
    if movie_id in movies:
        bot.send_document(message.chat.id, movies[movie_id])
    else:
        bot.send_message(message.chat.id, "Kino topilmadi.")

# Kino qo‘shish (faqat admin)
@bot.message_handler(func=lambda m: m.text == "Kino qo‘shish")
def add_handler(message):
    if not user_is_admin(message.from_user.id):
        return bot.send_message(message.chat.id, "Faqat admin qo‘shishi mumkin.")
    msg = bot.send_message(message.chat.id, "Yangi kino raqamini kiriting:")
    bot.register_next_step_handler(msg, get_movie_id)

def get_movie_id(message):
    movie_id = message.text
    msg = bot.send_message(message.chat.id, f"{movie_id} raqamli kinoga faylni yuboring:")
    bot.register_next_step_handler(msg, lambda m: save_file(m, movie_id))

def save_file(message, movie_id):
    if message.document:
        file_id = message.document.file_id
    elif message.photo:
        file_id = message.photo[-1].file_id
    elif message.video:
        file_id = message.video.file_id
    else:
        return bot.send_message(message.chat.id, "Fayl turi noto‘g‘ri.")
    
    movies[movie_id] = file_id
    save_movies(movies)
    bot.send_message(message.chat.id, f"{movie_id} raqamli kino saqlandi.")

# Kino o‘chirish (admin)
@bot.message_handler(func=lambda m: m.text == "Kino o‘chirish")
def delete_handler(message):
    if not user_is_admin(message.from_user.id):
        return bot.send_message(message.chat.id, "Faqat admin o‘chira oladi.")
    msg = bot.send_message(message.chat.id, "O‘chirmoqchi bo‘lgan kino raqamini kiriting:")
    bot.register_next_step_handler(msg, delete_movie)

def delete_movie(message):
    movie_id = message.text
    if movie_id in movies:
        del movies[movie_id]
        save_movies(movies)
        bot.send_message(message.chat.id, f"{movie_id} o‘chirildi.")
    else:
        bot.send_message(message.chat.id, "Bu raqamga mos kino topilmadi.")

# Yordam
@bot.message_handler(func=lambda m: m.text == "Yordam")
def help_handler(message):
    help_text = "Kino bot yordam:\n\n- Kino qidirish uchun: 'Kino qidirish'\n- Adminlar uchun: 'Kino qo‘shish', 'Kino o‘chirish'"
    bot.send_message(message.chat.id, help_text)

# Botni ishga tushurish
bot.polling()
