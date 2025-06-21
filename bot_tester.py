from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

# Función que se ejecuta cuando el usuario envía el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        f"¡Hola {user.mention_html()}! Soy tu bot de alertas de vuelos. "
        f"Estoy listo para empezar a buscar vuelos baratos desde Ezeiza hacia Dublin, Madrid o Barcelona.",
        # Puedes quitar 'reply_markup' si no quieres que aparezca el teclado de ejemplo
        # reply_markup=ForceReply(selective=True),
    )

# Función principal para iniciar el bot
def main() -> None:
    """Inicia el bot."""
    # Crea la aplicación y le pasa el token de tu bot.
    application = Application.builder().token(TOKEN).build()

    # Añade un manejador para el comando /start.
    application.add_handler(CommandHandler("start", start))

    # Ejecuta el bot hasta que presiones Ctrl-C
    print("Bot iniciado. Presiona Ctrl-C para detenerlo.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()