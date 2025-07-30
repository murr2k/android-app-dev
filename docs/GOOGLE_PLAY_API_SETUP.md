# Google Play Console API Access Setup

## Current Status
Your app is in review for closed testing. API access typically becomes available after your first successful release.

## When API Access Becomes Available

The API access section usually appears in one of these locations after your app is approved:
1. **Users and permissions** → **API access** (tab)
2. **Settings** → **Developer account** → **API access**
3. A new menu item appears after first release

## Setup Steps (Once Available)

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project: "linknode-play-api"
3. Enable the **Google Play Android Developer API**:
   ```
   APIs & Services → Library → Search "Google Play Android Developer API" → Enable
   ```

### 2. Create Service Account

1. Go to **IAM & Admin** → **Service accounts**
2. Click **Create Service Account**
3. Details:
   - Name: `github-actions-play-store`
   - ID: Auto-generated
   - Description: `Automates releases from GitHub Actions`
4. Skip role assignment (roles are set in Play Console)
5. Create JSON key and download

### 3. Link in Play Console (When Available)

1. Find API access section
2. Link your Google Cloud project
3. Grant permissions to service account:
   - ✅ View app information
   - ✅ Create and edit draft apps
   - ✅ Release apps to testing tracks
   - ✅ Release apps to production

### 4. Add to GitHub Secrets

1. Go to: https://github.com/murr2k/android-app-dev/settings/secrets/actions
2. New repository secret:
   - Name: `PLAY_STORE_CREDENTIALS`
   - Value: Paste entire JSON file content

## Temporary Workaround

While waiting for API access:

### Option 1: Continue Manual Uploads
- Use the "Build Internal Testing (Simple)" workflow
- Download AAB from GitHub
- Upload manually to Play Console

### Option 2: Pre-configure Everything
Even without API access, you can:
1. Create the Google Cloud project
2. Enable the API
3. Create the service account
4. Add to GitHub (it just won't work until linked)

## Testing Automation (Once Set Up)

### Manual trigger test:
```bash
# Go to Actions → Google Play Release → Run workflow
# Select "internal" track
# This will build and attempt upload
```

### Tag trigger test:
```bash
git tag v1.0.1
git push origin v1.0.1
# Automatically builds and uploads to production
```

## Common Issues & Solutions

### "The caller does not have permission"
- Service account not linked in Play Console
- Missing required permissions

### "Package not found: com.linknode.demo"
- App must have at least one uploaded release
- Package name mismatch

### "Version code already exists"
- Version codes must always increment
- Check GITHUB_RUN_NUMBER is being used

## Timeline Expectations

1. **App Review**: 2-24 hours (first submission)
2. **API Access Appears**: Usually within 24-48 hours after approval
3. **Full Automation**: Ready immediately after setup

## What You Can Do Now

1. ✅ Create Google Cloud project
2. ✅ Enable Play Developer API
3. ✅ Create service account & download JSON
4. ⏳ Wait for API access in Play Console
5. ⏳ Link and configure permissions
6. ✅ Add JSON to GitHub Secrets
7. 🚀 Test automated deployment!

---

**Note**: Some new developer accounts need to have a published app before API access is granted. Your internal testing release should satisfy this requirement.