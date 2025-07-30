# Keystore Troubleshooting Guide

## Current Situation
- Google Play expects SHA1: `EE:C4:81:75:B1:DD:21:49:0C:F1:D6:74:B9:CE:77:CE:EE:63:F6:B0`
- Your local keystore has SHA1: `BC:06:6B:B8:C3:CC:22:5D:18:01:AF:FD:85:A0:35:8B:43:F2:1D:F9`
- This mismatch prevents uploading new versions

## How to Check Google Play App Signing Status

1. Go to Google Play Console
2. Select your app
3. Navigate to **Setup > App signing**
4. Check if you see:
   - **"Google Play App Signing is enabled"** - If yes, proceed to Option A
   - **"Enroll in Google Play App Signing"** - If yes, proceed to Option B

### Option A: If Google Play App Signing is ENABLED

You'll see two certificates:
1. **App signing certificate** (managed by Google) - This is the one with SHA1: `EE:C4...`
2. **Upload certificate** - This is what you use to upload

**Solution**: 
- You need to register your current keystore as the upload certificate
- Or download the upload certificate if one exists

### Option B: If Google Play App Signing is NOT enabled

The app was uploaded with a keystore you don't have access to (likely from Codemagic).

**Solutions**:
1. **Find the Codemagic keystore**: Check Codemagic dashboard for keystore management
2. **Create a new app**: Since you're in internal testing, creating a fresh app might be easier
3. **Contact support**: Google Play support might help with key replacement

## Using Your Current Keystore

If you decide to use your current keystore (`linknode-release.keystore`):

```bash
# Prepare for GitHub Actions
./scripts/prepare_keystore_for_github.sh android/linknode-release.keystore

# The keystore password is: linknode2024
# The key alias is: linknode
# The key password is: linknode2024
```

## Next Steps

1. Check your Google Play Console App Signing status
2. Let me know what you find, and we'll proceed with the appropriate solution
3. If creating a new app, we can automate the entire process with your current keystore