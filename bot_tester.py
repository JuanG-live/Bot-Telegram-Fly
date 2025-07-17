from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
import asyncio
import threading
from level_api import get_month_prices
from telegram import Bot
from datetime import datetime
from dateutil.relativedelta import relativedelta

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


# Función que se ejecuta cuando el usuario envía el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    user = update.effective_user
    if user:
        await update.message.reply_html(
            f"¡Hola {user.mention_html()}! Soy tu bot de alertas de vuelos. "
            f"Estoy listo para empezar a buscar vuelos baratos desde Ezeiza hacia Dublin, Madrid o Barcelona.",
        )
    else:
        await update.message.reply_text("¡Hola! Soy tu bot de alertas de vuelos.")


def get_next_three_months():
    today = datetime.now()
    end_date = today + relativedelta(days=90)

    month_To_Check = []
    current = today.replace(day=1)
    while current <= end_date:
        month_To_Check.append((current.year, current.month))
        current += relativedelta(months=1)
    return month_To_Check


# Tarea de fondo para verificar ofertas cada 60 segundos
async def verificar_ofertas(bot: Bot, chat_id: str):
    destinations = ["DUB", "MAD", "BCN", "FCO"]
    while True:
        try:
            for year, month in get_next_three_months():
                for dest in destinations:
                    print(
                        f"Buscando vuelos baratos desde EZE -> {dest} Fecha aproximada: {year}-{month:02d}..."
                    )
                    result = get_month_prices(
                        origin="EZE",
                        dest=dest,
                        outbound=f"{year}-{month:02d}-01",
                        year=year,
                        month=month,
                    )
            for vuelo in result:
                print(vuelo)
                price = vuelo.get("price")
                date = vuelo.get("date")
                if price and price < 850:
                    msg = f"🔥 ¡VUELO BARATO!\n"
                    msg += f"Fecha: {date}\n"
                    msg += f"Precio: €{price}\n"
                    msg += f"Desde: EZE\n"
                    msg += f"Hacia: {dest}"
                    print(msg)
                    await bot.send_message(chat_id=chat_id, text=msg)

        except Exception as e:
            msgError = f"⚠️ Error de búsqueda {month:02d}-{year}: {e}"
            print(msgError)
            await bot.send_message(chat_id=chat_id, text=msgError)

        await asyncio.sleep(60)

        
def start_background_loop(loop, bot, chat_id):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(verificar_ofertas(bot, chat_id))


# Función principal para iniciar el bot
def main() -> None:
    """Inicia el bot."""
    if not TOKEN:
        print("❌ BOT_TOKEN not found")
        return
    application = Application.builder().token(TOKEN).build()

    # Añade un manejador para el comando /start.
    application.add_handler(CommandHandler("start", start))

    # Inicia la tarea de fondo en un hilo separado y pasa el bot + chat_id
    chat_id = os.getenv("CHAT_ID")
    bot = application.bot

    loop = asyncio.new_event_loop()
    t = threading.Thread(
        target=start_background_loop, args=(loop, bot, chat_id), daemon=True
    )
    t.start()

    print("Bot iniciado. Presiona Ctrl-C para detenerlo.\n")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
