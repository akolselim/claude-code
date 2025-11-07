# ⚖️ Avukat Dosya Asistanı - Kullanım Kılavuzu

## 🎯 Sistem Nedir?

Bu sistem, hukuki dosyalarınızı yükleyip üzerinde soru-cevap yapabileceğiniz bir RAG (Retrieval-Augmented Generation) asistanıdır. Google Gemini API kullanır ve dosyalarınızdan kaynak göstererek yanıt verir.

---

## 📋 İLK KURULUM (Tek Seferlik)

### 1️⃣ Python Kurulumu

**Python yüklü mü kontrol edin:**
```bash
python --version
```

Eğer yüklü değilse:
- Windows: https://www.python.org/downloads/ adresinden indirin
- "Add Python to PATH" kutucuğunu işaretlemeyi unutmayın!

### 2️⃣ API Key Yapılandırması

⚠️ **ÖNEMLİ GÜVENLİK ADIMI:**

1. https://aistudio.google.com/apikey adresine gidin
2. **ESKİ API KEY'İNİZİ SİLİN** (önceki yanlışlıkla paylaşılan)
3. "Create API Key" butonuna tıklayın
4. Yeni key'i kopyalayın
5. `config.py` dosyasını açın
6. Bu satırı bulun:
   ```python
   GOOGLE_API_KEY = "BURAYA_YENİ_API_KEY_YAPIŞTIRIN"
   ```
7. Tırnak içine yeni key'inizi yapıştırın:
   ```python
   GOOGLE_API_KEY = "AIzaSyAbc123YeniKeyiniz..."
   ```
8. Dosyayı kaydedin (Ctrl+S)

### 3️⃣ Gerekli Kütüphaneleri Yükleyin

Terminal/Komut İstemi'ni açın ve proje klasörüne gidin:

```bash
cd C:\yol\to\claude-code
```

Kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
```

⏳ Bu işlem 2-3 dakika sürebilir. İnternet bağlantınızın açık olduğundan emin olun.

---

## 🚀 SİSTEMİ ÇALIŞTIRMA (Her Kullanımda)

### 1️⃣ Terminali Açın

- **Windows:**
  - `Win + R` tuşlarına basın
  - `cmd` yazıp Enter

- **Mac/Linux:**
  - Terminal uygulamasını açın

### 2️⃣ Proje Klasörüne Gidin

```bash
cd C:\yol\to\claude-code
```

### 3️⃣ Uygulamayı Başlatın

```bash
streamlit run app.py
```

✅ Eğer başarılı olursa:
- Terminal şöyle bir mesaj gösterir:
  ```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  ```
- Tarayıcınızda otomatik açılır
- Eğer açılmazsa, tarayıcınızda `http://localhost:8501` adresine gidin

---

## 💻 SİSTEMİ KULLANMA

### 📁 1. Corpus Oluşturma (İlk Kez)

1. Sol menüde "🆕 Yeni Corpus Oluştur" butonuna tıklayın
2. "✅ Yeni corpus oluşturuldu" mesajını görmelisiniz

**Corpus Nedir?**
Dosyalarınızın saklandığı Google'daki bir koleksiyon. Her oturum için bir tane oluşturmalısınız.

### 📤 2. Dosya Yükleme

1. Sol menüde "📤 Dosya Yükle" bölümüne gidin
2. "Browse files" butonuna tıklayın veya dosyaları sürükleyip bırakın
3. PDF, DOCX, TXT dosyalarını seçin (birden fazla seçebilirsiniz)
4. "⬆️ Dosyaları İşle ve Yükle" butonuna tıklayın
5. İşlem tamamlanana kadar bekleyin (progress bar gösterir)

**Desteklenen Formatlar:**
- ✅ PDF (.pdf)
- ✅ Word (.docx, .doc)
- ✅ Metin (.txt)

### 💬 3. Soru Sorma

1. Ana ekranda en alttaki metin kutusuna sorunuzu yazın
2. Enter'a basın veya gönder butonuna tıklayın
3. AI yanıt verene kadar bekleyin (genellikle 5-15 saniye)
4. Yanıt altında "📎 Kaynaklar" bölümünü açarak hangi dosyalardan alıntı yapıldığını görebilirsiniz

**Örnek Sorular:**
- "Tapu devri için hangi belgeler gerekiyor?"
- "Bu sözleşmedeki fesih şartları nelerdir?"
- "Davaya hangi tarihte başvurulmuş?"
- "Müvekkilin savunması nedir?"

### 🗑️ 4. Sohbet Geçmişini Temizleme

Sol menüde "🗑️ Sohbet Geçmişini Temizle" butonuna tıklayın. Sohbet sıfırlanır ama dosyalar corpus'ta kalır.

