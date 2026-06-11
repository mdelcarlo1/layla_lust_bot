import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# 1. Paste your secret keys here
TELEGRAM_TOKEN = "8688569021:AAEZWUbg2DYUhXekhdUHmuGvTojirjGU0hM"

# 2. Initialize the OpenAI Client
load_dotenv()
ai_client = OpenAI(api_key=OPENAI_API_KEY)

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
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = "Hey... 😉 I'm finally online. Tell me your name, or just tell me what's on your mind."
    await update.message.reply_text(welcome_text)

# 6. Handle normal text messages and call OpenAI
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        # Send the user's message to OpenAI along with the flirty system prompt
        response = ai_client.chat.completions.create(
            model="gpt-4o-mini", # Fast, cheap, and smart model
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            max_tokens=150,
            temperature=0.85 # Higher temperature means more creative, playful responses
        )

        bot_reply = response.choices[0].message.content
        await update.message.reply_text(bot_reply)

    except Exception as e:
        logging.error(f"Error calling OpenAI: {e}")
        await update.message.reply_text("Oops... my heart skipped a beat. Try messaging me again! 😉")

# 7. Start the bot application
if __name__ == '__main__':
    print("Starting your flirty bot... Press Ctrl+C to stop.")
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers for the start command and text messages
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until you close the terminal
    app.run_polling()
