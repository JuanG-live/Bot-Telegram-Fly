from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Reemplaza 'TU_TOKEN_DEL_BOT' con el token que te dio BotFatherr
# ¡Importante: No compartas tu token públicamente!
TOKEN = '7811585862:AAFJlaeCbCnrbBkeLFq28UyRgzqA1lhlxUA' # <--- Pega tu token aquí

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