---

## ⚙️ AYARLAR VE İPUÇLARI

### 🔍 Daha İyi Sonuçlar İçin

**İyi Soru Örnekleri:**
- ✅ "Sözleşmede kira bedeli ne kadardır?"
- ✅ "Davalının itirazları nelerdir?"
- ✅ "Taraflar arasındaki uyuşmazlık konusu nedir?"

**Kötü Soru Örnekleri:**
- ❌ "Ne var burada?" (çok genel)
- ❌ "Söyle bakalım" (belirsiz)

### 💰 Maliyet

**Şu an için çok düşük:**
- İlk yükleme: ~$0.15 / 1 milyon token (1000 sayfa = ~1M token)
- Sorgular: Neredeyse ücretsiz
- **Tahmini:** 1000 dosya + 10,000 soru/ay ≈ $5-15

**Maliyetinizi takip edin:**
https://aistudio.google.com/app/apikey → API key'inize tıklayın → Usage görebilirsiniz

### 🔒 Gizlilik

**Dikkat:**
- Yüklenen dosyalar Google sunucularında saklanır
- Hassas bilgiler için anonim hale getirin (isim, TC No, vb.)
- Corpus'ları düzenli temizleyin (ihtiyacınız kalmayınca)

**Corpus Silme:**
Şu an otomatik silme yok. İsterseniz Google AI Studio'dan manuel silebilirsiniz:
https://aistudio.google.com/app/corpora

---

## 🛠️ SORUN GİDERME

### ❌ "config.py dosyası bulunamadı"

**Çözüm:**
- `config.py` dosyasının `app.py` ile aynı klasörde olduğundan emin olun
- Dosya adını kontrol edin (tam olarak `config.py` olmalı)

### ❌ "API key yapılandırma hatası"

**Çözüm:**
1. `config.py`'ı açın
2. API key'in doğru yapıştırıldığından emin olun
3. Tırnak işaretleri düzgün mü kontrol edin
4. Örnek:
   ```python
   GOOGLE_API_KEY = "AIzaSyAbc123..."  # Doğru
   GOOGLE_API_KEY = AIzaSyAbc123...    # Yanlış (tırnak yok)
   ```

### ❌ "ModuleNotFoundError: No module named 'streamlit'"

**Çözüm:**
```bash
pip install -r requirements.txt
```
Eğer hala çözülmezse:
```bash
pip install streamlit google-generativeai
```

### ❌ "Address already in use" hatası

**Çözüm:**
Başka bir Streamlit uygulaması zaten çalışıyor. Terminali kapatıp yeniden açın.

### ❌ "Permission denied" hatası

**Çözüm (Windows):**
- Terminali "Yönetici olarak çalıştır" modunda açın

**Çözüm (Mac/Linux):**
```bash
sudo streamlit run app.py
```

### ❌ Yavaş çalışıyor

**Nedenler:**
- İnternet bağlantısı yavaş (dosyalar Google'a yükleniyor)
- Çok büyük dosyalar (>50MB)
- Gemini API'da yoğunluk

**Çözüm:**
- Daha hızlı internet kullanın
- Dosyaları parçalara bölün
- Biraz bekleyin ve tekrar deneyin

---

## 📞 DESTEK

### Claude (Ben!) ile İletişim

Ben sizinle bu projede çalıştım ve size tam destek verebilirim:
- Hata mesajlarını bana gönderin
- Özellik ekleme isteklerinizi belirtin
- Kullanımda zorlandığınız yerleri sorun

### Faydalı Linkler

- **Google AI Studio:** https://aistudio.google.com/
- **API Key Yönetimi:** https://aistudio.google.com/apikey
- **Gemini Dökümantasyonu:** https://ai.google.dev/gemini-api/docs
- **Streamlit Dökümantasyonu:** https://docs.streamlit.io/

---

## 🔄 SİSTEMİ KAPATMA

1. Terminal penceresinde `Ctrl + C` tuşlarına basın
2. "Terminate batch job (Y/N)?" sorusuna `Y` yazıp Enter
3. Tarayıcı sekmesini kapatın

Sistem tamamen durur. Tekrar kullanmak için `streamlit run app.py` komutunu çalıştırın.

---

## ✅ BAŞARILAR!

Sisteminiz hazır! Artık hukuki dosyalarınızı yükleyip üzerinde soru-cevap yapabilirsiniz.

**İlk 3 Adım:**
1. ✅ Corpus oluştur
2. ✅ 2-3 test dosyası yükle
3. ✅ Basit bir soru sor ve çalıştığını gör

**Keyifli Kullanımlar!** ⚖️✨
