#!/bin/bash

# Generate simple launcher icons using ImageMagick (if available) or create placeholders

ANDROID_DIR="../android/app/src/main/res"

# Create directories if they don't exist
mkdir -p "$ANDROID_DIR/mipmap-mdpi"
mkdir -p "$ANDROID_DIR/mipmap-hdpi"
mkdir -p "$ANDROID_DIR/mipmap-xhdpi"
mkdir -p "$ANDROID_DIR/mipmap-xxhdpi"
mkdir -p "$ANDROID_DIR/mipmap-xxxhdpi"

# Function to create a simple icon
create_icon() {
    local size=$1
    local output=$2
    
    # Try to use ImageMagick if available
    if command -v convert &> /dev/null; then
        convert -size ${size}x${size} \
            -background '#2196F3' \
            -fill white \
            -gravity center \
            -pointsize $((size/3)) \
            -annotate +0+0 'L' \
            "$output"
    else
        # Create a minimal PNG file (1x1 blue pixel)
        printf '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x00\x05\x00\x01\x0d\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82' > "$output"
    fi
}

# Generate icons for each density
create_icon 48 "$ANDROID_DIR/mipmap-mdpi/ic_launcher.png"
create_icon 72 "$ANDROID_DIR/mipmap-hdpi/ic_launcher.png"
create_icon 96 "$ANDROID_DIR/mipmap-xhdpi/ic_launcher.png"
create_icon 144 "$ANDROID_DIR/mipmap-xxhdpi/ic_launcher.png"
create_icon 192 "$ANDROID_DIR/mipmap-xxxhdpi/ic_launcher.png"

# Copy for round icons
cp "$ANDROID_DIR/mipmap-mdpi/ic_launcher.png" "$ANDROID_DIR/mipmap-mdpi/ic_launcher_round.png"
cp "$ANDROID_DIR/mipmap-hdpi/ic_launcher.png" "$ANDROID_DIR/mipmap-hdpi/ic_launcher_round.png"
cp "$ANDROID_DIR/mipmap-xhdpi/ic_launcher.png" "$ANDROID_DIR/mipmap-xhdpi/ic_launcher_round.png"
cp "$ANDROID_DIR/mipmap-xxhdpi/ic_launcher.png" "$ANDROID_DIR/mipmap-xxhdpi/ic_launcher_round.png"
cp "$ANDROID_DIR/mipmap-xxxhdpi/ic_launcher.png" "$ANDROID_DIR/mipmap-xxxhdpi/ic_launcher_round.png"

echo "Icons generated successfully!"