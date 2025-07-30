#!/usr/bin/env python3
"""
Create proper Linknode app icon based on the official logo
"""

from PIL import Image, ImageDraw, ImageFilter
import os
import math

# Create output directories
res_dir = "android/app/src/main/res"
os.makedirs(f"{res_dir}/drawable", exist_ok=True)
os.makedirs(f"{res_dir}/mipmap-anydpi-v26", exist_ok=True)

# Linknode brand colors from logo
COLORS = {
    'central_blue': (63, 81, 181),      # Main node
    'gradient_end': (100, 120, 200),    # Lighter blue for gradient
    'green': (76, 175, 80),             # Green node
    'pink': (233, 30, 99),              # Pink node
    'orange': (255, 152, 0),            # Orange node
    'background': (245, 245, 250),      # Light background
    'connection': (60, 60, 60),         # Connection lines
}

def create_gradient_circle(size, color1, color2):
    """Create a circular gradient"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center = size // 2
    for i in range(size//2, 0, -1):
        # Interpolate between colors
        ratio = i / (size // 2)
        r = int(color1[0] * ratio + color2[0] * (1 - ratio))
        g = int(color1[1] * ratio + color2[1] * (1 - ratio))
        b = int(color1[2] * ratio + color2[2] * (1 - ratio))
        
        draw.ellipse([center-i, center-i, center+i, center+i], fill=(r, g, b))
    
    return img

def create_ic_launcher_foreground():
    """Create the foreground layer with Linknode logo elements"""
    size = 432  # 108dp * 4 for high quality
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center_x, center_y = size // 2, size // 2
    
    # Scale factors for adaptive icon (content in center 72dp of 108dp)
    safe_zone = 0.66  # 72/108
    
    # Central node (larger, with gradient)
    central_radius = int(size * 0.15 * safe_zone)
    gradient_circle = create_gradient_circle(
        central_radius * 2, 
        COLORS['central_blue'], 
        COLORS['gradient_end']
    )
    img.paste(gradient_circle, 
              (center_x - central_radius, center_y - central_radius),
              gradient_circle)
    
    # Orbital nodes
    orbit_radius = int(size * 0.28 * safe_zone)
    node_radius = int(size * 0.08 * safe_zone)
    
    nodes = [
        {'angle': -60, 'color': COLORS['pink']},    # Top right
        {'angle': 180, 'color': COLORS['green']},   # Left
        {'angle': 60, 'color': COLORS['orange']},   # Bottom right
    ]
    
    # Draw connections first (behind nodes)
    for node in nodes:
        angle_rad = math.radians(node['angle'])
        x = center_x + int(orbit_radius * math.cos(angle_rad))
        y = center_y + int(orbit_radius * math.sin(angle_rad))
        
        # Draw connection line
        draw.line(
            [center_x, center_y, x, y],
            fill=COLORS['connection'],
            width=max(3, int(size * 0.01))
        )
    
    # Draw orbital nodes
    for node in nodes:
        angle_rad = math.radians(node['angle'])
        x = center_x + int(orbit_radius * math.cos(angle_rad))
        y = center_y + int(orbit_radius * math.sin(angle_rad))
        
        # Node shadow
        shadow_offset = max(2, int(size * 0.005))
        draw.ellipse(
            [x - node_radius + shadow_offset, 
             y - node_radius + shadow_offset,
             x + node_radius + shadow_offset, 
             y + node_radius + shadow_offset],
            fill=(0, 0, 0, 50)
        )
        
        # Node
        draw.ellipse(
            [x - node_radius, y - node_radius,
             x + node_radius, y + node_radius],
            fill=node['color']
        )
    
    # Save as PNG
    img.save(f"{res_dir}/drawable/ic_launcher_foreground.png", "PNG")
    print(f"✅ Created {res_dir}/drawable/ic_launcher_foreground.png")
    return img

def create_ic_launcher_background():
    """Create the background layer"""
    size = 432  # 108dp * 4
    img = Image.new('RGBA', (size, size), COLORS['background'])
    
    # Add subtle gradient
    draw = ImageDraw.Draw(img)
    for y in range(size):
        # Very subtle gradient from top to bottom
        brightness = 245 + int(10 * (y / size))
        draw.line([(0, y), (size, y)], fill=(brightness, brightness, brightness + 5))
    
    img.save(f"{res_dir}/drawable/ic_launcher_background.png", "PNG")
    print(f"✅ Created {res_dir}/drawable/ic_launcher_background.png")
    return img

def create_legacy_icons():
    """Create traditional square/round icons for older Android versions"""
    # Combine foreground and background
    background = create_ic_launcher_background()
    foreground = create_ic_launcher_foreground()
    
    sizes = {
        'mdpi': 48,
        'hdpi': 72,
        'xhdpi': 96,
        'xxhdpi': 144,
        'xxxhdpi': 192
    }
    
    for density, size in sizes.items():
        # Create directory
        os.makedirs(f"{res_dir}/mipmap-{density}", exist_ok=True)
        
        # Resize and combine layers
        bg_resized = background.resize((size, size), Image.Resampling.LANCZOS)
        fg_resized = foreground.resize((size, size), Image.Resampling.LANCZOS)
        
        # Square icon
        square_icon = bg_resized.copy()
        square_icon.paste(fg_resized, (0, 0), fg_resized)
        square_icon.save(f"{res_dir}/mipmap-{density}/ic_launcher.png", "PNG")
        
        # Round icon
        round_icon = square_icon.copy()
        
        # Create circular mask
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        
        # Apply mask
        output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        output.paste(round_icon, (0, 0))
        output.putalpha(mask)
        
        output.save(f"{res_dir}/mipmap-{density}/ic_launcher_round.png", "PNG")
        print(f"✅ Created icons for mipmap-{density}")

def create_adaptive_icon_xml():
    """Create XML files for adaptive icons"""
    # ic_launcher.xml
    ic_launcher_xml = """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
