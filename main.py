
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

    try:
        produto_id = int(data['data']['product']['id'])
        buyer_name = data['data']['buyer']['name']
        telegram_username = data['data']['custom_fields'][0]['value']  # Ex: @usuario
    except Exception as e:
        print("Erro ao ler payload:", e)
        return jsonify({"status": "invalid payload"}), 400

    print(f"Compra de {buyer_name} (@{telegram_username}) - Produto ID: {produto_id}")

    bot = telegram_app.bot
    try:
        if produto_id == 5694273:  # Mensal
            link = bot.create_chat_invite_link(chat_id=GROUP_ID_MENSAL, member_limit=1)
            msg = f"Olá {buyer_name}, aqui está seu link de acesso ao grupo Super Vip 2025 (válido para 1 uso):\n{link.invite_link}"

        elif produto_id == 5694356:  # Vitalício
            link = bot.create_chat_invite_link(chat_id=GROUP_ID_MENSAL, member_limit=1)
            msg = f"Olá {buyer_name}, aqui está seu link vitalício ao grupo Super Vip 2025:\n{link.invite_link}"

        elif produto_id == 5694376:  # Vitalício + Camgirl
            link1 = bot.create_chat_invite_link(chat_id=GROUP_ID_MENSAL, member_limit=1)
            link2 = bot.create_chat_invite_link(chat_id=GROUP_ID_CAMGIRL, member_limit=1)
            msg = f"Olá {buyer_name}, aqui estão seus links de acesso:\n\nSuper Vip 2025:\n{link1.invite_link}\n\nCamgirl Lives:\n{link2.invite_link}"

        else:
            msg = "Produto não reconhecido."

        bot.send_message(chat_id=telegram_username, text=msg)
        return jsonify({"status": "link enviado"}), 200

    except Exception as e:
        print("Erro ao enviar mensagem:", e)
        return jsonify({"status": "erro no envio"}), 500

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bem-vindo ao Super Vip 2025! Escolha um plano:")

telegram_app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    import asyncio
    asyncio.run(telegram_app.initialize())
    telegram_app.bot.set_webhook(url=f"https://your-deploy-url.onrender.com/{WEBHOOK_SECRET}")
