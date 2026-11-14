# ⚡ YouDow - Modern YouTube Video & Audio Downloader

**YouDow** — Python, **CustomTkinter** və **yt-dlp** əsasında hazırlanmış, müasir Flat/Dark interfeysə malik, çoxdilli (Azərbaycan, English, Türkçe), sürətli, **Multi-URL yükləmə dəstəkli** və istifadəsi olduqca asan olan masaüstü (Desktop) tətbiqidir.

---

## 🌟 Əsas Xüsusiyyətlər

1. **⚡ Çoxlu Yükləmə (Multi-Download - Maksimum 10 Link):**
   - **"Çoxlu Yükləmə (Multi-URL)"** rejimini yandırdıqda URL sətrinin yanında **`➕`** düyməsi görünür.
   - Hər basdıqda yeni bir URL xanası əlavə olunur (ümumi 10 ədədə qədər).
   - Hər sətirdə sürətli yapışdırma (`📋`) və silmə (`🗑`) düymələri mövcuddur.
   - Eyni anda 10 müxtəlif video və ya mahnını tək kliklə növbəli şəkildə yüksək sürətlə yükləyə bilərsiniz.

2. **🌐 3 Dil Dəstəyi (Multilingual):**
   - **Azərbaycan dili**, **English** və **Türkçe**. Proqram daxilində dili dəyişdikdə bütün interfeys, düymələr, bildirişlər və seçimlər dərhal seçilən dilə uyğunlaşır.

3. **✏️ Fərdi Fayl Adı (Custom Filename):**
   - Tək video yükləyərkən videonun adını istədiyiniz kimi dəyişə və ya qısalda bilərsiniz. "↺ Orijinal Ad" düyməsi ilə istənilən vaxt orijinal YouTube başlığına qayıtmaq mümkündür.

4. **📁 İstənilən Qovluğa Birbaşa Çıxarış:**
   - Heç bir lazımsız "NA" və ya kənar alt qovluq yaratmadan, seçdiyiniz qovluğun daxilinə birbaşa və səliqəli şəkildə yazılır.

5. **⚡ Yüksək Sürətli və Donmayan Yükləmə:**
   - Çoxaxınlı (Multi-threaded) arxitektura sayəsində yükləmə zamanı proqram interfeysi tam sərbəst işləyir.

6. **🎬 Geniş Keyfiyyət və Format Seçimi:**
   - **Video:** Ən yüksək (Best / 4K / 2K), 1080p Full HD, 720p HD, 480p, 360p və **MP4, MKV, WebM** konteynerləri.
   - **Audio:** Yalnız səs faylı olaraq **MP3, M4A, WAV, FLAC** formatlarında və **320kbps, 256kbps, 192kbps, 128kbps** bitreyt seçimləri ilə.

7. **📊 Canlı İrəliləyiş və Statistikalar:**
   - Real-vaxt Progress Bar, faiz göstəricisi (%), endirilən həcm, cari yükləmə sürəti (MB/s), qalan təxmini vaxt (ETA) və canlı Terminal/Log konsolu.

---

## 📂 Layihənin Fayl Strukturu

```text
youdow/
├── app.py                   # Əsas masaüstü tətbiq kodu (CustomTkinter GUI + Multi-Download + yt-dlp)
├── requirements.txt         # Tələb olunan Python kitabxanaları
├── download_ffmpeg.py       # FFmpeg və FFprobe-u avtomatik yükləyən köməkçi skript
├── build_exe.py             # PyInstaller ilə tək .exe yaradan avtomatik skript
├── create_release_zip.py    # Paylaşıla bilən portativ (.zip) paket yaradan skript
├── generate_icon.py         # Tətbiq üçün xüsusi .ico loqosunu hazırlayan skript
├── install_requirements.bat # Asılılıqları quraşdıran bir-klik faylı
├── run.bat                  # Tətbiqi işə salan bir-klik faylı
├── build.bat                # .EXE paketləyən bir-klik faylı
├── make_zip.bat             # .ZIP portativ paket yaradan bir-klik faylı
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

## 📦 Proqramı .EXE və Portativ .ZIP Şəklinə Salmaq

### 1. Tək .exe Faylı Yaratmaq:
```powershell
python build_exe.py
```
*(və ya `build.bat` faylına klikləyin)*

### 2. Paylaşılabilən Portativ (.ZIP) Paket Hazırlamaq:
```powershell
python create_release_zip.py
```
*(və ya `make_zip.bat` faylına klikləyin)*

Bu əmr `release/` qovluğunda **`YouDow-v1.0-Portable-Windows-x64.zip`** arxivini hazırlayır. Həmin arxivi istənilən istifadəçiyə göndərə və ya **GitHub Releases** bölməsinə yükləyə bilərsiniz.
