from flask import Flask, request, jsonify
from telegram import Bot
from telegram.constants import ChatMemberStatus
from telegram.error import TelegramError
import os
import datetime

app = Flask(__name__)

TOKEN = os.getenv("TOKEN")
GROUP_ID_MENSAL = os.getenv("GROUP_ID_MENSAL")
GROUP_ID_CAMGIRL = os.getenv("GROUP_ID_CAMGIRL")
bot = Bot(token=TOKEN)

def create_invite_link(group_id, expire_date=None):
    return bot.create_chat_invite_link(chat_id=group_id, member_limit=1, expire_date=expire_date)

@app.route("/")
def home():
    return "Bot está rodando!"

@app.route("/hotmart", methods=["POST"])
def handle_hotmart():
    try:
        payload = request.json
        print("Hotmart payload:", payload)

        data = payload.get("data", {})
        buyer = data.get("buyer", {})
        custom_fields = data.get("custom_fields", [])

        # Extrair nome de usuário do Telegram dos campos personalizados
        telegram_username = None
        for field in custom_fields:
            if field.get("key") == "usuario":
                telegram_username = field.get("value")
                break

        if not telegram_username:
            return "Campo personalizado 'usuario' não encontrado.", 400

        # Verificar produto comprado
        product_id = str(data.get("product", {}).get("id"))
        access_links = []

        # Super Vip Mensal
        if product_id == "5694273":
            expire = datetime.datetime.now() + datetime.timedelta(days=30)
            invite = create_invite_link(GROUP_ID_MENSAL, expire_date=expire)
            access_links.append(invite.invite_link)

        # Super Vip Vitalício
        elif product_id == "5694356":
            invite = create_invite_link(GROUP_ID_MENSAL)
            access_links.append(invite.invite_link)

        # Vitalício + Camgirl
        elif product_id == "5694376":
            vip_link = create_invite_link(GROUP_ID_MENSAL)
            camgirl_link = create_invite_link(GROUP_ID_CAMGIRL)
            access_links.append(vip_link.invite_link)
            access_links.append(camgirl_link.invite_link)

        else:
            return "Produto não reconhecido", 400

        # Enviar link para o usuário no Telegram
        text = "✅ Compra confirmada!
Acesse seu grupo:
" + "
".join(access_links)
        bot.send_message(chat_id=f"@{telegram_username}", text=text)

        return "OK", 200

    except Exception as e:
        print("Erro ao processar Hotmart:", e)
        return "Erro interno", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
