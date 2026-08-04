import os
import requests
import streamlit as st

# --- НАСТРОЙКА КЛЮЧЕЙ ТЕЛЕГРАМА ---
TELEGRAM_BOT_TOKEN = "8965640431:AAHVgQfVrj7HFHI2MYbCATAP4fMKwEIGsME"  
YOUR_TELEGRAM_CHAT_ID = "1586057111"  

st.set_page_config(page_title="Чат-бот заказа | InfographicsAI", page_icon="🤖", layout="centered")

def send_to_telegram(text):
    url = f"https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": YOUR_TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    try: 
        requests.post(url, json=payload)
    except: 
        pass

banner_file = None
for file in os.listdir("."):
    if "banner" in file.lower(): 
        banner_file = file
        break

with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00B4D8;'>🔥 InfographicsAI</h2>", unsafe_allow_html=True)
    if banner_file: 
        st.image(banner_file, use_container_width=True)
    st.divider()
    st.markdown("📌 **Навигация по сайту:**")

st.title("🤖 Умный чат-бот для оформления заказа")
st.write("Привет! Я помогу вам быстро составить ТЗ, выбрать тариф и передам все данные нашему дизайнеру.")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Здравствуйте! Я — ваш бот-помощник студии InfographicsAI. Какой товар вы планируете продавать на маркетплейсе? Напишите название, и мы начнем оформление брифа!"}
    ]
    st.session_state.step = 1
    st.session_state.order_data = {}

for message in st.session_state.messages:
    with st.chat_message(message["role"]): 
        st.write(message["content"])

if user_input := st.chat_input("Напишите ваш ответ здесь..."):
    with st.chat_message("user"): 
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    low_input = user_input.lower().strip()
    is_flood = any(word in low_input for word in ["привет", "как дела", "ты кто", "зачем", "почему", "дурак", "тупой", "что ты умеешь", "хей", "hello"])
    
    if is_flood and st.session_state.step < 4:
        with st.chat_message("assistant"):
            ai_response = "🤖 Я — автоматический бот-менеджер. С радостью поболтал бы с вами, но моя главная задача — помочь вам создать взрывную инфографику маркетплейсов! На каком товаре мы остановились? Напишите его название или детали."
            st.write(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
    else:
        with st.chat_message("assistant"):
            with st.spinner("Бот пишет ответ..."):
                if st.session_state.step == 1:
                    st.session_state.order_data["product"] = user_input
                    ai_response = f"Отлично, проект для товара «{user_input}» успешно запущен в систему! Напишите 2-3 главных преимущества или характеристики предмета (например: материал, мощность, подарки в комплекте), которые мы обязательно должны крупно и сочно выделить на слайдах?"
                    st.session_state.step = 2
                elif st.session_state.step == 2:
                    st.session_state.order_data["utp"] = user_input
                    ai_response = f"Зафиксировал эти преимущества для товара {st.session_state.order_data.get('product')}, сделаем на них максимальный маркетинговый акцент! Подскажите, какой тариф вам подходит больше всего?\n\n• 🚀 **Тест Ниши** (1 слайд — 300 руб.)\n• 👑 **Premium-Воронка** (от 5 слайдов — от 250 руб./шт.)\n• 🎭 **Сложный дизайн** (ИИ-модели людей — от 700 руб./слайд)"
                    st.session_state.step = 3
                elif st.session_state.step == 3:
                    st.session_state.order_data["tariff"] = user_input
                    ai_response = "Превосходный выбор! И последний шаг для завершения бронирования брифа: оставьте, пожалуйста, ваш Telegram (юзернейм обязательно со знаком @) или ваш номер телефона для связи. Это необходимо, чтобы зафиксировать за вами цену по акции!"
                    st.session_state.step = 4
                elif st.session_state.step == 4:
                    has_digits = any(char.isdigit() for char in user_input)
                    if "@" not in user_input and not has_digits:
                        ai_response = "⚠️ Ой, кажется, вы ввели некорректный контакт. Пожалуйста, укажите ваш юзернейм Telegram со знаком @ (например, @ivan_seller) или напишите номер телефона. Иначе наш дизайнер не сможет связаться с вами!"
                    else:
                        st.session_state.order_data["contact"] = user_input
                        ai_response = "🎉 **Ваш бриф успешно сформирован и отправлен дизайнеру!**\n\nЯ сохранил данные вашей заявки. Финальный шаг для завершения оформления и загрузки фотографий ждет вас на кнопке ниже! ТЗ уже летит на телефон мастеру."
                        st.session_state.step = 5
                        st.session_state.order_finished = True
                        
                        full_order_log = f"🔔 **НОВЫЙ БРИФ С САЙТА!**\n\n👤 **Контакты селлера:** {st.session_state.order_data.get('contact')}\n🛍 **Товар:** {st.session_state.order_data.get('product')}\n💎 **Выбранный тариф:** {st.session_state.order_data.get('tariff')}\n📝 **Преимущества (ТЗ):** {st.session_state.order_data.get('utp')}"
                        send_to_telegram(full_order_log)
                        st.balloons()
                else:
                    ai_response = "Ваша заявка уже у мастера! Пожалуйста, переходите в нашего Telegram-бота по кнопке ниже для отслеживания готовности."
                st.write(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

if st.session_state.get("order_finished", False):
    st.divider()
    st.success("🎯 **Финишируем оформление брифа!**")
    st.write("Чтобы **загрузить фотографии вашего товара**, отслеживать статус готовности карточек в 4K и общаться с дизайнером, запустите нашего официального Telegram-робота прямо сейчас:")
    st.link_button("🚀 ЗАПУСТИТЬ ТЕЛЕГРАМ-БОТА СТУДИИ 🚀", "https://t.me/my_infographics_ai_bot")
