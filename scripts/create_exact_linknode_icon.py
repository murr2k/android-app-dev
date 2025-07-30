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

def create_adaptive_icon_direct():
    """Create adaptive icon layers using the original logo directly"""
    
    # Load the original logo without any interpretation
    original = Image.open(original_logo_path)
    
    # Get original dimensions
    orig_width, orig_height = original.size
    print(f"Original logo dimensions: {orig_width}x{orig_height}")
    
    # Convert to RGBA for transparency support
    if original.mode != 'RGBA':
        # Create a new RGBA image with white background
        rgba_original = Image.new('RGBA', original.size, (255, 255, 255, 255))
        # Paste the original image
        rgba_original.paste(original, (0, 0))
        original = rgba_original
    
    # Create background layer (white)
    for density, size in foreground_sizes.items():
        background = Image.new("RGBA", (size, size), (255, 255, 255, 255))
        
        # Save background
        bg_dir = os.path.join(android_res_dir, f"mipmap-{density}")
        os.makedirs(bg_dir, exist_ok=True)
        background.save(os.path.join(bg_dir, "ic_launcher_background.png"))
    
    # Create foreground layer - directly use the original logo
    for density, size in foreground_sizes.items():
        # Create transparent foreground
        foreground = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        
        # Calculate safe zone (72dp of 108dp total)
        # This gives us more room than the strict 66dp safe zone
        safe_zone_ratio = 72 / 108
        safe_size = int(size * safe_zone_ratio)
        
        # Calculate scaling to fit the logo in safe zone
        scale_x = safe_size / orig_width
        scale_y = safe_size / orig_height
        scale = min(scale_x, scale_y)  # Use smaller scale to fit both dimensions
        
        new_width = int(orig_width * scale)
        new_height = int(orig_height * scale)
        
        # Resize using high-quality Lanczos resampling
        resized_logo = original.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Center the logo in the foreground
        x = (size - new_width) // 2
        y = (size - new_height) // 2
        
        # Paste the logo onto the foreground
        foreground.paste(resized_logo, (x, y), resized_logo)
        
        # Save foreground
        fg_dir = os.path.join(android_res_dir, f"mipmap-{density}")
        foreground.save(os.path.join(fg_dir, "ic_launcher_foreground.png"))

def create_legacy_icons_direct():
    """Create legacy icons using the original logo directly"""
    
    original = Image.open(original_logo_path)
    
    # Convert to RGBA
    if original.mode != 'RGBA':
        rgba_original = Image.new('RGBA', original.size, (255, 255, 255, 255))
        rgba_original.paste(original, (0, 0))
        original = rgba_original
    
    orig_width, orig_height = original.size
    
    for density, size in icon_sizes.items():
        # Create white background
        icon_bg = Image.new("RGBA", (size, size), (255, 255, 255, 255))
        
        # Calculate scaling (85% of icon size for some padding)
        max_logo_size = int(size * 0.85)
        
        scale_x = max_logo_size / orig_width
        scale_y = max_logo_size / orig_height
        scale = min(scale_x, scale_y)
        
        new_width = int(orig_width * scale)
        new_height = int(orig_height * scale)
        
        # Resize the logo
        resized_logo = original.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Center the logo
        x = (size - new_width) // 2
        y = (size - new_height) // 2
        
        # Create square icon
        square_icon = icon_bg.copy()
        square_icon.paste(resized_logo, (x, y), resized_logo)
        
        # Create round icon
        round_icon_bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        
        # Create circular mask
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        
        # Apply white background circle
        round_base = Image.new("RGBA", (size, size), (255, 255, 255, 255))
        round_base.putalpha(mask)
        
        # Composite the logo on top
        round_icon_bg.paste(round_base, (0, 0), round_base)
        round_icon_bg.paste(resized_logo, (x, y), resized_logo)
        
        # Save icons
        icon_dir = os.path.join(android_res_dir, f"mipmap-{density}")
        os.makedirs(icon_dir, exist_ok=True)
        
        square_icon.save(os.path.join(icon_dir, "ic_launcher.png"))
        round_icon_bg.save(os.path.join(icon_dir, "ic_launcher_round.png"))

