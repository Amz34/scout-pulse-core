#!/usr/bin/env python3
"""
Generate a punchy, ultra-aesthetic fluffy cybersecurity/AI scout mascot logo.
"""
from PIL import Image, ImageDraw, ImageFilter
import math

width, height = 800, 800
img = Image.new("RGBA", (width, height), (13, 17, 23, 255))
draw = ImageDraw.Draw(img)

# Background gradient / glowing cyber grid aura
for r in range(350, 0, -5):
    alpha = int(35 * (1.0 - r / 350))
    glow_color = (99, 102, 241, alpha)  # Indigo neon glow
    draw.ellipse([400 - r, 400 - r, 400 + r, 400 + r], fill=glow_color)

# Outer cloud / fluffy body shadow & base
# We generate layered circles to create a high-definition fluffy cloud creature mascot
def draw_fluff_circle(cx, cy, radius, color):
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=color)

# Base fluffy puff layers (Cute cyber-guardian creature)
fluff_coords = [
    (400, 430, 200, (199, 210, 254, 255)),   # Body center
    (310, 450, 150, (165, 180, 252, 255)),   # Left puff
    (490, 450, 150, (165, 180, 252, 255)),   # Right puff
    (250, 410, 120, (147, 197, 253, 255)),   # Far left fluff
    (550, 410, 120, (147, 197, 253, 255)),   # Far right fluff
    (330, 310, 140, (224, 231, 255, 255)),   # Top left puff
    (470, 310, 140, (224, 231, 255, 255)),   # Top right puff
    (400, 280, 150, (243, 244, 246, 255)),   # Crown puff
    (400, 390, 190, (255, 255, 255, 255)),   # Center bright chest
]

for cx, cy, r, col in fluff_coords:
    draw_fluff_circle(cx, cy, r, col)

# Fluffy ears / sensory horns with cyber accents
draw.polygon([(260, 230), (320, 120), (370, 220)], fill=(129, 140, 248, 255))
draw.polygon([(280, 215), (320, 140), (355, 215)], fill=(244, 114, 182, 255)) # Pink ear fluff

draw.polygon([(540, 230), (480, 120), (430, 220)], fill=(129, 140, 248, 255))
draw.polygon([(520, 215), (480, 140), (445, 215)], fill=(244, 114, 182, 255))

# Cybernetic Scanner Visor / Eyes (Large glowing holographic visor)
visor_box = [290, 335, 510, 415]
draw.rounded_rectangle(visor_box, radius=40, fill=(15, 23, 42, 255), outline=(56, 189, 248, 255), width=6)

# Glowing eyes / Radar scanlines inside visor
draw.ellipse([325, 355, 375, 395], fill=(56, 189, 248, 255))
draw.ellipse([425, 355, 475, 395], fill=(56, 189, 248, 255))
draw.ellipse([345, 360, 365, 380], fill=(255, 255, 255, 255)) # reflection
draw.ellipse([445, 360, 465, 380], fill=(255, 255, 255, 255)) # reflection

# Digital blush / radar blips
draw.ellipse([270, 425, 310, 445], fill=(244, 114, 182, 180))
draw.ellipse([490, 425, 530, 445], fill=(244, 114, 182, 180))

# Cute smile / mouth
draw.arc([375, 420, 425, 450], start=10, end=170, fill=(71, 85, 105, 255), width=5)

# Antenna with pulsing radar star on crown
draw.line([(400, 210), (400, 130)], fill=(56, 189, 248, 255), width=7)
draw.ellipse([385, 115, 415, 145], fill=(234, 179, 8, 255)) # Golden radar star
draw.ellipse([392, 122, 408, 138], fill=(255, 255, 255, 255))

# Floating Tech Badges / Hologram Shields around mascot
badges = [
    (180, 520, "CA", (16, 185, 129, 255)),   # Emerald Corrective Action
    (620, 520, "REA", (239, 68, 68, 255)),   # Crimson Risk Exposure
    (400, 640, "EGM", (139, 92, 246, 255)),  # Purple Enterprise Gov
]

for bx, by, text, bg in badges:
    draw.rounded_rectangle([bx - 60, by - 26, bx + 60, by + 26], radius=15, fill=bg)
    # Simple label dots
    draw.ellipse([bx - 45, by - 5, bx - 35, by + 5], fill=(255, 255, 255, 255))

# Outer cyber-ring orbital path
draw.arc([120, 160, 680, 680], start=-30, end=210, fill=(99, 102, 241, 140), width=4)

# Save
logo_path = "/home/ubuntu/agy-argon-home/.gemini/antigravity-cli/scratch/scout-pulse-core/assets/mascot_logo.png"
img.save(logo_path, "PNG")
print("Fluffy logo generated successfully at:", logo_path)
