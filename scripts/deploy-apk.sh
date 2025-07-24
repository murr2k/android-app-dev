#!/bin/bash

# Script to download APK from Codemagic and deploy to Firebase Hosting

API_TOKEN="8u2x8z907-AgIZ114Ofpyea_sSKWZHC2-tBIxRjBn_E"
APP_ID="6882243327296f27a20aeaea"

echo "Fetching latest build info..."

# Get the latest successful build
LATEST_BUILD=$(curl -s -H "x-auth-token: $API_TOKEN" \
    "https://api.codemagic.io/builds?appId=$APP_ID&status=finished&limit=1" | \
    jq -r '.builds[0]')

if [ "$LATEST_BUILD" = "null" ]; then
    echo "No successful builds found"
    exit 1
fi

BUILD_ID=$(echo "$LATEST_BUILD" | jq -r '._id')
echo "Latest build ID: $BUILD_ID"

# Get artifacts
echo "Fetching artifacts..."
ARTIFACTS=$(curl -s -H "x-auth-token: $API_TOKEN" \
    "https://api.codemagic.io/builds/$BUILD_ID/artifacts")

# Find the debug APK
APK_URL=$(echo "$ARTIFACTS" | jq -r '.[] | select(.name | contains("app-debug.apk")) | .url' | head -1)

if [ -z "$APK_URL" ]; then
    echo "No debug APK found in artifacts"
    exit 1
fi

echo "Downloading APK..."
curl -L -H "x-auth-token: $API_TOKEN" "$APK_URL" -o ../public/app-debug.apk

if [ -f "../public/app-debug.apk" ]; then
    echo "APK downloaded successfully!"
    echo "File size: $(ls -lh ../public/app-debug.apk | awk '{print $5}')"
    
    # Commit and push to trigger Firebase deployment
    cd ..
    git add public/app-debug.apk
    git commit -m "Add APK from build $BUILD_ID for download"
    git push origin main
    
    echo "APK deployed! It will be available at:"
    echo "https://android-swarm-dev-1-4d7c7.firebaseapp.com/app-debug.apk"
else
    echo "Failed to download APK"
    exit 1
fi