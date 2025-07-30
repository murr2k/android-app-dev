#!/bin/bash

# Script to prepare keystore for GitHub Actions

echo "=== Keystore Preparation for GitHub Actions ==="
echo ""
echo "This script will help you prepare your keystore for GitHub Actions."
echo ""

# Check if keystore file is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <path-to-keystore>"
    echo "Example: $0 android/linknode-release.keystore"
    exit 1
fi

KEYSTORE_PATH=$1

# Check if keystore exists
if [ ! -f "$KEYSTORE_PATH" ]; then
    echo "Error: Keystore file not found at $KEYSTORE_PATH"
    exit 1
fi

echo "Found keystore at: $KEYSTORE_PATH"
echo ""

# Get keystore info
echo "=== Keystore Information ==="
keytool -list -v -keystore "$KEYSTORE_PATH" 2>/dev/null | grep -E "Alias name:|SHA1:" | head -4

echo ""
echo "=== Encoding keystore as base64 ==="
ENCODED_KEYSTORE=$(base64 -w 0 "$KEYSTORE_PATH")

echo ""
echo "=== Instructions for GitHub ==="
echo ""
echo "1. Go to your GitHub repository: https://github.com/murr2k/android-app-dev"
echo "2. Navigate to Settings > Secrets and variables > Actions"
echo "3. Click 'New repository secret'"
echo ""
echo "4. Add the following secrets:"
echo ""
echo "   Secret name: KEYSTORE_BASE64"
echo "   Secret value: (copy the base64 string below)"
echo ""
echo "----------------------------------------"
echo "$ENCODED_KEYSTORE"
echo "----------------------------------------"
echo ""
echo "   Secret name: KEYSTORE_PASSWORD"
echo "   Secret value: [your keystore password]"
echo ""
echo "   Secret name: KEY_ALIAS"
echo "   Secret value: [your key alias, likely 'linknode']"
echo ""
echo "   Secret name: KEY_PASSWORD"
echo "   Secret value: [your key password]"
echo ""
echo "5. Save each secret"
echo ""
echo "Once done, we'll update the workflow to use these secrets."