import os
import telebot
from telebot import types
from flask import Flask, request

TOKEN = "8735473938:AAH7UAN0KsYv12grxoSy089pGZYgDL5w-a4"
ADMIN_PHONE = "0997046363"
GAME_URL = "https://aman-blue-bingo.vercel.app" 

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🎮 Play Bingo", "💰 Wallet", "💳 Withdraw", "📞 Support")
    welcome = (f"💎 <b>እንኳን ወደ Aman Blue Bingo በሰላም መጡ!</b>\n\n"
               f"💵 የእርስዎ ቀሪ ሂሳብ: <b>0.00 ETB</b>\n\n"
               f"ለመጫወት ከታች ያለውን <b>'Play Bingo'</b> ቁልፍ ይጫኑ።")
    bot.send_message(message.chat.id, welcome, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text == "🎮 Play Bingo")
def play_game(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("🎰 Start Game (10 ETB)", web_app=types.WebAppInfo(GAME_URL))
    markup.add(btn)
    bot.send_message(message.chat.id, "🎯 መልካም እድል! ለመጫወት 'Start Game' የሚለውን ይጫኑ።", reply_markup=markup)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://' + os.environ.get('VERCEL_URL', 'aman-bingo.vercel.app') + '/' + TOKEN)
    return "Bot is running!", 200
