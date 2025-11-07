# ================================================================
# 🌌 GEMINI AI — FINAL SHOWCASE EDITION (By Agung Maulana)
# ================================================================
import os
import streamlit as st
import google.generativeai as genai
import pandas as pd
from datetime import datetime

# ---------------------- KONFIGURASI DASAR -----------------------
st.set_page_config(
    page_title="Gemini AI — Final Showcase Edition",
    page_icon="🌌",
    layout="wide"
)

# ---------------------- TEMA FUTURISTIK --------------------------
st.markdown("""
<style>
/* Latar belakang glowing */
.main {
    background: linear-gradient(135deg, #05010f, #0a1a2f, #000000);
    background-attachment: fixed;
    color: #e5e7eb;
    font-family: 'Poppins', sans-serif;
}

/* Animasi Judul */
@keyframes glow {
    from { text-shadow: 0 0 10px #3b82f6, 0 0 20px #8b5cf6; }
    to { text-shadow: 0 0 20px #3b82f6, 0 0 40px #8b5cf6; }
}
h1 {
    text-align: center;
    color: white;
    animation: glow 1.5s ease-in-out infinite alternate;
}
h2, h3 {
    color: #a5b4fc;
}

/* Bubble chat futuristik */
.stChatMessage {
    border-radius: 20px;
    padding: 16px;
    margin: 12px 0;
    max-width: 85%;
    font-size: 1rem;
}
.stChatMessage.user {
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    color: white;
    margin-left: auto;
    text-align: right;
    box-shadow: 0 0 25px rgba(59,130,246,0.4);
}
.stChatMessage.assistant {
    background: rgba(17,24,39,0.8);
    color: #f9fafb;
    box-shadow: 0 0 25px rgba(139,92,246,0.3);
}

/* Sidebar futuristik */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #1f2937);
    color: #e5e7eb;
    border-right: 2px solid #3b82f6;
}
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 12px;
    font-weight: 600;
    transition: all 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
}

/* Chat input glow */
div[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.05);
    border-radius: 15px;
    box-shadow: 0 0 15px rgba(99,102,241,0.4);
}

/* Metric glowing */
[data-testid="stMetricValue"] {
    color: #60a5fa !important;
    font-weight: 700;
    text-shadow: 0 0 10px #2563eb;
}

/* Scrollbar neon */
::-webkit-scrollbar {
    width: 10px;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #3b82f6, #8b5cf6);
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- HEADER --------------------------
st.title("🌌 **GEMINI AI Edition TERBATAS** 🚀")
st.caption("✨ Chatbot Futuristik dengan Analisis Otomotif dan AI Natural — by Agung Maulana")

# ---------------------- SIDEBAR --------------------------
with st.sidebar:
    st.image("https://i.imgur.com/DT8HtuM.png", width=180)
    st.markdown("## ⚙️ **Control Panel**")
    API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
    if not API_KEY:
        st.error("❌ API Key belum diset.\nJalankan di PowerShell:\n`$env:GEMINI_API_KEY='PASTE_KEY_KAMU'`")
        st.stop()
    else:
        st.success("✅ API Key Aktif")

    # Budget
    user_budget = st.number_input("💰 Budget Mobil (Rp)", min_value=0, step=1_000_000)
    if user_budget > 0:
        st.session_state.user_budget = user_budget
        st.info(f"🎯 Budget diset ke Rp {user_budget:,}")

    # Upload CSV
    uploaded_file = st.file_uploader("📂 Upload Dataset Mobil (CSV)", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state["car_data"] = df
        st.success(f"✅ {len(df)} data mobil berhasil dimuat.")
        with st.expander("👀 Pratinjau Data"):
            st.dataframe(df.head())

    # Reset Chat
    if st.button("🔄 Reset Chat"):
        st.session_state.clear()
        st.experimental_rerun()

    st.markdown("---")
    st.caption("🌟 Developed by **Agung Maulana** · Powered by Google Gemini 2.0 Flash")

# ---------------------- SETUP MODEL --------------------------
genai.configure(api_key=API_KEY)
GMODEL = genai.GenerativeModel("models/gemini-2.0-flash")

# ---------------------- STATE --------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "Halo 🌌 Aku **Gemini**, asisten AI futuristikmu. Aku siap membantu tugas akhir kamu — "
            "baik dalam analisis data, prediksi harga mobil 🚗, atau diskusi sains & AI! ✨\n\n"
            "Coba kirim pertanyaan seperti:\n"
            "- `prediksi harga  CIVIC TURBO manual`\n"
            "- `rekomendasi mobil di bawah 700 juta`\n"
            "- `ceritain konsep AI generatif`\n"
            "- `bantu analisis file CSV yang ku-upload`\n\n"
            "Mari kita mulai! 🚀"
        )
    }]
    st.session_state.start_time = datetime.now()

# ---------------------- CHAT HISTORY --------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------- INPUT --------------------------
user_input = st.chat_input("Ketik pesan kamu di sini... ✨")
if not user_input:
    st.stop()

# Tampilkan pesan user
st.session_state.messages.append({"role": "user", "content": user_input})
with st.chat_message("user"):
    st.markdown(user_input)

# ---------------------- PROMPT LOGIKA --------------------------
context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-8:]])
budget_info = f"User memiliki budget Rp {st.session_state.user_budget:,}" if st.session_state.get("user_budget") else ""
data_hint = f"User telah mengupload dataset mobil dengan {len(st.session_state['car_data'])} baris." if "car_data" in st.session_state else ""

prompt = f"""
Kamu adalah Gemini, asisten AI masa depan dengan gaya bicara profesional, cerdas, dan futuristik.
Fokus utamamu adalah membantu analisis mobil dan memberikan saran berbasis data.

Riwayat percakapan:
{context}

Konteks tambahan:
{budget_info}
{data_hint}

Instruksi:
- Jika topik mobil, analisis menggunakan data (jika ada).
- Jika pertanyaan umum, jawab dengan gaya inspiratif futuristik.
- Jangan bilang 'tidak tahu'; selalu beri analisis logis.
- Gunakan emoji dengan elegan.
"""

# ---------------------- GENERATE --------------------------
with st.spinner("🚀 Gemini sedang berpikir..."):
    response = GMODEL.generate_content(prompt)
    answer = response.text.strip() if response and response.text else "😅 Maaf, aku tidak bisa memproses permintaanmu."

# ---------------------- TAMPILKAN HASIL --------------------------
with st.chat_message("assistant"):
    st.markdown(answer)

st.session_state.messages.append({"role": "assistant", "content": answer})

# ---------------------- FOOTER --------------------------
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("🕒 Durasi Sesi", f"{(datetime.now() - st.session_state.start_time).seconds} detik")
col2.metric("💬 Pesan", len(st.session_state.messages))
col3.metric("⚡ Model", "Gemini 2.0 Flash")
