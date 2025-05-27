import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7773162114:AAG7jlwgMrZRhGCmRMCrXWSwsl-ez95ntuM"
OMDB_API_KEY = "b7f1eaab"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Welcome to Movie Review Bot!\nSend me any movie title to get a review.")

# Handle movie title queries
async def get_movie_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_title = update.message.text
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url).json()

    if response.get("Response") == "True":
        title = response.get("Title")
        year = response.get("Year")
        rating = response.get("imdbRating")
        plot = response.get("Plot")
        reply = f"🎥 *{title}* ({year})\n⭐ IMDb: {rating}\n📝 {plot}"
    else:
        reply = "❌ Movie not found. Try a different title."

    await update.message.reply_text(reply, parse_mode="Markdown")

# Setup bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_movie_review))

app.run_polling()
