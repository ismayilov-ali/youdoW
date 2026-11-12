"""
=============================================================================
YouDow - Modern YouTube Video & Audio Yükləyicisi
Müəllif: Full-Stack Desktop Specialist
Texnologiyalar: Python, CustomTkinter, yt-dlp, FFmpeg, Pillow
Dillər: Azərbaycan dili (AZ), English (EN), Türkçe (TR)
=============================================================================
"""

import os
import sys
import shutil
import threading
import time
import re
import urllib.request
from io import BytesIO
from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image

try:
    import yt_dlp
except ImportError:
    yt_dlp = None


# =============================================================================
# Çoxdillilik Lüğəti (Internationalization / i18n Dictionary)
# =============================================================================

LANGUAGES = {
    "az": {
        "code": "az",
        "name": "Azərbaycan",
        "subtitle": "YouTube-dan yüksək sürətli Video və Audio yükləyici",
        "lang_label": "Dil:",
        "theme_label": "Tema:",
        "theme_dark": "Qaranlıq (Dark)",
        "theme_light": "İşıqlı (Light)",
        "theme_system": "Sistem",
        "url_label": "YouTube Video və ya Playlist Linki:",
        "url_placeholder": "https://www.youtube.com/watch?v=... və ya Playlist linkini bura yapışdırın",
        "paste_btn": "📋 Yapışdır",
        "clear_btn": "✖ Təmizlə",
        "fetch_btn": "🔍 Məlumatı Al",
        "preview_empty": "Link daxil edin və ya 'Məlumatı Al' düyməsini sıxın",
        "preview_loading": "⏳ Məlumatlar YouTube-dan gətirilir, zəhmət olmasa gözləyin...",
        "preview_error": "Məlumat gətirilərkən xəta baş verdi.",
        "channel_prefix": "Kanal: ",
        "duration_prefix": "Müddət: ",
        "views_prefix": " • Baxış: ",
        "type_single": "Tək Video",
        "type_playlist": "Playlist",
        "video_count_prefix": "Video Sayı: ",
        "filename_label": "Faylın Saxlanılacaq Adı (İstəyinizə görə dəyişdirə bilərsiniz):",
        "filename_hint": "*Boş saxlasanız, YouTube-dakı orijinal başlıq istifadə ediləcək",
        "filename_placeholder": "Fayl üçün istədiyiniz xüsusi adı daxil edin...",
        "reset_btn": "↺ Orijinal Ad",
        "mode_label": "Yükləmə Rejimi:",
        "mode_video": "🎬 Video Yüklə",
        "mode_audio": "🎵 Yalnız Səs (Audio)",
        "video_quality_label": "Video Keyfiyyəti:",
        "video_format_label": "Konteyner / Format:",
        "audio_format_label": "Audio Formatı:",
        "audio_bitrate_label": "Audio Bitreyti:",
        "quality_best": "Ən Yüksək (Best)",
        "bitrate_320": "320 kbps (Ən yüksək)",
        "bitrate_256": "256 kbps",
        "bitrate_192": "192 kbps (Standart)",
        "bitrate_128": "128 kbps",
        "playlist_checkbox": "Əgər playlist linkidirsə, bütün videoları yüklə",
        "subtitles_checkbox": "Altyazıları yüklə (mövcuddursa)",
        "dest_label": "Saxlanılacaq Qovluq (İstənilən Qovluğu Seçə Bilərsiniz):",
        "browse_btn": "📂 Qovluq Seç",
        "open_dir_btn": "🚀 Qovluğu Aç",
        "status_ready": "Hazırdır. Yükləməyə başlamaq üçün link daxil edin.",
        "status_fetching": "Video məlumatları yüklənir...",
        "status_fetched": "Məlumatlar əldə edildi. İstəsəniz fayl adını dəyişib yükləməyə başlaya bilərsiniz.",
        "status_preparing": "Yükləmə parametrləri hazırlanır...",
        "status_downloading": "Yüklənir: ",
        "status_converting": "Fayl endirildi! FFmpeg konvertasiyası / birləşdirilməsi aparılır...",
        "status_done": "🎉 Yükləmə uğurla tamamlandı!",
        "status_cancelled": "Yükləmə dayandırıldı.",
        "status_error": "Yükləmə zamanı xəta yarandı!",
        "size_label": "Həcm: ",
        "speed_label": "Sürət: ",
        "eta_label": "Qalan Vaxt: ",
        "download_btn": "⬇  Yükləməyə Başla",
        "cancel_btn": "⛔ Dayandır",
        "log_header": "Əməliyyat Tarixçəsi (Canlı Log):",
        "ffmpeg_active": "FFmpeg: Aktiv [✔]",
        "ffmpeg_missing": "FFmpeg: Tapılmadı [!] (Video birləşdirmə məhdud ola bilər)",
        "warn_title": "Xəbərdarlıq",
        "warn_enter_url": "Zəhmət olmasa bir YouTube linki daxil edin!",
        "warn_no_dir": "Qeyd olunan qovluq mövcud deyil.",
        "error_title": "Xəta",
        "complete_title": "Tamamlandı!",
        "complete_msg": "Fayl uğurla yükləndi!\n\nSaxlanılan qovluğu açmaq istəyirsiniz?",
        "cancel_info_title": "Məlumat",
        "cancel_info_msg": "Yükləmə prosesi uğurla dayandırıldı.",
    },
    "en": {
        "code": "en",
        "name": "English",
        "subtitle": "High-speed YouTube Video & Audio Downloader",
        "lang_label": "Language:",
        "theme_label": "Theme:",
        "theme_dark": "Dark",
        "theme_light": "Light",
        "theme_system": "System",
        "url_label": "YouTube Video or Playlist URL:",
        "url_placeholder": "https://www.youtube.com/watch?v=... or paste playlist link here",
        "paste_btn": "📋 Paste",
        "clear_btn": "✖ Clear",
        "fetch_btn": "🔍 Get Info",
        "preview_empty": "Enter a link or click 'Get Info'",
        "preview_loading": "⏳ Fetching metadata from YouTube, please wait...",
        "preview_error": "Failed to fetch video information.",
        "channel_prefix": "Channel: ",
        "duration_prefix": "Duration: ",
        "views_prefix": " • Views: ",
        "type_single": "Single Video",
        "type_playlist": "Playlist",
        "video_count_prefix": "Videos: ",
        "filename_label": "Save File Name (Optional customization):",
        "filename_hint": "*Leave empty to use original YouTube title",
        "filename_placeholder": "Enter your custom file name here...",
        "reset_btn": "↺ Original Title",
        "mode_label": "Download Mode:",
        "mode_video": "🎬 Download Video",
        "mode_audio": "🎵 Audio Only",
        "video_quality_label": "Video Quality:",
        "video_format_label": "Container / Format:",
        "audio_format_label": "Audio Format:",
        "audio_bitrate_label": "Audio Bitrate:",
        "quality_best": "Best Available",
        "bitrate_320": "320 kbps (Highest)",
        "bitrate_256": "256 kbps",
        "bitrate_192": "192 kbps (Standard)",
        "bitrate_128": "128 kbps",
        "playlist_checkbox": "If playlist link, download all videos",
        "subtitles_checkbox": "Download subtitles (if available)",
        "dest_label": "Save Directory (Select Any Folder):",
        "browse_btn": "📂 Browse",
        "open_dir_btn": "🚀 Open Folder",
        "status_ready": "Ready. Enter a link to start downloading.",
        "status_fetching": "Fetching video details...",
        "status_fetched": "Metadata loaded. You can customize the file name and start downloading.",
        "status_preparing": "Preparing download parameters...",
        "status_downloading": "Downloading: ",
        "status_converting": "Download finished! FFmpeg post-processing / merging...",
        "status_done": "🎉 Download completed successfully!",
        "status_cancelled": "Download was cancelled.",
        "status_error": "An error occurred during download!",
        "size_label": "Size: ",
        "speed_label": "Speed: ",
        "eta_label": "ETA: ",
        "download_btn": "⬇  Start Download",
        "cancel_btn": "⛔ Cancel",
        "log_header": "Activity History (Live Log):",
        "ffmpeg_active": "FFmpeg: Active [✔]",
        "ffmpeg_missing": "FFmpeg: Not Found [!] (Video merging may be limited)",
        "warn_title": "Warning",
        "warn_enter_url": "Please enter a valid YouTube URL!",
        "warn_no_dir": "The specified folder does not exist.",
        "error_title": "Error",
        "complete_title": "Completed!",
        "complete_msg": "File downloaded successfully!\n\nWould you like to open the destination folder?",
        "cancel_info_title": "Information",
        "cancel_info_msg": "Download was successfully cancelled.",
    },
    "tr": {
        "code": "tr",
        "name": "Türkçe",
        "subtitle": "YouTube Yüksek Hızlı Video ve Ses İndirici",
        "lang_label": "Dil:",
        "theme_label": "Tema:",
        "theme_dark": "Karanlık (Dark)",
        "theme_light": "Aydınlık (Light)",
        "theme_system": "Sistem",
        "url_label": "YouTube Video veya Oynatma Listesi Bağlantısı:",
        "url_placeholder": "https://www.youtube.com/watch?v=... veya oynatma listesi linkini yapıştırın",
        "paste_btn": "📋 Yapıştır",
        "clear_btn": "✖ Temizle",
        "fetch_btn": "🔍 Bilgileri Getir",
        "preview_empty": "Bağlantı girin veya 'Bilgileri Getir' butonuna tıklayın",
        "preview_loading": "⏳ Bilgiler YouTube üzerinden alınıyor, lütfen bekleyin...",
        "preview_error": "Video bilgileri alınırken hata oluştu.",
        "channel_prefix": "Kanal: ",
        "duration_prefix": "Süre: ",
        "views_prefix": " • İzlenme: ",
        "type_single": "Tek Video",
        "type_playlist": "Oynatma Listesi",
        "video_count_prefix": "Video Sayısı: ",
        "filename_label": "Kaydedilecek Dosya Adı (İsteğe bağlı):",
        "filename_hint": "*Boş bırakırsanız orijinal YouTube başlığı kullanılır",
        "filename_placeholder": "Dosya için istediğiniz özel adı yazın...",
        "reset_btn": "↺ Orijinal Ad",
        "mode_label": "İndirme Modu:",
        "mode_video": "🎬 Video İndir",
        "mode_audio": "🎵 Sadece Ses (Audio)",
        "video_quality_label": "Video Kalitesi:",
        "video_format_label": "Format / Kapsayıcı:",
        "audio_format_label": "Ses Formatı:",
        "audio_bitrate_label": "Ses Bit Hızı:",
        "quality_best": "En Yüksek (Best)",
        "bitrate_320": "320 kbps (En yüksek)",
        "bitrate_256": "256 kbps",
        "bitrate_192": "192 kbps (Standart)",
        "bitrate_128": "128 kbps",
        "playlist_checkbox": "Oynatma listesi bağlantısı ise tüm videoları indir",
        "subtitles_checkbox": "Altyazıları indir (varsa)",
        "dest_label": "Kayıt Klasörü (İstediğiniz Klasörü Seçebilirsiniz):",
        "browse_btn": "📂 Klasör Seç",
        "open_dir_btn": "🚀 Klasörü Aç",
        "status_ready": "Hazır. İndirmeye başlamak için bir bağlantı girin.",
        "status_fetching": "Video bilgileri alınıyor...",
        "status_fetched": "Bilgiler getirildi. İsterseniz dosya adını değiştirip indirmeyi başlatabilirsiniz.",
        "status_preparing": "İndirme parametreleri hazırlanıyor...",
        "status_downloading": "İndiriliyor: ",
        "status_converting": "Dosya indirildi! FFmpeg dönüştürme / birleştirme yapılıyor...",
        "status_done": "🎉 İndirme başarıyla tamamlandı!",
        "status_cancelled": "İndirme iptal edildi.",
        "status_error": "İndirme sırasında bir hata oluştu!",
        "size_label": "Boyut: ",
        "speed_label": "Hız: ",
        "eta_label": "Kalan Süre: ",
        "download_btn": "⬇  İndirmeyi Başlat",
        "cancel_btn": "⛔ İptal Et",
        "log_header": "İşlem Geçmişi (Canlı Günlük):",
        "ffmpeg_active": "FFmpeg: Aktif [✔]",
        "ffmpeg_missing": "FFmpeg: Bulunamadı [!] (Video birleştirme sınırlı olabilir)",
        "warn_title": "Uyarı",
        "warn_enter_url": "Lütfen geçerli bir YouTube bağlantısı girin!",
        "warn_no_dir": "Belirtilen klasör mevcut değil.",
        "error_title": "Hata",
        "complete_title": "Tamamlandı!",
        "complete_msg": "Dosya başarıyla indirildi!\n\nKayıt klasörünü açmak ister misiniz?",
        "cancel_info_title": "Bilgi",
        "cancel_info_msg": "İndirme işlemi başarıyla durduruldu.",
    }
}


