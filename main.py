import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
import random
import json

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory user data storage (replace with persistent DB for production)
users_data = {}

# YouTube and Telegram task URLs
YOUTUBE_CHANNEL_URL = "https://www.youtube.com/channel/YOUR_CHANNEL_ID"
TELEGRAM_CHANNEL_URL = "https://t.me/YOUR_CHANNEL_ID"

# Start command: Initializes the game
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    # Initialize new user
    if user_id not in users_data:
        users_data[user_id] = {"username": username, "points": 0, "energy": 100, "tasks_completed": {"youtube": False, "telegram": False}}

    update.message.reply_text(
        f"Welcome to Mining Game, {username}! 🏞\n\n"
        "Use /mine to start mining and earn points! 🏆\n"
        "Complete tasks to earn more rewards: \n"
        "/subscribe_youtube - Subscribe to YouTube channel\n"
        "/subscribe_telegram - Join the Telegram channel\n"
        "Use /status to check your energy and points! 🔋"
    )

# Help command: Lists available commands
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "/start - Start the game\n"
        "/mine - Start mining\n"
        "/status - Check your status\n"
        "/leaderboard - See the top miners\n"
        "/subscribe_youtube - Complete YouTube subscription task\n"
        "/subscribe_telegram - Complete Telegram subscription task"
    )

# Mine command: Simulates mining, consumes energy, and rewards points
def mine(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if user_id not in users_data:
        update.message.reply_text("Please use /start to initialize the game.")
        return

    user = users_data[user_id]
    
    if user["energy"] < 10:
        update.message.reply_text("You are too tired to mine. Come back later when your energy is restored.")
        return

    reward = random.randint(5, 20)
    user["points"] += reward
    user["energy"] -= 10

    update.message.reply_text(f"You mined {reward} points! You now have {user['points']} points.")

# Status command: Displays user's points and energy
def status(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if user_id not in users_data:
        update.message.reply_text("Please use /start to initialize the game.")
        return

    user = users_data[user_id]
    update.message.reply_text(
        f"🔋 Energy: {user['energy']}\n"
        f"🏆 Points: {user['points']}\n"
        f"📺 YouTube Subscription: {'Completed' if user['tasks_completed']['youtube'] else 'Pending'}\n"
        f"📢 Telegram Subscription: {'Completed' if user['tasks_completed']['telegram'] else 'Pending'}"
    )

# YouTube subscription task: Provides the link and asks the user to confirm
def subscribe_youtube(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user = users_data.get(user_id)

    if user and not user["tasks_completed"]["youtube"]:
        update.message.reply_text(
            f"Please subscribe to our YouTube channel: {YOUTUBE_CHANNEL_URL}\n"
            "After subscribing, use /confirm_youtube to claim your reward!"
        )
    else:
        update.message.reply_text("You have already completed the YouTube subscription task.")

# Telegram subscription task: Provides the link and asks the user to confirm
def subscribe_telegram(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user = users_data.get(user_id)

    if user and not user["tasks_completed"]["telegram"]:
        update.message.reply_text(
            f"Please join our Telegram channel: {TELEGRAM_CHANNEL_URL}\n"
            "After joining, use /confirm_telegram to claim your reward!"
        )
    else:
        update.message.reply_text("You have already completed the Telegram subscription task.")

# Confirm YouTube subscription
def confirm_youtube(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user = users_data.get(user_id)

    if user and not user["tasks_completed"]["youtube"]:
        user["tasks_completed"]["youtube"] = True
        user["points"] += 50  # Reward for completing the task
        update.message.reply_text("You have successfully completed the YouTube subscription task! You earned 50 points!")
    else:
        update.message.reply_text("You have already completed this task or use /subscribe_youtube first.")

# Confirm Telegram subscription
def confirm_telegram(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user = users_data.get(user_id)

    if user and not user["tasks_completed"]["telegram"]:
        user["tasks_completed"]["telegram"] = True
        user["points"] += 50  # Reward for completing the task
        update.message.reply_text("You have successfully completed the Telegram subscription task! You earned 50 points!")
    else:
        update.message.reply_text("You have already completed this task or use /subscribe_telegram first.")

# Leaderboard command: Shows the top miners
def leaderboard(update: Update, context: CallbackContext) -> None:
    sorted_users = sorted(users_data.items(), key=lambda x: x[1]['points'], reverse=True)
    leaderboard_text = "🏆 Leaderboard 🏆\n"

    for idx, (user_id, user) in enumerate(sorted_users[:10], 1):
        leaderboard_text += f"{idx}. {user['username']} - {user['points']} points\n"

    update.message.reply_text(leaderboard_text)

# Main function to set up the bot and commands
def main():
    # Replace 'YOUR_TOKEN' with your actual bot token
    updater = Updater("7645756916:AAEsMfv_Rl8xYCY3RjvxY-mbFnsHv12ffV8", use_context=True)
    dispatcher = updater.dispatcher

    # Register commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("mine", mine))
    dispatcher.add_handler(CommandHandler("status", status))
    dispatcher.add_handler(CommandHandler("leaderboard", leaderboard))
    dispatcher.add_handler(CommandHandler("subscribe_youtube", subscribe_youtube))
    dispatcher.add_handler(CommandHandler("subscribe_telegram", subscribe_telegram))
    dispatcher.add_handler(CommandHandler("confirm_youtube", confirm_youtube))
    dispatcher.add_handler(CommandHandler("confirm_telegram", confirm_telegram))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
