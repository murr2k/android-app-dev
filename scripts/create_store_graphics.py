#!/usr/bin/env python3

import os
from PIL import Image, ImageDraw, ImageFont
import subprocess

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
output_dir = os.path.join(project_root, "store_graphics")
logo_path = os.path.join(project_root, "linknode_logo.jpg")

# Create output directory
os.makedirs(output_dir, exist_ok=True)

def create_feature_graphic():
    """Create 1024x500 feature graphic for Play Store"""
    print("Creating feature graphic...")
    
    # Create gradient background
    img = Image.new('RGB', (1024, 500), '#6366f1')
    draw = ImageDraw.Draw(img)
    
    # Add gradient effect
    for y in range(500):
        # Purple to blue gradient
        r = int(99 + (147 - 99) * (y / 500))
        g = int(102 + (51 - 102) * (y / 500))
        b = int(241 + (217 - 241) * (y / 500))
        draw.rectangle([(0, y), (1024, y+1)], fill=(r, g, b))
    
    # Load and place logo
    logo = Image.open(logo_path).convert("RGBA")
    logo_size = 200
    logo_aspect = logo.width / logo.height
    if logo_aspect > 1:
        new_width = logo_size
        new_height = int(logo_size / logo_aspect)
    else:
        new_height = logo_size
        new_width = int(logo_size * logo_aspect)
    
    logo = logo.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Create white circle background for logo
    circle_img = Image.new('RGBA', (logo_size + 20, logo_size + 20), (0, 0, 0, 0))
    circle_draw = ImageDraw.Draw(circle_img)
    circle_draw.ellipse([0, 0, logo_size + 20, logo_size + 20], fill=(255, 255, 255, 255))
    
    # Paste circle and logo
    img.paste(circle_img, (100, 150), circle_img)
    logo_x = 110 + (logo_size - new_width) // 2
    logo_y = 160 + (logo_size - new_height) // 2
    img.paste(logo, (logo_x, logo_y), logo)
    
    # Add text (using default font)
    draw = ImageDraw.Draw(img)
    
    # Title
    try:
        # Try to use a better font if available
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        tagline_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        tagline_font = ImageFont.load_default()
    
    # Add text with shadow effect
    shadow_offset = 3
    
    # Title shadow
    draw.text((370, 180 + shadow_offset), "Linknode Showcase", font=title_font, fill=(0, 0, 0, 128))
    draw.text((370, 180), "Linknode Showcase", font=title_font, fill="white")
    
    # Subtitle shadow
    draw.text((370, 280 + shadow_offset), "Real-Time IoT Energy Monitoring", font=subtitle_font, fill=(0, 0, 0, 128))
    draw.text((370, 280), "Real-Time IoT Energy Monitoring", font=subtitle_font, fill="white")
    
    # Tagline shadow
    draw.text((370, 340 + shadow_offset), "Built with AI • Deployed on Fly.io", font=tagline_font, fill=(0, 0, 0, 128))
    draw.text((370, 340), "Built with AI • Deployed on Fly.io", font=tagline_font, fill="white")
    
    # Save
    img.save(os.path.join(output_dir, "feature_graphic.png"))
    print("✓ Created feature_graphic.png (1024x500)")

