# GitHub Actions Setup for Play Store Deployment

## Complete Setup Procedure

### 1. Add Google Play Service Account to GitHub Secrets

1. Copy the JSON content:
   ```bash
   cat /tmp/google-play-service-account.json
   ```

2. Go to: https://github.com/murr2k/android-app-dev/settings/secrets/actions

3. Click **"New repository secret"**
   - Name: `GOOGLE_PLAY_SERVICE_ACCOUNT`
   - Value: Paste the entire JSON content

### 2. Add Keystore Secrets

Run this to encode your keystore:
```bash
cd /home/murr2k/projects/android
base64 -w 0 android/linknode-release.keystore
```

Then add these secrets to GitHub:

1. **ANDROID_SIGNING_KEY**
   - Value: The base64 string from above

2. **ANDROID_ALIAS**
   - Value: `linknode` (or check with: `keytool -list -keystore android/linknode-release.keystore`)

3. **ANDROID_KEYSTORE_PASSWORD**
   - Value: Your keystore password

4. **ANDROID_KEY_PASSWORD**
   - Value: Your key password (often same as keystore password)

### 3. Test the Workflow

The workflow is already created at `.github/workflows/play-store-deploy.yml`

To test:
1. Create a new version tag:
   ```bash
   git add .github/workflows/play-store-deploy.yml
   git commit -m "Add Play Store deployment workflow"
   git push
   git tag v1.0.1
   git push --tags
   ```

2. Or trigger manually:
   - Go to Actions tab in GitHub
   - Select "Deploy to Play Store"
   - Click "Run workflow"

### 4. Monitor Deployment

1. Check GitHub Actions: https://github.com/murr2k/android-app-dev/actions
2. Check Play Console: https://play.google.com/console/developers/6461866616503612119/app/4972515549389209525/tracks/internal-testing

### 5. Workflow Features

The workflow:
- ✅ Triggers on version tags (v1.2.3)
- ✅ Builds release AAB
- ✅ Signs with your keystore
- ✅ Uploads to Internal Testing track
- ✅ Uses changelog from `fastlane/metadata/android/en-US/changelogs/`

### 6. Version Management

Update version in `android/app/build.gradle`:
```gradle
android {
    defaultConfig {
        versionCode 33  // Increment this
        versionName "1.0.1"  // Update this
    }
}
```

### 7. Changelog

Create a changelog file:
```bash
echo "• Automated deployment via GitHub Actions
• Bug fixes and improvements" > fastlane/metadata/android/en-US/changelogs/33.txt
```

### 8. Promotion to Production

Once tested in internal track, update the workflow:
```yaml
track: production  # Change from 'internal'
```

## Troubleshooting

### "Insufficient permissions"
- Wait 24-48 hours after inviting service account
- Check Play Console permissions

### "Version code already exists"
- Increment versionCode in build.gradle

### "Signing failed"
- Verify keystore secrets are correct
- Check alias name matches

## Security Notes

- Never commit secrets to the repository
- Keep keystore file secure
- Rotate service account keys periodically

## Next Steps

1. Add all required GitHub secrets
2. Test with a minor version bump
3. Monitor first automated deployment
4. Consider adding build number automation