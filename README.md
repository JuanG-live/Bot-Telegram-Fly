# ✈️ Cheap Flight Alerts Bot

Un bot de Telegram que detecta automáticamente vuelos baratos desde **Buenos Aires (EZE)** hacia ciudades europeas como **Barcelona (BCN)**, **Madrid (MAD)**, **Roma (FCO)** y **Dublín (DUB)**.  
Ideal para los que buscan 🛫 **volar por menos de €250** sin perderse las mejores ofertas.

---

## 🚀 ¿Qué hace este bot?

✅ Consulta una API no oficial de la aerolínea LEVEL.  
✅ Escanea vuelos de los próximos **90 días**.  
✅ Filtra vuelos con precios **por debajo de un umbral configurable** (ej: €250).  
✅ Envía automáticamente alertas por Telegram a un grupo o chat privado.  
✅ Corre en segundo plano y se ejecuta de forma continua.

---

## 📦 Requisitos

- Python 3.10+
- Cuenta de Telegram
- [BotFather](https://t.me/botfather) para generar un `BOT_TOKEN`
- (Opcional) Cuenta de [Cursor.sh](https://cursor.sh/) para desarrollo asistido por IA

---

## ⚙️ Instalación

```bash
git clone https://github.com/tuusuario/cheap-flight-alerts-bot.git
cd cheap-flight-alerts-bot
python -m venv venv
source venv/bin/activate  # o .\venv\Scripts\activate en Windows
pip install -r requirements.txt
