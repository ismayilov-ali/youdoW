"""
=============================================================================
YouDow - Portativ Yükləmə ZİP Paketi Yaradıcı (Release Packager)
=============================================================================
Bu skript istifadəçilərin heç bir Python və ya əlavə proqram quraşdırmadan
birbaşa işlədə biləcəyi 'YouDow-v1.0-Portable-x64.zip' arxivini hazırlayır.
"""

import os
import sys
import shutil
import zipfile

def create_zip_progress(src_dir, output_zip_path):
    """Qovluğu ZIP formatında arxivləyir."""
    total_files = sum([len(files) for _, _, files in os.walk(src_dir)])
    processed = 0

    print(f"[*] Arxiv sıxılır ({total_files} fayl)...")
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(src_dir))
                zipf.write(file_path, arcname)
                processed += 1
                percent = (processed / total_files) * 100
                sys.stdout.write(f"\rArxivlənir: %{percent:.1f} ({file})")
                sys.stdout.flush()
    print("\n[✔] Sıxılma tamamlandı!")

def main():
    print("=" * 65)
    print("  YouDow - Paylaşılabilən Portativ (.ZIP) Paket Yaradılır")
    print("=" * 65)

    project_dir = os.path.dirname(os.path.abspath(__file__))
    dist_exe = os.path.join(project_dir, "dist", "YouDow.exe")

    # 1. YouDow.exe yoxlanışı
    if not os.path.exists(dist_exe):
        print("[!] 'dist/YouDow.exe' tapılmadı.")
        print("[*] Əvvəlcə PyInstaller ilə .exe faylı yığılır...")
        build_script = os.path.join(project_dir, "build_exe.py")
        if os.path.exists(build_script):
            import build_exe
            success = build_exe.run_build()
            if not success or not os.path.exists(dist_exe):
                print("[!] .exe yaradıla bilmədi. Zəhmət olmasa xətaları yoxlayın.")
                return
        else:
            print("[!] build_exe.py tapılmadı.")
            return

    # 2. Hazırlıq qovluqları
    release_dir = os.path.join(project_dir, "release")
    package_name = "YouDow-v1.0-Portable"
    portable_folder = os.path.join(release_dir, package_name)

    if os.path.exists(portable_folder):
        shutil.rmtree(portable_folder)
    os.makedirs(portable_folder, exist_ok=True)

    # 3. Faylların kopyalanması
    print("\n[*] Fayllar portativ qovluğa kopyalanır...")

    # YouDow.exe
    shutil.copy2(dist_exe, os.path.join(portable_folder, "YouDow.exe"))
    print(" -> YouDow.exe kopyalandı")

    # ffmpeg.exe və ffprobe.exe
    for bin_name in ["ffmpeg.exe", "ffprobe.exe"]:
        bin_path = os.path.join(project_dir, bin_name)
        if os.path.exists(bin_path):
            shutil.copy2(bin_path, os.path.join(portable_folder, bin_name))
            print(f" -> {bin_name} kopyalandı")

    # Qısa təlimat faylı (README.txt)
    readme_content = """==================================================
  YouDow - Modern YouTube Video & Audio Downloader
  Versiya: 1.0.0 (Portativ / Portable)
==================================================

Quraşdırma tələb olunmur!

İstifadə qaydası:
1. Bu qovluğu istədiyiniz yerə (məsələn: İş masasına) çıxarın.
2. "YouDow.exe" faylına iki dəfə klikləyərək proqramı işə salın.
3. YouTube linkini daxil edin və formatı seçərək "Yüklə" düyməsini sıxın.

Qeyd:
Qovluqdakı "ffmpeg.exe" və "ffprobe.exe" fayllarını silməyin.
Bu fayllar 1080p+ Full HD videoların və MP3 audio fayllarının
yüksək keyfiyyətlə hazırlanması üçün tələb olunur.
"""
    with open(os.path.join(portable_folder, "OXU_MENI.txt"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(" -> OXU_MENI.txt yaradıldı")

    # 4. ZIP arxivinin yaradılması
    final_zip_name = f"{package_name}-Windows-x64.zip"
    final_zip_path = os.path.join(release_dir, final_zip_name)

    if os.path.exists(final_zip_path):
        os.remove(final_zip_path)

    create_zip_progress(portable_folder, final_zip_path)

    # Ölçü hesablama
    zip_size_mb = os.path.getsize(final_zip_path) / (1024 * 1024)

    print("\n" + "=" * 65)
    print("🎉 TƏBRİKLƏR! Portativ ZIP paketi hazırdır!")
    print(f"📦 Arxiv faylı: {final_zip_name} ({zip_size_mb:.1f} MB)")
    print(f"📂 Yolu: {final_zip_path}")
    print("=" * 65)
    print("\n💡 Bu .ZIP faylını istənilən istifadəçiyə göndərə və ya")
    print("   GitHub Repozitorinizin 'Releases' bölməsinə yükləyə bilərsiniz.")

if __name__ == "__main__":
    main()

