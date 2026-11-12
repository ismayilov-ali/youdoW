"""
FFmpeg Avtomatik Yükləyici Köməkçisi
Bu skript Windows üçün ən son FFmpeg və FFprobe arxivini yükləyir
və layihə qovluğuna çıxarır ki, video və audio konvertasiyaları problemsiz işləsin.
"""

import os
import sys
import zipfile
import shutil
import urllib.request
import gc

FFMPEG_ZIP_URL = "https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"

def download_progress_hook(block_num, block_size, total_size):
    downloaded = block_num * block_size
    if total_size > 0:
        percent = min(100.0, (downloaded / total_size) * 100)
        mb_down = downloaded / (1024 * 1024)
        mb_total = total_size / (1024 * 1024)
        sys.stdout.write(f"\rYüklənir: {percent:.1f}% ({mb_down:.1f} MB / {mb_total:.1f} MB)")
        sys.stdout.flush()

def safe_remove(file_path):
    """Windows-da fayl kilidlənməsinə qarşı təhlükəsiz silmə köməkçisi."""
    if not os.path.exists(file_path):
        return
    gc.collect()
    try:
        os.remove(file_path)
    except Exception:
        pass

def setup_ffmpeg():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    target_ffmpeg = os.path.join(project_dir, "ffmpeg.exe")
    target_ffprobe = os.path.join(project_dir, "ffprobe.exe")
    zip_path = os.path.join(project_dir, "ffmpeg_temp.zip")

    # Əgər artıq çıxarılıbsa, uğurlu hesab et
    if os.path.exists(target_ffmpeg) and os.path.exists(target_ffprobe):
        safe_remove(zip_path)
        print("[✔] ffmpeg.exe və ffprobe.exe artıq layihə qovluğunda mövcuddur və hazırdır!")
        return True

    print(f"[*] FFmpeg arxivi yüklənir:\n    {FFMPEG_ZIP_URL}")

    try:
        urllib.request.urlretrieve(FFMPEG_ZIP_URL, zip_path, download_progress_hook)
        print("\n[+] Yükləmə tamamlandı! Arxiv çıxarılır...")

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                filename = os.path.basename(member)
                if filename in ("ffmpeg.exe", "ffprobe.exe"):
                    target_file_path = os.path.join(project_dir, filename)
                    with zip_ref.open(member) as source, open(target_file_path, "wb") as target:
                        shutil.copyfileobj(source, target)
                    print(f" -> {filename} uğurla çıxarıldı.")

        # Arxiv faylını bağladıqdan sonra zibil toplayıcını işə salıb təhlükəsiz silirik
        safe_remove(zip_path)

        print("\n[✔] FFmpeg quraşdırılması uğurla tamamlandı!")
        return True
    except Exception as e:
        safe_remove(zip_path)
        if os.path.exists(target_ffmpeg) and os.path.exists(target_ffprobe):
            print("\n[✔] ffmpeg.exe və ffprobe.exe uğurla yerləşdirilib və istifadəyə hazırdır!")
            return True
        print(f"\n[!] Xəta baş verdi: {e}")
        return False

if __name__ == "__main__":
    setup_ffmpeg()
