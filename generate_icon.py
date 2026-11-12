"""
YouDow üçün təmiz və modern .ico loqo faylı yaradan skript.
Pillow vasitəsilə 256x256 ölçüdə Windows ikonu hazırlayır.
"""

from PIL import Image, ImageDraw

def create_app_icon():
    size = (256, 256)
    # RGBA şəffaf fon
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Qırmızı-Bənövşəyi müasir gradient əvəzinə hamar dairəvi arxa fon
    margin = 16
    draw.rounded_rectangle(
        [margin, margin, size[0] - margin, size[1] - margin],
        radius=54,
        fill=(230, 57, 70),  # Modern Qırmızı (YouTube red)
        outline=(200, 40, 50),
        width=4
    )

    # Daxili ağ rəngli Play üçbucağı və yükləmə oxu
    # Ağ Play üçbucağı (sol mərkəz)
    points = [
        (100, 75),   # Yuxarı sol
        (100, 181),  # Aşağı sol
        (185, 128)   # Sağ künc
    ]
    draw.polygon(points, fill=(255, 255, 255))

    # Aşağı hissədə ağ endirmə xətti
    draw.rounded_rectangle([80, 195, 176, 207], radius=6, fill=(255, 255, 255))

    icon_path = "icon.ico"
    img.save(icon_path, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print(f"[✔] İkon uğurla yaradıldı: {icon_path}")

if __name__ == "__main__":
    create_app_icon()

