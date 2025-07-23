from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
import asyncio
from level_api import get_month_prices
from telegram import Bot
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import time
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ARCHIVO_VUELOS = "vuelos.json"


# Función que se ejecuta cuando el usuario envía el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    user = update.effective_user
    if user:
        await update.message.reply_html(
            f"¡Hola {user.mention_html()}! Soy tu bot de alertas de vuelos. "
            f"Estoy listo para empezar a buscar vuelos baratos desde Ezeiza hacia Dublin, Madrid, Barcelona o Roma.",
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

#Funcion para guardar los vuelos en un archivo json
def guardar_vuelos_json(vuelo):
    if not os.path.exists(ARCHIVO_VUELOS):
        with open(ARCHIVO_VUELOS, "w") as f:
            json.dump([], f) #Si el archivo no existe, se crea con una lista vacía

    with open(ARCHIVO_VUELOS, "r") as f:
        vuelos_guardados = json.load(f) #Cargamos los vuelos guardados
    vuelos_guardados.append(vuelo) #Agregamos el vuelo a la lista de vuelos guardados
    with open(ARCHIVO_VUELOS, "w") as f:
        json.dump(vuelos_guardados, f) #Guardamos los vuelos en el archivo
    return True

#Funcion para verificar si el vuelo ya esta guardado por fecha y destino
def vuelos_existentes(vuelo):
    if not os.path.exists(ARCHIVO_VUELOS):
        return False
    with open(ARCHIVO_VUELOS, "r") as f:
        vuelos_guardados = json.load(f)
        for vuelo_guardado in vuelos_guardados:
            if vuelo_guardado["date"] == vuelo["date"] and vuelo_guardado["dest"] == vuelo["dest"] and vuelo_guardado["price"] == vuelo["price"]:
                return True
    return False

# Tarea de fondo para verificar ofertas cada 60 segundos
async def verificar_ofertas(context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    chat_id = os.getenv("CHAT_ID")
    if not chat_id:
        raise ValueError("❌ CHAT_ID is not defined in the .env file")
    chat_id = int(chat_id)
    destinations = ["DUB", "MAD", "BCN", "FCO"]

    print("⏱️ Empezando ejecución completa")
    start_total = time.time()

    for year, month in get_next_three_months():
        for dest in destinations:
            try:
                print(f"🌍 Consultando: {dest} {year}-{month}")
                start = time.time()
                result = get_month_prices(
                    origin="EZE",
                    dest=dest,
                    outbound=f"{year}-{month:02d}-01",
                    year=year,
                    month=month,
                )
                print(f"⏳ Duración get_month_prices: {time.time() - start:.2f}s")

                for vuelo in result:
                    vuelo["dest"] = dest
                    print(vuelo)
                    price = vuelo.get("price")
                    date = vuelo.get("date")
                    if price and price < 800:
                        if not vuelos_existentes(vuelo):
                            guardar_vuelos_json(vuelo)
                            msg = (
                                f"✈️ ALERTA DE PRECIO BAJO ✈️\n\n"
                                f"🗓️ Fecha: {date}\n"
                                f"💶 Precio: €{price}\n"
                                f"📍 Ruta: EZE ➡️ {dest}"
                            )
                            print(msg)
                            await bot.send_message(chat_id=chat_id, text=msg)
                        else:
                            print(f"🟡 Vuelo ya guardado: {vuelo}")
            except Exception as e:
                msgError = f"⚠️ Error en {dest} {month:02d}-{year}: {e}"
                print(msgError)
                await bot.send_message(chat_id=chat_id, text=msgError)

    print(f"✅ Ejecución completa en {time.time() - start_total:.2f}s")
    

async def post_init(application):
    application.job_queue.run_repeating(verificar_ofertas, interval=300)


# Función principal para iniciar el bot
def main() -> None:
    """Inicia el bot."""
    if not TOKEN:
        print("❌ BOT_TOKEN not found")
        return


    application = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init) 
        .build()
    )

    
    # Añade un manejador para el comando /start.
    application.add_handler(CommandHandler("start", start))


    print("Bot iniciado. Presiona Ctrl-C para detenerlo.\n")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
