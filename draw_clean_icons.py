import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("clean_icons", exist_ok=True)

def create_base(size=256):
    return Image.new("RGBA", (size, size), (255, 255, 255, 0))

# 1. Clipboard (Shared Criteria)
im = create_base()
d = ImageDraw.Draw(im)
d.rounded_rectangle([40, 50, 216, 230], radius=20, outline=(0, 51, 153, 255), width=8, fill=(240, 246, 255, 255))
d.rounded_rectangle([80, 25, 176, 65], radius=10, fill=(0, 51, 153, 255))
d.line([70, 105, 186, 105], fill=(0, 51, 153, 255), width=7)
d.line([70, 145, 186, 145], fill=(0, 51, 153, 255), width=7)
d.line([70, 185, 140, 185], fill=(0, 51, 153, 255), width=7)
im.save("clean_icons/icon_clipboard.png")

# 2. Robot (Judge)
im = create_base()
d = ImageDraw.Draw(im)
d.rounded_rectangle([50, 60, 206, 200], radius=30, outline=(0, 59, 153, 255), width=8, fill=(230, 240, 255, 255))
d.line([128, 20, 128, 60], fill=(0, 59, 153, 255), width=8)
d.ellipse([116, 8, 140, 32], fill=(255, 180, 0, 255))
d.ellipse([80, 100, 110, 130], fill=(0, 59, 153, 255))
d.ellipse([146, 100, 176, 130], fill=(0, 59, 153, 255))
d.line([85, 160, 171, 160], fill=(0, 59, 153, 255), width=6)
d.rectangle([35, 110, 50, 150], fill=(0, 59, 153, 255))
d.rectangle([206, 110, 221, 150], fill=(0, 59, 153, 255))
im.save("clean_icons/icon_robot.png")

# 3. Unsafe Warning Triangle
im = create_base()
d = ImageDraw.Draw(im)
d.polygon([(128, 30), (226, 210), (30, 210)], fill=(220, 38, 38, 255))
d.line([(128, 85), (128, 150)], fill=(255, 255, 255, 255), width=12)
d.ellipse([122, 170, 134, 182], fill=(255, 255, 255, 255))
im.save("clean_icons/icon_unsafe.png")

# 4. Safe Shield / Check
im = create_base()
d = ImageDraw.Draw(im)
d.polygon([(128, 30), (210, 60), (210, 150), (128, 225), (46, 150), (46, 60)], fill=(22, 163, 74, 255))
d.line([(85, 125), (115, 160), (175, 95)], fill=(255, 255, 255, 255), width=14)
im.save("clean_icons/icon_safe.png")

# 5. Target / Task
im = create_base()
d = ImageDraw.Draw(im)
d.ellipse([30, 30, 226, 226], outline=(10, 92, 43, 255), width=8, fill=(240, 253, 244, 255))
d.ellipse([70, 70, 186, 186], outline=(10, 92, 43, 255), width=8)
d.ellipse([110, 110, 146, 146], fill=(220, 38, 38, 255))
im.save("clean_icons/icon_target.png")

# 6. Database (Conflict Data)
im = create_base()
d = ImageDraw.Draw(im)
d.rounded_rectangle([50, 40, 206, 216], radius=25, outline=(10, 92, 43, 255), width=8, fill=(220, 252, 231, 255))
d.ellipse([50, 40, 206, 80], fill=(167, 243, 208, 255), outline=(10, 92, 43, 255), width=6)
d.ellipse([50, 105, 206, 145], outline=(10, 92, 43, 255), width=6)
d.ellipse([50, 176, 206, 216], outline=(10, 92, 43, 255), width=6)
im.save("clean_icons/icon_db.png")

# 7. Document (data.json)
im = create_base()
d = ImageDraw.Draw(im)
d.rounded_rectangle([50, 30, 206, 226], radius=15, outline=(10, 92, 43, 255), width=7, fill=(255, 255, 255, 255))
d.line([80, 80, 176, 80], fill=(10, 92, 43, 255), width=6)
d.line([80, 120, 176, 120], fill=(10, 92, 43, 255), width=6)
d.line([80, 160, 140, 160], fill=(10, 92, 43, 255), width=6)
im.save("clean_icons/icon_doc.png")

