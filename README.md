# Android Cloud Development Environment with Codemagic.io

## 🎯 Project Overview

This repository contains a complete setup for cloud-based Android app development using Codemagic.io as the CI/CD platform. No local Android SDK installation required!

## 📁 Repository Structure

```
android/
├── README.md                      # This file
├── codemagic.yaml                # Codemagic CI/CD configuration
├── android-cloud-dev-guide.md    # Comprehensive development guide
├── cloud-ide-integration.md      # Cloud IDE setup instructions
├── firebase-test-lab-guide.md    # Firebase Test Lab integration guide
└── scripts/
    ├── codemagic-api.sh         # API automation script
    └── firebase-test-lab.sh     # Firebase Test Lab automation
```

## 🚀 Quick Start

1. **Fork/Clone this repository**
2. **Add to Codemagic.io** using the API token
3. **Choose your cloud IDE**:
   - GitHub Codespaces
   - Gitpod
   - CodeSandbox
   - Replit
4. **Set up Firebase Test Lab** for cloud-based device testing
5. **Start developing** - builds and tests run automatically on push!

## 🔑 API Access

Your Codemagic API token has been verified and can:
- List and manage applications
- Trigger builds programmatically
- Download build artifacts
- Monitor build status

## 📱 Existing Android App

Found configured app: **android-1-demo** (ID: 688072f631568a5302db7b26)

## 🛠️ Available Tools

### Codemagic API Script
```bash
# List all apps
./scripts/codemagic-api.sh list-apps

# Trigger a build
./scripts/codemagic-api.sh trigger [app-id] [workflow] [branch]

# Monitor build progress
./scripts/codemagic-api.sh monitor [build-id]
```

### Firebase Test Lab Script
```bash
# Run instrumentation tests
./scripts/firebase-test-lab.sh instrumentation app.apk test.apk

# Run Robo tests (automated UI exploration)
./scripts/firebase-test-lab.sh robo app.apk

# Run full test suite on multiple devices
./scripts/firebase-test-lab.sh full app.apk test.apk
```

### Build Configuration
- See `codemagic.yaml` for complete CI/CD pipeline
- Supports APK and AAB builds
- Automated testing (unit & instrumented)
- Google Play deployment ready

### Cloud IDE Integration
- Pre-configured development containers
- Android SDK auto-installation
- Gradle build support
- VS Code extensions included

## 📚 Documentation

- **[Android Cloud Dev Guide](android-cloud-dev-guide.md)** - Complete setup and workflow
- **[Cloud IDE Integration](cloud-ide-integration.md)** - IDE-specific configurations
- **[Firebase Test Lab Guide](firebase-test-lab-guide.md)** - Cloud testing setup
- **[Codemagic YAML](codemagic.yaml)** - Build pipeline configuration

## 🔐 Required Secrets

Configure these in Codemagic or your IDE:
- `CM_KEYSTORE` - Android signing keystore (base64)
- `CM_KEYSTORE_PASSWORD` - Keystore password
- `CM_KEY_ALIAS` - Key alias name
- `CM_KEY_ALIAS_PASSWORD` - Key alias password
- `GCLOUD_SERVICE_ACCOUNT_CREDENTIALS` - For Play Store deployment
- `GCLOUD_KEY_FILE` - Firebase service account JSON
- `FIREBASE_PROJECT` - Firebase project ID

## 🌟 Features

✅ **Cloud-Native Development** - No local setup required
✅ **Automated CI/CD** - Push to build automatically
✅ **Multiple IDE Support** - Choose your favorite
✅ **API Automation** - Full programmatic control
✅ **Production Ready** - Signing and deployment included
✅ **Cloud Testing** - Firebase Test Lab integration with real devices
✅ **Multi-Device Testing** - Test on 100+ device configurations

## 🚦 Next Steps

1. Set up your Android project in the repository
2. Configure environment variables in Codemagic
3. Choose and set up your preferred cloud IDE
4. Start developing and let Codemagic handle the builds!

## 🌐 Live Demo

- Firebase Hosting: https://android-swarm-dev-1-4d7c7.firebaseapp.com

## 📞 Support

- Codemagic Docs: https://docs.codemagic.io
- API Reference: https://docs.codemagic.io/rest-api/overview/

---

Happy cloud-based Android development! 🎉