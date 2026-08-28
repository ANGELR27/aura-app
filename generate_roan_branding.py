import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_roan_app_icon(size):
    # Base transparent canvas
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    
    # 1. Obsidian Matte Black Squircle with subtle luxury gradient
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(bg)
    radius = int(size * 0.23)
    
    # Create smooth dark gradient from top-left (#1a1921) to bottom-right (#09080c)
    for y in range(size):
        ratio = y / size
        r = int(22 - ratio * 14)
        g = int(21 - ratio * 14)
        b = int(28 - ratio * 18)
        bg_draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
    
    # Mask to squircle
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (size - 1, size - 1)], radius=radius, fill=255)
    
    img = Image.composite(bg, img, mask)
    draw = ImageDraw.Draw(img)
    
    # 2. Subtle White Light / Luxury Glow Vignette (Top-Right / Center light flare)
    glow_size = int(size * 0.6)
    glow_canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_canvas)
    
    # Soft pure white/silver glow in top-right corner
    center_x = int(size * 0.75)
    center_y = int(size * 0.22)
    max_r = int(size * 0.45)
    for i in range(max_r, 0, -4):
        alpha = int(45 * (1 - i / max_r) ** 1.8)
        glow_draw.ellipse(
            [(center_x - i, center_y - i), (center_x + i, center_y + i)],
            fill=(255, 255, 255, alpha)
        )
    
    # Bottom ambient warm silver glow
    for i in range(int(size * 0.35), 0, -5):
        alpha = int(25 * (1 - i / (size * 0.35)) ** 1.5)
        glow_draw.ellipse(
            [(int(size*0.25) - i, int(size*0.8) - i), (int(size*0.25) + i, int(size*0.8) + i)],
            fill=(240, 240, 255, alpha)
        )
        
    img = Image.alpha_composite(img, glow_canvas)
    draw = ImageDraw.Draw(img)
    
    # 3. Sleek border with subtle top-highlight
    border_w = max(2, int(size * 0.022))
    # Border highlight
    draw.rounded_rectangle(
        [(border_w // 2, border_w // 2), (size - 1 - border_w // 2, size - 1 - border_w // 2)],
        radius=radius - 1,
        outline=(255, 255, 255, 60),
        width=border_w
    )
    
    # 4. Premium ROAN Typography
    font_size = int(size * 0.24)
    font = None
    font_names = ["timesbd.ttf", "georgiab.ttf", "timesbi.ttf", "georgiaz.ttf", "arialbd.ttf"]
    for fn in font_names:
        try:
            font = ImageFont.truetype(fn, font_size)
            break
        except Exception:
            continue
    if not font:
        font = ImageFont.load_default()
        
    text = "ROAN"
    
    # Draw custom letter spacing for high fashion look
    # Measure letters individually
    letters = ["R", "O", "A", "N"]
    letter_widths = []
    for l in letters:
        bbox = draw.textbbox((0, 0), l, font=font)
        letter_widths.append((bbox[2] - bbox[0], bbox[3] - bbox[1], bbox))
        
    spacing = int(size * 0.04)
    total_w = sum(w for w, h, b in letter_widths) + spacing * (len(letters) - 1)
    start_x = (size - total_w) // 2
    base_y = int(size * 0.44)
    
    # Text glow layer
    text_glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_t_draw = ImageDraw.Draw(text_glow)
    
    curr_x = start_x
    for i, l in enumerate(letters):
        w, h, bbox = letter_widths[i]
        glow_t_draw.text((curr_x - bbox[0], base_y - bbox[1]), l, font=font, fill=(255, 255, 255, 200))
        curr_x += w + spacing
        
    text_glow = text_glow.filter(ImageFilter.GaussianBlur(radius=max(2, int(size * 0.025))))
    img = Image.alpha_composite(img, text_glow)
    draw = ImageDraw.Draw(img)
    
    # Draw Crisp Platinum White Text
    curr_x = start_x
    for i, l in enumerate(letters):
        w, h, bbox = letter_widths[i]
        y_pos = base_y - bbox[1]
        x_pos = curr_x - bbox[0]
        
        # Soft drop shadow
        draw.text((x_pos, y_pos + max(1, int(size*0.015))), l, font=font, fill=(0, 0, 0, 200))
        # Main pure white
        draw.text((x_pos, y_pos), l, font=font, fill=(255, 255, 255, 255))
        
        # Custom Luxury Flourishes on 'R' and 'A':
        if l == "R":
            # Delicate diamond star at the top corner of R
            star_cx = x_pos + int(w * 0.22)
            star_cy = y_pos + int(h * 0.08)
            star_r = max(2, int(size * 0.012))
            draw.polygon([
                (star_cx, star_cy - star_r),
                (star_cx + int(star_r*0.4), star_cy),
                (star_cx, star_cy + star_r),
                (star_cx - int(star_r*0.4), star_cy)
            ], fill=(255, 255, 255, 255))
            
        elif l == "A":
            # Diamond crossbar accent on 'A'
            star_cx = x_pos + int(w * 0.5)
            star_cy = y_pos + int(h * 0.58)
            star_r = max(2, int(size * 0.012))
            draw.polygon([
                (star_cx, star_cy - star_r),
                (star_cx + int(star_r*0.4), star_cy),
                (star_cx, star_cy + star_r),
                (star_cx - int(star_r*0.4), star_cy)
            ], fill=(255, 255, 255, 255))
            
        curr_x += w + spacing

    # 5. Bottom Subtitle: 'ÁNGEL & ROXANA' in refined micro-typography
    sub_font_size = int(size * 0.065)
    try:
        sub_font = ImageFont.truetype("arialbd.ttf", sub_font_size)
    except:
        sub_font = ImageFont.load_default()
        
    sub_text = "ÁNGEL  &  ROXANA"
    sub_bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
    sub_w = sub_bbox[2] - sub_bbox[0]
    sub_x = (size - sub_w) // 2 - sub_bbox[0]
    sub_y = int(size * 0.72)
    
    # Subtitle with soft silver tracking
    draw.text((sub_x, sub_y), sub_text, font=sub_font, fill=(200, 205, 215, 210))
    
    # Small divider dots / accent line
    line_w = int(size * 0.18)
    line_y = int(size * 0.83)
    draw.line([(size // 2 - line_w // 2, line_y), (size // 2 + line_w // 2, line_y)], fill=(255, 255, 255, 120), width=max(1, int(size*0.005)))
    
    return img

def create_roan_badge_icon(size):
    # Pure white monochrome silhouette on transparent background for Android Notification Bar
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    font_size = int(size * 0.58)
    try:
        font = ImageFont.truetype("timesbd.ttf", font_size)
    except:
        font = ImageFont.load_default()
        
    text = "R"
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (size - w) // 2 - bbox[0]
    y = (size - h) // 2 - bbox[1]
    
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
    return img

if __name__ == "__main__":
    icon_512 = create_roan_app_icon(512)
    icon_192 = create_roan_app_icon(192)
    badge_96 = create_roan_badge_icon(96)
    
    # Save in current directory
    icon_512.save("roan_icon_512.png", "PNG")
    icon_192.save("roan_icon_192.png", "PNG")
    badge_96.save("roan_badge_96.png", "PNG")
    print("ROAN Luxury Brand Icons created successfully!")