# =============================================================================
# Köməkçi Funksiyalar (Utils & Helpers)
# =============================================================================

def get_base_dir():
    """Tətbiqin icra olunduğu əsas qovluğu qaytarır (PyInstaller dəstəkli)."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def get_ffmpeg_path():
    """
    FFmpeg icra faylının yolunu müəyyən edir:
    1. PyInstaller müvəqqəti qovluğu (_MEIPASS)
    2. Tətbiqin yerləşdiyi qovluq və ya 'bin' alt qovluğu
    3. Əməliyyat sisteminin PATH mühit dəyişəni
    """
    if hasattr(sys, '_MEIPASS'):
        bundle_ffmpeg = os.path.join(sys._MEIPASS, "ffmpeg.exe")
        if os.path.exists(bundle_ffmpeg):
            return bundle_ffmpeg

    base_dir = get_base_dir()

    local_ffmpeg = os.path.join(base_dir, "ffmpeg.exe")
    if os.path.exists(local_ffmpeg):
        return local_ffmpeg

    bin_ffmpeg = os.path.join(base_dir, "bin", "ffmpeg.exe")
    if os.path.exists(bin_ffmpeg):
        return bin_ffmpeg

    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg

    return None


def sanitize_filename(name):
    """
    Windows əməliyyat sistemində fayl adında qadağan olunmuş simvolları
    təmizləyir (\ / : * ? " < > |) və təhlükəsiz fayl adına çevirir.
    """
    if not name:
        return ""
    cleaned = re.sub(r'[\\/*?:"<>|]', '_', name)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip('. ')
    return cleaned[:160]


def format_bytes(bytes_num):
    """Baytları insan oxuya bilən formata (KB, MB, GB) çevirir."""
    if not bytes_num or bytes_num <= 0:
        return "0 MB"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_num < 1024.0:
            return f"{bytes_num:.2f} {unit}"
        bytes_num /= 1024.0
    return f"{bytes_num:.2f} PB"


def format_seconds(seconds):
    """Saniyələri 'MM:SS' və ya 'HH:MM:SS' formatına salır."""
    if seconds is None or seconds < 0:
        return "--:--"
    seconds = int(seconds)
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    if hours > 0:
        return f"{hours:02d}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"


# =============================================================================
# Xüsusi yt-dlp Logger Sinfi
# =============================================================================

class YTDLPLogger:
    """yt-dlp konsol çıxışlarını tutub GUI log pəncərəsinə yönləndirir."""
    def __init__(self, log_callback):
        self.log_callback = log_callback

    def debug(self, msg):
        if msg.startswith('[download]') or msg.startswith('[ExtractAudio]') or msg.startswith('[Merger]'):
            self.log_callback(f"[MƏLUMAT] {msg}")

    def info(self, msg):
        self.log_callback(f"[MƏLUMAT] {msg}")

    def warning(self, msg):
        self.log_callback(f"[XƏBƏRDARLIQ] {msg}")

    def error(self, msg):
        self.log_callback(f"[XƏTA] {msg}")


# =============================================================================
# Əsas Tətbiq İnterfeysi (GUI)
# =============================================================================

class YouDowApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pəncərənin əsas parametrləri
        self.title("YouDow - Modern YouTube Downloader")
        self.geometry("940x820")
        self.minsize(840, 720)

        # Standart görünüş rejimi və rəng teması
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Cari dil (Standart: Azərbaycan dili)
        self.current_lang = "az"

        # Proqram vəziyyətləri (State variables)
        self.download_thread = None
        self.fetch_thread = None
        self.is_downloading = False
        self.cancel_requested = False
        self.current_video_info = None
        self.original_video_title = ""

        # Standart yükləmə qovluğu (İstifadəçinin "Downloads" qovluğu)
        default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        self.output_dir_var = ctk.StringVar(value=default_download_dir)
        self.custom_filename_var = ctk.StringVar(value="")

        # UI Elementlərinin qurulması
        self._setup_ui()
        self._apply_language(self.current_lang)
        self._check_ffmpeg_status()

    def t(self, key):
        """Cari dildə tərcümə mətnini qaytarır."""
        return LANGUAGES.get(self.current_lang, LANGUAGES["az"]).get(key, "")

    # -------------------------------------------------------------------------
    # UI Tərtibatı və Komponentləri
    # -------------------------------------------------------------------------
    def _setup_ui(self):
        # Əsas konteyner (Scrollable Frame)
        self.main_container = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=15)

        # 1. Başlıq, Dil və Tema Keçidi
        self._create_header_section()

        # 2. URL Daxil Etmə Bölməsi
        self._create_url_section()

        # 3. Video Məlumatı / Önizləmə Kartı (Preview Card)
        self._create_preview_section()

        # 4. Fərdi Fayl Adı Təyinetmə Bölməsi (Custom Filename)
        self._create_filename_section()

        # 5. Yükləmə Format və Keyfiyyət Seçimləri
        self._create_options_section()

        # 6. Saxlanma Qovluğu Seçimi (Directory)
        self._create_destination_section()

        # 7. Gedişat və İrəliləyiş Göstəricisi (Progress Bar)
        self._create_progress_section()

        # 8. Əməliyyat Düymələri (Start / Cancel)
        self._create_action_buttons()

        # 9. Canlı Log və Status Konsolu
        self._create_log_section()

    def _create_header_section(self):
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))

        title_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_box.pack(side="left")

        app_title = ctk.CTkLabel(
            title_box,
            text="⚡ YouDow",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=("#1f538d", "#3a86ff")
        )
        app_title.pack(anchor="w")

        self.app_subtitle = ctk.CTkLabel(
            title_box,
            text=self.t("subtitle"),
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.app_subtitle.pack(anchor="w")

        # Sağ tərəfdə Dil və Tema idarəetmə paneli
        controls_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        controls_box.pack(side="right", anchor="e")

        # Dil Seçimi
        self.lang_label = ctk.CTkLabel(controls_box, text=self.t("lang_label"), font=ctk.CTkFont(size=12))
        self.lang_label.pack(side="left", padx=(0, 6))

        self.lang_menu = ctk.CTkOptionMenu(
            controls_box,
            values=["Azərbaycan", "English", "Türkçe"],
            command=self._on_language_changed,
            width=115
        )
        self.lang_menu.set("Azərbaycan")
        self.lang_menu.pack(side="left", padx=(0, 16))

        # Tema Seçimi
        self.theme_label = ctk.CTkLabel(controls_box, text=self.t("theme_label"), font=ctk.CTkFont(size=12))
        self.theme_label.pack(side="left", padx=(0, 6))

        self.theme_switch = ctk.CTkOptionMenu(
            controls_box,
            values=["Qaranlıq (Dark)", "İşıqlı (Light)", "Sistem"],
            command=self._change_theme,
            width=125
        )
        self.theme_switch.set("Qaranlıq (Dark)")
        self.theme_switch.pack(side="left")

    def _create_url_section(self):
        url_frame = ctk.CTkFrame(self.main_container, corner_radius=12)
        url_frame.pack(fill="x", pady=(0, 12), padx=5)

        url_inner = ctk.CTkFrame(url_frame, fg_color="transparent")
        url_inner.pack(fill="x", padx=15, pady=12)

        self.url_lbl = ctk.CTkLabel(
            url_inner,
            text=self.t("url_label"),
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.url_lbl.pack(anchor="w", pady=(0, 6))

        input_row = ctk.CTkFrame(url_inner, fg_color="transparent")
        input_row.pack(fill="x")

        self.url_entry = ctk.CTkEntry(
            input_row,
            placeholder_text=self.t("url_placeholder"),
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.url_entry.bind("<Return>", lambda event: self._start_fetch_metadata())

        self.paste_btn = ctk.CTkButton(
            input_row,
            text=self.t("paste_btn"),
            width=90,
            height=40,
            command=self._paste_clipboard
        )
        self.paste_btn.pack(side="left", padx=(0, 8))

        self.clear_btn = ctk.CTkButton(
            input_row,
            text=self.t("clear_btn"),
            width=80,
            height=40,
            fg_color="#e63946",
            hover_color="#b02a37",
            command=self._clear_url
        )
        self.clear_btn.pack(side="left", padx=(0, 8))

        self.fetch_btn = ctk.CTkButton(
            input_row,
            text=self.t("fetch_btn"),
            width=115,
            height=40,
            fg_color="#2b9348",
            hover_color="#1f6f36",
            command=self._start_fetch_metadata
        )
        self.fetch_btn.pack(side="left")

    def _create_preview_section(self):
        self.preview_frame = ctk.CTkFrame(self.main_container, corner_radius=12)
        self.preview_frame.pack(fill="x", pady=(0, 12), padx=5)

        preview_inner = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
        preview_inner.pack(fill="x", padx=15, pady=12)

        self.thumb_label = ctk.CTkLabel(
            preview_inner,
            text="[ Önizləmə ]",
            width=160,
            height=90,
            corner_radius=8,
            fg_color=("#d0d0d0", "#2b2b2b")
        )
        self.thumb_label.pack(side="left", padx=(0, 15))

        meta_box = ctk.CTkFrame(preview_inner, fg_color="transparent")
        meta_box.pack(side="left", fill="both", expand=True)

        self.video_title_lbl = ctk.CTkLabel(
            meta_box,
            text=self.t("preview_empty"),
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w",
            wraplength=520,
            justify="left"
        )
        self.video_title_lbl.pack(anchor="w", pady=(0, 4))

        self.video_channel_lbl = ctk.CTkLabel(
            meta_box,
            text=f"{self.t('channel_prefix')}--",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w"
        )
        self.video_channel_lbl.pack(anchor="w")

        self.video_duration_lbl = ctk.CTkLabel(
            meta_box,
            text=f"{self.t('duration_prefix')}--:-- | --",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w"
        )
        self.video_duration_lbl.pack(anchor="w")

    def _create_filename_section(self):
        name_frame = ctk.CTkFrame(self.main_container, corner_radius=12)
        name_frame.pack(fill="x", pady=(0, 12), padx=5)

        name_inner = ctk.CTkFrame(name_frame, fg_color="transparent")
        name_inner.pack(fill="x", padx=15, pady=12)

        lbl_row = ctk.CTkFrame(name_inner, fg_color="transparent")
        lbl_row.pack(fill="x", pady=(0, 6))

        self.filename_lbl = ctk.CTkLabel(
            lbl_row,
            text=self.t("filename_label"),
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.filename_lbl.pack(side="left")

        self.filename_hint = ctk.CTkLabel(
            lbl_row,
            text=self.t("filename_hint"),
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.filename_hint.pack(side="right")

        row = ctk.CTkFrame(name_inner, fg_color="transparent")
        row.pack(fill="x")

        self.filename_entry = ctk.CTkEntry(
            row,
            textvariable=self.custom_filename_var,
            placeholder_text=self.t("filename_placeholder"),
            font=ctk.CTkFont(size=12),
            height=36
        )
        self.filename_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.reset_filename_btn = ctk.CTkButton(
            row,
            text=self.t("reset_btn"),
            width=110,
            height=36,
            fg_color="#495057",
            hover_color="#343a40",
            command=self._reset_filename_to_original
        )
        self.reset_filename_btn.pack(side="left", padx=(0, 8))

        self.clear_filename_btn = ctk.CTkButton(
            row,
            text=self.t("clear_btn"),
            width=80,
            height=36,
            fg_color="#6c757d",
            hover_color="#495057",
            command=lambda: self.custom_filename_var.set("")
        )
        self.clear_filename_btn.pack(side="left")

    def _create_options_section(self):
        opt_frame = ctk.CTkFrame(self.main_container, corner_radius=12)
        opt_frame.pack(fill="x", pady=(0, 12), padx=5)

        opt_inner = ctk.CTkFrame(opt_frame, fg_color="transparent")
        opt_inner.pack(fill="x", padx=15, pady=12)

        top_row = ctk.CTkFrame(opt_inner, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 10))

        self.mode_lbl = ctk.CTkLabel(top_row, text=self.t("mode_label"), font=ctk.CTkFont(size=13, weight="bold"))
        self.mode_lbl.pack(side="left", padx=(0, 15))

        self.mode_selector = ctk.CTkSegmentedButton(
            top_row,
            values=[self.t("mode_video"), self.t("mode_audio")],
            command=self._on_mode_changed,
            height=32
        )
        self.mode_selector.set(self.t("mode_video"))
        self.mode_selector.pack(side="left")

        # Dinamik seçimlər paneli
        self.dynamic_options_row = ctk.CTkFrame(opt_inner, fg_color="transparent")
        self.dynamic_options_row.pack(fill="x", pady=(0, 10))

        # 1-ci Seçim Qutusu
        self.opt1_label = ctk.CTkLabel(self.dynamic_options_row, text=self.t("video_quality_label"), font=ctk.CTkFont(size=12))
        self.opt1_label.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=4)

        self.opt1_menu = ctk.CTkOptionMenu(
            self.dynamic_options_row,
            values=["Best", "1080p", "720p", "480p", "360p"],
            width=180
        )
        self.opt1_menu.set("Best")
        self.opt1_menu.grid(row=0, column=1, sticky="w", padx=(0, 25), pady=4)

        # 2-ci Seçim Qutusu
        self.opt2_label = ctk.CTkLabel(self.dynamic_options_row, text=self.t("video_format_label"), font=ctk.CTkFont(size=12))
        self.opt2_label.grid(row=0, column=2, sticky="w", padx=(0, 10), pady=4)

        self.opt2_menu = ctk.CTkOptionMenu(
            self.dynamic_options_row,
            values=["MP4", "MKV", "WEBM"],
            width=150
        )
        self.opt2_menu.set("MP4")
        self.opt2_menu.grid(row=0, column=3, sticky="w", pady=4)

        # Əlavə Seçimlər
        extra_row = ctk.CTkFrame(opt_inner, fg_color="transparent")
        extra_row.pack(fill="x", pady=(5, 0))

        self.playlist_var = ctk.BooleanVar(value=False)
        self.playlist_checkbox = ctk.CTkCheckBox(
            extra_row,
            text=self.t("playlist_checkbox"),
            variable=self.playlist_var,
            font=ctk.CTkFont(size=12)
        )
        self.playlist_checkbox.pack(side="left", padx=(0, 20))

        self.subtitles_var = ctk.BooleanVar(value=False)
        self.subtitles_checkbox = ctk.CTkCheckBox(
            extra_row,
            text=self.t("subtitles_checkbox"),
            variable=self.subtitles_var,
            font=ctk.CTkFont(size=12)
        )
        self.subtitles_checkbox.pack(side="left")

    def _create_destination_section(self):
        dest_frame = ctk.CTkFrame(self.main_container, corner_radius=12)
        dest_frame.pack(fill="x", pady=(0, 12), padx=5)

        dest_inner = ctk.CTkFrame(dest_frame, fg_color="transparent")
        dest_inner.pack(fill="x", padx=15, pady=12)

        self.dest_lbl = ctk.CTkLabel(dest_inner, text=self.t("dest_label"), font=ctk.CTkFont(size=13, weight="bold"))
        self.dest_lbl.pack(anchor="w", pady=(0, 6))

        row = ctk.CTkFrame(dest_inner, fg_color="transparent")
        row.pack(fill="x")

        self.dest_entry = ctk.CTkEntry(
            row,
            textvariable=self.output_dir_var,
            font=ctk.CTkFont(size=12),
            height=36
        )
        self.dest_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.browse_btn = ctk.CTkButton(
            row,
            text=self.t("browse_btn"),
            width=110,
            height=36,
            command=self._browse_directory
        )
        self.browse_btn.pack(side="left", padx=(0, 8))

        self.open_dir_btn = ctk.CTkButton(
            row,
            text=self.t("open_dir_btn"),
            width=110,
            height=36,
            fg_color="#4a4e69",
            hover_color="#22223b",
            command=self._open_current_directory
        )
        self.open_dir_btn.pack(side="left")

    def _create_progress_section(self):
        self.prog_frame = ctk.CTkFrame(self.main_container, corner_radius=12)
        self.prog_frame.pack(fill="x", pady=(0, 12), padx=5)

        prog_inner = ctk.CTkFrame(self.prog_frame, fg_color="transparent")
        prog_inner.pack(fill="x", padx=15, pady=12)

        status_row = ctk.CTkFrame(prog_inner, fg_color="transparent")
        status_row.pack(fill="x", pady=(0, 6))

        self.status_lbl = ctk.CTkLabel(
            status_row,
            text=self.t("status_ready"),
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        self.status_lbl.pack(side="left", fill="x", expand=True)

        self.percent_lbl = ctk.CTkLabel(
            status_row,
            text="0%",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=("#1f538d", "#3a86ff")
        )
        self.percent_lbl.pack(side="right")

        self.progress_bar = ctk.CTkProgressBar(prog_inner, height=14, corner_radius=7)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(0, 6))

        stats_row = ctk.CTkFrame(prog_inner, fg_color="transparent")
        stats_row.pack(fill="x")

        self.size_lbl = ctk.CTkLabel(stats_row, text=f"{self.t('size_label')}-- / --", font=ctk.CTkFont(size=11), text_color="gray")
        self.size_lbl.pack(side="left", padx=(0, 20))

        self.speed_lbl = ctk.CTkLabel(stats_row, text=f"{self.t('speed_label')}-- MB/s", font=ctk.CTkFont(size=11), text_color="gray")
        self.speed_lbl.pack(side="left", padx=(0, 20))

        self.eta_lbl = ctk.CTkLabel(stats_row, text=f"{self.t('eta_label')}--:--", font=ctk.CTkFont(size=11), text_color="gray")
        self.eta_lbl.pack(side="left")

    def _create_action_buttons(self):
        btn_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 12), padx=5)

        self.download_btn = ctk.CTkButton(
            btn_frame,
            text=self.t("download_btn"),
            font=ctk.CTkFont(size=15, weight="bold"),
            height=46,
            fg_color="#0077b6",
            hover_color="#023e8a",
            command=self._start_download
        )
        self.download_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.cancel_btn = ctk.CTkButton(
            btn_frame,
            text=self.t("cancel_btn"),
            font=ctk.CTkFont(size=14, weight="bold"),
            height=46,
            width=140,
            fg_color="#d90429",
            hover_color="#9a031e",
            state="disabled",
            command=self._cancel_download
        )
        self.cancel_btn.pack(side="left")

    def _create_log_section(self):
        log_frame = ctk.CTkFrame(self.main_container, corner_radius=12)
        log_frame.pack(fill="both", expand=True, pady=(0, 5), padx=5)

        log_inner = ctk.CTkFrame(log_frame, fg_color="transparent")
        log_inner.pack(fill="both", expand=True, padx=15, pady=12)

        header_row = ctk.CTkFrame(log_inner, fg_color="transparent")
        header_row.pack(fill="x", pady=(0, 6))

        self.log_header_lbl = ctk.CTkLabel(header_row, text=self.t("log_header"), font=ctk.CTkFont(size=12, weight="bold"))
        self.log_header_lbl.pack(side="left")

        self.ffmpeg_badge = ctk.CTkLabel(
            header_row,
            text="FFmpeg...",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.ffmpeg_badge.pack(side="right")

        self.log_box = ctk.CTkTextbox(log_inner, height=110, font=ctk.CTkFont(family="Consolas", size=11))
        self.log_box.pack(fill="both", expand=True)
        self.log_box.insert("end", "[System] YouDow initialized.\n")

    # -------------------------------------------------------------------------
    # Dil Dəyişməsi və Yenilənməsi (Dynamic Language Switch)
    # -------------------------------------------------------------------------
    def _on_language_changed(self, lang_name):
        code_map = {"Azərbaycan": "az", "English": "en", "Türkçe": "tr"}
        code = code_map.get(lang_name, "az")
        self._apply_language(code)

    def _apply_language(self, lang_code):
        self.current_lang = lang_code
        t = LANGUAGES.get(lang_code, LANGUAGES["az"])

        # Başlıq və üst idarəetmələr
        self.app_subtitle.configure(text=t["subtitle"])
        self.lang_label.configure(text=t["lang_label"])
        self.theme_label.configure(text=t["theme_label"])

        # URL bölməsi
        self.url_lbl.configure(text=t["url_label"])
        self.url_entry.configure(placeholder_text=t["url_placeholder"])
        self.paste_btn.configure(text=t["paste_btn"])
        self.clear_btn.configure(text=t["clear_btn"])
        self.fetch_btn.configure(text=t["fetch_btn"])

        # Önizləmə
        if not self.current_video_info:
            self.video_title_lbl.configure(text=t["preview_empty"])
            self.video_channel_lbl.configure(text=f"{t['channel_prefix']}--")
            self.video_duration_lbl.configure(text=f"{t['duration_prefix']}--:-- | --")
            self.status_lbl.configure(text=t["status_ready"])

        # Fayl adı
        self.filename_lbl.configure(text=t["filename_label"])
        self.filename_hint.configure(text=t["filename_hint"])
        self.filename_entry.configure(placeholder_text=t["filename_placeholder"])
        self.reset_filename_btn.configure(text=t["reset_btn"])
        self.clear_filename_btn.configure(text=t["clear_btn"])

        # Rejim və seçimlər
        current_mode = self.mode_selector.get()
        is_video_mode = "Video" in current_mode or "Video" in self.t("mode_video")

        self.mode_lbl.configure(text=t["mode_label"])
        self.mode_selector.configure(values=[t["mode_video"], t["mode_audio"]])
        self.mode_selector.set(t["mode_video"] if is_video_mode else t["mode_audio"])
        self._on_mode_changed(self.mode_selector.get())

        self.playlist_checkbox.configure(text=t["playlist_checkbox"])
        self.subtitles_checkbox.configure(text=t["subtitles_checkbox"])

        # Qovluq bölməsi
        self.dest_lbl.configure(text=t["dest_label"])
        self.browse_btn.configure(text=t["browse_btn"])
        self.open_dir_btn.configure(text=t["open_dir_btn"])

        # Düymələr və Log
        self.download_btn.configure(text=t["download_btn"])
        self.cancel_btn.configure(text=t["cancel_btn"])
        self.log_header_lbl.configure(text=t["log_header"])

        # Statistikalar
        self.size_lbl.configure(text=f"{t['size_label']}-- / --")
        self.speed_lbl.configure(text=f"{t['speed_label']}-- MB/s")
        self.eta_lbl.configure(text=f"{t['eta_label']}--:--")

        self._check_ffmpeg_status()

    # -------------------------------------------------------------------------
    # UI Hadisələri və Məntiq (Event Handlers)
    # -------------------------------------------------------------------------
    def _change_theme(self, choice):
        if "Dark" in choice or "Qaranlıq" in choice or "Karanlık" in choice:
            ctk.set_appearance_mode("dark")
        elif "Light" in choice or "İşıqlı" in choice or "Aydınlık" in choice:
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("system")

    def _on_mode_changed(self, mode):
        t = LANGUAGES.get(self.current_lang, LANGUAGES["az"])
        if mode == t["mode_video"] or "Video" in mode:
            self.opt1_label.configure(text=t["video_quality_label"])
            self.opt1_menu.configure(values=[f"{t['quality_best']}", "1080p (Full HD)", "720p (HD)", "480p", "360p"])
            self.opt1_menu.set(f"{t['quality_best']}")

            self.opt2_label.configure(text=t["video_format_label"])
            self.opt2_menu.configure(values=["MP4", "MKV", "WEBM"])
            self.opt2_menu.set("MP4")
        else:
            self.opt1_label.configure(text=t["audio_format_label"])
            self.opt1_menu.configure(values=["MP3", "M4A", "WAV", "FLAC"])
            self.opt1_menu.set("MP3")

            self.opt2_label.configure(text=t["audio_bitrate_label"])
            self.opt2_menu.configure(values=[t["bitrate_320"], t["bitrate_256"], t["bitrate_192"], t["bitrate_128"]])
            self.opt2_menu.set(t["bitrate_320"])

    def _paste_clipboard(self):
        try:
            clipboard_text = self.clipboard_get().strip()
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, clipboard_text)
            self._start_fetch_metadata()
        except Exception:
            pass

    def _clear_url(self):
        t = LANGUAGES.get(self.current_lang, LANGUAGES["az"])
        self.url_entry.delete(0, "end")
        self.custom_filename_var.set("")
        self.original_video_title = ""
        self.video_title_lbl.configure(text=t["preview_empty"])
        self.video_channel_lbl.configure(text=f"{t['channel_prefix']}--")
        self.video_duration_lbl.configure(text=f"{t['duration_prefix']}--:-- | --")
        self.thumb_label.configure(text="[ Preview ]", image="")
        self.progress_bar.set(0)
        self.percent_lbl.configure(text="0%")
        self.current_video_info = None

    def _reset_filename_to_original(self):
        if self.original_video_title:
            self.custom_filename_var.set(sanitize_filename(self.original_video_title))

    def _browse_directory(self):
        selected_dir = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if selected_dir:
            self.output_dir_var.set(os.path.normpath(selected_dir))

    def _open_current_directory(self):
        path = self.output_dir_var.get()
        if os.path.exists(path):
            os.startfile(path)
        else:
            messagebox.showwarning(self.t("warn_title"), self.t("warn_no_dir"))

    def _append_log(self, text):
        def _insert():
            self.log_box.insert("end", text.strip() + "\n")
            self.log_box.see("end")
        self.after(0, _insert)

    def _check_ffmpeg_status(self):
        ffmpeg_bin = get_ffmpeg_path()
        if ffmpeg_bin:
            self.ffmpeg_badge.configure(text=self.t("ffmpeg_active"), text_color="#2b9348")
        else:
            self.ffmpeg_badge.configure(text=self.t("ffmpeg_missing"), text_color="#e63946")

    # -------------------------------------------------------------------------
    # Video Məlumatlarını Gətirmək (Fetch Metadata)
    # -------------------------------------------------------------------------
    def _start_fetch_metadata(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning(self.t("warn_title"), self.t("warn_enter_url"))
            return

        if self.fetch_thread and self.fetch_thread.is_alive():
            return

        self.fetch_btn.configure(state="disabled")
        self.video_title_lbl.configure(text=self.t("preview_loading"))
        self.status_lbl.configure(text=self.t("status_fetching"))

        self.fetch_thread = threading.Thread(target=self._fetch_metadata_worker, args=(url,), daemon=True)
        self.fetch_thread.start()

    def _fetch_metadata_worker(self, url):
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': 'in_playlist',
                'skip_download': True
            }

            ffmpeg_bin = get_ffmpeg_path()
            if ffmpeg_bin:
                ydl_opts['ffmpeg_location'] = ffmpeg_bin

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                self.current_video_info = info
                self.after(0, self._update_preview_ui, info)
        except Exception as e:
            err_msg = str(e)
            self.after(0, self._on_fetch_error, err_msg)

    def _update_preview_ui(self, info):
        t = LANGUAGES.get(self.current_lang, LANGUAGES["az"])
        self.fetch_btn.configure(state="normal")
        self.status_lbl.configure(text=t["status_fetched"])

        is_playlist = 'entries' in info and info['entries'] is not None

        if is_playlist:
            title = info.get('title', 'YouTube Playlist')
            count = len(list(info.get('entries', [])))
            channel = info.get('uploader', info.get('channel', 'Various'))
            self.original_video_title = title
            self.video_title_lbl.configure(text=f"📋 {t['type_playlist']}: {title}")
            self.video_channel_lbl.configure(text=f"{t['channel_prefix']}{channel}")
            self.video_duration_lbl.configure(text=f"{t['video_count_prefix']}{count} | {t['type_playlist']}")
            self.thumb_label.configure(text=f"[ {t['type_playlist']} ]", image="")
            self._append_log(f"[INFO] Playlist: '{title}' ({count})")
        else:
            title = info.get('title', 'Unknown Title')
            channel = info.get('uploader', info.get('channel', 'Unknown'))
            duration = format_seconds(info.get('duration', 0))
            views = info.get('view_count', 0)
            views_str = f"{views:,}" if views else "--"

            self.original_video_title = title
            if not self.custom_filename_var.get().strip():
                self.custom_filename_var.set(sanitize_filename(title))

            self.video_title_lbl.configure(text=title)
            self.video_channel_lbl.configure(text=f"{t['channel_prefix']}{channel}{t['views_prefix']}{views_str}")
            self.video_duration_lbl.configure(text=f"{t['duration_prefix']}{duration} | {t['type_single']}")
            self._append_log(f"[INFO] Video: '{title}' ({duration})")

            thumb_url = info.get('thumbnail')
            if thumb_url:
                threading.Thread(target=self._load_thumbnail, args=(thumb_url,), daemon=True).start()

    def _load_thumbnail(self, url):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=8) as response:
                image_data = response.read()
            pil_img = Image.open(BytesIO(image_data))
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(160, 90))

            def _set_img():
                self.thumb_label.configure(image=ctk_img, text="")
            self.after(0, _set_img)
        except Exception:
            pass

    def _on_fetch_error(self, err_msg):
        t = LANGUAGES.get(self.current_lang, LANGUAGES["az"])
        self.fetch_btn.configure(state="normal")
        self.video_title_lbl.configure(text=t["preview_error"])
        self.status_lbl.configure(text=t["status_error"])
        self._append_log(f"[ERROR] {err_msg}")
        messagebox.showerror(t["error_title"], f"{t['preview_error']}\n\n{err_msg}")

    # -------------------------------------------------------------------------
    # Yükləmə Əməliyyatları (Download Worker & Hook)
    # -------------------------------------------------------------------------
    def _start_download(self):
        t = LANGUAGES.get(self.current_lang, LANGUAGES["az"])
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning(t["warn_title"], t["warn_enter_url"])
            return

        dest_folder = self.output_dir_var.get().strip()
        if not os.path.exists(dest_folder):
            try:
                os.makedirs(dest_folder, exist_ok=True)
            except Exception as e:
                messagebox.showerror(t["error_title"], f"{t['warn_no_dir']}\n{e}")
                return

        if self.is_downloading:
            return

        self.is_downloading = True
        self.cancel_requested = False
        self.download_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.progress_bar.set(0)
        self.percent_lbl.configure(text="0%")
        self.status_lbl.configure(text=t["status_preparing"])

        mode = self.mode_selector.get()
        opt1 = self.opt1_menu.get()
        opt2 = self.opt2_menu.get()
        allow_playlist = self.playlist_var.get()
        get_subtitles = self.subtitles_var.get()
        custom_filename = self.custom_filename_var.get().strip()

        self.download_thread = threading.Thread(
            target=self._download_worker,
            args=(url, dest_folder, mode, opt1, opt2, allow_playlist, get_subtitles, custom_filename),
            daemon=True
        )
        self.download_thread.start()

    def _cancel_download(self):
        if self.is_downloading:
            self.cancel_requested = True
            self.status_lbl.configure(text=self.t("status_cancelled"))
            self.cancel_btn.configure(state="disabled")
            self._append_log("[SYSTEM] Cancel requested by user.")

    def _progress_hook(self, d):
        if self.cancel_requested:
            raise Exception("DOWNLOAD_CANCELLED_BY_USER")

        t = LANGUAGES.get(self.current_lang, LANGUAGES["az"])
        status = d.get('status')
        if status == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            speed = d.get('speed', 0)
            eta = d.get('eta', 0)
            filename = os.path.basename(d.get('filename', 'File'))

            percent = 0.0
            if total > 0:
                percent = downloaded / total
                percent_str = f"{int(percent * 100)}%"
            else:
                percent_str = "--%"

            speed_str = f"{format_bytes(speed)}/s" if speed else "-- MB/s"
            size_str = f"{t['size_label']}{format_bytes(downloaded)} / {format_bytes(total)}"
            eta_str = f"{t['eta_label']}{format_seconds(eta)}"

            def _update():
                self.progress_bar.set(percent)
                self.percent_lbl.configure(text=percent_str)
                self.status_lbl.configure(text=f"{t['status_downloading']}{filename}")
                self.size_lbl.configure(text=size_str)
                self.speed_lbl.configure(text=f"{t['speed_label']}{speed_str}")
                self.eta_lbl.configure(text=eta_str)

            self.after(0, _update)

        elif status == 'finished':
            def _finished_download():
                self.progress_bar.set(1.0)
                self.percent_lbl.configure(text="100%")
                self.status_lbl.configure(text=t["status_converting"])
                self._append_log("[INFO] Download completed, processing...")
            self.after(0, _finished_download)

    def _download_worker(self, url, dest_folder, mode, opt1, opt2, allow_playlist, get_subtitles, custom_filename):
        t = LANGUAGES.get(self.current_lang, LANGUAGES["az"])
        try:
            ffmpeg_bin = get_ffmpeg_path()
            is_audio = mode == t["mode_audio"] or "Audio" in mode or "Ses" in mode

            clean_custom_name = sanitize_filename(custom_filename)
            if clean_custom_name:
                filename_template = clean_custom_name
            else:
                filename_template = "%(title)s"

            # Doğrudan seçilmiş qovluğa çıxarış (Heç vaxt "NA" qovluğu açmır)
            if allow_playlist:
                outtmpl = os.path.join(dest_folder, "%(playlist_title&{}/|)s" + f"{filename_template}.%(ext)s")
            else:
                outtmpl = os.path.join(dest_folder, f"{filename_template}.%(ext)s")

            ydl_opts = {
                'outtmpl': outtmpl,
                'progress_hooks': [self._progress_hook],
                'logger': YTDLPLogger(self._append_log),
                'noplaylist': not allow_playlist,
                'ignoreerrors': True,
            }

            if ffmpeg_bin:
                ydl_opts['ffmpeg_location'] = ffmpeg_bin

            if get_subtitles:
                ydl_opts['writesubtitles'] = True
                ydl_opts['writeautomaticsub'] = True
                ydl_opts['subtitlesformat'] = 'srt/best'

            if is_audio:
                audio_format = opt1.lower()
                bitrate_match = re.search(r'\d+', opt2)
                bitrate = bitrate_match.group(0) if bitrate_match else "192"

                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': audio_format,
                    'preferredquality': bitrate,
                }]
                self._append_log(f"[MODE] Audio: {audio_format.upper()}, {bitrate}kbps")
            else:
                video_format = opt2.lower()
                res_limit = None
                if "1080p" in opt1:
                    res_limit = 1080
                elif "720p" in opt1:
                    res_limit = 720
                elif "480p" in opt1:
                    res_limit = 480
                elif "360p" in opt1:
                    res_limit = 360

                if res_limit:
                    ydl_opts['format'] = f'bestvideo[height<={res_limit}]+bestaudio/best[height<={res_limit}]/best'
                else:
                    ydl_opts['format'] = 'bestvideo+bestaudio/best'

                ydl_opts['merge_output_format'] = video_format
                self._append_log(f"[MODE] Video: {opt1}, {video_format.upper()}")

            self._append_log(f"[STARTED] Dest: {dest_folder}")
            self._append_log(f"[STARTED] Template: {filename_template}")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.after(0, self._on_download_complete, None)

        except Exception as e:
            err_msg = str(e)
            if "DOWNLOAD_CANCELLED_BY_USER" in err_msg:
                self.after(0, self._on_download_cancelled)
            else:
                self.after(0, self._on_download_complete, err_msg)

    def _on_download_complete(self, error=None):
        t = LANGUAGES.get(self.current_lang, LANGUAGES["az"])
        self.is_downloading = False
        self.download_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")

        if error:
            self.status_lbl.configure(text=t["status_error"])
            self._append_log(f"[ERROR] {error}")
            messagebox.showerror(t["error_title"], f"{t['status_error']}\n\n{error}")
        else:
            self.progress_bar.set(1.0)
            self.percent_lbl.configure(text="100%")
            self.status_lbl.configure(text=t["status_done"])
            self._append_log("[SUCCESS] Download finished!")

            resp = messagebox.askyesno(
                t["complete_title"],
                t["complete_msg"]
            )
            if resp:
                self._open_current_directory()

    def _on_download_cancelled(self):
        t = LANGUAGES.get(self.current_lang, LANGUAGES["az"])
        self.is_downloading = False
        self.download_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        self.progress_bar.set(0)
        self.percent_lbl.configure(text="0%")
        self.status_lbl.configure(text=t["status_cancelled"])
        self._append_log("[CANCELLED] Download stopped by user.")
        messagebox.showinfo(t["cancel_info_title"], t["cancel_info_msg"])


# =============================================================================
# Proqramın Giriş Nöqtəsi (Entry Point)
# =============================================================================
if __name__ == "__main__":
    app = YouDowApp()
    app.mainloop()
