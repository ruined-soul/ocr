import os
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from PIL import Image
import pytesseract
from flask import Flask

# Initialize Flask app (needed for Koyeb deployment)
app = Flask(__name__)

# OCR function
def extract_text(image_path):
    try:
        # Open image and perform OCR
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text if text.strip() else "No text found!"
    except Exception as e:
        return f"Error during OCR: {str(e)}"

# Start command
async def start(update: Update, context):
    await update.message.reply_text("Hi! Send me a manga image, and I'll extract the text for you!")

# Handle received images
async def handle_image(update: Update, context):
    file = await update.message.photo[-1].get_file()  # Get the highest quality image
    file_path = f"{file.file_id}.jpg"
    await file.download_to_drive(file_path)
    
    # Extract text from image
    extracted_text = extract_text(file_path)
    
    # Send the extracted text back to the user
    await update.message.reply_text(f"Extracted Text:\n\n{extracted_text}")
    
    # Clean up the downloaded image
    os.remove(file_path)

# Fallback message handler for non-image messages
async def unknown_message(update: Update, context):
    await update.message.reply_text("Please send an image for OCR.")

# Flask route to keep bot alive (for Koyeb)
@app.route('/')
def index():
    return "Bot is running!"

# Main function
async def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")  # Your Telegram bot token should be in the environment variable
    # main.py (add this line in the `main` function)
await app.start_webhook(listen="0.0.0.0", port=8080, url_path=token, webhook_url=f"https://mature-tabitha-xebal-fc34731e.koyeb.app/{token}")
    # Create the Application instance
    app = ApplicationBuilder().token(token).build()
    
    # Add command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.add_handler(MessageHandler(filters.ALL, unknown_message))

    # Start the bot
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
