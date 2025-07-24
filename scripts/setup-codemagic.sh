#!/bin/bash

# Script to add android-app-dev repository to Codemagic

API_TOKEN="8u2x8z907-AgIZ114Ofpyea_sSKWZHC2-tBIxRjBn_E"
API_BASE="https://api.codemagic.io"

echo "Adding android-app-dev to Codemagic..."

# Create new app
curl -H "Content-Type: application/json" \
     -H "x-auth-token: $API_TOKEN" \
     --data '{
       "repositoryUrl": "https://github.com/murr2k/android-app-dev",
       "projectType": "android-app"
     }' \
     -X POST "$API_BASE/apps"

echo ""
echo "Done! Please check your Codemagic dashboard for the new app."
echo ""
echo "Next steps:"
echo "1. Go to https://codemagic.io/apps"
echo "2. Find 'android-app-dev' in your apps list"
echo "3. Configure build settings if needed"
echo "4. Start a build to test"