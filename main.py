from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import os
import logging
import asyncio
import requests

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to extract text from images (placeholder function using Tesseract OCR)
def extract_text(image_path):
    try:
        from PIL import Image
        import pytesseract
        # Extract text from image using Tesseract
        return pytesseract.image_to_string(Image.open(image_path))
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        return "Could not extract text."

# Handler for the /start command
async def start(update: Update, context):
    await update.message.reply_text("Welcome! Send me an image, and I'll extract the text for you.")

# Handler for image messages
async def handle_image(update: Update, context):
    try:
        # Get the file from the image
        file = await update.message.photo[-1].get_file()
        file_path = f"{file.file_id}.jpg"
        await file.download_to_drive(file_path)

        # Extract text from the image
        extracted_text = extract_text(file_path)

        # Send the extracted text back to the user
        await update.message.reply_text(f"Extracted Text:\n\n{extracted_text}")

        # Remove the image file after processing
        os.remove(file_path)
    except Exception as e:
        logger.error(f"Error handling image: {e}")
        await update.message.reply_text("Sorry, something went wrong while processing the image.")

# Main function to start the bot
async def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN')  # Get bot token from environment variable
    app = ApplicationBuilder().token(token).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    # Start the webhook (assuming Koyeb auto-assigns PORT and webhook URL)
    PORT = int(os.getenv("PORT", 8443))
    webhook_url = f"https://{os.getenv('KOYEB_APP_URL')}/{token}"

    logger.info(f"Setting webhook: {webhook_url}")
    await app.start_webhook(listen="0.0.0.0", port=PORT, url_path=token)
    await app.bot.set_webhook(url=webhook_url)

    # Keep the bot running
    await app.wait_for_shutdown()

if __name__ == '__main__':
    asyncio.run(main())
