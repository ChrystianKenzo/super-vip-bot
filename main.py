
from flask import Flask, request, jsonify
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("TOKEN")

GROUP_ID_MENSAL = int(os.getenv("GROUP_ID_MENSAL", "-1002888110541"))
GROUP_ID_CAMGIRL = int(os.getenv("GROUP_ID_CAMGIRL", "-1002555928953"))
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "Vj0MP8L74Ow7m1Kfb3mQznYZ1mApAnecf0ddab-12ed-4d80-b2c0-85834d9668a8")

app = Flask(__name__)

telegram_app = Application.builder().token(TOKEN).build()

@app.route(f"/{WEBHOOK_SECRET}", methods=["POST"])
async def webhook() -> str:
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    await telegram_app.process_update(update)
    return "ok"

@app.route("/hotmart", methods=["POST"])
def hotmart_webhook():
    data = request.json
    print("Hotmart payload:", data)
    # Aqui você vai verificar qual produto foi comprado e criar link de convite
    return jsonify({"status": "received"})

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bem-vindo ao Super Vip 2025! Escolha um plano:")

telegram_app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    import asyncio
    asyncio.run(telegram_app.initialize())
    telegram_app.bot.set_webhook(url=f"https://your-deploy-url.onrender.com/{WEBHOOK_SECRET}")
