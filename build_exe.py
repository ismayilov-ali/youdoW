"""
=============================================================================
YouDow - PyInstaller ilə .EXE Paketləmə Skripti
=============================================================================
Bu skript bütün asılılıqları (CustomTkinter mövzuları, yt-dlp və FFmpeg)
avtomatik toplayaraq 'dist' qovluğunda tək bir 'YouDow.exe' faylı yaradır.
"""

import os
import sys
import subprocess
import shutil

def run_build():
    print("=" * 60)
    print("  YouDow Desktop App -> .EXE Paketləmə Başlayır")
    print("=" * 60)

    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    # 1. PyInstaller yoxlanışı
    try:
        import PyInstaller
        print("[✔] PyInstaller aşkarlandı.")
    except ImportError:
        print("[!] PyInstaller tapılmadı. Zəhmət olmasa quraşdırın:")
        print("    pip install pyinstaller")
        return False

    # 2. FFmpeg fayllarının yoxlanışı
    ffmpeg_exe = os.path.join(project_dir, "ffmpeg.exe")
    ffprobe_exe = os.path.join(project_dir, "ffprobe.exe")
    include_ffmpeg = os.path.exists(ffmpeg_exe) and os.path.exists(ffprobe_exe)

    if include_ffmpeg:
        print("[✔] ffmpeg.exe və ffprobe.exe aşkarlandı! .exe daxilinə inteqrasiya olunacaq.")
    else:
        print("[i] Qeyd: ffmpeg.exe layihə qovluğunda tapılmadı.")
        print("    Əgər video/audio konvertasiyalarının tək .exe daxilində hazır olmasını istəyirsinizsə,")
        print("    əvvəlcə 'python download_ffmpeg.py' əmrini icra edin.")

    # 3. İkon yoxlanışı
    icon_file = os.path.join(project_dir, "icon.ico")
    has_icon = os.path.exists(icon_file)

    # 4. PyInstaller parametrlərinin qurulması
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--noconsole",                  # Konsol (qara cmd pəncərəsi) görünməsin
        "--onefile",                    # Tək və portativ .exe faylı
        "--name=YouDow",                # Çıxış faylının adı (YouDow.exe)
        "--clean",                      # Əvvəlki build keşini təmizlə
        "--collect-all", "customtkinter", # CustomTkinter-in bütün dizayn və şrift fayllarını topla
        "--collect-all", "yt_dlp",      # yt-dlp-nin bütün ekstraktorlarını topla
    ]

    # İkon əlavə et
    if has_icon:
        cmd.extend(["--icon", "icon.ico"])

    # FFmpeg binar fayllarını .exe-nin daxilinə kopyala (Windows üçün separator ;)
    if include_ffmpeg:
        cmd.extend([
            "--add-binary", f"{ffmpeg_exe};.",
            "--add-binary", f"{ffprobe_exe};."
        ])

    # Əsas skript
    cmd.append("app.py")

    print("\n[*] İcra olunan əmr:")
    print(" ".join(cmd))
    print("\n[*] Zəhmət olmasa gözləyin, paketləmə bir neçə dəqiqə çəkə bilər...\n")

    # Əmri icra et
    result = subprocess.run(cmd)

    if result.returncode == 0:
        dist_exe = os.path.join(project_dir, "dist", "YouDow.exe")
        print("\n" + "=" * 60)
        print("🎉 TƏBRİKLƏR! Paketləmə uğurla tamamlandı!")
        print(f"👉 Hazır .exe faylının yeri:\n   {dist_exe}")
        print("=" * 60)
        return True
    else:
        print("\n[!] Paketləmə zamanı xəta baş verdi.")
        return False

if __name__ == "__main__":
    run_build()

