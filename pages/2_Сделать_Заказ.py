import os
import requests
import streamlit as st
import threading
import telebot
from telebot import types

# --- НАСТРОЙКА КЛЮЧЕЙ И ВАШЕГО ID ---
TELEGRAM_BOT_TOKEN = "8965640431:AAHVgQfVrj7HFHI2MYbCATAP4fMKwEIGsME"  
YOUR_TELEGRAM_CHAT_ID = 1586057111  
YOUR_TG_USERNAME = "dvaevgena"
BOT_USERNAME = "my_infographics_ai_bot"  

st.set_page_config(page_title="Чат-бот заказа | InfographicsAI", page_icon="🤖", layout="centered")

# =====================================================================
# 🛠 ТРЮК: ОФИЦИАЛЬНЫЙ ЗАПУСК ТГ-БОТА ПРЯМО ВНУТРИ ХОСТИНГА САЙТА
# =====================================================================
if "bot_instance" not in st.session_state:
    st.session_state.bot_instance = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
    client_database = {}

    def get_main_menu():
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📂 Смотреть примеры работ", callback_data="show_portfolio"),
            types.InlineKeyboardButton("📝 Условия и Сроки", callback_data="show_terms"),
            types.InlineKeyboardButton("🚦 Узнать статус моего заказа", callback_data="show_status"),
            types.InlineKeyboardButton("👑 Связаться с Дизайнером", callback_data="show_contact")
        )
        return markup

    def get_admin_keyboard():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(types.KeyboardButton("📊 Список контактов базы"), types.KeyboardButton("📢 Рассылка акции (-15%)"), types.KeyboardButton("💡 Справка по командам"))
        return markup

    @st.session_state.bot_instance.message_handler(commands=['start'])
    def send_welcome(message):
        chat_id = message.chat.id
        username = message.from_user.username
        if username: client_database[username.lower().strip()] = chat_id
        
        if chat_id == YOUR_TELEGRAM_CHAT_ID or (username and username.lower() == YOUR_TG_USERNAME.lower()):
            st.session_state.bot_instance.send_message(chat_id, "👑 **Добро пожаловать, Шеф!**\n\nАктивирована панель управления студией!", reply_markup=get_admin_keyboard(), parse_mode="Markdown")
            return
            
        st.session_state.bot_instance.send_message(chat_id, "🎉 **Добро пожаловать в официальный бот студии InfographicsAI!**", reply_markup=get_main_menu(), parse_mode="Markdown")

    @st.session_state.bot_instance.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        chat_id = call.message.chat.id
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ Вернуться в меню", callback_data="back_to_menu"))
        if call.data == "show_portfolio":
            st.session_state.bot_instance.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="📂 **Примеры наших лучших ИИ-генераций:**\n\n• Повербанк в стиле Cyber Neon 🔋\n• Наушники в стиле Hi-Tech Neon 🎧\n• Корейский крем в стиле Эко-минимализм 🌿\n\nВы можете рассмотреть эти макеты в 4K на нашем официальном сайте-витрине!", reply_markup=markup, parse_mode="Markdown")
        elif call.data == "back_to_menu":
            st.session_state.bot_instance.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="👇 **Выберите раздел:**", reply_markup=get_main_menu(), parse_mode="Markdown")

    @st.session_state.bot_instance.message_handler(func=lambda message: True)
    def handle_messages(message):
        chat_id = message.chat.id
        text = message.text.strip()
        username = message.from_user.username
        if username: client_database[username.lower().strip()] = chat_id

        if chat_id == YOUR_TELEGRAM_CHAT_ID or (username and username.lower() == YOUR_TG_USERNAME.lower()):
            if text == "📊 Список контактов базы":
                db_text = "📊 **База активных клиентов студии:**\n\n"
                for nick, c_id in client_database.items(): db_text += f"🔹 @{nick}\n"
                st.session_state.bot_instance.send_message(chat_id, db_text, parse_mode="Markdown")
            elif " " in text:
                parts = text.split(" ", 1)
                target_nick = parts[0].replace("@", "").lower().strip()
                if target_nick in client_database:
                    st.session_state.bot_instance.send_message(client_database[target_nick], f"👑 **Сообщение от Дизайнера:**\n\n{parts[1]}")
            return

    # Запускаем прослушивание ТГ-бота в отдельном независимом потоке хостинга
    threading.Thread(target=st.session_state.bot_instance.infinity_polling, daemon=True).start()

