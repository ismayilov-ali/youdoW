# ⚡ YouDow - Modern YouTube Video & Audio Downloader

**YouDow** — Python, **CustomTkinter** və **yt-dlp** əsasında hazırlanmış, müasir Flat/Dark interfeysə malik, çoxdilli (Azərbaycan, English, Türkçe), sürətli və istifadəsi olduqca asan olan masaüstü (Desktop) tətbiqidir.

---

## 🌟 Əsas Xüsusiyyətlər

1. **🌐 3 Dil Dəstəyi (Multilingual):**
   - **Azərbaycan dili**, **English** və **Türkçe**. Proqram daxilində dili dəyişdikdə bütün interfeys, düymələr, bildirişlər və seçimlər dərhal seçilən dilə uyğunlaşır.

2. **✏️ Fərdi Fayl Adı (Custom Filename):**
   - Yükləməzdən əvvəl videonun adını istədiyiniz kimi dəyişə və ya qısalda bilərsiniz. "↺ Orijinal Ad" düyməsi ilə istənilən vaxt orijinal YouTube başlığına qayıtmaq mümkündür.

3. **📁 İstənilən Qovluğa Birbaşa Çıxarış:**
   - Heç bir lazımsız "NA" və ya kənar alt qovluq yaratmadan, seçdiyiniz qovluğun daxilinə birbaşa və səliqəli şəkildə yazılır.

4. **⚡ Yüksək Sürətli və Donmayan Yükləmə:**
   - Çoxaxınlı (Multi-threaded) arxitektura sayəsində yükləmə zamanı proqram interfeysi tam sərbəst işləyir.

5. **🎬 Geniş Keyfiyyət və Format Seçimi:**
   - **Video:** Ən yüksək (Best / 4K / 2K), 1080p Full HD, 720p HD, 480p, 360p və **MP4, MKV, WebM** konteynerləri.
   - **Audio:** Yalnız səs faylı olaraq **MP3, M4A, WAV, FLAC** formatlarında və **320kbps, 256kbps, 192kbps, 128kbps** bitreyt seçimləri ilə.

6. **📊 Canlı İrəliləyiş və Statistikalar:**
   - Real-vaxt Progress Bar, faiz göstəricisi (%), endirilən həcm, cari yükləmə sürəti (MB/s), qalan təxmini vaxt (ETA) və canlı Terminal/Log konsolu.

---

## 📂 Layihənin Fayl Strukturu

```text
youdow/
├── app.py                   # Əsas masaüstü tətbiq kodu (CustomTkinter GUI + Çoxdillilik + yt-dlp)
├── requirements.txt         # Tələb olunan Python kitabxanaları
├── download_ffmpeg.py       # FFmpeg və FFprobe-u avtomatik yükləyən köməkçi skript
├── build_exe.py             # PyInstaller ilə tək .exe yaradan avtomatik skript
├── generate_icon.py         # Tətbiq üçün xüsusi .ico loqosunu hazırlayan skript
├── install_requirements.bat # Asılılıqları quraşdıran bir-klik faylı
├── run.bat                  # Tətbiqi işə salan bir-klik faylı
├── build.bat                # .EXE paketləyən bir-klik faylı
└── README.md                # Təlimat və sənədləşmə
```

---

## 🚀 Quraşdırma və İşə Salma

```powershell
# 1. Asılılıqları quraşdırın
pip install -r requirements.txt

# 2. Tətbiqi işə salın
python app.py
```
*(və ya birbaşa `run.bat` faylına iki dəfə klikləyin)*

---

## 📦 Proqramı Tək Bir ".exe" Faylına Paketləmək (PyInstaller)

Sadəcə bu əmri icra edin:
```powershell
python build_exe.py
```
*(və ya `build.bat` faylına klikləyin)*
Nəticədə `dist/YouDow.exe` faylı yaranacaq.
