import os
from PIL import Image, ImageDraw, ImageFont

def create_ar_intertwined_icon(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. Luxury Obsidian Matte Black Squircle
    radius = int(size * 0.24)
    bg_color = (14, 13, 17, 255)
    draw.rounded_rectangle([(0, 0), (size - 1, size - 1)], radius=radius, fill=bg_color)
    
    # 2. Glowing Rose-Gold / Amber Border
    border_color = (249, 115, 22, 190)
    border_width = max(2, int(size * 0.025))
    draw.rounded_rectangle(
        [(border_width // 2, border_width // 2), (size - 1 - border_width // 2, size - 1 - border_width // 2)],
        radius=radius - 2,
        outline=border_color,
        width=border_width
    )
    
    # 3. Ambient Glow Orb
    glow_size = int(size * 0.48)
    glow_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    glow_draw.ellipse(
        [(size - glow_size, -int(glow_size * 0.25)), (size + int(glow_size * 0.25), int(glow_size * 0.85))],
        fill=(234, 88, 12, 100)
    )
    img = Image.alpha_composite(img, glow_img)
    draw = ImageDraw.Draw(img)
    
    # 4. Serif Monogram 'A' and 'R' intertwined
    font = None
    font_size = int(size * 0.44)
    font_names = ["timesbi.ttf", "georgiaz.ttf", "georgiab.ttf", "timesbd.ttf", "arialbd.ttf"]
    for fn in font_names:
        try:
            font = ImageFont.truetype(fn, font_size)
            break
        except Exception:
            continue
    if not font:
        font = ImageFont.load_default()
        
    text_A = "A"
    text_R = "R"
    
    # Draw 'A' slightly left-shifted in soft Rose Quartz
    bbox_A = draw.textbbox((0, 0), text_A, font=font)
    w_A = bbox_A[2] - bbox_A[0]
    h_A = bbox_A[3] - bbox_A[1]
    x_A = int(size * 0.24)
    y_A = (size - h_A) // 2 - bbox_A[1] - int(size * 0.02)
    
    # Shadow for A
    draw.text((x_A + max(1, int(size*0.015)), y_A + max(2, int(size*0.02))), text_A, font=font, fill=(0, 0, 0, 220))
    draw.text((x_A, y_A), text_A, font=font, fill=(244, 114, 182, 255)) # Soft Rose Quartz
    
    # Draw '&' or mini heart or intertwined 'R' in Glowing Amber Gold
    bbox_R = draw.textbbox((0, 0), text_R, font=font)
    w_R = bbox_R[2] - bbox_R[0]
    h_R = bbox_R[3] - bbox_R[1]
    x_R = int(size * 0.48)
    y_R = (size - h_R) // 2 - bbox_R[1] + int(size * 0.02)
    
    # Shadow for R
    draw.text((x_R + max(1, int(size*0.015)), y_R + max(2, int(size*0.02))), text_R, font=font, fill=(0, 0, 0, 220))
    draw.text((x_R, y_R), text_R, font=font, fill=(251, 191, 36, 255)) # Warm Golden Amber
    
    return img

if __name__ == "__main__":
    icon_512 = create_ar_intertwined_icon(512)
    icon_192 = create_ar_intertwined_icon(192)
    
    # Save preview
    icon_512.save("logo_ar_preview.png", "PNG")
    print("Logo AR preview created successfully!")
