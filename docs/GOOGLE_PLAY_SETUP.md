# Google Play Publishing Setup Guide

This guide walks through setting up the Google Play publishing pipeline for the LinkNode Demo app.

## Prerequisites

1. Google Play Developer Account
2. Google Cloud Platform account
3. GitHub repository with Actions enabled

## Setup Steps

### 1. Google Play Console Setup

1. Log in to [Google Play Console](https://play.google.com/console)
2. Create a new app or select existing app
3. Complete all required store listing information
4. Upload at least one APK/AAB manually to create the app

### 2. Google Cloud Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable the Google Play Android Developer API:
   ```
   APIs & Services → Enable APIs → Search "Google Play Android Developer API" → Enable
   ```
4. Create Service Account:
   ```
   IAM & Admin → Service Accounts → Create Service Account
   ```
   - Name: `github-actions-play-store`
   - Grant no roles in GCP (roles are granted in Play Console)
   - Create JSON key and download

### 3. Link Service Account to Play Console

1. In Google Play Console, go to Settings → API access
2. Link your Google Cloud project
3. Find your service account email (e.g., `github-actions-play-store@project.iam.gserviceaccount.com`)
4. Click "Grant access"
5. Add permissions:
   - View app information
   - Manage production releases
   - Manage testing track releases
   - View financial data (optional)

### 4. GitHub Secrets Setup

Add these secrets to your GitHub repository (Settings → Secrets → Actions):

| Secret Name | Description | How to Get |
|------------|-------------|------------|
| `RELEASE_KEYSTORE` | Base64 encoded keystore | `base64 -i android/linknode-release.keystore` |
| `KEYSTORE_PASSWORD` | Keystore password | Password used when creating keystore |
| `KEY_ALIAS` | Key alias | Alias used when creating keystore (e.g., "linknode") |
| `KEY_PASSWORD` | Key password | Password for the key |
| `PLAY_STORE_CREDENTIALS` | Service account JSON | Contents of downloaded JSON file |

### 5. Prepare Release Assets

1. **App Icon**: Place in `fastlane/metadata/android/en-US/images/icon.png` (512x512px)
2. **Feature Graphic**: Place in `fastlane/metadata/android/en-US/images/featureGraphic.png` (1024x500px)
3. **Screenshots**: Add at least 2 phone screenshots in `fastlane/metadata/android/en-US/images/phoneScreenshots/`
   - Recommended: 1080x1920px or similar aspect ratio
   - Name them: `1_en-US.png`, `2_en-US.png`, etc.

### 6. Test the Setup

1. Create a test tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. Or trigger manually:
   - Go to Actions → Google Play Release → Run workflow
   - Select track (internal/alpha/beta/production)
   - Run

## Release Process

### Automated Release (Recommended)

1. Update version in code if needed
2. Commit and push changes
3. Create and push a version tag:
   ```bash
   git tag v1.2.3
   git push origin v1.2.3
   ```
4. GitHub Actions will automatically:
   - Build the app
   - Sign with release key
   - Upload to Play Store production track
   - Create GitHub release

### Manual Release

1. Go to Actions → Google Play Release
2. Click "Run workflow"
3. Select:
   - Track: internal/alpha/beta/production
   - Rollout percentage (for production)
4. Run workflow

## Rollout Strategy

- **Internal**: For internal testing team
- **Alpha**: For early testers
- **Beta**: For wider testing group
- **Production**: Public release
  - Start with 10% rollout
  - Monitor for issues
  - Gradually increase to 100%

## Monitoring

- Check GitHub Actions for build status
- Monitor Play Console for:
  - Crash reports
  - User feedback
  - Download statistics
  - Revenue (if applicable)

## Troubleshooting

### Common Issues

1. **"Package name not found"**
   - Ensure app is created in Play Console
   - Upload at least one APK/AAB manually first

2. **"Insufficient permissions"**
   - Check service account has correct permissions in Play Console
   - Verify API is enabled in Google Cloud

3. **"Version code already exists"**
   - Version codes must be unique and increasing
   - Check `github.run_number` is being used correctly

4. **Signing issues**
   - Verify keystore secrets are correctly base64 encoded
   - Check passwords match those used when creating keystore

## Best Practices

1. Always test in internal track first
2. Use semantic versioning for tags (v1.2.3)
3. Write meaningful commit messages for auto-generated release notes
4. Monitor initial rollout carefully before increasing percentage
5. Keep keystore backup in secure location
6. Rotate service account keys periodically