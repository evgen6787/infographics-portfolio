import os
import sqlite3
import streamlit as st

st.set_page_config(page_title="Цены и Акции | InfographicsAI", page_icon="💰", layout="wide")

DB_FILE = "orders.db"

# Инициализация базы данных, если её нет
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

# Кастомные стили для тёмной темы
st.markdown("""
    <style>
    .stApp { background-color: #0D0D11 !important; color: #FFFFFF !important; }
    .promo-box { background-color: #1A1A24; border-left: 5px solid #00B4D8; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 👑 СЕКРЕТНАЯ АДМИНКА ЕВГЕНИЯ ПО ПАРОЛЮ ---
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

# Маленькая скрытая кнопка-спойлер в самом верху страницы
with st.expander("🛠 Панель Владельца Студии"):
    if not st.session_state.admin_authenticated:
        master_pwd = st.text_input("Внесите мастер-пароль:", type="password", placeholder="••••••••", key="admin_pwd_field")
        if st.button("🔓 Войти в пульт"):
            if master_pwd == "Шеф2026":
                st.session_state.admin_authenticated = True
                st.success("Доступ разрешен!")
                st.rerun()
            else:
                st.error("Неверный пароль!")
    else:
        if st.button("🚪 Выйти из админки"):
            st.session_state.admin_authenticated = False
            st.rerun()

# Если пароль введен верно — разворачиваем пульт управления заказами
if st.session_state.admin_authenticated:
    st.title("🔒 Пульт управления заказами студии")
    st.write("Привет, Евгений! Здесь отображаются все ТЗ, отправленные клиентами с чат-бота сайта.")
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
    else:
        st.info("Пока нет активных брифов с сайта.")
    st.divider()

# --- 💰 СТАНДАРТНЫЙ БЛОК ЦЕН (ВИДЯТ ВСЕ КЛИЕНТЫ) ---
st.title("💰 Прайс-лист и Горящие Акции")
st.write("Выберите подходящий формат генерации для вашего бизнеса на маркетплейсах.")

st.header("🔥 Мега-Акции этой недели")
st.markdown("""
<div class="promo-box">
    <h3 style='color: #00B4D8; margin-top:0; font-size:18px;'>🎁 Акция "Быстрый Старт"</h3>
    <p style='margin:0;'>При заказе полной воронки от 5 слайдов — <b>Маркетинговый анализ 3 главных конкурентов</b> в вашей нише сделаю абсолютно БЕСПЛАТНО!</p>
</div>
""", unsafe_allow_html=True)

st.header("💎 Наши Тарифы")
tab1, tab2, tab3 = st.tabs(["🚀 Тест Ниши (1 слайд)", "👑 Премиум-Воронка", "🎭 Сложный (с Моделями)"])

with tab1:
    st.markdown("### **300 руб. / слайд**")
    st.write("• Полная генерация ИИ под ключ: предмет встраивается в сочный неоновый, эко или мраморный фон.")
with tab2:
    st.markdown("### **от 250 руб. / слайд**")
    st.write("• Разработка сквозной логики и воронки: Главная обложка -> Характеристики -> CTA.")
with tab3:
    st.markdown("### **от 700 руб. / слайд**")
    st.write("• Высокотехнологичная генерация фотореалистичных ИИ-моделей (людей) в движении.")

st.divider()
st.header("🤝 Готовы запустить продажи?")
st.link_button("🚀 ПЕРЕЙТИ В TELEGRAM-КАНАЛ СТУДИИ 🚀", "https://t.me/InfographicsAI")
