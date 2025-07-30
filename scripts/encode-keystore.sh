#!/bin/bash

# Script to encode keystore for GitHub secrets

KEYSTORE_PATH="android/linknode-release.keystore"

if [ ! -f "$KEYSTORE_PATH" ]; then
    echo "Error: Keystore not found at $KEYSTORE_PATH"
    echo "Please run this script from the project root directory"
    exit 1
fi

echo "Encoding keystore..."
ENCODED=$(base64 -i "$KEYSTORE_PATH")

echo ""
echo "Base64 encoded keystore (copy this for RELEASE_KEYSTORE secret):"
echo "=================================================="
echo "$ENCODED"
echo "=================================================="
echo ""
echo "Keystore successfully encoded!"
echo ""
echo "Next steps:"
echo "1. Copy the encoded string above"
echo "2. Go to GitHub repository settings → Secrets → Actions"
echo "3. Create new secret named 'RELEASE_KEYSTORE'"
echo "4. Paste the encoded string as the value"
echo ""
echo "Also create these additional secrets:"
echo "- KEYSTORE_PASSWORD: linknode2024"
echo "- KEY_ALIAS: linknode"
echo "- KEY_PASSWORD: linknode2024"