#!/usr/bin/env python3
"""
Create a visual workflow diagram for Linknode's development pipeline
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Create output directory
output_dir = "docs/images"
os.makedirs(output_dir, exist_ok=True)

# Define colors
COLORS = {
    'bg': (245, 245, 250),
    'primary': (63, 81, 181),      # Indigo
    'secondary': (255, 87, 34),     # Deep Orange
    'accent': (0, 188, 212),        # Cyan
    'success': (76, 175, 80),       # Green
    'text': (33, 33, 33),
    'text_light': (117, 117, 117),
    'box_bg': (255, 255, 255),
    'ai_blue': (33, 150, 243),      # AI Assistant blue
}

def create_workflow_diagram():
    """Create the main workflow diagram"""
    width, height = 1200, 800
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    # Try to load font
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font_large = None
        font_medium = None
        font_small = None
    
    # Title
    title = "Linknode Demo - Development Pipeline"
    if font_large:
        draw.text((width//2, 30), title, fill=COLORS['primary'], font=font_large, anchor="mm")
    
    # Draw workflow stages
    stages = [
        {
            'title': '1. Development',
            'color': COLORS['primary'],
            'items': ['Kotlin + Android Studio', 'AI-Powered Coding', 'Git Version Control'],
            'x': 150, 'y': 120
        },
        {
            'title': '2. CI/CD Pipeline',
            'color': COLORS['secondary'],
            'items': ['GitHub Actions', 'Automated Builds', 'Code Signing'],
            'x': 450, 'y': 120
        },
        {
            'title': '3. Distribution',
            'color': COLORS['success'],
            'items': ['Google Play Console', 'Internal Testing', 'Production Release'],
            'x': 750, 'y': 120
        },
        {
            'title': '4. Monitoring',
            'color': COLORS['accent'],
            'items': ['Analytics', 'Crash Reports', 'User Feedback'],
            'x': 1050, 'y': 120
        }
    ]
    
    # Draw stage boxes
    for i, stage in enumerate(stages):
        # Box
        box_width, box_height = 200, 200
        x, y = stage['x'] - box_width//2, stage['y']
        
        # Shadow
        draw.rounded_rectangle([x+3, y+3, x+box_width+3, y+box_height+3], 
                               radius=10, fill=(200, 200, 200))
        
        # Main box
        draw.rounded_rectangle([x, y, x+box_width, y+box_height], 
                               radius=10, fill=COLORS['box_bg'], outline=stage['color'], width=3)
        
        # Title
        if font_medium:
            draw.text((stage['x'], y+25), stage['title'], 
                      fill=stage['color'], font=font_medium, anchor="mm")
        
        # Items
        item_y = y + 60
        for item in stage['items']:
            if font_small:
                draw.text((stage['x'], item_y), item, 
                          fill=COLORS['text'], font=font_small, anchor="mm")
            item_y += 30
        
        # Draw arrows between stages
        if i < len(stages) - 1:
            arrow_start = x + box_width + 10
            arrow_end = stages[i+1]['x'] - box_width//2 - 10
            arrow_y = y + box_height // 2
            
            # Arrow line
            draw.line([arrow_start, arrow_y, arrow_end, arrow_y], 
                      fill=COLORS['text_light'], width=2)
            
            # Arrow head
            draw.polygon([(arrow_end, arrow_y), 
                          (arrow_end-10, arrow_y-5), 
                          (arrow_end-10, arrow_y+5)], 
                         fill=COLORS['text_light'])
    
    # Add technology badges at bottom
    tech_y = 400
    technologies = [
        ('Kotlin', COLORS['primary']),
        ('GitHub Actions', COLORS['secondary']),
        ('Google Play', COLORS['success']),
        ('Material Design 3', COLORS['accent']),
        ('AI-Assisted', COLORS['ai_blue'])
    ]
    
    tech_x = 200
    for tech, color in technologies:
        # Badge background
        badge_width = 140
        draw.rounded_rectangle([tech_x, tech_y, tech_x+badge_width, tech_y+40], 
                               radius=20, fill=color)
        
        # Badge text
        if font_small:
            draw.text((tech_x+badge_width//2, tech_y+20), tech, 
                      fill=(255, 255, 255), font=font_small, anchor="mm")
        
        tech_x += 160
    
    # Add metrics section
    metrics_y = 500
    if font_medium:
        draw.text((width//2, metrics_y), "Key Metrics", 
                  fill=COLORS['primary'], font=font_medium, anchor="mm")
    
    metrics = [
        "⚡ 5 min build time",
        "🚀 10 min to production",
        "📱 18,000+ supported devices",
        "🔒 Enterprise-grade security"
    ]
    
    metric_x = 250
    for metric in metrics:
        if font_small:
            draw.text((metric_x, metrics_y + 40), metric, 
                      fill=COLORS['text'], font=font_small, anchor="mm")
        metric_x += 230
    
    # Add footer
    if font_small:
        draw.text((width//2, height-40), 
                  "Built with modern DevOps practices | linknode.com", 
                  fill=COLORS['text_light'], font=font_small, anchor="mm")
    
    # Save the diagram
    img.save(f"{output_dir}/workflow_diagram.png", "PNG", optimize=True)
    print(f"✅ Created workflow diagram: {output_dir}/workflow_diagram.png")

def create_tech_stack_infographic():
    """Create a tech stack infographic"""
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), COLORS['bg'])
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        font_section = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font_item = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        font_title = None
        font_section = None
        font_item = None
    
    # Title
    if font_title:
        draw.text((width//2, 40), "Tech Stack", fill=COLORS['primary'], font=font_title, anchor="mm")
    
    # Stack sections
    sections = [
        {
            'title': 'Frontend',
            'color': COLORS['primary'],
            'items': ['Kotlin', 'Material Design 3', 'Android View System', 'Gradle Build'],
            'y': 120
        },
        {
            'title': 'Backend/Cloud',
            'color': COLORS['secondary'],
            'items': ['GitHub Actions', 'Google Play API', 'Firebase (Optional)', 'Cloud Storage'],
            'y': 320
        },
        {
            'title': 'DevOps',
            'color': COLORS['success'],
            'items': ['Git/GitHub', 'CI/CD Pipeline', 'Automated Testing', 'Code Signing'],
            'y': 520
        },
        {
            'title': 'Monitoring',
            'color': COLORS['accent'],
            'items': ['Play Console', 'Crash Analytics', 'Performance Metrics', 'User Reviews'],
            'y': 720
        }
    ]
    
    for section in sections:
        # Section header
        header_height = 50
        draw.rectangle([50, section['y'], width-50, section['y']+header_height], 
                       fill=section['color'])
        
        if font_section:
            draw.text((width//2, section['y']+header_height//2), section['title'], 
                      fill=(255, 255, 255), font=font_section, anchor="mm")
        
        # Items
        item_y = section['y'] + header_height + 20
        for item in section['items']:
            # Bullet point
            draw.ellipse([70, item_y-5, 80, item_y+5], fill=section['color'])
            
            if font_item:
                draw.text((100, item_y), item, fill=COLORS['text'], font=font_item, anchor="lm")
            
            item_y += 35
    
    # Footer
    if font_item:
        draw.text((width//2, height-30), "linknode.com", 
                  fill=COLORS['primary'], font=font_item, anchor="mm")
    
    img.save(f"{output_dir}/tech_stack.png", "PNG", optimize=True)
    print(f"✅ Created tech stack infographic: {output_dir}/tech_stack.png")

if __name__ == "__main__":
    print("Creating workflow visualizations...")
    create_workflow_diagram()
    create_tech_stack_infographic()
    print("\n✅ All visualizations created successfully!")
    print(f"📁 Location: {output_dir}/")