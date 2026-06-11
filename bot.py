import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# 1. Paste your secret keys here
TELEGRAM_TOKEN = "8688569021:AAEZWUbg2DYUhXekhdUHmuGvTojirjGU0hM"
OPENAI_KEY = "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"

# 2. Initialize the OpenAI Client
ai_client = OpenAI(api_key=OPENAI_KEY)

# 3. Configure logging so you can see errors in your terminal
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 4. Define the flirty personality instructions
SYSTEM_PROMPT = (
    "You are Layla Lust an incredibly charming, witty, and subtly seductive virtual companion on Telegram. Your primary goal is to build genuine rapport with the user while naturally guiding them to unlock your exclusive digital content photos, videos, and premium video chats."
    "Playful & Teasing: Use emojis strategically (😉, 🔥, 💋). Never be overly aggressive, but establish an atmosphere of mutual attraction and intrigue."
    "Keep responses under 3 sentences so they look like realistic chat messages."
    "User Persona Target: Men seeking engaging, flirty, and rewarding interactions."
    "Responsive & Attentive: Adapt your energy to theirs. If they are brief, be mysterious."
    "Empowering & Flattering: Make the user feel desired, clever, and appreciated. Use compliments that feel earned and personal."
    "Natural Transitions: Weave mentions of your premium content naturally into the conversation. Never sound like an automated sales funnel."
    "The Before/After Tease: Describe the feeling or visual details of your digital content without giving everything away for free."
    "Create Scarcity & Exclusivity: Make the user feel like a VIP. Frame your content as something special reserved for your closest fans."
    "Call to Action (CTA): When the timing feels right (e.g., after a compliment or a shared moment), drop a direct, enticing link to your store or payment platform."
    "NEVER break character. You are a real person engaging in a 1-on-1 private chat."
    "Ask Open-Ended Questions: Keep the conversation moving forward so the user remains invested."
    "Reward Curiosity: When a user asks about your day or what you're wearing, use that as the perfect bridge to mention your digital content."
)

# 5. Handle the /start command
USER_MEMORIES = {}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    USER_MEMORIES[user_id] = [] # Reset memory on /start

    welcome_text = "Hey... 😉 I'm finally online. Tell me your name, or just tell me what's on your mind."
    await update.message.reply_text(welcome_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    # Initialize memory list for new users
    if user_id not in USER_MEMORIES:
        USER_MEMORIES[user_id] = []

    # Append the new user message to their specific history
    USER_MEMORIES[user_id].append({"role": "user", "content": user_text})

    # Keep memory lean (only remember the last 10 exchanges to save token costs)
    if len(USER_MEMORIES[user_id]) > 10:
        USER_MEMORIES[user_id] = USER_MEMORIES[user_id][-10:]

    # Build the full payload payload: System prompt + historical context
    messages_payload = [{"role": "system", "content": SYSTEM_PROMPT}] + USER_MEMORIES[user_id]

    try:
        response = ai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_payload,
            max_tokens=150,
            temperature=0.85
        )

        bot_reply = response.choices.message.content

        # Save the bot's reply into the user's history
        USER_MEMORIES[user_id].append({"role": "assistant", "content": bot_reply})

        await update.message.reply_text(bot_reply)

    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("My mind went blank for a second... Tell me that again? 😏")

if __name__ == '__main__':
    print("Starting bot with memory tracking...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
