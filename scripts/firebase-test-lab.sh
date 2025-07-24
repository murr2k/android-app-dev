#!/bin/bash

# Firebase Test Lab Automation Script
# This script provides utilities for running Android tests on Firebase Test Lab

set -e

# Configuration
FIREBASE_PROJECT="${FIREBASE_PROJECT:-your-firebase-project}"
RESULTS_BUCKET="${RESULTS_BUCKET:-gs://$FIREBASE_PROJECT-test-results}"
BUILD_ID="${CM_BUILD_ID:-local-$(date +%Y%m%d-%H%M%S)}"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v gcloud &> /dev/null; then
        log_error "gcloud CLI not found. Please install Google Cloud SDK."
        exit 1
    fi
    
    if [ -z "$GCLOUD_KEY_FILE" ]; then
        log_error "GCLOUD_KEY_FILE environment variable not set."
        exit 1
    fi
    
    log_info "Prerequisites check passed."
}

# Authenticate with Firebase
authenticate() {
    log_info "Authenticating with Firebase..."
    echo "$GCLOUD_KEY_FILE" > /tmp/gcloud_key_file.json
    gcloud auth activate-service-account --key-file=/tmp/gcloud_key_file.json
    gcloud --quiet config set project "$FIREBASE_PROJECT"
    rm /tmp/gcloud_key_file.json
    log_info "Authentication successful."
}

# List available devices
list_devices() {
    log_info "Available test devices:"
    gcloud firebase test android models list
}

# Run instrumentation tests
run_instrumentation_tests() {
    local app_apk=$1
    local test_apk=$2
    local devices=${3:-"model=Pixel4,version=30"}
    local timeout=${4:-"20m"}
    
    log_info "Running instrumentation tests..."
    log_info "App APK: $app_apk"
    log_info "Test APK: $test_apk"
    log_info "Devices: $devices"
    
    gcloud firebase test android run \
        --type instrumentation \
        --app "$app_apk" \
        --test "$test_apk" \
        --device $devices \
        --timeout "$timeout" \
        --results-bucket "$RESULTS_BUCKET" \
        --results-dir "$BUILD_ID/instrumentation" \
        --environment-variables coverage=true,coverageFile="/sdcard/coverage.ec" \
        --directories-to-pull /sdcard
}

# Run Robo tests
run_robo_tests() {
    local app_apk=$1
    local device=${2:-"model=Pixel4,version=30"}
    local timeout=${3:-"10m"}
    
    log_info "Running Robo tests..."
    log_info "App APK: $app_apk"
    log_info "Device: $device"
    
    gcloud firebase test android run \
        --type robo \
        --app "$app_apk" \
        --device $device \
        --timeout "$timeout" \
        --results-bucket "$RESULTS_BUCKET" \
        --results-dir "$BUILD_ID/robo" \
        --robo-directives click:button_login=,text:username_field=testuser
}

# Run tests on multiple devices
run_multi_device_tests() {
    local app_apk=$1
    local test_apk=$2
    
    log_info "Running tests on multiple devices..."
    
    # Define device matrix
    local devices=(
        "model=Pixel2,version=28,locale=en_US,orientation=portrait"
        "model=Pixel4,version=30,locale=en_US,orientation=portrait"
        "model=Pixel5,version=31,locale=en_US,orientation=portrait"
        "model=Nexus9,version=25,locale=en_US,orientation=landscape"
    )
    
    for device in "${devices[@]}"; do
        log_info "Testing on: $device"
        run_instrumentation_tests "$app_apk" "$test_apk" "$device" "15m" || log_warning "Test failed on $device"
    done
}

# Run performance tests
run_performance_tests() {
    local app_apk=$1
    local test_apk=$2
    
    log_info "Running performance tests..."
    
    gcloud firebase test android run \
        --type instrumentation \
        --app "$app_apk" \
        --test "$test_apk" \
        --device model=Pixel5,version=31 \
        --environment-variables additionalTestOutputDir=/sdcard/test_output \
        --directories-to-pull /sdcard/test_output \
        --performance-metrics \
        --results-bucket "$RESULTS_BUCKET" \
        --results-dir "$BUILD_ID/performance"
}

