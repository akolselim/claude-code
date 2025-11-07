import streamlit as st
import google.generativeai as genai
from pathlib import Path
import time
import os
from typing import List, Dict
import json

# Sayfa yapılandırması
st.set_page_config(
    page_title="Avukat Dosya Asistanı",
    page_icon="⚖️",
    layout="wide"
)

# Config'den API key'i al
try:
    from config import GOOGLE_API_KEY
    genai.configure(api_key=GOOGLE_API_KEY)
except ImportError:
    st.error("❌ config.py dosyası bulunamadı! Lütfen config.py dosyasını oluşturun ve API key'inizi ekleyin.")
    st.stop()
except Exception as e:
    st.error(f"❌ API key yapılandırma hatası: {e}")
    st.stop()

# Session state başlat
if 'corpus' not in st.session_state:
    st.session_state.corpus = None
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'temp_folder' not in st.session_state:
    st.session_state.temp_folder = Path("./temp_uploads")
    st.session_state.temp_folder.mkdir(exist_ok=True)

# Başlık
st.title("⚖️ Avukat Dosya Asistanı")
st.markdown("### Google File Search API ile Güçlendirilmiş RAG Sistemi")
st.markdown("---")

# Sidebar - Dosya Yönetimi
with st.sidebar:
    st.header("📁 Dosya Yönetimi")

    # Corpus oluştur butonu
    if st.button("🆕 Yeni Corpus Oluştur"):
        try:
            corpus = genai.create_corpus(display_name="Avukat Dosyaları")
            st.session_state.corpus = corpus
            st.session_state.uploaded_files = []
            st.session_state.chat_history = []
            st.success(f"✅ Yeni corpus oluşturuldu: {corpus.name}")
        except Exception as e:
            st.error(f"❌ Corpus oluşturma hatası: {e}")

    # Corpus durumu
    if st.session_state.corpus:
        st.success(f"📚 Aktif Corpus: {st.session_state.corpus.name}")
        st.info(f"📄 Yüklenen dosya sayısı: {len(st.session_state.uploaded_files)}")
    else:
        st.warning("⚠️ Önce bir corpus oluşturun")

    st.markdown("---")

    # Dosya yükleme
    st.subheader("📤 Dosya Yükle")
    uploaded_files = st.file_uploader(
        "PDF, DOCX, TXT dosyalarını yükleyin",
        type=['pdf', 'docx', 'txt', 'doc'],
        accept_multiple_files=True,
        key="file_uploader"
    )

    if uploaded_files and st.session_state.corpus:
        if st.button("⬆️ Dosyaları İşle ve Yükle"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            for idx, uploaded_file in enumerate(uploaded_files):
                try:
                    # Dosyayı geçici olarak kaydet
                    temp_file_path = st.session_state.temp_folder / uploaded_file.name
                    with open(temp_file_path, 'wb') as f:
                        f.write(uploaded_file.getbuffer())

                    status_text.text(f"İşleniyor: {uploaded_file.name}")

                    # Dosyayı corpus'a yükle
                    document = genai.upload_file(path=str(temp_file_path))

                    # Corpus'a ekle
                    genai.create_document(
                        corpus_name=st.session_state.corpus.name,
                        display_name=uploaded_file.name,
                        document=document
                    )

                    st.session_state.uploaded_files.append(uploaded_file.name)

                    # Geçici dosyayı sil
                    temp_file_path.unlink()

                    progress_bar.progress((idx + 1) / len(uploaded_files))

                except Exception as e:
                    st.error(f"❌ {uploaded_file.name} yüklenirken hata: {e}")

            status_text.text("✅ Tüm dosyalar yüklendi!")
            time.sleep(1)
            status_text.empty()
            progress_bar.empty()
            st.rerun()

    st.markdown("---")

    # Yüklenen dosyalar listesi
    if st.session_state.uploaded_files:
        st.subheader("📋 Yüklü Dosyalar")
        for file_name in st.session_state.uploaded_files:
            st.text(f"• {file_name}")

    st.markdown("---")

    # Sohbet geçmişini temizle
    if st.button("🗑️ Sohbet Geçmişini Temizle"):
        st.session_state.chat_history = []
        st.rerun()

# Ana alan - Sohbet
st.header("💬 Soru Sorun")

# Sohbet geçmişini göster
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📎 Kaynaklar"):
                for source in message["sources"]:
                    st.markdown(f"- **{source['file']}** (Sayfa {source['page']})")
                    if 'text' in source:
                        st.markdown(f"  > _{source['text'][:200]}..._")

# Soru input
if prompt := st.chat_input("Dosyalarınız hakkında soru sorun..."):
    if not st.session_state.corpus:
        st.error("❌ Lütfen önce bir corpus oluşturun!")
    elif not st.session_state.uploaded_files:
        st.error("❌ Lütfen önce dosya yükleyin!")
    else:
        # Kullanıcı mesajını ekle
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI yanıtı al
        with st.chat_message("assistant"):
            with st.spinner("Düşünüyorum..."):
                try:
                    # Model oluştur
                    model = genai.GenerativeModel(
                        model_name="gemini-2.0-flash-exp",
                        tools=[
                            genai.protos.Tool(
                                retrieval=genai.protos.Retrieval(
                                    retrieval_type=genai.protos.Retrieval.RetrievalType.SEMANTIC_SIMILARITY,
                                    corpus_name=st.session_state.corpus.name,
                                )
                            )
                        ]
                    )

                    # Yanıt al
                    response = model.generate_content(
                        f"""Sen bir avukat asistanısın. Yüklenen dosyalara dayanarak soruları yanıtla.

Soru: {prompt}

Lütfen:
1. Yanıtını dokümanlardan aldığın bilgilere dayandır
2. Eğer dokümanlarda ilgili bilgi yoksa "Bu bilgi yüklenen dosyalarda mevcut değil" de
3. Yanıtında hangi dosyadan alıntı yaptığını belirt
4. Türkçe ve profesyonel bir dil kullan"""
                    )

                    answer = response.text

                    # Kaynakları çıkar (eğer varsa)
                    sources = []
                    if hasattr(response, 'grounding_metadata'):
                        for chunk in response.grounding_metadata.grounding_chunks:
                            if hasattr(chunk, 'web') and chunk.web:
                                sources.append({
                                    'file': chunk.web.title or 'Unknown',
                                    'page': 'N/A',
                                    'text': chunk.text[:200] if hasattr(chunk, 'text') else ''
                                })

                    # Yanıtı göster
                    st.markdown(answer)

                    # Kaynakları göster
                    if sources:
                        with st.expander("📎 Kaynaklar"):
                            for source in sources:
                                st.markdown(f"- **{source['file']}** (Sayfa {source['page']})")
                                if 'text' in source and source['text']:
                                    st.markdown(f"  > _{source['text']}..._")

                    # Chat history'ye ekle
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })

                except Exception as e:
                    st.error(f"❌ Yanıt alınırken hata: {e}")
                    st.error("Detay: " + str(type(e).__name__))

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8em;'>
⚖️ Avukat Dosya Asistanı | Google File Search API ile güçlendirilmiştir<br>
⚠️ Bu sistem yardımcı bir araçtır. Hukuki kararlarınızı mutlaka dokümanları kontrol ederek verin.
</div>
""", unsafe_allow_html=True)