def create_play_store_icon_direct():
    """Create Play Store icon using the original logo directly"""
    
    original = Image.open(original_logo_path)
    
    # Convert to RGBA
    if original.mode != 'RGBA':
        rgba_original = Image.new('RGBA', original.size, (255, 255, 255, 255))
        rgba_original.paste(original, (0, 0))
        original = rgba_original
    
    orig_width, orig_height = original.size
    
    # Create white background
    play_store_icon = Image.new("RGBA", (512, 512), (255, 255, 255, 255))
    
    # Calculate scaling (85% of 512px)
    max_size = int(512 * 0.85)
    
    scale_x = max_size / orig_width
    scale_y = max_size / orig_height
    scale = min(scale_x, scale_y)
    
    new_width = int(orig_width * scale)
    new_height = int(orig_height * scale)
    
    # Resize the logo
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

def verify_imagemagick():
    """Check if ImageMagick is available for direct conversion"""
    try:
        result = subprocess.run(['convert', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("ImageMagick is available")
            return True
    except:
        pass
    return False

def create_icons_with_imagemagick():
    """Alternative method using ImageMagick for exact reproduction"""
    if not verify_imagemagick():
        print("ImageMagick not found, using PIL method")
        return False
    
    print("Using ImageMagick for exact logo reproduction...")
    
    # Create Play Store icon with ImageMagick
    cmd = [
        'convert', original_logo_path,
        '-resize', '435x435',  # 85% of 512
        '-gravity', 'center',
        '-background', 'white',
        '-extent', '512x512',
        os.path.join(project_root, "fastlane", "metadata", "android", "en-US", "images", "icon.png")
    ]
    subprocess.run(cmd)
    
    # Create app icons
    for density, size in icon_sizes.items():
        icon_dir = os.path.join(android_res_dir, f"mipmap-{density}")
        os.makedirs(icon_dir, exist_ok=True)
        
        # Calculate logo size
        logo_size = int(size * 0.85)
        
        # Square icon
        cmd = [
            'convert', original_logo_path,
            '-resize', f'{logo_size}x{logo_size}',
            '-gravity', 'center',
            '-background', 'white',
            '-extent', f'{size}x{size}',
            os.path.join(icon_dir, "ic_launcher.png")
        ]
        subprocess.run(cmd)
        
        # Round icon
        cmd = [
            'convert', original_logo_path,
            '-resize', f'{logo_size}x{logo_size}',
            '-gravity', 'center',
            '-background', 'white',
            '-extent', f'{size}x{size}',
            '(',
                '+clone',
                '-alpha', 'extract',
                '-draw', f'fill black polygon 0,0 0,{size} {size},{size} {size},0',
                '-draw', f'fill white circle {size//2},{size//2} {size//2},0',
            ')',
            '-alpha', 'off',
            '-compose', 'CopyOpacity',
            '-composite',
            os.path.join(icon_dir, "ic_launcher_round.png")
        ]
        subprocess.run(cmd)
    
    return True

def main():
    print("Creating Android app icons using exact copy of official Linknode logo...")
    
    # Check if original logo exists
    if not os.path.exists(original_logo_path):
        print(f"Error: Original logo not found at {original_logo_path}")
        return
    
    # Try ImageMagick first for most accurate reproduction
    if create_icons_with_imagemagick():
        print("\nAll icons created with ImageMagick!")
    else:
        # Fall back to PIL
        print("Using PIL for icon generation...")
        
        # Create adaptive icons
        print("Creating adaptive icon layers...")
        create_adaptive_icon_direct()
        print("✓ Created adaptive icon layers")
        
        # Create legacy icons
        print("Creating legacy icons...")
        create_legacy_icons_direct()
        print("✓ Created legacy icons")
        
        # Create Play Store icon
        print("Creating Play Store icon...")
        create_play_store_icon_direct()
    
    print("\nAll icons created successfully!")
    print("The original logo has been used directly without any interpretation or modification.")

if __name__ == "__main__":
    main()