# Download test results
download_results() {
    local output_dir=${1:-"./test-results"}
    
    log_info "Downloading test results..."
    mkdir -p "$output_dir"
    
    gsutil -m cp -r "$RESULTS_BUCKET/$BUILD_ID" "$output_dir/" || log_warning "Some results may not be available"
    
    log_info "Results downloaded to: $output_dir"
}

# Generate test report
generate_report() {
    local results_dir=${1:-"./test-results"}
    
    log_info "Generating test report..."
    
    # Create summary report
    cat > "$results_dir/summary.md" << EOF
# Firebase Test Lab Results

**Build ID:** $BUILD_ID  
**Date:** $(date)  
**Project:** $FIREBASE_PROJECT  

## Test Summary

### Instrumentation Tests
$(find "$results_dir" -name "test_result_*.xml" -exec grep -l "testsuites" {} \; | wc -l) test suites executed

### Robo Tests
$(find "$results_dir" -name "robo-tests.log" | wc -l) Robo test sessions completed

### Performance Metrics
Check \`$results_dir/$BUILD_ID/performance\` for detailed metrics

## Artifacts
- Test results: \`$results_dir/$BUILD_ID\`
- Screenshots: \`$results_dir/$BUILD_ID/*/artifacts\`
- Logs: \`$results_dir/$BUILD_ID/*/logs\`
EOF

    log_info "Report generated: $results_dir/summary.md"
}

# Main command handler
case "${1:-help}" in
    auth)
        check_prerequisites
        authenticate
        ;;
    list-devices)
        authenticate
        list_devices
        ;;
    instrumentation)
        check_prerequisites
        authenticate
        run_instrumentation_tests "$2" "$3" "${4:-model=Pixel4,version=30}" "${5:-20m}"
        ;;
    robo)
        check_prerequisites
        authenticate
        run_robo_tests "$2" "${3:-model=Pixel4,version=30}" "${4:-10m}"
        ;;
    multi-device)
        check_prerequisites
        authenticate
        run_multi_device_tests "$2" "$3"
        ;;
    performance)
        check_prerequisites
        authenticate
        run_performance_tests "$2" "$3"
        ;;
    download)
        download_results "${2:-./test-results}"
        ;;
    report)
        generate_report "${2:-./test-results}"
        ;;
    full)
        # Run complete test suite
        check_prerequisites
        authenticate
        run_robo_tests "$2"
        run_instrumentation_tests "$2" "$3"
        run_performance_tests "$2" "$3"
        download_results
        generate_report
        ;;
    *)
        echo "Firebase Test Lab Automation Script"
        echo ""
        echo "Usage: $0 <command> [arguments]"
        echo ""
        echo "Commands:"
        echo "  auth                    Authenticate with Firebase"
        echo "  list-devices           List available test devices"
        echo "  instrumentation <app> <test> [device] [timeout]"
        echo "                         Run instrumentation tests"
        echo "  robo <app> [device] [timeout]"
        echo "                         Run Robo tests"
        echo "  multi-device <app> <test>"
        echo "                         Run tests on multiple devices"
        echo "  performance <app> <test>"
        echo "                         Run performance tests"
        echo "  download [dir]         Download test results"
        echo "  report [dir]           Generate test report"
        echo "  full <app> <test>      Run complete test suite"
        echo ""
        echo "Environment variables:"
        echo "  FIREBASE_PROJECT       Firebase project ID"
        echo "  GCLOUD_KEY_FILE       Service account JSON key"
        echo "  RESULTS_BUCKET        GCS bucket for results"
        echo "  CM_BUILD_ID           Build identifier"
        ;;
esac