# =====================================================================
# 🤖 ОТОБРАЖЕНИЕ ИНТЕРФЕЙСА САЙТА ДЛЯ КЛИЕНТА
# =====================================================================
def send_to_telegram_site(text):
    url = f"https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": YOUR_TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"})
    except: pass

banner_file = None
for file in os.listdir("."):
    if "banner" in file.lower(): banner_file = file; break

with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00B4D8;'>🔥 InfographicsAI</h2>", unsafe_allow_html=True)
    if banner_file: st.image(banner_file, use_container_width=True)

st.title("🤖 Умный чат-бот для оформления заказа")
st.write("Привет! Я помогу вам быстро составить ТЗ, выбрать тариф и передам все данные нашему дизайнеру.")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Здравствуйте! Какой товар вы планируете продавать на маркетплейсе? Напишите название, и мы начнем оформление брифа!"}]
    st.session_state.step = 1
    st.session_state.order_data = {}

for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.write(message["content"])

if user_input := st.chat_input("Напишите ваш ответ здесь..."):
    with st.chat_message("user"): st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
        if st.session_state.step == 1:
            st.session_state.order_data["product"] = user_input
            ai_response = f"Отлично, проект для товара «{user_input}» успешно запущен в систему! Напишите 2-3 главных преимущества предмета, которые мы выделим на слайдах?"
            st.session_state.step = 2
        elif st.session_state.step == 2:
            st.session_state.order_data["utp"] = user_input
            ai_response = f"Зафиксировал преимущества! Подскажите, какой тариф вам подходит больше всего?\n\n• 🚀 **Тест Ниши** (1 слайд — 300 руб.)\n• 👑 **Premium-Воронка** (от 5 слайдов — от 250 руб./шт.)\n• 🎭 **Сложный дизайн** (ИИ-модели людей — от 700 руб./слайд)"
            st.session_state.step = 3
        elif st.session_state.step == 3:
            st.session_state.order_data["tariff"] = user_input
            ai_response = "Превосходный выбор! Оставьте, пожалуйста, ваш Telegram со знаком @ или ваш номер телефона для связи. Это необходимо, чтобы зафиксировать цену по акции!"
            st.session_state.step = 4
        elif st.session_state.step == 4:
            if "@" not in user_input and not any(char.isdigit() for char in user_input):
                ai_response = "⚠️ Укажите ваш юзернейм Telegram со знаком @ (например, @ivan_seller) или напишите номер телефона!"
            else:
                st.session_state.order_data["contact"] = user_input
                ai_response = "🎉 **Ваш бриф успешно сформирован и передан дизайнеру!** Финальный шаг для загрузки фотографий ждет вас на кнопке ниже!"
                st.session_state.step = 5
                st.session_state.order_finished = True
                
                full_order_log = f"🔔 **НОВЫЙ БРИФ С САЙТА!**\n\n👤 **Контакты:** {st.session_state.order_data.get('contact')}\n🛍 **Товар:** {st.session_state.order_data.get('product')}\n💎 **Тариф:** {st.session_state.order_data.get('tariff')}\n📝 **ТЗ:** {st.session_state.order_data.get('utp')}"
                send_to_telegram_site(full_order_log)
                st.balloons()
        else:
            ai_response = "Ваша заявка уже у мастера! Пожалуйста, переходите в нашего Telegram-бота по кнопке ниже."
        st.write(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

if st.session_state.get("order_finished", False):
    st.divider()
    st.success("🎯 **Финишируем оформление брифа!**")
    st.link_button("🚀 ЗАПУСТИТЬ ТЕЛЕГРАМ-БОТА СТУДИИ 🚀", f"https://t.me")
