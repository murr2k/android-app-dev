# Cloud IDE Integration Guide for Android Development

## Overview

This guide covers integrating popular cloud-based IDEs with Codemagic.io for a complete cloud Android development environment.

## Supported Cloud IDEs

### 1. GitHub Codespaces

#### Setup

Create `.devcontainer/devcontainer.json`:

```json
{
  "name": "Android Cloud Dev",
  "image": "mcr.microsoft.com/devcontainers/android:1-34",
  "features": {
    "ghcr.io/devcontainers/features/java:1": {
      "version": "17",
      "installGradle": true
    },
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "vscjava.vscode-java-pack",
        "vscjava.vscode-gradle",
        "mathiasfrohlich.kotlin",
        "esbenp.prettier-vscode"
      ],
      "settings": {
        "java.home": "/usr/lib/jvm/java-17-openjdk-amd64",
        "terminal.integrated.defaultProfile.linux": "bash"
      }
    }
  },
  "postCreateCommand": "bash .devcontainer/setup.sh",
  "remoteUser": "vscode"
}
```

Create `.devcontainer/setup.sh`:

```bash
#!/bin/bash
# Setup Android development environment
echo "Setting up Android development environment..."

# Create local.properties
echo "sdk.dir=$ANDROID_SDK_ROOT" > local.properties

# Install Codemagic CLI tools
npm install -g @codemagic/cli-tools

# Configure git
git config --global user.email "$GITHUB_USER@users.noreply.github.com"
git config --global user.name "$GITHUB_USER"

# Create Android emulator (optional)
if [ -n "$ANDROID_SDK_ROOT" ]; then
    echo "Android SDK found at: $ANDROID_SDK_ROOT"
    sdkmanager --update
    sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"
fi

echo "Setup complete!"
```

### 2. Gitpod

Create `.gitpod.yml`:

```yaml
image:
  file: .gitpod.Dockerfile

tasks:
  - name: Android Setup
    init: |
      # Install Android SDK
      sudo apt-get update
      sudo apt-get install -y wget unzip
      
      # Download Android command line tools
      wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip
      unzip commandlinetools-linux-9477386_latest.zip -d android-sdk
      rm commandlinetools-linux-9477386_latest.zip
      
      # Set up environment
      export ANDROID_SDK_ROOT=$PWD/android-sdk
      export PATH=$PATH:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools
      
      # Accept licenses and install components
      yes | sdkmanager --sdk_root=$ANDROID_SDK_ROOT --licenses
      sdkmanager --sdk_root=$ANDROID_SDK_ROOT "platform-tools" "platforms;android-34" "build-tools;34.0.0"
      
      # Create local.properties
      echo "sdk.dir=$ANDROID_SDK_ROOT" > local.properties
    command: |
      echo "Android development environment ready!"
      echo "Run './gradlew build' to build your project"

  - name: Codemagic Integration
    init: npm install -g @codemagic/cli-tools
    command: echo "Codemagic CLI tools installed"

vscode:
  extensions:
    - vscjava.vscode-java-pack
    - vscjava.vscode-gradle
    - mathiasfrohlich.kotlin
    - esbenp.prettier-vscode

ports:
  - port: 8080
    visibility: public
  - port: 5037
    visibility: private
```

Create `.gitpod.Dockerfile`:

```dockerfile
FROM gitpod/workspace-full

# Install Java 17
RUN bash -c ". /home/gitpod/.sdkman/bin/sdkman-init.sh && sdk install java 17.0.8-tem"

# Install Android dependencies
RUN sudo apt-get update && \
    sudo apt-get install -y \
    build-essential \
    file \
    apt-utils
```

### 3. CodeSandbox

Create `sandbox.config.json`:

```json
{
  "infiniteLoopProtection": true,
  "hardReloadOnChange": false,
  "view": "terminal",
  "template": "node",
  "container": {
    "node": "16",
    "port": 8080
  }
}
```

Create `.codesandbox/tasks.json`:

```json
{
  "setupTasks": [
    {
      "name": "Install Dependencies",
      "command": "npm install"
    },
    {
      "name": "Setup Android Environment",
      "command": "bash setup-android.sh"
    }
  ],
  "tasks": {
    "build": {
      "name": "Build Android App",
      "command": "./gradlew assembleDebug",
      "runAtStart": false
    },
    "test": {
      "name": "Run Tests",
      "command": "./gradlew test",
      "runAtStart": false
    }
  }
}
```

### 4. Replit

Create `.replit`:

