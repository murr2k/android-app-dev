# Instructions for Claude Code - Android App Deployment

## Project Overview
This is the LinkNode Demo Android app with automated Play Store deployment.

## Deployment System

### Available Deployment Methods

1. **Branch-based Deployment** (Recommended for Claude Code)
   - Create and push branches with specific patterns to trigger deployments
   - Works from any git environment

2. **Tag-based Deployment**
   - Creating version tags deploys to Alpha track
   - Example: `git tag v1.0.2 && git push --tags`

3. **Manual GitHub Actions**
   - Via GitHub web UI only

### Branch-based Deployment Instructions

When the user asks to deploy the app, use these branch patterns:

```bash
# Internal testing (small team testing)
git checkout -b release/internal/description
git push origin release/internal/description

# Alpha testing (closed testing group)
git checkout -b release/alpha/v1.0.2
git push origin release/alpha/v1.0.2

# Beta testing (open testing)
git checkout -b release/beta/v1.0.2
git push origin release/beta/v1.0.2

# Production - DRAFT (manual review needed)
git checkout -b release/production/v1.0.2
git push origin release/production/v1.0.2

# Production - AUTO-SUBMIT for Google review
git checkout -b release/production/v1.0.2/submit
git push origin release/production/v1.0.2/submit
```

### Version Management
- Versions are stored in `version.properties`
- Version code auto-increments on each deployment
- Version name can be specified in branch (e.g., v1.0.2) or auto-increments

### Examples for Common Requests

**"Deploy a test version"**
```bash
git checkout -b release/internal/test-feature
git push origin release/internal/test-feature
```

**"Deploy to alpha testers"**
```bash
git checkout -b release/alpha/v1.0.2
git push origin release/alpha/v1.0.2
```

**"Release to production"**
```bash
# Ask user: "Should I submit for Google review or save as draft?"
# If submit:
git checkout -b release/production/v1.0.2/submit
# If draft:
git checkout -b release/production/v1.0.2

git push origin release/production/v1.0.2[/submit]
```

### Important Notes
- Always create branches from main: `git checkout main && git pull`
- Version changes are auto-committed back to main after deployment
- Deployment takes ~5-10 minutes
- Check GitHub Actions for progress: https://github.com/murr2k/android-app-dev/actions

### Current Configuration
- Package name: `com.linknode.showcase`
- App name: "Linknode Demo"
- Current version: Check `version.properties`
- Minimum SDK: 24 (Android 7.0)
- Target SDK: 35 (Android 15)

### Deployment Status
- Internal/Alpha/Beta: Available immediately after deployment
- Production: Requires Google review (2-24 hours) if submitted

### Troubleshooting
- Version conflicts: Ensure version code increments (handled automatically)
- Build failures: Check GitHub Actions logs
- Signing issues: Keystore is configured in GitHub Secrets