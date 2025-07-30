#!/usr/bin/env python3
"""
Create Google Play Store graphics for LinkNode Demo app
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# Create output directory
output_dir = "fastlane/metadata/android/en-US/images"
os.makedirs(output_dir, exist_ok=True)

# Define colors based on the LinkNode theme
PRIMARY_COLOR = (63, 81, 181)  # Indigo
SECONDARY_COLOR = (255, 87, 34)  # Deep Orange
ACCENT_COLOR = (0, 188, 212)  # Cyan
BACKGROUND_GRADIENT_START = (25, 25, 112)  # Midnight Blue
BACKGROUND_GRADIENT_END = (138, 43, 226)  # Blue Violet

def create_gradient(width, height, start_color, end_color):
    """Create a gradient background"""
    base = Image.new('RGB', (width, height), start_color)
    top = Image.new('RGB', (width, height), end_color)
    mask = Image.new('L', (width, height))
    mask_draw = ImageDraw.Draw(mask)
    
    for y in range(height):
        mask_draw.rectangle([(0, y), (width, y)], fill=int(255 * y / height))
    
    base.paste(top, (0, 0), mask)
    return base

def create_app_icon():
    """Create 512x512 app icon"""
    size = 512
    icon = create_gradient(size, size, BACKGROUND_GRADIENT_START, BACKGROUND_GRADIENT_END)
    draw = ImageDraw.Draw(icon)
    
    # Draw connected nodes pattern
    center_x, center_y = size // 2, size // 2
    
    # Central node
    node_radius = 60
    draw.ellipse([center_x - node_radius, center_y - node_radius,
                  center_x + node_radius, center_y + node_radius],
                 fill=(255, 255, 255, 200))
    
    # Surrounding nodes
    import math
    nodes = 6
    orbit_radius = 140
    small_radius = 30
    
    for i in range(nodes):
        angle = (2 * math.pi * i) / nodes
        x = center_x + orbit_radius * math.cos(angle)
        y = center_y + orbit_radius * math.sin(angle)
        
        # Draw connection lines
        draw.line([center_x, center_y, x, y], fill=(255, 255, 255, 150), width=3)
        
        # Draw nodes
        colors = [SECONDARY_COLOR, ACCENT_COLOR, (76, 175, 80), (255, 193, 7), (233, 30, 99), (156, 39, 176)]
        draw.ellipse([x - small_radius, y - small_radius,
                      x + small_radius, y + small_radius],
                     fill=colors[i % len(colors)])
    
    # Add "LN" text in center
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    except:
        font = None
    
    if font:
        draw.text((center_x, center_y), "LN", fill=(0, 0, 0), font=font, anchor="mm")
    
    icon.save(f"{output_dir}/icon.png", "PNG")
    print(f"✅ Created app icon: {output_dir}/icon.png")

def create_feature_graphic():
    """Create 1024x500 feature graphic"""
    width, height = 1024, 500
    graphic = create_gradient(width, height, BACKGROUND_GRADIENT_START, BACKGROUND_GRADIENT_END)
    draw = ImageDraw.Draw(graphic)
    
    # Draw network pattern in background
    import random
    random.seed(42)
    nodes = []
    for _ in range(15):
        x = random.randint(50, width - 50)
        y = random.randint(50, height - 50)
        nodes.append((x, y))
    
    # Draw connections
    for i, (x1, y1) in enumerate(nodes):
        for j, (x2, y2) in enumerate(nodes[i+1:i+4]):
            draw.line([x1, y1, x2, y2], fill=(255, 255, 255, 30), width=1)
    
    # Draw nodes
    for x, y in nodes:
        draw.ellipse([x-8, y-8, x+8, y+8], fill=(255, 255, 255, 50))
    
    # Add title text
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
    except:
        font_large = None
        font_medium = None
    
    if font_large:
        # Title
        draw.text((width // 2, height // 2 - 50), "LinkNode Demo", 
                  fill=(255, 255, 255), font=font_large, anchor="mm")
        
        if font_medium:
            # Subtitle
            draw.text((width // 2, height // 2 + 30), 
                      "Transform Any Device Into a Smart IoT Node", 
                      fill=(255, 255, 255, 200), font=font_medium, anchor="mm")
    
    graphic.save(f"{output_dir}/featureGraphic.png", "PNG")
    print(f"✅ Created feature graphic: {output_dir}/featureGraphic.png")

def create_screenshots():
    """Create sample screenshots"""
    phone_dir = f"{output_dir}/phoneScreenshots"
    os.makedirs(phone_dir, exist_ok=True)
    
    width, height = 1080, 1920
    
    # Screenshot 1: Main dashboard
    screen1 = create_gradient(width, height, (30, 30, 30), (60, 60, 60))
    draw = ImageDraw.Draw(screen1)
    
    # Status bar
    draw.rectangle([0, 0, width, 80], fill=(20, 20, 20))
    
    # App header
    draw.rectangle([0, 80, width, 200], fill=PRIMARY_COLOR)
    
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
    except:
        font_title = None
        font_body = None
    
    if font_title:
        draw.text((width // 2, 140), "LinkNode Demo", fill=(255, 255, 255), font=font_title, anchor="mm")
    
    # Feature cards
    card_y = 300
    features = [
        ("🔐", "Enterprise Security", "End-to-end encryption"),
        ("📡", "Universal Connectivity", "WiFi, Bluetooth, NFC"),
        ("📊", "Advanced Analytics", "Real-time monitoring")
    ]
    
    for emoji, title, desc in features:
        # Card background
        draw.rounded_rectangle([50, card_y, width - 50, card_y + 200], 
                               radius=20, fill=(255, 255, 255, 20))
        
        if font_body:
            draw.text((150, card_y + 60), title, fill=(255, 255, 255), font=font_body)
            draw.text((150, card_y + 110), desc, fill=(200, 200, 200), font=font_body)
        
        card_y += 250
    
    screen1.save(f"{phone_dir}/1_en-US.png", "PNG")
    print(f"✅ Created screenshot 1: {phone_dir}/1_en-US.png")
    
    # Screenshot 2: Connectivity view
    screen2 = create_gradient(width, height, (30, 30, 30), (60, 60, 60))
    draw = ImageDraw.Draw(screen2)
    
    # Header
    draw.rectangle([0, 0, width, 80], fill=(20, 20, 20))
    draw.rectangle([0, 80, width, 200], fill=SECONDARY_COLOR)
    
    if font_title:
        draw.text((width // 2, 140), "Device Connectivity", fill=(255, 255, 255), font=font_title, anchor="mm")
    
    # Network visualization
    center_x, center_y = width // 2, height // 2
    
    # Central device
    draw.ellipse([center_x - 100, center_y - 100, center_x + 100, center_y + 100],
                 fill=(255, 255, 255))
    
    # Connected devices
    import math
    for i in range(6):
        angle = (2 * math.pi * i) / 6
        x = center_x + 250 * math.cos(angle)
        y = center_y + 250 * math.sin(angle)
        
        # Connection line
        draw.line([center_x, center_y, x, y], fill=ACCENT_COLOR, width=4)
        
        # Device node
        draw.ellipse([x - 60, y - 60, x + 60, y + 60], fill=ACCENT_COLOR)
    
    screen2.save(f"{phone_dir}/2_en-US.png", "PNG")
    print(f"✅ Created screenshot 2: {phone_dir}/2_en-US.png")

if __name__ == "__main__":
    print("Creating Google Play Store graphics...")
    create_app_icon()
    create_feature_graphic()
    create_screenshots()
    print("\n✅ All graphics created successfully!")
    print(f"📁 Location: {output_dir}/")