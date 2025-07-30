#!/usr/bin/env python3
"""
Fix/regenerate Android launcher icons
"""

from PIL import Image, ImageDraw
import os

# Base directory for Android resources
res_dir = "android/app/src/main/res"

# Icon sizes for different densities
icon_sizes = {
    "mdpi": 48,
    "hdpi": 72,
    "xhdpi": 96,
    "xxhdpi": 144,
    "xxxhdpi": 192
}

def create_launcher_icon(size):
    """Create a simple launcher icon"""
    # Create a new image with gradient background
    icon = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    
    # Draw gradient background (indigo to purple)
    for y in range(size):
        # Gradient from indigo (63, 81, 181) to purple (156, 39, 176)
        r = int(63 + (156 - 63) * y / size)
        g = int(81 + (39 - 81) * y / size)
        b = int(181 + (176 - 181) * y / size)
        draw.rectangle([(0, y), (size, y+1)], fill=(r, g, b, 255))
    
    # Draw a white "L" for Linknode
    margin = size // 6
    line_width = size // 8
    
    # Vertical line of L
    draw.rectangle([
        (margin, margin),
        (margin + line_width, size - margin - line_width)
    ], fill=(255, 255, 255, 255))
    
    # Horizontal line of L
    draw.rectangle([
        (margin, size - margin - line_width),
        (size - margin, size - margin)
    ], fill=(255, 255, 255, 255))
    
    return icon

def create_round_icon(size):
    """Create a round version of the launcher icon"""
    # Start with square icon
    square_icon = create_launcher_icon(size)
    
    # Create circular mask
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    
    # Apply mask to create round icon
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(square_icon, (0, 0))
    output.putalpha(mask)
    
    return output

def main():
    print("Fixing Android launcher icons...")
    
    # Create directories if they don't exist
    for density in icon_sizes:
        dir_path = f"{res_dir}/mipmap-{density}"
        os.makedirs(dir_path, exist_ok=True)
    
    # Generate icons for each density
    for density, size in icon_sizes.items():
        # Square icon
        icon = create_launcher_icon(size)
        icon_path = f"{res_dir}/mipmap-{density}/ic_launcher.png"
        icon.save(icon_path, "PNG", optimize=True)
        print(f"✅ Created {icon_path} ({size}x{size})")
        
        # Round icon
        round_icon = create_round_icon(size)
        round_icon_path = f"{res_dir}/mipmap-{density}/ic_launcher_round.png"
        round_icon.save(round_icon_path, "PNG", optimize=True)
        print(f"✅ Created {round_icon_path} ({size}x{size})")
    
    print("\n✅ All launcher icons fixed!")

if __name__ == "__main__":
    main()