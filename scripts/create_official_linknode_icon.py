#!/usr/bin/env python3

import os
import subprocess
from PIL import Image, ImageDraw

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
android_res_dir = os.path.join(project_root, "android", "app", "src", "main", "res")
original_logo_path = os.path.join(project_root, "linknode_logo.jpg")

# Icon sizes for different densities
icon_sizes = {
    "mdpi": 48,
    "hdpi": 72,
    "xhdpi": 96,
    "xxhdpi": 144,
    "xxxhdpi": 192
}

# Foreground size (108dp at xxxhdpi = 432px)
foreground_sizes = {
    "mdpi": 108,
    "hdpi": 162,
    "xhdpi": 216,
    "xxhdpi": 324,
    "xxxhdpi": 432
}

def create_adaptive_icon_from_official_logo():
    """Create adaptive icon layers from the official Linknode logo"""
    
    # Load the original logo
    original = Image.open(original_logo_path).convert("RGBA")
    
    # Create background layer (white)
    for density, size in foreground_sizes.items():
        background = Image.new("RGBA", (size, size), (255, 255, 255, 255))
        
        # Save background
        bg_dir = os.path.join(android_res_dir, f"mipmap-{density}")
        os.makedirs(bg_dir, exist_ok=True)
        background.save(os.path.join(bg_dir, "ic_launcher_background.png"))
    
    # Create foreground layer with the official logo
    for density, size in foreground_sizes.items():
        # Create transparent foreground
        foreground = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        
        # Calculate safe zone (66dp at xxxhdpi = 264px)
        safe_zone_ratio = 66 / 108  # 66dp safe zone in 108dp foreground
        safe_size = int(size * safe_zone_ratio)
        
        # Resize original logo to fit within safe zone
        # Preserve aspect ratio
        original_ratio = original.width / original.height
        if original_ratio > 1:
            # Wider than tall
            new_width = safe_size
            new_height = int(safe_size / original_ratio)
        else:
            # Taller than wide
            new_height = safe_size
            new_width = int(safe_size * original_ratio)
        
        # Use high-quality resampling
        resized_logo = original.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Center the logo in the foreground
        x = (size - new_width) // 2
        y = (size - new_height) // 2
        
        # Paste the logo onto the foreground
        foreground.paste(resized_logo, (x, y), resized_logo)
        
        # Save foreground
        fg_dir = os.path.join(android_res_dir, f"mipmap-{density}")
        foreground.save(os.path.join(fg_dir, "ic_launcher_foreground.png"))

def create_legacy_icons_from_official_logo():
    """Create legacy round and square icons from the official logo"""
    
    original = Image.open(original_logo_path).convert("RGBA")
    
    for density, size in icon_sizes.items():
        # Create white background
        icon_bg = Image.new("RGBA", (size, size), (255, 255, 255, 255))
        
        # Calculate logo size (80% of icon size for padding)
        logo_size = int(size * 0.8)
        
        # Resize logo preserving aspect ratio
        original_ratio = original.width / original.height
        if original_ratio > 1:
            new_width = logo_size
            new_height = int(logo_size / original_ratio)
        else:
            new_height = logo_size
            new_width = int(logo_size * original_ratio)
        
        resized_logo = original.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Center the logo
        x = (size - new_width) // 2
        y = (size - new_height) // 2
        
        # Create square icon
        square_icon = icon_bg.copy()
        square_icon.paste(resized_logo, (x, y), resized_logo)
        
        # Create round icon with mask
        round_icon = icon_bg.copy()
        round_icon.paste(resized_logo, (x, y), resized_logo)
        
        # Apply circular mask
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        
        output = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        output.paste(round_icon, (0, 0))
        output.putalpha(mask)
        
        # Save icons
        icon_dir = os.path.join(android_res_dir, f"mipmap-{density}")
        os.makedirs(icon_dir, exist_ok=True)
        
        square_icon.save(os.path.join(icon_dir, "ic_launcher.png"))
        output.save(os.path.join(icon_dir, "ic_launcher_round.png"))

def create_play_store_icon_from_official_logo():
    """Create 512x512 icon for Play Store from official logo"""
    
    original = Image.open(original_logo_path).convert("RGBA")
    
    # Create white background
    play_store_icon = Image.new("RGBA", (512, 512), (255, 255, 255, 255))
    
    # Calculate logo size (80% of icon size)
    logo_size = int(512 * 0.8)
    
    # Resize preserving aspect ratio
    original_ratio = original.width / original.height
    if original_ratio > 1:
        new_width = logo_size
        new_height = int(logo_size / original_ratio)
    else:
        new_height = logo_size
        new_width = int(logo_size * original_ratio)
    
    resized_logo = original.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Center the logo
    x = (512 - new_width) // 2
    y = (512 - new_height) // 2
    
    play_store_icon.paste(resized_logo, (x, y), resized_logo)
    
    # Save Play Store icon
    fastlane_dir = os.path.join(project_root, "fastlane", "metadata", "android", "en-US", "images")
    os.makedirs(fastlane_dir, exist_ok=True)
    play_store_icon.save(os.path.join(fastlane_dir, "icon.png"))
    
    print("✓ Created Play Store icon (512x512)")

def main():
    print("Creating Android app icons from official Linknode logo...")
    
    # Check if original logo exists
    if not os.path.exists(original_logo_path):
        print(f"Error: Original logo not found at {original_logo_path}")
        return
    
    # Create adaptive icons
    print("Creating adaptive icon layers...")
    create_adaptive_icon_from_official_logo()
    print("✓ Created adaptive icon layers")
    
    # Create legacy icons
    print("Creating legacy icons...")
    create_legacy_icons_from_official_logo()
    print("✓ Created legacy icons")
    
    # Create Play Store icon
    print("Creating Play Store icon...")
    create_play_store_icon_from_official_logo()
    
    print("\nAll icons created successfully!")
    print("\nNote: The official logo has been preserved exactly while adapting to Android's icon requirements.")
    print("The logo is centered on a white background to maintain its original appearance.")

if __name__ == "__main__":
    main()