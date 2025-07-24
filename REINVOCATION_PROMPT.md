# Linknode Android Project - Reinvocation Context

## Project Overview
This is the **Linknode** cloud-native Android development project that demonstrates AI-augmented development capabilities. The entire platform was built in under 24 hours and includes both an Android app and a live IoT energy monitoring system.

## Key URLs and Resources
- **GitHub Repository**: https://github.com/murr2k/android-app-dev
- **Live Energy Monitor**: https://linknode.com (from rackspace-k8s-demo repo)
- **Firebase Hosting**: https://android-swarm-dev-1-4d7c7.firebaseapp.com
- **Codemagic API Token**: 8u2x8z907-AgIZ114Ofpyea_sSKWZHC2-tBIxRjBn_E
- **Codemagic App ID**: 688072f631568a5302db7b26 (android-1-demo)

## Current Project State
1. **Android App Features**:
   - Animated gradient background (deep blue to purple: #1a237e to #7c4dff)
   - Particle animation system with floating effects
   - Linknode logo integrated in hero section
   - Material Design 3 UI
   - "Learn More" button opens linknode.com
   - All branding updated from "LinkNode" to "Linknode"
   - Attribution: "by Murray Kopit"

2. **CI/CD Setup**:
   - GitHub Actions workflow builds APK on every push
   - Codemagic.io integration (requires subscription for downloads)
   - APK available as GitHub Actions artifacts
   - Firebase hosting deployed

3. **Technical Stack**:
   - Kotlin for Android development
   - Gradle build system
   - Material Design Components
   - Custom animation views
   - NFC capabilities documented (read/write tags)

## Key Files
- `/android/app/src/main/java/com/linknode/demo/MainActivity.kt` - Main activity
- `/android/app/src/main/java/com/linknode/demo/ParticleAnimationView.kt` - Particle effects
- `/android/app/src/main/res/layout/activity_main.xml` - Main layout
- `/android/app/src/main/res/drawable/animated_gradient_background.xml` - Gradient animation
- `/android/app/src/main/res/drawable/linknode_logo.jpg` - Logo asset
- `/.github/workflows/build-apk-simple.yml` - GitHub Actions workflow
- `/codemagic.yaml` - Codemagic CI/CD configuration

## Recent Tasks Completed
1. ✅ Created native Android app with landing page similar to linknode.com
2. ✅ Set up git repository and pushed to GitHub
3. ✅ Fixed Firebase hosting deployment
4. ✅ Updated all "LinkNode" text to "Linknode"
5. ✅ Added "by Murray Kopit" attribution
6. ✅ Fixed Codemagic build issues (removed signing, changed instance type)
7. ✅ Set up GitHub Actions as free alternative to Codemagic
8. ✅ Redesigned app with animated gradient background matching linknode.com
9. ✅ Added particle animation effects
10. ✅ Integrated linknode logo
11. ✅ Updated feature cards to IoT/energy monitoring theme
12. ✅ Made "Learn More" button open linknode.com
13. ✅ Created comprehensive README showcasing IoT capabilities

## Known Issues
- APK installation requires uninstalling previous version due to signature conflicts
- Codemagic requires subscription for APK downloads (use GitHub Actions instead)

## Next Potential Tasks
- Implement actual NFC tag reading/writing functionality
- Add real-time power monitoring data from linknode.com API
- Create WebView for embedded Grafana dashboard
- Implement push notifications for energy alerts
- Add user authentication
- Create settings screen for API configuration
- Implement data caching for offline viewing
- Add charts/graphs for energy visualization
- Create onboarding flow
- Publish to Google Play Store

## Important Context
- The linknode.com website source is in the rackspace-k8s-demo repository
- The app showcases what can be built with AI-augmented development
- Focus is on demonstrating rapid development capabilities (24 hours)
- Designed as a portfolio piece for IoT and mobile development services

## Reinvocation Instructions
When continuing work on this project:
1. Check GitHub Actions for latest build status
2. The working directory is `/home/murr2k/projects/android`
3. To test changes, push to GitHub and download APK from Actions artifacts
4. Remember to uninstall old APK before installing new versions
5. All text should use "Linknode" (not "LinkNode")
6. Maintain the deep blue/purple color scheme
7. Keep focus on IoT/energy monitoring capabilities

---
*Last updated: 2025-07-24*