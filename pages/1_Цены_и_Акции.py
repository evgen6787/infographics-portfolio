import os
import sqlite3
import streamlit as st

st.set_page_config(page_title="Цены и Акции | InfographicsAI", page_icon="💰", layout="wide")

DB_FILE = "orders.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT, product TEXT, utp TEXT, tariff TEXT, status TEXT, date_created TEXT)')
    conn.commit()
    conn.close()

init_db()

def db_query(query, params=(), fetch=False, commit=False):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(query, params)
    res = cursor.fetchall() if fetch else None
    if commit: conn.commit()
    conn.close()
    return res

# --- 🎨 МОЩНЫЙ НЕОНОВЫЙ CSS-ДИЗАЙН СТУДИИ ---
st.markdown("""
    <style>
    /* Глубокий космический фон */
    .stApp { 
        background-color: #0A0A0E !important; 
        color: #FFFFFF !important; 
    }
    
    /* Сочные неоновые разделители вместо серых полос */
    hr {
        border: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #7B2CBF, #00B4D8, transparent);
        margin: 40px 0 !important;
    }
    
    /* Стилизация плашек акций с двойным неоновым свечением */
    .promo-box { 
        background: linear-gradient(135deg, #12121A, #1A1A26); 
        border-left: 5px solid #00B4D8; 
        padding: 20px; 
        border-radius: 12px; 
        margin-bottom: 25px; 
        box-shadow: 0 0 15px rgba(0, 180, 216, 0.2);
    }
    
    /* Футуристичные карточки тарифов */
    .tariff-card {
        background: #14141F;
        border: 1px solid #24243A;
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        transition: all 0.3s ease;
    }
    .tariff-card:hover {
        border-color: #7B2CBF;
        box-shadow: 0 0 20px rgba(123, 44, 191, 0.3);
        transform: translateY(-2px);
    }
    
    /* Кастомизация вкладок (Tabs) */
    button[data-baseweb="tab"] {
        color: #888899 !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #00B4D8 !important;
        border-bottom-color: #00B4D8 !important;
        text-shadow: 0 0 10px rgba(0, 180, 216, 0.5);
    }
    
    /* Дизайн главной кнопки с градиентом */
    div.stLinkButton > a {
        background: linear-gradient(135deg, #7B2CBF, #00B4D8) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 0 20px rgba(123, 44, 191, 0.5) !important;
        transition: all 0.3s ease !important;
        padding: 14px 28px !important;
        text-decoration: none !important;
        display: inline-flex !important;
    }
    div.stLinkButton > a:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 0 30px rgba(0, 180, 216, 0.8) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 👑 СЕКРЕТНАЯ АДМИНКА ЕВГЕНИЯ ПО ПАРОЛЮ ---
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

with st.expander("🛠 Панель Владельца Студии"):
    if not st.session_state.admin_authenticated:
        master_pwd = st.text_input("Внесите мастер-пароль:", type="password", placeholder="••••••••", key="admin_pwd_field")
        if st.button("🔓 Войти в пульт"):
            if master_pwd == "Шеф2026":
                st.session_state.admin_authenticated = True
                st.success("Доступ разрешен!")
                st.rerun()
            else: st.error("Неверный пароль!")
    else:
        if st.button("🚪 Выйти из админки"):
            st.session_state.admin_authenticated = False
            st.rerun()

if st.session_state.admin_authenticated:
    st.title("🔒 Пульт управления заказами студии")
    st.write("Привет, Евгений! Здесь отображаются все ТЗ, отправленные клиентами.")
    st.divider()
    
    orders = db_query("SELECT id, client_name, product, tariff, status, date_created, utp FROM orders ORDER BY id DESC", fetch=True)
    if orders:
        for order in orders:
            o_id, client, prod, tariff, status, date, utp = order
            with st.container(border=True):
                col_info, col_status = st.columns(2)
                with col_info:
                    st.markdown(f"### Заказ №{o_id} от **@{client}**")
                    st.write(f"📅 **Дата:** {date} | 💎 **Тариф:** {tariff}")
                    st.write(f"🛍 **Товар:** {prod} | 📝 **ТЗ:** {utp}")
                    
                    uploaded_file = st.file_uploader(f"Выдать дизайн для @{client}", type=["png"], key=f"up_{o_id}")
                    if uploaded_file and st.button("✅ Опубликовать файл", key=f"pub_{o_id}"):
                        with open(f"{client}.png", "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        st.success("Файл успешно выдан селлеру!")
                with col_status:
                    st.write("🚦 **Статус работы:**")
                    new_status = st.selectbox("Изменить статус:", ["Ожидает проверки", "Нужна предоплата 50%", "В работе", "Готов! Скачивайте"], index=["Ожидает проверки", "Нужна предоплата 50%", "В работе", "Готов! Скачивайте"].index(status), key=f"status_{o_id}")
                    if st.button("Обновить статус", key=f"btn_stat_{o_id}"):
                        db_query("UPDATE orders SET status = ? WHERE id = ?", (new_status, o_id), commit=True)
                        st.success("Статус обновлен!")
                        st.rerun()
    else: st.info("Пока нет активных брифов.")
    st.divider()

# --- 💰 ОБНОВЛЕННЫЙ БЛОК ЦЕН ---
st.title("💰 Прайс-лист и Горящие Акции")
st.write("Выберите подходящий формат генерации для вашего бизнеса на маркетплейсах.")

st.header("🔥 Мега-Акции этой недели")
st.markdown("""
<div class="promo-box">
    <h3 style='color: #00B4D8; margin-top:0; font-size:18px; text-shadow: 0 0 10px rgba(0,180,216,0.3);'>🎁 Акция "Быстрый Старт"</h3>
    <p style='margin:0; opacity: 0.9;'>При заказе полной воронки от 5 слайдов — <b>Маркетинговый анализ 3 главных конкурентов</b> в вашей нише сделаю абсолютно БЕСПЛАТНО!</p>
</div>
""", unsafe_allow_html=True)

st.header("💎 Наши Тарифы")
tab1, tab2, tab3 = st.tabs(["🚀 Тест Ниши (1 слайд)", "👑 Премиум-Воронка", "🎭 Сложный (с Моделями)"])

with tab1:
    st.markdown("""
    <div class="tariff-card">
        <h3 style="color: #00B4D8; margin-top:0;">🚀 Тест Ниши</h3>
        <h2 style="margin: 10px 0; font-size: 32px;">300 ₽ <span style="font-size:16px; color:#888;">/ слайд</span></h2>
        <p style="color:#bbb;"><b>Для кого:</b> Быстрый стартап, тест новых карточек на WB/Ozon или штучные макеты.</p>
        <p style="margin:5px 0; color:#eee;">• Предмет встраивается в сочный неоновый, эко или мраморный фон.</p>
        <p style="margin:5px 0; color:#eee;">• Выделение преимуществ, проработка ровного русского текста.</p>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div class="tariff-card">
        <h3 style="color: #7B2CBF; margin-top:0;">👑 Premium-Воронка</h3>
        <h2 style="margin: 10px 0; font-size: 32px;">от 250 ₽ <span style="font-size:16px; color:#888;">/ слайд</span></h2>
        <p style="color:#bbb;"><b>Для кого:</b> Селлеров, готовых выжимать максимум продаж со всей карточки товара (от 5 слайдов).</p>
        <p style="margin:5px 0; color:#eee;">• Разработка сквозной логики: Главная обложка ➔ Характеристики ➔ CTA.</p>
        <p style="margin:5px 0; color:#eee;">• Глубокая проработка болей целевой аудитории через ИИ.</p>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div class="tariff-card">
        <h3 style="color: #FF007F; margin-top:0;">🎭 Сложный дизайн</h3>
        <h2 style="margin: 10px 0; font-size: 32px;">от 700 ₽ <span style="font-size:16px; color:#888;">/ слайд</span></h2>
        <p style="color:#bbb;"><b>Для кого:</b> Одежда, обувь, бьюти-сфера и премиальные аксессуары.</p>
        <p style="margin:5px 0; color:#eee;">• Высокотехнологичная генерация фотореалистичных ИИ-моделей (людей).</p>
        <p style="margin:5px 0; color:#eee;">• Товар в реальной жизни: одежда на человеке, гаджет в руках.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.header("🤝 Готовы запустить продажи?")
st.write("Нажмите на кнопку ниже, чтобы перейти в наш официальный Telegram-канал и зафиксировать цену:")
st.link_button("🚀 ПЕРЕЙТИ В TELEGRAM-КАНАЛ СТУДИИ 🚀", "https://t.me/InfographicsAI")
st.success("👈 Также вы можете нажать на вкладку **«Сделать Заказ»** в меню слева для начала диалога с ботом!")
