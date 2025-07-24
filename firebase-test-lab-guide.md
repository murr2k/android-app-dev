# Firebase Test Lab Integration Guide for Android

## Overview

Firebase Test Lab provides cloud-based infrastructure for testing Android apps on real and virtual devices. It integrates seamlessly with Codemagic.io for automated testing in your CI/CD pipeline.

## Comparison of Cloud Testing Platforms

| Feature | Firebase Test Lab | AWS Device Farm | BrowserStack |
|---------|------------------|-----------------|---------------|
| **Free Tier** | 15 tests/day (10 virtual, 5 physical) | No free tier | Trial only |
| **Pricing** | $1/hour virtual, $5/hour physical | Pay-per-minute | Subscription-based |
| **Device Count** | Hundreds | Hundreds | 3,500+ |
| **Codemagic Integration** | ✅ Native support | ⚠️ Custom scripts | ⚠️ Custom scripts |
| **Test Types** | Robo, Instrumentation, Game Loop | All types | All types |
| **Best For** | Google ecosystem, Cost-effective | AWS users | Large device coverage |

## Firebase Test Lab Setup

### 1. Create Firebase Project

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login and create project
firebase login
firebase projects:create your-android-app-id
```

### 2. Create Service Account

1. Go to [Firebase Console](https://console.firebase.google.com)
2. Select your project → Settings → Service accounts
3. Generate new private key
4. Save the JSON file securely

### 3. Enable Test Lab API

```bash
# Enable required APIs
gcloud services enable testing.googleapis.com
gcloud services enable toolresults.googleapis.com
```

### 4. Configure Codemagic Environment

Add these variables to Codemagic:

```yaml
environment_variables:
  - GCLOUD_KEY_FILE: Encrypted(your-service-account-json)
  - FIREBASE_PROJECT: your-project-id
```

## Updated Codemagic Configuration

### Basic Firebase Test Lab Integration

```yaml
workflows:
  android-with-firebase-test-lab:
    name: Android App with Firebase Test Lab
    instance_type: linux_x2
    max_build_duration: 60
    environment:
      android_signing:
        - android_keystore
      groups:
        - android_credentials
        - firebase_credentials
      vars:
        PACKAGE_NAME: "com.example.app"
      java: 17
      
    scripts:
      # Build APKs for testing
      - name: Build debug APK
        script: |
          cd android
          ./gradlew assembleDebug
          
      - name: Build test APK
        script: |
          cd android
          ./gradlew assembleAndroidTest
          
      # Run Firebase Test Lab tests
      - name: Authenticate with Firebase
        script: |
          echo $GCLOUD_KEY_FILE > $CM_BUILD_DIR/gcloud_key_file.json
          gcloud auth activate-service-account --key-file=$CM_BUILD_DIR/gcloud_key_file.json
          gcloud --quiet config set project $FIREBASE_PROJECT
          
      - name: Run instrumentation tests on Firebase Test Lab
        script: |
          cd android
          
          # Run tests on multiple devices
          gcloud firebase test android run \
            --type instrumentation \
            --app app/build/outputs/apk/debug/app-debug.apk \
            --test app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk \
            --device model=Pixel2,version=28,locale=en_US,orientation=portrait \
            --device model=Nexus6,version=25,locale=en_US,orientation=portrait \
            --device model=Nexus9,version=24,locale=en_US,orientation=landscape \
            --timeout 30m \
            --results-bucket gs://$FIREBASE_PROJECT-test-results \
            --results-dir $CM_BUILD_ID
            
      - name: Run Robo tests
        script: |
          cd android
          
          # Robo test explores your app automatically
          gcloud firebase test android run \
            --type robo \
            --app app/build/outputs/apk/debug/app-debug.apk \
            --device model=Pixel4,version=30,locale=en_US,orientation=portrait \
            --timeout 10m \
            --robo-directives text:username_field=testuser,text:password_field=testpass
            
    artifacts:
      - android/app/build/outputs/**/*.apk
      - android/app/build/outputs/**/*.aab
      - firebase-test-results/**/*
```

### Advanced Configuration with Multiple Test Types

```yaml
scripts:
  # Performance testing
  - name: Run performance tests
    script: |
      gcloud firebase test android run \
        --type instrumentation \
        --app app/build/outputs/apk/release/app-release.apk \
        --test app/build/outputs/apk/androidTest/release/app-release-androidTest.apk \
        --device model=Pixel5,version=31 \
        --environment-variables additionalTestOutputDir=/sdcard/test_output \
        --directories-to-pull /sdcard/test_output \
        --performance-metrics
        
  # Game Loop testing (for game apps)
  - name: Run game loop tests
    script: |
      gcloud firebase test android run \
        --type game-loop \
        --app app/build/outputs/apk/debug/app-debug.apk \
        --scenario-numbers 1,2,3 \
        --device model=Pixel4,version=30
```

## Test Configuration Options

### Device Selection

```yaml
# Popular test devices
devices:
  # Phones
  - model=Pixel2,version=28         # Android 9
  - model=Pixel4,version=30         # Android 11
  - model=Pixel5,version=31         # Android 12
  - model=Pixel6,version=32         # Android 12L
  - model=Pixel7,version=33         # Android 13
  
  # Tablets
  - model=Nexus9,version=25         # Android 7.1
  
  # Low-end devices
  - model=AndroidGoPhone,version=28 # Android Go
