import os
import datetime
import time
import streamlit as st
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# 1. KONFIGURASI HALAMAN
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Ramalan AI Hiburan 🔮",
    page_icon="🔮",
    layout="centered"
)

# -----------------------------------------------------------------------------
# 2. INISIALISASI GEMINI API
# -----------------------------------------------------------------------------
# Ambil API key dari Environment Variable atau Streamlit Secrets
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    # Jika di lokal, kamu bisa masukkan key langsung di kolom input ini
    api_key = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")
    if not api_key:
        st.info("💡 Silakan masukkan Gemini API Key di sidebar untuk memulai.")
        st.stop()

# Inisialisasi client Gemini
client = genai.Client(api_key=api_key)

# -----------------------------------------------------------------------------
# 3. TAMPILAN UTAMA (UI)
# -----------------------------------------------------------------------------
st.title("🔮 Ramalan Nasib AI")
st.write("Penasaran dengan apa yang dikatakan semesta hari ini? Tanyakan pada AI Mistik!")

st.divider()

# Form Input Pengguna
with st.form("ramalan_form"):
    nama = st.text_input("Nama Lengkap / Panggilan:", placeholder="Contoh: Budi")
    tanggal_lahir = st.date_input(
        "Tanggal Lahir:",
        min_value=datetime.date(1950, 1, 1),
        max_value=datetime.date.today(),
        value=datetime.date(2000, 1, 1) # Tanggal default saat web dibuka
)

    fokus = st.selectbox(
        "Apa yang ingin kamu ketahui?",
        ["Asmara & Hubungan 💕", "Karir & Keuangan 💰", "Keberuntungan Umum 🌟", "Saran Mistik Hari Ini 🧘‍♂️"]
    )
    
    submitted = st.form_submit_button("🔮 Bacakan Nasibku!")

# -----------------------------------------------------------------------------
# 4. LOGIKA GENERASI RAMALAN
# -----------------------------------------------------------------------------
if submitted:
    with st.spinner("🔮 Sedang membaca garis tangan dan bintang-bintang..."):
        prompt = f"Nama: {nama}\nTanggal Lahir: {tanggal_lahir.strftime('%d %B %Y')}\nFokus Ramalan: {fokus}"
        
        # --- TAMBAHKAN BARIS INI KALO BELUM ADA ---
        system_instruction = "Kamu adalah seorang peramal garis tangan profesional yang memberikan ramalan secara bijak, menarik, dan menghibur."

        models_to_try = ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-3.0-flash"]

        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.8,
                    ),
                
                st.success("✨ Kristal Takdir Telah Terbuka!")
                st.markdown(response.text)
                st.divider()
                break
                
            except Exception as e:
                if ("503" in str(e) or "429" in str(e)) and model_name != models_to_try[-1]:
                    continue
                else:
                    st.error(f"Terjadi kesalahan saat membaca bola kristal: {e}")
                    break
                    
                )
                
                # Jika sukses, tampilkan hasil dan hentikan perulangan
                st.success("✨ Kristal Takdir Telah Terbuka!")
                st.markdown(response.text)
                st.divider()
                berhasil = True
                break
                
            except Exception as e:
                # Jika server sibuk (503/429), otomatis lanjut coba model berikutnya
                if ("503" in str(e) or "429" in str(e)) and model_name != models_to_try[-1]:
                    continue
                else:
                    st.error(f"Terjadi kesalahan saat membaca bola kristal: {e}")
                    break
                    
    
    
    
    
    
    if not nama:
        st.warning("Silakan isi nama kamu terlebih dahulu!")
    else:
        # Tampilkan animasi loading
        with st.spinner("Sedang memutar bola kristal & membaca aura bintang... 🌌"):
            time.sleep(2) # Efek dramatis
            
            # Merancang System Instruction & Prompt khusus peramal
            system_instruction = (
                "Kamu adalah seorang peramal AI yang bijak, ramah, dan sedikit humoris. "
                "Tugasmu adalah memberikan ramalan yang MENGHIBUR, POSITIF, dan MEMBANGKITKAN SEMANGAT. "
                "Gunakan gaya bahasa santai dengan sedikit istilah mistik yang lucu (seperti 'aura bintang', 'kristal takdir'). "
                "Jangan memberikan prediksi negatif yang menakutkan atau klaim fakta medis/keuangan riil."
            )
            
            prompt = f"""
            Buatkan ramalan hiburan unik untuk:
            - Nama: {nama}
            - Tanggal Lahir: {tanggal_lahir.strftime('%d %B %Y')}
            - Fokus Ramalan: {fokus}

            Format jawaban:
            1. **Kondisi Aura Hari Ini** (penilaian lucu tentang energi mereka).
            2. **Prediksi Utama** (cerita ramalan yang positif dan mengagumkan).
            3. **Angka & Warna Keberuntungan**.
            4. **Pesan Mistik** (satu kalimat motivasi/saran kocak).
            """

            try:
                # Panggil model Gemini 2.5 Flash
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.8,
                    ),
                )

                # Tampilkan Hasil Ramalan
                st.success("✨ Kristal Takdir Telah Terbuka!")
                st.markdown(response.text)
                
                st.divider()
                
                # -------------------------------------------------------------
                # 5. MONETISASI (DONASI & MONETIZATION)
                # -------------------------------------------------------------
                st.subheader("☕ Suka dengan ramalannya?")
                st.write("Bantu AI Peramal tetap 'menyala' dengan mentraktir kopi!")
                
                # Ganti link ini dengan link Saweria, KaryaKarsa, atau BuyMeACoffee milikmu
                link_saweria = "https://saweria.co/username_kamu" 
                
                st.link_button("🎁 Traktir Kopi lewat Saweria / QRIS", link_saweria)

            except Exception as e:
                st.error(f"Terjadi kesalahan saat membaca bola kristal: {e}")

# -----------------------------------------------------------------------------
# 6. FOOTER & DISCLAIMER (SANGAT PENTING)
# -----------------------------------------------------------------------------
st.divider()
st.caption(
    "⚠️ **Disclaimer:** Web ini dibuat murni **hanya untuk tujuan hiburan**. "
    "Hasil ramalan digenerasi oleh AI secara acak dan kreatif, serta tidak boleh digunakan sebagai "
    "landasan pengambilan keputusan medis, hukum, atau keuangan nyata."
)
