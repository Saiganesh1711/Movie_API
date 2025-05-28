import os
from flask import Flask, request
import telebot

# Your Telegram Bot Token (load from environment variable for security)
TOKEN = os.getenv("TELEGRAM_TOKEN", "7773162114:AAG7jlwgMrZRhGCmRMCrXWSwsl-ez95ntuM")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Sample movie reviews dictionary
movie_reviews = {
    "inception": "Inception is a mind-bending thriller with stunning visuals. 9/10",
    "avatar": "Avatar is a visually spectacular blockbuster. 8/10",
    "titanic": "Titanic is an emotional epic with unforgettable performances. 9.5/10"
}

# Webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.get_data(as_text=True))
    bot.process_new_updates([update])
    return "OK", 200

# Command handler
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "🎬 Welcome to Movie Reviewer Bot!\nSend me the name of a movie and I'll review it.")

# Review handler
@bot.message_handler(func=lambda message: True)
def review_movie(message):
    movie = message.text.strip().lower()
    review = movie_reviews.get(movie, f"Sorry, I don't have a review for '{movie.title()}' yet.")
    bot.reply_to(message, review)

# Flask server entry point
if __name__ == "__main__":
    # Set the webhook URL (only needed once or when IP/domain changes)
    WEBHOOK_URL = os.getenv(f"https://movie-api-f6k0.onrender.com/{TOKEN}")  # e.g., https://your-service.onrender.com
    if WEBHOOK_URL:
        bot.remove_webhook()
        bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")

    # Run the Flask server
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

