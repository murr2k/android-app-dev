# Internal Testing Setup Guide

This guide helps you set up Internal Testing for the LinkNode Demo app.

## Step 1: Prepare the Keystore

Since we already have a keystore created (`android/linknode-release.keystore`), we need to commit it encrypted or store it as a GitHub secret.

### Option A: Use GitHub Secrets (Recommended)

1. Encode the keystore:
   ```bash
   cd android
   base64 -i linknode-release.keystore | tr -d '\n' > keystore-base64.txt
   ```

2. Copy the contents of `keystore-base64.txt`

3. Go to GitHub repository → Settings → Secrets and variables → Actions

4. Add these secrets:
   - `RELEASE_KEYSTORE`: (paste the base64 content)
   - `KEYSTORE_PASSWORD`: linknode2024
   - `KEY_ALIAS`: linknode
   - `KEY_PASSWORD`: linknode2024

### Option B: Use the existing keystore (for testing only)

The workflow will use the keystore that's already in the repository. Note: This is only safe because this is a demo app. Never commit production keystores!

## Step 2: Build the APK/AAB

1. Go to your GitHub repository
2. Click on "Actions" tab
3. Select "Build for Internal Testing" workflow
4. Click "Run workflow"
5. Choose build type:
   - `apk` - For direct installation
   - `aab` - For Play Store (recommended)
   - `both` - Build both formats
6. Click "Run workflow" (green button)

## Step 3: Download the Build

1. Wait for the workflow to complete (2-5 minutes)
2. Click on the completed workflow run
3. Scroll down to "Artifacts"
4. Download:
   - `linknode-release-aab` for Play Store upload
   - `linknode-release-apk` for direct testing

## Step 4: Create Internal Testing Release

1. In Google Play Console, go to "Release" → "Testing" → "Internal testing"
2. Click "Create new release"
3. Upload the AAB file
4. Add release notes:
   ```
   Initial internal testing release
   - Core LinkNode Demo functionality
   - Testing Play Store integration
   ```
5. Save and review
6. Start rollout to Internal testing

## Step 5: Add Testers

1. In Internal testing, go to "Testers" tab
2. Create a new email list or use existing
3. Add your email: murr2k@gmail.com
4. Save changes

## Step 6: Join Testing Program

1. Copy the "Join on web" link from the Testers tab
2. Open the link in a browser while signed in as murr2k@gmail.com
3. Accept the invitation to become a tester
4. You'll get a link to install from Play Store

## Testing Checklist

- [ ] APK/AAB builds successfully in GitHub Actions
- [ ] File can be downloaded from GitHub
- [ ] AAB uploads successfully to Play Console
- [ ] Internal testing release is created
- [ ] Tester (murr2k@gmail.com) can join program
- [ ] App can be installed from Play Store
- [ ] App runs correctly when installed

## Next Steps

Once internal testing works:
1. Set up service account for automated uploads
2. Test the full automation pipeline
3. Add more testers if needed
4. Progress to closed/open testing tracks

## Troubleshooting

### "Package name already exists"
- Make sure the applicationId in build.gradle is unique
- Current: `com.linknode.demo`

### "Version code already used"
- Each upload needs a unique, increasing version code
- The workflow uses GitHub run number for this

### Can't find app in Play Store
- Make sure you joined the testing program
- It can take up to 1 hour for the app to appear
- Try the direct link from the Internal testing page