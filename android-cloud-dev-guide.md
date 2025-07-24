# Android Cloud Development Environment with Codemagic.io

## Overview

This guide demonstrates how to set up a complete cloud-based Android development environment using Codemagic.io for CI/CD.

## Key Features

- **Cloud-based builds**: No local Android SDK required
- **Automated testing**: Unit and instrumented tests
- **Code signing**: Automated APK/AAB signing
- **Deployment**: Direct to Google Play Store
- **API integration**: Programmatic build triggers

## Prerequisites

1. Codemagic.io account with API token
2. Android project in Git repository
3. Google Play Console access (for deployment)
4. Android signing credentials

## Setup Steps

### 1. Configure Repository

Add your Android project to Codemagic:

```bash
# Using the API
curl -H "Content-Type: application/json" \
     -H "x-auth-token: YOUR_API_TOKEN" \
     --data '{
       "repositoryUrl": "https://github.com/your-username/your-android-app",
       "projectType": "android-app"
     }' \
     -X POST https://api.codemagic.io/apps
```

### 2. Configure Build Settings

Create `codemagic.yaml` in your repository root (see example file).

### 3. Set Environment Variables

In Codemagic dashboard or via API:

```bash
# Android signing credentials
CM_KEYSTORE: base64 encoded keystore file
CM_KEYSTORE_PASSWORD: your keystore password
CM_KEY_ALIAS: your key alias
CM_KEY_ALIAS_PASSWORD: your key alias password

# Google Play credentials
GCLOUD_SERVICE_ACCOUNT_CREDENTIALS: JSON service account
```

### 4. Trigger Builds

#### Via API:
```bash
curl -H "Content-Type: application/json" \
     -H "x-auth-token: YOUR_API_TOKEN" \
     --data '{
       "appId": "YOUR_APP_ID",
       "workflowId": "android-workflow",
       "branch": "main"
     }' \
     -X POST https://api.codemagic.io/builds
```

#### Via Webhook:
Configure GitHub/GitLab/Bitbucket webhooks to trigger on push/PR.

## Cloud IDE Integration

### 1. GitHub Codespaces

```json
// .devcontainer/devcontainer.json
{
  "name": "Android Dev Container",
  "image": "mcr.microsoft.com/devcontainers/android:1-34",
  "features": {
    "ghcr.io/devcontainers/features/java:1": {
      "version": "17"
    }
  },
  "postCreateCommand": "echo 'sdk.dir=/opt/android-sdk' > local.properties"
}
```

### 2. Gitpod

```yaml
# .gitpod.yml
image: gitpod/workspace-full

tasks:
  - name: Setup Android SDK
    init: |
      sudo apt-get update
      sudo apt-get install -y android-sdk
      echo "sdk.dir=/usr/lib/android-sdk" > local.properties

vscode:
  extensions:
    - vscjava.vscode-java-pack
    - msjsdiag.vscode-react-native
```

## Development Workflow

1. **Code**: Use cloud IDE (Codespaces, Gitpod, CodeSandbox)
2. **Commit**: Push changes to Git repository
3. **Build**: Codemagic automatically builds on push
4. **Test**: Automated unit and UI tests run
5. **Deploy**: Successful builds deploy to Google Play

## API Automation Scripts

### Build Status Monitor
```bash
#!/bin/bash
BUILD_ID=$(curl -s -H "x-auth-token: $API_TOKEN" \
  -X GET "https://api.codemagic.io/builds?appId=$APP_ID&limit=1" \
  | jq -r '.builds[0]._id')

STATUS=$(curl -s -H "x-auth-token: $API_TOKEN" \
  -X GET "https://api.codemagic.io/builds/$BUILD_ID" \
  | jq -r '.status')

echo "Build $BUILD_ID status: $STATUS"
```

### Batch Build Trigger
```bash
#!/bin/bash
BRANCHES=("main" "develop" "feature/*")

for branch in "${BRANCHES[@]}"; do
  curl -H "Content-Type: application/json" \
       -H "x-auth-token: $API_TOKEN" \
       --data "{
         \"appId\": \"$APP_ID\",
         \"workflowId\": \"android-workflow\",
         \"branch\": \"$branch\"
       }" \
       -X POST https://api.codemagic.io/builds
done
```

## Best Practices

1. **Version Control**: Store `codemagic.yaml` in repository
2. **Secrets**: Use environment variables, never commit
3. **Testing**: Run tests before deployment
4. **Monitoring**: Set up email/Slack notifications
5. **Caching**: Enable dependency caching for faster builds

## Troubleshooting

### Common Issues:

1. **Build failures**: Check Android SDK versions
2. **Signing errors**: Verify keystore credentials
3. **API limits**: Monitor rate limits (1000 req/hour)
4. **Test failures**: Review test reports in artifacts

## Next Steps

1. Set up branch protection rules
2. Configure automatic versioning
3. Implement release notes generation
4. Add performance monitoring
5. Set up crash reporting integration