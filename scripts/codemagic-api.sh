#!/bin/bash

# Codemagic API Automation Scripts
# Configure these environment variables:
# export CODEMAGIC_API_TOKEN="your-api-token"
# export CODEMAGIC_APP_ID="your-app-id"

API_BASE="https://api.codemagic.io"
API_TOKEN="${CODEMAGIC_API_TOKEN:-8u2x8z907-AgIZ114Ofpyea_sSKWZHC2-tBIxRjBn_E}"
APP_ID="${CODEMAGIC_APP_ID:-6882243327296f27a20aeaea}"  # android-app-dev

# Function to make API calls
api_call() {
    local method=$1
    local endpoint=$2
    local data=$3
    
    curl -s -X "$method" \
        -H "x-auth-token: $API_TOKEN" \
        -H "Content-Type: application/json" \
        ${data:+-d "$data"} \
        "$API_BASE$endpoint"
}

# List all applications
list_apps() {
    echo "Listing all applications..."
    api_call GET "/apps" | jq '.applications[] | {id: ._id, name: .appName, type: .projectType}'
}

# Get app details
get_app() {
    local app_id=${1:-$CODEMAGIC_APP_ID}
    echo "Getting app details for: $app_id"
    api_call GET "/apps/$app_id" | jq '.'
}

# Trigger a build
trigger_build() {
    local app_id=${1:-$CODEMAGIC_APP_ID}
    local workflow_id=${2:-"android-workflow"}
    local branch=${3:-"main"}
    
    echo "Triggering build for app: $app_id, workflow: $workflow_id, branch: $branch"
    
    local data=$(cat <<EOF
{
    "appId": "$app_id",
    "workflowId": "$workflow_id",
    "branch": "$branch"
}
EOF
)
    
    api_call POST "/builds" "$data" | jq '{buildId: ._id, status: .status}'
}

# Get build status
get_build_status() {
    local build_id=$1
    echo "Getting build status for: $build_id"
    api_call GET "/builds/$build_id" | jq '{id: ._id, status: .status, workflow: .workflowId, duration: .duration}'
}

# List recent builds
list_builds() {
    local app_id=${1:-$CODEMAGIC_APP_ID}
    local limit=${2:-10}
    
    echo "Listing recent builds for app: $app_id"
    api_call GET "/builds?appId=$app_id&limit=$limit" | \
        jq '.builds[] | {id: ._id, status: .status, branch: .branch, started: .startedAt}'
}

# Download artifacts
download_artifacts() {
    local build_id=$1
    local output_dir=${2:-"./artifacts"}
    
    echo "Downloading artifacts for build: $build_id"
    mkdir -p "$output_dir"
    
    # Get artifact URLs
    local artifacts=$(api_call GET "/builds/$build_id/artifacts")
    
    echo "$artifacts" | jq -r '.[] | .url' | while read -r url; do
        local filename=$(echo "$url" | rev | cut -d'/' -f1 | rev)
        echo "Downloading: $filename"
        curl -s -L -H "x-auth-token: $API_TOKEN" "$url" -o "$output_dir/$filename"
    done
}

# Cancel a build
cancel_build() {
    local build_id=$1
    echo "Cancelling build: $build_id"
    api_call POST "/builds/$build_id/cancel" | jq '{id: ._id, status: .status}'
}

# Monitor build progress
monitor_build() {
    local build_id=$1
    echo "Monitoring build: $build_id"
    
    while true; do
        local status=$(api_call GET "/builds/$build_id" | jq -r '.status')
        echo "$(date): Build status: $status"
        
        case $status in
            "finished"|"failed"|"canceled")
                echo "Build completed with status: $status"
                break
                ;;
            *)
                sleep 30
                ;;
        esac
    done
}

# Batch build trigger for multiple branches
batch_build() {
    local app_id=${1:-$CODEMAGIC_APP_ID}
    local workflow_id=${2:-"android-workflow"}
    shift 2
    local branches=("$@")
    
    if [ ${#branches[@]} -eq 0 ]; then
        branches=("main" "develop")
    fi
    
    echo "Triggering builds for branches: ${branches[*]}"
    
    for branch in "${branches[@]}"; do
        trigger_build "$app_id" "$workflow_id" "$branch"
        sleep 2  # Avoid rate limiting
    done
}

# Main command handler
case "${1:-help}" in
    list-apps)
        list_apps
        ;;
    get-app)
        get_app "$2"
        ;;
    trigger)
        trigger_build "$2" "$3" "$4"
        ;;
    status)
        get_build_status "$2"
        ;;
    list-builds)
        list_builds "$2" "$3"
        ;;
    artifacts)
        download_artifacts "$2" "$3"
        ;;
    cancel)
        cancel_build "$2"
        ;;
    monitor)
        monitor_build "$2"
        ;;
    batch)
        batch_build "$2" "$3" "${@:4}"
        ;;
    *)
        echo "Codemagic API CLI"
        echo ""
        echo "Usage: $0 <command> [arguments]"
        echo ""
        echo "Commands:"
        echo "  list-apps                    List all applications"
        echo "  get-app [app-id]            Get app details"
        echo "  trigger [app] [workflow] [branch]  Trigger a build"
        echo "  status <build-id>           Get build status"
        echo "  list-builds [app] [limit]   List recent builds"
        echo "  artifacts <build-id> [dir]  Download build artifacts"
        echo "  cancel <build-id>           Cancel a build"
        echo "  monitor <build-id>          Monitor build progress"
        echo "  batch [app] [workflow] [branches...]  Trigger multiple builds"
        echo ""
        echo "Environment variables:"
        echo "  CODEMAGIC_API_TOKEN - Your API token"
        echo "  CODEMAGIC_APP_ID    - Default app ID"
        ;;
esac