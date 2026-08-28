import os
from PIL import Image, ImageDraw, ImageFont

def create_aura_app_icon(size):
    # Create image with RGBA
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. Base Squircle / Rounded Rectangle
    radius = int(size * 0.24)
    # Background color: Luxury Obsidian Matte Black
    bg_color = (14, 13, 17, 255)
    draw.rounded_rectangle([(0, 0), (size - 1, size - 1)], radius=radius, fill=bg_color)
    
    # 2. Glowing Rose-Gold Border
    border_color = (249, 115, 22, 180) # Orange / Amber / Rose Gold
    border_width = max(2, int(size * 0.025))
    draw.rounded_rectangle(
        [(border_width // 2, border_width // 2), (size - 1 - border_width // 2, size - 1 - border_width // 2)],
        radius=radius - 2,
        outline=border_color,
        width=border_width
    )
    
    # 3. Ambient Glow Orb (top right corner)
    glow_size = int(size * 0.45)
    glow_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    glow_draw.ellipse(
        [(size - glow_size, -int(glow_size * 0.2)), (size + int(glow_size * 0.3), int(glow_size * 0.9))],
        fill=(234, 88, 12, 90)
    )
    img = Image.alpha_composite(img, glow_img)
    draw = ImageDraw.Draw(img)
    
    # 4. Serif Italic 'R' Glyph
    # Try finding an elegant Serif font, fallback to standard
    font = None
    font_size = int(size * 0.58)
    font_names = ["timesbd.ttf", "georgiab.ttf", "timesbi.ttf", "georgiaz.ttf", "georgia.ttf", "times.ttf", "arialbd.ttf"]
    for fn in font_names:
        try:
            font = ImageFont.truetype(fn, font_size)
            break
        except Exception:
            continue
    if not font:
        font = ImageFont.load_default()
        
    text = "R"
    # Measure text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    # Center position
    text_x = (size - text_w) // 2 - bbox[0]
    text_y = (size - text_h) // 2 - bbox[1] - int(size * 0.02)
    
    # Draw text shadow
    draw.text((text_x + max(1, int(size*0.015)), text_y + max(2, int(size*0.02))), text, font=font, fill=(0, 0, 0, 200))
    # Draw primary text in Glowing Golden Amber
    draw.text((text_x, text_y), text, font=font, fill=(251, 191, 36, 255))
    
    return img

def create_android_notification_badge(size):
    # Android notification badge MUST be a white silhouette on 100% transparent background!
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    font = None
    font_size = int(size * 0.72)
    font_names = ["timesbd.ttf", "georgiab.ttf", "timesbi.ttf", "georgiaz.ttf", "arialbd.ttf"]
    for fn in font_names:
        try:
            font = ImageFont.truetype(fn, font_size)
            break
        except Exception:
            continue
    if not font:
        font = ImageFont.load_default()
        
    text = "R"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    text_x = (size - text_w) // 2 - bbox[0]
    text_y = (size - text_h) // 2 - bbox[1]
    
    # Pure solid white silhouette on 100% transparent background
    draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 255))
    return img

if __name__ == "__main__":
    # Generate app icons
    icon_512 = create_aura_app_icon(512)
    icon_192 = create_aura_app_icon(192)
    badge_96 = create_android_notification_badge(96)
    
    # Save to root and www
    paths = [
        ".",
        "www",
        "../aura-chat",
        "../aura-chat/www"
    ]
    
    for p in paths:
        if os.path.exists(p):
            icon_512.save(os.path.join(p, "icon-512.png"), "PNG")
            icon_192.save(os.path.join(p, "icon-192.png"), "PNG")
            badge_96.save(os.path.join(p, "badge-96.png"), "PNG")
            print(f"Saved icons to {p}")
            
    # Also update Android res mipmap folders
    android_res = "android/app/src/main/res"
    if os.path.exists(android_res):
        sizes = {
            "mipmap-mdpi": 48,
            "mipmap-hdpi": 72,
            "mipmap-xhdpi": 96,
            "mipmap-xxhdpi": 144,
            "mipmap-xxxhdpi": 192
        }
        for folder, sz in sizes.items():
            dir_path = os.path.join(android_res, folder)
            if os.path.exists(dir_path):
                ico = create_aura_app_icon(sz)
                ico.save(os.path.join(dir_path, "ic_launcher.png"), "PNG")
                ico.save(os.path.join(dir_path, "ic_launcher_round.png"), "PNG")
                ico.save(os.path.join(dir_path, "ic_launcher_foreground.png"), "PNG")
                print(f"Updated Android {folder} ({sz}x{sz})")
    print("All icons successfully generated!")