def create_screenshots():
    """Create phone screenshots for Play Store"""
    print("Creating screenshots...")
    
    # Phone screenshot dimensions (common sizes)
    sizes = [
        ("phone", 1080, 1920),  # Standard phone
        ("phone_small", 720, 1280),  # Smaller phone
    ]
    
    screenshots = [
        {
            "title": "Real-Time Monitoring",
            "subtitle": "Track your energy usage live",
            "bg_color": "#6366f1",
            "features": [
                "• Eagle-200 Smart Meter Integration",
                "• Live Power Consumption Data",
                "• Beautiful Animated Interface",
                "• Cloud-Native Architecture"
            ]
        },
        {
            "title": "Modern Design",
            "subtitle": "Beautiful Material UI",
            "bg_color": "#9333ea",
            "features": [
                "• Animated Particle Effects",
                "• Gradient Backgrounds",
                "• Responsive Layouts",
                "• Dark Mode Ready"
            ]
        },
        {
            "title": "Privacy First",
            "subtitle": "Your data stays yours",
            "bg_color": "#3b82f6",
            "features": [
                "• No Personal Data Collection",
                "• Transparent Privacy Policy",
                "• Secure Architecture",
                "• Open Source Compatible"
            ]
        }
    ]
    
    for size_name, width, height in sizes:
        for i, screenshot in enumerate(screenshots):
            # Create image with gradient
            img = Image.new('RGB', (width, height), screenshot["bg_color"])
            draw = ImageDraw.Draw(img)
            
            # Add gradient
            for y in range(height):
                fade = y / height
                r = int(int(screenshot["bg_color"][1:3], 16) * (1 - fade * 0.3))
                g = int(int(screenshot["bg_color"][3:5], 16) * (1 - fade * 0.3))
                b = int(int(screenshot["bg_color"][5:7], 16) * (1 - fade * 0.3))
                draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b))
            
            # Add logo at top
            logo = Image.open(logo_path).convert("RGBA")
            logo_size = width // 4
            logo_aspect = logo.width / logo.height
            if logo_aspect > 1:
                new_width = logo_size
                new_height = int(logo_size / logo_aspect)
            else:
                new_height = logo_size
                new_width = int(logo_size * logo_aspect)
            
            logo = logo.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # White circle for logo
            circle_size = logo_size + 40
            circle_img = Image.new('RGBA', (circle_size, circle_size), (0, 0, 0, 0))
            circle_draw = ImageDraw.Draw(circle_img)
            circle_draw.ellipse([0, 0, circle_size, circle_size], fill=(255, 255, 255, 255))
            
            logo_x = (width - circle_size) // 2
            logo_y = height // 6
            img.paste(circle_img, (logo_x, logo_y), circle_img)
            
            # Center logo in circle
            actual_logo_x = logo_x + (circle_size - new_width) // 2
            actual_logo_y = logo_y + (circle_size - new_height) // 2
            img.paste(logo, (actual_logo_x, actual_logo_y), logo)
            
            # Add text
            try:
                title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", width // 20)
                subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", width // 30)
                feature_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", width // 35)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                feature_font = ImageFont.load_default()
            
            # Title
            text_y = logo_y + circle_size + height // 10
            draw.text((width // 2, text_y), screenshot["title"], 
                     font=title_font, fill="white", anchor="mm")
            
            # Subtitle
            text_y += height // 15
            draw.text((width // 2, text_y), screenshot["subtitle"], 
                     font=subtitle_font, fill=(255, 255, 255, 200), anchor="mm")
            
            # Features
            text_y += height // 10
            for feature in screenshot["features"]:
                draw.text((width // 10, text_y), feature, 
                         font=feature_font, fill=(255, 255, 255, 180))
                text_y += height // 20
            
            # Add device frame hint
            frame_width = 20
            draw.rectangle([0, 0, width, frame_width], fill=(0, 0, 0, 50))
            draw.rectangle([0, height-frame_width, width, height], fill=(0, 0, 0, 50))
            draw.rectangle([0, 0, frame_width, height], fill=(0, 0, 0, 50))
            draw.rectangle([width-frame_width, 0, width, height], fill=(0, 0, 0, 50))
            
            # Save
            filename = f"screenshot_{size_name}_{i+1}.png"
            img.save(os.path.join(output_dir, filename))
            print(f"✓ Created {filename} ({width}x{height})")

def create_app_icon():
    """Create 512x512 app icon for store listing"""
    print("Creating store app icon...")
    
    # Copy the existing Play Store icon
    source_icon = os.path.join(project_root, "fastlane/metadata/android/en-US/images/icon.png")
    if os.path.exists(source_icon):
        # Just copy it
        import shutil
        shutil.copy(source_icon, os.path.join(output_dir, "app_icon_512.png"))
    else:
        # Create a new one
        icon = Image.new('RGBA', (512, 512), (255, 255, 255, 255))
        
        # Load logo
        logo = Image.open(logo_path).convert("RGBA")
        
        # Resize to fit
        logo_size = 410  # 80% of 512
        aspect = logo.width / logo.height
        if aspect > 1:
            new_width = logo_size
            new_height = int(logo_size / aspect)
        else:
            new_height = logo_size
            new_width = int(logo_size * aspect)
        
        logo = logo.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Center and paste
        x = (512 - new_width) // 2
        y = (512 - new_height) // 2
        icon.paste(logo, (x, y), logo)
        
        icon.save(os.path.join(output_dir, "app_icon_512.png"))
    
    print("✓ Created app_icon_512.png (512x512)")

def main():
    print("Creating Google Play Store graphics...")
    print(f"Output directory: {output_dir}")
    print()
    
    create_app_icon()
    create_feature_graphic()
    create_screenshots()
    
    print("\n✅ All graphics created successfully!")
    print(f"\nFiles saved to: {output_dir}/")
    print("\nUpload these to Google Play Console:")
    print("- app_icon_512.png → App icon")
    print("- feature_graphic.png → Feature graphic")  
    print("- screenshot_phone_*.png → Phone screenshots")

if __name__ == "__main__":
    main()