```

### Test Sharding

```yaml
# Split tests across multiple devices for faster execution
- name: Run sharded tests
  script: |
    gcloud firebase test android run \
      --type instrumentation \
      --app app-debug.apk \
      --test app-debug-androidTest.apk \
      --device model=Pixel4,version=30 \
      --num-uniform-shards 5
```

## Cost Optimization

### 1. Use Virtual Devices for Most Tests

```yaml
# Virtual devices cost $1/hour vs $5/hour for physical
--device model=Pixel2.arm,version=28  # Virtual device
```

### 2. Optimize Test Execution Time

```yaml
# Set appropriate timeouts
--timeout 15m  # Don't use default 30m if not needed

# Use test filtering
--test-targets "class com.example.CriticalTests"
```

### 3. Use Test Matrix Efficiently

```yaml
# Test only critical device/OS combinations
devices:
  - model=Pixel4,version=30    # Most common
  - model=Nexus5X,version=26   # Minimum supported
  - model=Pixel6,version=32    # Latest
```

## Integration with Other Tools

### 1. Slack Notifications

```yaml
- name: Notify test results
  script: |
    TEST_RESULTS=$(gcloud firebase test android operations describe $TEST_ID --format json)
    STATUS=$(echo $TEST_RESULTS | jq -r '.state')
    
    curl -X POST $SLACK_WEBHOOK_URL \
      -H 'Content-type: application/json' \
      --data "{\"text\":\"Firebase Test Lab: $STATUS\"}"
```

### 2. Test Reports

```yaml
- name: Generate test report
  script: |
    # Download test results
    gsutil -m cp -r gs://$FIREBASE_PROJECT-test-results/$CM_BUILD_ID .
    
    # Parse results
    python scripts/parse_test_results.py
```

## Alternatives Configuration

### AWS Device Farm Integration

```yaml
- name: Run tests on AWS Device Farm
  script: |
    # Install AWS CLI
    pip install awscli
    
    # Configure AWS
    aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
    
    # Create test run
    PROJECT_ARN=$(aws devicefarm create-project --name "Android App" --query 'project.arn' --output text)
    
    UPLOAD_ARN=$(aws devicefarm create-upload \
      --project-arn $PROJECT_ARN \
      --name app-debug.apk \
      --type ANDROID_APP \
      --query 'upload.arn' --output text)
      
    # Upload and run tests
    aws devicefarm create-run \
      --project-arn $PROJECT_ARN \
      --app-arn $UPLOAD_ARN \
      --device-pool-arn $DEVICE_POOL_ARN \
      --test type=INSTRUMENTATION
```

### BrowserStack Integration

```yaml
- name: Run tests on BrowserStack
  script: |
    # Upload app
    APP_URL=$(curl -u "$BROWSERSTACK_USERNAME:$BROWSERSTACK_ACCESS_KEY" \
      -X POST "https://api-cloud.browserstack.com/app-automate/upload" \
      -F "file=@app-debug.apk" | jq -r '.app_url')
    
    # Upload test suite
    TEST_URL=$(curl -u "$BROWSERSTACK_USERNAME:$BROWSERSTACK_ACCESS_KEY" \
      -X POST "https://api-cloud.browserstack.com/app-automate/espresso/test-suite" \
      -F "file=@app-debug-androidTest.apk" | jq -r '.test_url')
    
    # Execute tests
    curl -u "$BROWSERSTACK_USERNAME:$BROWSERSTACK_ACCESS_KEY" \
      -X POST "https://api-cloud.browserstack.com/app-automate/espresso/build" \
      -d '{
        "app": "'$APP_URL'",
        "testSuite": "'$TEST_URL'",
        "devices": ["Google Pixel 4-10.0", "Samsung Galaxy S21-11.0"]
      }'
```

## Best Practices

1. **Start with Robo Tests**: Quick smoke tests to catch obvious issues
2. **Use Virtual Devices First**: Cheaper and faster for most tests
3. **Reserve Physical Devices**: For final validation and hardware-specific tests
4. **Implement Test Sharding**: Reduce overall test time
5. **Monitor Costs**: Use Firebase Console to track spending
6. **Cache Test Results**: Avoid re-running unchanged tests

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   ```bash
   # Verify service account permissions
   gcloud projects add-iam-policy-binding $FIREBASE_PROJECT \
     --member="serviceAccount:your-service-account@your-project.iam.gserviceaccount.com" \
     --role="roles/cloudtestservice.testAdmin"
   ```

2. **Test Timeouts**
   - Increase timeout value
   - Split large test suites
   - Use test sharding

3. **Device Not Available**
   - Check device catalog: `gcloud firebase test android models list`
   - Use alternative device models

## Summary

Firebase Test Lab is the most cost-effective solution for Android testing with excellent Codemagic integration. Start with the free tier (15 tests/day) and scale as needed. For extensive device coverage, consider BrowserStack; for AWS users, Device Farm integrates well with existing infrastructure.