```toml
run = "bash run.sh"

[nix]
channel = "stable-22_11"

[env]
ANDROID_HOME = "/home/runner/$REPL_SLUG/android-sdk"
JAVA_HOME = "/nix/store/jdk-17"
PATH = "/home/runner/$REPL_SLUG/android-sdk/cmdline-tools/latest/bin:${PATH}"

[packager]
language = "java"

[packager.features]
packageSearch = true
guessImports = true
```

Create `replit.nix`:

```nix
{ pkgs }: {
  deps = [
    pkgs.jdk17
    pkgs.gradle
    pkgs.kotlin
    pkgs.android-studio
  ];
}
```

## Codemagic Integration Scripts

### Auto-deploy on Push

Create `.github/workflows/codemagic-trigger.yml`:

```yaml
name: Trigger Codemagic Build

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  trigger-build:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Codemagic Build
        run: |
          curl -H "Content-Type: application/json" \
               -H "x-auth-token: ${{ secrets.CODEMAGIC_API_TOKEN }}" \
               --data '{
                 "appId": "${{ secrets.CODEMAGIC_APP_ID }}",
                 "workflowId": "android-workflow",
                 "branch": "${{ github.ref_name }}"
               }' \
               -X POST https://api.codemagic.io/builds
```

### VS Code Tasks

Create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Build Debug APK",
      "type": "shell",
      "command": "./gradlew assembleDebug",
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "problemMatcher": ["$gradle"]
    },
    {
      "label": "Trigger Codemagic Build",
      "type": "shell",
      "command": "bash scripts/codemagic-api.sh trigger",
      "problemMatcher": []
    },
    {
      "label": "Check Build Status",
      "type": "shell",
      "command": "bash scripts/codemagic-api.sh list-builds",
      "problemMatcher": []
    },
    {
      "label": "Run Local Tests",
      "type": "shell",
      "command": "./gradlew test",
      "group": "test",
      "problemMatcher": ["$gradle"]
    }
  ]
}
```

## Best Practices

### 1. Environment Variables

Store sensitive data in IDE secrets:

```bash
# GitHub Codespaces
gh secret set CODEMAGIC_API_TOKEN

# Gitpod
gp env CODEMAGIC_API_TOKEN=your-token

# Replit
# Use Secrets tab in IDE

# CodeSandbox
# Use Environment Variables in project settings
```

### 2. Resource Optimization

- Use lightweight Android SDK installations
- Cache Gradle dependencies
- Minimize emulator usage in cloud IDEs
- Leverage Codemagic for heavy builds

### 3. Development Workflow

1. **Edit** code in cloud IDE
2. **Test** locally with unit tests
3. **Push** to trigger Codemagic build
4. **Monitor** build status in IDE terminal
5. **Deploy** automatically on success

### 4. Performance Tips

- Pre-build base images with Android SDK
- Use Gradle build cache
- Optimize dependency downloads
- Leverage IDE-specific caching

## Troubleshooting

### Common Issues

1. **Out of Memory**
   ```bash
   # Increase Gradle memory
   echo "org.gradle.jvmargs=-Xmx2048m" >> gradle.properties
   ```

2. **SDK Not Found**
   ```bash
   # Verify SDK path
   echo "sdk.dir=$ANDROID_SDK_ROOT" > local.properties
   ```

3. **Build Timeout**
   - Use Codemagic for long builds
   - Optimize build configuration
   - Cache dependencies

4. **Permission Errors**
   ```bash
   # Fix gradlew permissions
   chmod +x gradlew
   ```

## Advanced Integration

### Custom Build Triggers

```javascript
// webhook-handler.js
const express = require('express');
const app = express();

app.post('/webhook', async (req, res) => {
  const { action, pull_request } = req.body;
  
  if (action === 'opened' || action === 'synchronize') {
    // Trigger Codemagic build
    await triggerBuild(pull_request.head.ref);
  }
  
  res.status(200).send('OK');
});
```

### IDE Extensions

Develop custom extensions for better integration:

```typescript
// codemagic-vscode-extension/src/extension.ts
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  const triggerBuild = vscode.commands.registerCommand(
    'codemagic.triggerBuild',
    async () => {
      const branch = await vscode.window.showInputBox({
        prompt: 'Enter branch name',
        value: 'main'
      });
      
      // Call Codemagic API
      await callCodemagicAPI(branch);
    }
  );
  
  context.subscriptions.push(triggerBuild);
}
```

This completes the cloud IDE integration guide with practical examples for major cloud development platforms.