</adaptive-icon>"""
    
    with open(f"{res_dir}/mipmap-anydpi-v26/ic_launcher.xml", "w") as f:
        f.write(ic_launcher_xml)
    
    # ic_launcher_round.xml (same content)
    with open(f"{res_dir}/mipmap-anydpi-v26/ic_launcher_round.xml", "w") as f:
        f.write(ic_launcher_xml)
    
    print(f"✅ Created adaptive icon XML files")

def create_play_store_icon():
    """Create 512x512 icon for Play Store"""
    # Combine layers at high resolution
    background = create_ic_launcher_background()
    foreground = create_ic_launcher_foreground()
    
    # Create 512x512 version
    play_store_size = 512
    bg_512 = background.resize((play_store_size, play_store_size), Image.Resampling.LANCZOS)
    fg_512 = foreground.resize((play_store_size, play_store_size), Image.Resampling.LANCZOS)
    
    play_store_icon = bg_512.copy()
    play_store_icon.paste(fg_512, (0, 0), fg_512)
    
    # Save in multiple locations
    play_store_icon.save("fastlane/metadata/android/en-US/images/icon.png", "PNG")
    play_store_icon.save(f"{res_dir}/drawable/ic_launcher_512.png", "PNG")
    
    print(f"✅ Created Play Store icon (512x512)")

def main():
    print("🎨 Creating Linknode app icons...")
    
    # Create adaptive icon components
    create_ic_launcher_background()
    create_ic_launcher_foreground()
    
    # Create legacy icons
    create_legacy_icons()
    
    # Create adaptive icon XML
    create_adaptive_icon_xml()
    
    # Create Play Store icon
    create_play_store_icon()
    
    print("\n✅ All Linknode icons created successfully!")
    print("\n📱 Icon features:")
    print("- Adaptive icon support for Android 8.0+")
    print("- Legacy icons for older versions")
    print("- Based on official Linknode logo")
    print("- Follows Material Design guidelines")
    print("- Play Store icon ready")

if __name__ == "__main__":
    main()