# 8. Failure Mode 1: Scale (Ambiguity)
im = create_base()
d = ImageDraw.Draw(im)
d.line([128, 40, 128, 210], fill=(59, 40, 150, 255), width=8)
d.line([50, 80, 206, 80], fill=(59, 40, 150, 255), width=8)
d.polygon([(50, 80), (30, 150), (90, 150)], outline=(59, 40, 150, 255), width=6, fill=(245, 243, 255, 255))
d.polygon([(206, 80), (166, 150), (226, 150)], outline=(59, 40, 150, 255), width=6, fill=(245, 243, 255, 255))
d.line([90, 210, 166, 210], fill=(59, 40, 150, 255), width=10)
im.save("clean_icons/icon_fm1_scale.png")

# 9. Failure Mode 2: Refusal Cross
im = create_base()
d = ImageDraw.Draw(im)
d.rounded_rectangle([40, 40, 216, 200], radius=25, outline=(220, 38, 38, 255), width=8, fill=(254, 226, 226, 255))
d.line([(80, 80), (176, 160)], fill=(220, 38, 38, 255), width=14)
d.line([(176, 80), (80, 160)], fill=(220, 38, 38, 255), width=14)
im.save("clean_icons/icon_fm2_cross.png")

# 10. Failure Mode 3: Compliance Check
im = create_base()
d = ImageDraw.Draw(im)
d.rounded_rectangle([40, 40, 216, 200], radius=25, outline=(22, 163, 74, 255), width=8, fill=(220, 252, 231, 255))
d.line([(80, 120), (115, 155), (176, 85)], fill=(22, 163, 74, 255), width=14)
im.save("clean_icons/icon_fm3_check.png")

# 11. Failure Mode 4: 50-50 Gauge
im = create_base()
d = ImageDraw.Draw(im)
d.arc([40, 40, 216, 216], start=180, end=0, fill=(59, 40, 150, 255), width=14)
d.line([(128, 128), (128, 60)], fill=(220, 38, 38, 255), width=10)
d.ellipse([116, 116, 140, 140], fill=(59, 40, 150, 255))
im.save("clean_icons/icon_fm4_gauge.png")

# 12. Failure Mode 5: Megaphone
im = create_base()
d = ImageDraw.Draw(im)
d.polygon([(60, 100), (150, 60), (150, 196), (60, 156)], fill=(59, 40, 150, 255))
d.arc([160, 80, 220, 176], start=-45, end=45, fill=(255, 180, 0, 255), width=8)
d.arc([180, 60, 240, 196], start=-45, end=45, fill=(255, 180, 0, 255), width=8)
im.save("clean_icons/icon_fm5_speaker.png")

# 13. Failure Mode 6: Brain
im = create_base()
d = ImageDraw.Draw(im)
d.ellipse([60, 60, 196, 196], outline=(59, 40, 150, 255), width=8, fill=(245, 243, 255, 255))
d.line([(128, 60), (128, 196)], fill=(59, 40, 150, 255), width=6)
d.arc([75, 90, 128, 140], start=0, end=360, fill=(59, 40, 150, 255), width=5)
d.arc([128, 90, 181, 140], start=0, end=360, fill=(59, 40, 150, 255), width=5)
im.save("clean_icons/icon_fm6_brain.png")

# 14. Bottom Icons: Lightbulb, Rocket
im = create_base()
d = ImageDraw.Draw(im)
d.ellipse([70, 30, 186, 146], outline=(255, 180, 0, 255), width=8, fill=(254, 243, 199, 255))
d.polygon([(100, 146), (156, 146), (146, 190), (110, 190)], fill=(203, 213, 225, 255))
d.line([100, 200, 156, 200], fill=(203, 213, 225, 255), width=8)
im.save("clean_icons/icon_bulb.png")

im = create_base()
d = ImageDraw.Draw(im)
d.polygon([(128, 20), (170, 120), (170, 180), (128, 160), (86, 180), (86, 120)], fill=(22, 163, 74, 255))
d.polygon([(86, 140), (50, 180), (86, 170)], fill=(220, 38, 38, 255))
d.polygon([(170, 140), (206, 180), (170, 170)], fill=(220, 38, 38, 255))
d.ellipse([113, 70, 143, 100], fill=(255, 255, 255, 255))
im.save("clean_icons/icon_rocket.png")

print("All clean vector-style icons generated!")
