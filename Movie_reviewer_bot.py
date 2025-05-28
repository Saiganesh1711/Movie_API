import os
from flask import Flask, request
import telebot
import requests

TOKEN = os.environ.get("BOT_TOKEN", "7773162114:AAG7jlwgMrZRhGCmRMCrXWSwsl-ez95ntuM")
OMDB_API_KEY = os.environ.get("OMDB_API_KEY", "b7f1eaab")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

OMDB_URL = "http://www.omdbapi.com/?apikey={}&t={}"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.data.decode("utf-8"))
    bot.process_new_updates([update])
    return "!", 200

@app.route("/", methods=["GET"])
def index():
    return "🎥 Movie Reviewer Bot is running!"

@bot.message_handler(commands=["start"])
def welcome(message):
    bot.send_message(message.chat.id, "🎬 Welcome to the Movie Reviewer Bot! Send a movie name to get a review.")

@bot.message_handler(func=lambda msg: True)
def movie_lookup(message):
    title = message.text.strip()
    url = OMDB_URL.format(OMDB_API_KEY, title)
    response = requests.get(url)
    data = response.json()

    if data.get("Response") == "True":
        reply = (
            f"🎥 <b>{data['Title']} ({data['Year']})</b>\n"
            f"⭐ IMDb Rating: {data['imdbRating']}\n"
            f"📝 {data['Plot']}"
        )
    else:
        reply = "❌ Movie not found. Please try another title."

    bot.send_message(message.chat.id, reply, parse_mode="HTML")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    bot.remove_webhook()
    bot.set_webhook(url=f"https://movie-api-f6k0.onrender.com/{TOKEN}")
    app.run(host="0.0.0.0", port=port)
