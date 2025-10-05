import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import io
import base64 

# --- 1. Konfigurasi Halaman ---
st.set_page_config(
    page_title="BiblioBot Vision",
    page_icon="📸",
    layout="centered"
)

# --- 2. System Prompt yang Diperbarui untuk Kemampuan Vision ---
SYSTEM_PROMPT = """
Anda adalah "BiblioBot", seorang asisten AI yang sangat ahli tentang buku, literatur, dan penulis, dengan kemampuan untuk 'melihat' dan menganalisis gambar.

ATURAN KETAT:
1.  Jika pengguna mengunggah gambar, prioritas utama Anda adalah menganalisis gambar tersebut sesuai dengan pertanyaan pengguna. Identifikasi sampul buku, penulis di foto, atau teks di dalam gambar.
2.  JAWAB HANYA pertanyaan yang berhubungan dengan buku, penulis, plot, genre, rekomendasi buku, dan topik sastra lainnya.
3.  JIKA pengguna bertanya tentang topik lain di luar buku (baik dengan atau tanpa gambar), Anda HARUS menolak dengan sopan.
4.  Gunakan salah satu dari respons penolakan berikut:
    - "Maaf, saya adalah BiblioBot dan hanya bisa menjawab pertanyaan seputar buku. Ada yang bisa saya bantu terkait literatur?"
    - "Fokus saya adalah dunia buku. Saya tidak memiliki informasi mengenai topik tersebut. Mungkin Anda ingin bertanya tentang penulis atau novel tertentu?"
"""

# --- 3. Header Aplikasi ---
st.title("BiblioBot Vision 📸")
st.markdown("Saya bisa membantu semua hal tentang buku. Sekarang, Anda juga bisa **mengunggah gambar sampul buku** untuk saya analisis!")

# --- 4. Inisialisasi Model LLM ---
try:
    google_api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("Kunci Google API belum diatur di Streamlit Secrets!", icon="🗝️")
    st.stop()

if "llm" not in st.session_state:
    try:
        st.session_state.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=google_api_key,
            temperature=0.7,
        )
    except Exception as e:
        st.error(f"Terjadi kesalahan saat inisialisasi model: {e}")
        st.stop()

# --- 5. Fitur Unggah Gambar ---
uploaded_file = st.file_uploader(
    "Unggah gambar sampul buku di sini",
    type=["jpg", "jpeg", "png"]
)

if "uploaded_image_bytes" not in st.session_state:
    st.session_state.uploaded_image_bytes = None

col1, col2 = st.columns([1, 2])
with col1:
    if uploaded_file:
        st.session_state.uploaded_image_bytes = uploaded_file.getvalue()
        st.image(st.session_state.uploaded_image_bytes, caption="Gambar akan dianalisis", width=200)
    elif st.session_state.uploaded_image_bytes:
         st.image(st.session_state.uploaded_image_bytes, caption="Gambar akan dianalisis", width=200)

with col2:
    if st.session_state.uploaded_image_bytes:
        if st.button("Hapus Gambar"):
            st.session_state.uploaded_image_bytes = None
            st.rerun()

st.divider()

# --- 6. Manajemen Riwayat Obrolan ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 7. Logika Utama Aplikasi Multimodal ---
if prompt := st.chat_input("Tanyakan sesuatu tentang buku..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("BiblioBot sedang berpikir..."):
        
        # Siapkan konten untuk dikirim ke LLM dalam format yang benar
        message_content = []

        # 1. Tambahkan Teks Prompt dari Pengguna dalam format dictionary
        message_content.append({"type": "text", "text": prompt})

        # 2. Tambahkan Gambar jika ada, dalam format dictionary
        if st.session_state.uploaded_image_bytes:
            image_bytes = st.session_state.uploaded_image_bytes
            base64_image = base64.b64encode(image_bytes).decode("utf-8")
            
            message_content.append({
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{base64_image}"
            })

        # Buat pesan history dengan system prompt di awal
        history_for_llm = [AIMessage(content=SYSTEM_PROMPT)]
        for msg in st.session_state.messages[:-1]:
             if msg["role"] == "user":
                 history_for_llm.append(HumanMessage(content=msg["content"]))
             else:
                 history_for_llm.append(AIMessage(content=msg["content"]))
        
        # Tambahkan pesan terakhir pengguna (yang sudah diformat dengan benar)
        history_for_llm.append(HumanMessage(content=message_content))

        # Panggil LLM dengan konten multimodal
        try:
            response = st.session_state.llm.invoke(history_for_llm)
            answer = response.content
        except Exception as e:
            answer = f"Terjadi kesalahan: {e}"

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)